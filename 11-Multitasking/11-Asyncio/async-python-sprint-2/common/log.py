# Copyright (c) 2023 Artem Ustsov

import logging

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    level=logging.DEBUG,
)


def get_logger() -> logging.Logger:
    """

    :return:
    """

    return logging.getLogger(__name__)
