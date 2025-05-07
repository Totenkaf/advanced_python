# Copyright (c) 2023 Artem Ustsov

from typing import Callable


EVENTS = {
    'on_scheduler_started': set(),
    'on_scheduler_starting': set(),
    'on_scheduler_stopping': set(),
    'on_scheduler_stopped': set(),
    'on_job_scheduled': set(),
    'on_job_started': set(),
    'on_job_done': set(),
    'on_job_failed': set(),
}


class Singleton(type):
    """Singletone restriction for class creation"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def coroutine(func) -> Callable:
    """Coroutine wrapper. Make first initialise

    :param: func: Function to wrap as coroutine
    :return: Wrapped function
    """

    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen

    return wrapper


def subscribe(event) -> Callable:
    """Subscriber decorator to dispatch function on specific event

    :param: event: Event on subscribe
    :return: Wrapped function
    """

    def decorator(func) -> Callable:
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        EVENTS.setdefault(event, set()).add(wrapper)
        return wrapper

    return decorator
