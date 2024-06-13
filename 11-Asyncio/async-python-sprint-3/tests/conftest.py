# Copyright (c) 2023 Artem Ustsov

import asyncio
from asyncio import AbstractEventLoop

import pytest

from config import Settings
from server.server import Server
from client.client import Client

settings = Settings()


@pytest.fixture(scope='module')
def loop() -> AbstractEventLoop:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
def server(loop: AbstractEventLoop) -> Server:
    server = Server(settings.SERVER_HOST, settings.SERVER_PORT)
    loop.run_until_complete(server.start())
    asyncio.ensure_future(server.serve())
    yield server
    loop.run_until_complete(server.stop())


@pytest.fixture(scope='function')
def clients(loop: AbstractEventLoop) -> list[Client]:
    yield [Client(settings.SERVER_HOST, settings.SERVER_PORT) for _ in range(3)]
