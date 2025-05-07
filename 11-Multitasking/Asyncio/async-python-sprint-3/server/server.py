# Copyright (c) 2023 Artem Ustsov

import asyncio
import logging.config
from typing import Optional

from config import SETTINGS
from common.helpers import generate_random_name
from server.models import Gateway
from server.network import Request, Update
from server.handlers import Handler


logging.config.dictConfig(SETTINGS.LOGGING)
LOG = logging.getLogger(__name__)


class Server:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._server: Optional[asyncio.Server] = None

    async def start(self) -> None:
        """Server initialisation"""

        LOG.debug('Starting server on %s:%s', self._host, self._port)
        self._server = await asyncio.start_server(self._handle_connection, self._host, self._port)

    async def serve(self) -> None:
        """Start server serving for new connections"""

        async with self._server:
            LOG.debug('Server is ready to accept connections on %s:%s', self._host, self._port)
            await self._server.serve_forever()

    async def stop(self) -> None:
        """Server stopping"""

        self._server.close()
        await self._server.wait_closed()
        self._server = None
        LOG.debug('Server is stopped')

    @staticmethod
    async def _handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Try to receive a new data from established connection"""

        client = Gateway.objects.create(reader=reader, writer=writer, username=generate_random_name())
        LOG.debug('New connection from %s', client)
        while True:
            try:
                request: Request = await Gateway.receive(client)
                LOG.debug('Received request from %s.', client)
                update: Update = Handler.handle(request)
                await Gateway.send_update(update)
            except ConnectionError:
                break

        LOG.debug('Connection from %s is closed', client)
        await Gateway.close(client)
