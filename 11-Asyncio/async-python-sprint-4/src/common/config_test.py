# Copyright (c) 2023 Artem Ustsov

from common.config import Settings


class TestSettings(Settings):
    db_host: str = 'localhost'
    db_port: int = 5432
    db_name: str = 'test_db'
    db_password: str = 'test_password'
    db_user: str = 'test_user'


TEST_SETTINGS = TestSettings()
