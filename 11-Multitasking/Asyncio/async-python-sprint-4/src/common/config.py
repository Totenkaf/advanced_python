# Copyright (c) 2023 Artem Ustsov

from typing import ClassVar
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    server_port: int = 8080
    server_host: str = 'localhost'
    db_host: str = 'localhost'
    db_port: int = 5432
    db_name: str = 'postgres'
    db_password: str = 'postgres'
    db_user: str = 'postgres'
    db_echo: bool = False

    DEFAULT_DSN: ClassVar[str] = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'

    @property
    def database_dsn(self) -> str:
        return 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}'.format(
            db=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
        )

    @property
    def server_address(self) -> str:
        return f'http://{self.server_host}:{self.server_port}'

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


SETTINGS = Settings()
