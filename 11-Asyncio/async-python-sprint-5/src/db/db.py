from typing import Callable, Union

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from common.config import app_settings


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


def create_engine() -> AsyncEngine:
    return create_async_engine(
        app_settings.database_dsn,
        echo=app_settings.echo_queries,
        future=True
    )


def create_sessionmaker(
    bind_engine: Union[AsyncEngine, AsyncConnection]
) -> Callable[..., sessionmaker]:
    return sessionmaker(
        bind=bind_engine,
        autoflush=False,
        expire_on_commit=False,
        future=True,
        class_=AsyncSession,
    )


engine = create_engine()
async_session = create_sessionmaker(engine)
Base = declarative_base()
