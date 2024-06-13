# Copyright (c) 2023 Artem Ustsov

from enum import Enum
import datetime as dt
import threading
from typing import Any, Callable, Optional, Tuple
from uuid import uuid4, UUID

from common.exceptions import JobDependencyFailError
from common.log import get_logger
from scheduler.scheduler import Scheduler
from scheduler.dispatcher import dispatch

LOG = get_logger()


class Job:
    """Main Job class to save its state"""

    class Status(Enum):
        """Job statuses enum"""

        PENDING = 1
        RUNNING = 2
        DONE = 3
        FAILED = 3

    def __init__(
        self,
        func: Callable,
        args: Tuple = tuple(),
        start_at: dt.datetime = dt.datetime.now(),
        tries: int = 1,
        dependencies: Any = None,
        **kwargs,
    ) -> None:
        """Job initializer"""

        self._id = uuid4()
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._scheduler: Optional[Scheduler] = None
        self._result = None
        self._error = None
        self._status = self.Status.PENDING
        self._start_at = start_at
        self._tries = tries
        self._dependencies = dependencies
        self._dependency_event = threading.Event() if dependencies else None

    def run(self) -> None:
        """Run a job to be executed by scheduler

        :return: None
        """

        if self._dependency_event is not None:
            while not self._dependency_event.is_set():
                self._dependency_event.wait()
            if isinstance(self._error, JobDependencyFailError):
                self._tries = 0
                dispatch('on_job_failed', self._scheduler, job=self)
                return

        self._status = self.Status.RUNNING
        dispatch('on_job_started', self._scheduler, job=self)
        try:
            self._result = self._func(*self._args, **self._kwargs)
            self._status = self.Status.DONE
            dispatch('on_job_done', self._scheduler, job=self)
        except Exception as exc:
            self._error = exc
            self._status = self.Status.FAILED
            dispatch('on_job_failed', self._scheduler, job=self)

    def restart(self) -> None:
        """Restart job by executor by setting a tries flag

        :return: None
        """

        self._tries -= 1
        self._start_at = dt.datetime.now() + dt.timedelta(seconds=1)
        self._status = self.Status.PENDING
        self._result = None
        self._error = None

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def result(self) -> any:
        return self._result

    @property
    def error(self) -> Exception:
        return self._error

    @property
    def start_at(self) -> dt.datetime:
        return self._start_at

    @property
    def status(self) -> Status:
        return self._status

    @property
    def tries(self) -> int:
        return self._tries

    @property
    def dependencies(self):
        return self._dependencies or []

    @property
    def dependency_event(self) -> threading.Event:
        return self._dependency_event

    @property
    def scheduler(self) -> Scheduler:
        return self._scheduler

    @scheduler.setter
    def scheduler(self, scheduler) -> None:
        self._scheduler = scheduler

    def failed(self, error: Exception) -> None:
        LOG.debug('Job %s set to failed', self)
        self._status = self.Status.FAILED
        self._error = error

    def stop(self) -> None:
        self._status = self.Status.PENDING
        self._result = None
        self._error = None

    def __repr__(self) -> str:
        return f'<Job: {self._id}, {self._func.__name__}, {self._status.name}>'

    def __str__(self) -> str:
        return f'{self._func.__name__} {self._id}'

    def __lt__(self, other) -> bool:
        if self._dependencies is not None and other in self._dependencies:
            return False
        return self._dependencies is not None or self._start_at <= other._start_at
