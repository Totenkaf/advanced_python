# Copyright (c) 2023 Artem Ustsov

import time
from pathlib import Path

from common.log import get_logger
from client.api import YandexWeatherAPI
from client.schemas import Forecast
from client.utils import get_url_by_city_name

LOG = get_logger()

URL_MOSCOW = 'https://code.s3.yandex.net/async-module/moscow-response.json'

SOME_FILE_NAME = 'some_file.txt'
JOBS_FILE_NAME = 'jobs_data.json'
DIR_NAME = 'some_dir'
TIME_PATTERN = '%d.%m.%Y %H:%M:%S'

DEFAULT_DURATION = 0.1


def create_file() -> None:
    """Create file task

    :return: None
    """

    time.sleep(DEFAULT_DURATION)
    with open(SOME_FILE_NAME, 'w', encoding='UTF-8') as f:
        msg = f'File {SOME_FILE_NAME} created.'
        f.write(f'{msg}\n')
    LOG.debug(msg=msg)


def write_to_file() -> None:
    """Write file task

    :return: None
    """

    time.sleep(DEFAULT_DURATION)
    with open(SOME_FILE_NAME, 'a', encoding='UTF-8') as f:
        f.writelines([f'Some text {i + 1}\n' for i in range(10)])
    LOG.debug('Finished writing to file.')


def read_from_file() -> None:
    """Read file task

    :return: None
    """

    time.sleep(DEFAULT_DURATION)
    try:
        with open(SOME_FILE_NAME, 'r', encoding='UTF-8') as f:
            for line in f.readlines():
                LOG.info(line.strip())
        LOG.info('Finished reading file.')
    except EnvironmentError as error:
        LOG.error(error)


def delete_file() -> None:
    """Delete file task

    :return: None
    """

    time.sleep(DEFAULT_DURATION)
    path = Path(SOME_FILE_NAME)
    if path.is_file():
        path.unlink()
        LOG.debug('Deleted %s.', path)
    LOG.debug('Finished deleting file.')


def create_dir() -> None:
    """Create a directory task

    :return: None
    """

    time.sleep(DEFAULT_DURATION)
    for i in range(5):
        path = Path(f'{DIR_NAME} {i + 1}')
        if not path.is_dir():
            path.mkdir()
            LOG.debug('Created %s.', path)
    LOG.debug('Finished creating dir.')


def delete_dir() -> None:
    """Delete a directory task

    :return:
    """

    time.sleep(DEFAULT_DURATION)
    for i in range(5):
        path = Path(f'{DIR_NAME} {i + 1}')
        if path.is_dir():
            path.rmdir()
            LOG.info('Deleted %s.', path)
    LOG.info('Finished deleting dir.')


def get_whether() -> Forecast:
    """Make a fetching forecast data from YandexWeatherApi task

    :return: Forecast model object
    """

    city_url = get_url_by_city_name('MOSCOW')
    forecasts = Forecast(**YandexWeatherAPI().get_forecasting(city_url))
    LOG.debug(
        'Whether forecast for Moscow on %s received.',
        forecasts.forecasts[0].date
    )
    LOG.debug('Finished getting weather forecast.')
    return forecasts
