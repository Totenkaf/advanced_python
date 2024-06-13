# Copyright (c) 2023 Artem Ustsov

import pytest

from scheduler.scheduler import Scheduler


@pytest.fixture
def scheduler(request) -> Scheduler:
    """Yield a Scheduler instance

    NOTE: because of singletone Scheduler behaviour
    we should clean up its state before yielding new one
    in pytest testing scope!

    :param: request: Params to specify fixture
    :return: Scheduler singletone
    """

    yield Scheduler(request.param)
    Scheduler._instances = {}
