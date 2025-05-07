# Copyright (c) 2023 Artem Ustsov

import asyncio
import logging.config
from typing import Optional

from aioconsole import ainput

from server.network import DataTransport, Request, Update
from config import SETTINGS
from common.helpers import print_update

logging.config.dictConfig(SETTINGS.LOGGING)
LOG = logging.getLogger(__name__)


class Client:
    def __init__(self, server_host: str, server_port: int) -> None:
        self._server_host = server_host
        self._server_port = server_port
        self._transport: Optional[DataTransport] = None
        self._request_queue: asyncio.Queue = asyncio.Queue()
        self._receiver: Optional[asyncio.Task] = None

    async def __aenter__(self) -> 'Client':
        reader, writer = await asyncio.open_connection(self._server_host, self._server_port)
        self._transport = DataTransport(writer, reader)
        LOG.debug("Connected to %s:%s", self._server_host, self._server_port)
        self._receiver = asyncio.ensure_future(self._receive_data())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._request_queue.join()
        self._receiver.cancel()
        await self._transport.close()
        LOG.info("Connection to %s:%s is closed", self._server_host, self._server_port)

    async def _receive_data(self) -> None:
        """Try to recieve data from server"""

        while True:
            try:
                data = await self._transport.receive()
                update = Update.from_json(data)
                print_update(update)
            except ConnectionError:
                break

    async def send(self, statement: str) -> None:
        """Try to send a new data to server"""

        command, *value = statement.split()
        request = Request(command, ' '.join(value))
        await self._transport.transfer(request.to_json())

    async def handle_input(self) -> None:
        """Try to handle user input"""

        while True:
            statement = await ainput()
            match statement.split():
                case [command, *value]:  # noqa
                    await self.send(statement)
                    if command == 'exit':
                        break
                case _:
                    continue
