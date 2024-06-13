# Copyright (c) 2023 Artem Ustsov

from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from common.config import SETTINGS


Base = declarative_base()

engine = create_async_engine(url=SETTINGS.database_dsn, echo=SETTINGS.db_echo, future=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
