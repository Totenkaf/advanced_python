# Copyright (c) 2023 Artem Ustsov

import pytest
import subprocess
from unittest.mock import patch


@patch('sys.version_info')
@pytest.mark.parametrize(
    'major, minor, error',
    [
        pytest.param(3, 9, None, id='correct_version_3.9'),
        pytest.param(3, 10, None, id='correct_version_3.10'),
        pytest.param(3, 8, Exception, id='incorrect_version_3.8'),
        pytest.param(2, 8, Exception, id='incorrect_version_2.8'),
    ],
)
def test_check_python_version(mock_sys, major, minor, error):
    from utils import check_python_version
    from utils import MIN_MAJOR_PYTHON_VER, MIN_MINOR_PYTHON_VER

    mock_sys.major = major
    mock_sys.minor = minor
    if error:
        with pytest.raises(error) as error:
            check_python_version()
            assert error.value == f"Please use python version >= {MIN_MAJOR_PYTHON_VER}.{MIN_MINOR_PYTHON_VER}"
    else:
        check_python_version()


def test_check_api_response_ok():
    from external.client import YandexWeatherAPI
    from external import analyzer as azr
    from utils import get_url_by_city_name

    CITY_NAME_FOR_TEST = "MOSCOW"

    data_url = get_url_by_city_name(CITY_NAME_FOR_TEST)
    api = YandexWeatherAPI()
    resp = api.get_forecasting(url=data_url)

    assert resp == azr.load_data(f'examples/response.json')


def test_analyzer_analyze_json():
    from external import analyzer as azr

    command_to_execute = [
        "python3",
        "external/analyzer.py",
        "-i",
        "examples/response.json",
        "-o",
        "tests/output.json",
    ]

    run = subprocess.run(command_to_execute, capture_output=True)
    assert run.stdout == b''
    assert azr.load_data(f'tests/output.json') == azr.load_data(f'examples/output.json')
