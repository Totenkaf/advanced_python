# Copyright (c) 2023 Artem Ustsov

import asyncio
from asyncio import AbstractEventLoop

from fastapi import FastAPI
import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from httpx import AsyncClient

from common.config_test import TEST_SETTINGS
from db.db import Base, get_session
from main import app


class TestDB:
    def __init__(self) -> None:
        self.default_engine = create_async_engine(TEST_SETTINGS.DEFAULT_DSN, future=True, isolation_level="AUTOCOMMIT")
        self.active_engine = None
        self.sessionmaker = None

    async def create(self) -> None:
        async with self.default_engine.connect() as conn:
            await conn.execute(text(f' DROP DATABASE IF EXISTS {TEST_SETTINGS.db_name}'))
            await conn.execute(text(f'DROP USER IF EXISTS {TEST_SETTINGS.db_user}'))
            await conn.execute(text(f'CREATE DATABASE {TEST_SETTINGS.db_name}'))
            await conn.execute(
                text(f"CREATE USER {TEST_SETTINGS.db_user} WITH PASSWORD '{TEST_SETTINGS.db_password}'"),
            )
            await conn.execute(
                text(f'GRANT ALL PRIVILEGES ON DATABASE {TEST_SETTINGS.db_name} TO {TEST_SETTINGS.db_user}'),
            )

        self.active_engine = create_async_engine(TEST_SETTINGS.database_dsn, future=True)
        self.sessionmaker = async_sessionmaker(self.active_engine, expire_on_commit=False, class_=AsyncSession)
        async with self.active_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_test_session(self) -> AsyncSession:
        async with self.sessionmaker() as session:
            yield session

    async def drop(self) -> None:
        async with self.active_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await self.active_engine.dispose()

        async with self.default_engine.connect() as conn:
            await conn.execute(text(f'DROP DATABASE {TEST_SETTINGS.db_name}'))
            await conn.execute(text(f'DROP USER {TEST_SETTINGS.db_user}'))


@pytest.fixture(scope='session')
def event_loop() -> AbstractEventLoop:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='function')
async def db(event_loop: AbstractEventLoop) -> TestDB:
    test_db = TestDB()
    await test_db.create()
    yield test_db
    await test_db.drop()


@pytest_asyncio.fixture(scope='function')
async def fastapi_app(db: TestDB) -> FastAPI:
    app.dependency_overrides[get_session] = db.get_test_session
    yield app


@pytest_asyncio.fixture(scope='function')
async def client(fastapi_app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=fastapi_app, base_url=TEST_SETTINGS.server_address) as client:
        yield client


@pytest_asyncio.fixture(scope='function')
async def session(db: TestDB) -> AsyncSession:
    async with db.sessionmaker() as session:
        yield session
