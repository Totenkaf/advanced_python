from pydantic import BaseSettings, PostgresDsn


class AppSettings(BaseSettings):
    app_title: str = 'Fastapi file server'
    database_dsn: PostgresDsn = ('postgresql+asyncpg://postgres:'
                                 'postgres@postgres-fastapi:5432/postgres')
    project_host: str = '0.0.0.0'
    project_port: int = 8000
    token_expires_min: int = 120
    redis_host: str = 'cache'
    redis_port: int = 6379
    echo_queries: bool = False
    max_file_size: int = 268_435_456

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


app_settings = AppSettings()
