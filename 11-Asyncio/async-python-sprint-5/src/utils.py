# Copyright (c) 2023 Artem Ustsov

MIN_MAJOR_PYTHON_VER = 3
MIN_MINOR_PYTHON_VER = 9


def check_python_version() -> None:
    """Check if installed Python version satisfy restrictions

    :return: None
    """

    import sys

    if (
        sys.version_info.major < MIN_MAJOR_PYTHON_VER
        or sys.version_info.minor < MIN_MINOR_PYTHON_VER
    ):
        raise Exception(f'You should use python version >= {MIN_MAJOR_PYTHON_VER}.{MIN_MINOR_PYTHON_VER}')
