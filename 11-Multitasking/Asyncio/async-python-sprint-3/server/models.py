# Copyright (c) 2023 Artem Ustsov

import asyncio
from typing import Optional

from config import SETTINGS
from common.helpers import execute_later
from common.classes import Model
from server.network import DataTransport, Request, Update


class Gateway(Model):
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    username: str
    reported_by: set['Gateway'] = set()
    is_banned: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transport = DataTransport(writer=self.writer, reader=self.reader)

    def __str__(self):
        return f'client({self.username} transport={self.transport})'

    def ban(self):
        self.is_banned = True

    def unban(self):
        self.reported_by.clear()
        self.is_banned = False

    @classmethod
    async def close(cls, self):
        await self.transport.close()
        self.remove()

    @classmethod
    async def receive(cls, self) -> Request:
        data = await self.transport.receive()
        request = Request.from_json(data)
        request.client = self
        return request

    @classmethod
    async def send_update(cls, update: Update) -> None:
        if update.target == Gateway.BROADCAST:
            tasks = [client.transport.transfer(update.to_json()) for client in cls.objects.all()]
            await asyncio.gather(*tasks)
        else:
            client = update.target
            await client.transport.transfer(update.to_json())

    class BROADCAST:
        pass


class Message(Model):
    text: str
    sender: Gateway
    target: Gateway | Gateway.BROADCAST
    task: Optional[asyncio.Task] = None

    @property
    def status(self) -> str:
        if self.task is None:
            return 'NOT SENT'
        return self.task._state

    def __str__(self) -> str:
        return f'[MESSAGE] {self.sender.username} >>> {self.text}'

    def to_dict(self) -> dict:
        return {
            'text': self.text,
            'sender': self.sender.username,
            'target': self.target.username if self.target != Gateway.BROADCAST else 'BROADCAST',
        }

    def send(self, delay: Optional[int]) -> None:
        update = Update(status='MSG', data=self.to_dict(), target=self.target)
        if delay is None:
            self.task = asyncio.create_task(Gateway.send_update(update))
        else:
            self.task = asyncio.create_task(execute_later(func=Gateway.send_update, update=update, delay=delay))
        self.task.add_done_callback(self._destroy_self)

    def cancel(self) -> None:
        if self.status != 'PENDING':
            raise RuntimeError('Message is already sent')
        self.task.remove_done_callback(self._destroy_self)
        self.task.cancel()
        self.remove()

    def _destroy_self(self, task: asyncio.Task) -> None:
        asyncio.create_task(execute_later(self.remove, delay=SETTINGS.MESSAGE_TTL))
