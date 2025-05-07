# Copyright (c) 2023 Artem Ustsov

import os
from typing import Final

from pydantic import Field
from pydantic_settings import BaseSettings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    SERVER_HOST: Final[str] = Field(..., env='SERVER_HOST')
    SERVER_PORT: Final[int] = Field(..., env='SERVER_PORT')
    REPORTS_TO_BAN: Final[int] = 2
    MAX_NUMBER_OF_VIEW_MESSAGES: Final[int] = 20
    BAN_TIME: Final[int] = 4 * 60 * 60  # in seconds
    MESSAGE_TTL: Final[int] = 60 * 60  # in seconds
    LOGGING: Final[dict] = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '{levelname} {module} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

    class Config:
        env_file = os.path.join(BASE_DIR, '.env_example')
        env_file_encoding = 'utf-8'


SETTINGS = Settings()
