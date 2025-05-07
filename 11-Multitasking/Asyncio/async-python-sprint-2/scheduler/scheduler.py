# Copyright (c) 2023 Artem Ustsov

import datetime as dt
import pickle
import threading
import time

import common.exceptions as ex
from common.utils import coroutine, Singleton, subscribe
from common.log import get_logger
from scheduler.dispatcher import dispatch

LOG = get_logger()


class Scheduler(metaclass=Singleton):
    """Main Scheduler singletone class to keep its state"""

    def __init__(self, pool_size: int = 10) -> None:
        """Scheduler initializer

        :param: pool_size: Max number of simultaneously executed jobs
        """

        self._pending = []
        self._running = {}
        self._completed = {}
        self._is_active: bool = True
        self._pool_size = pool_size
        self._executor = self._executor()

    def schedule(self, *tasks) -> None:
        """Check if coming task is able to executed, if True - set a pending status

        :param tasks: Tasks to be scheduled and executed
        :return: None
        """

        for i, task in enumerate(tasks):
            if len(self._pending) + len(self._running) >= self._pool_size:
                raise ex.SchedulerPoolOverheadError(self._pool_size)

            task.scheduler = self
            for i, job in enumerate(self._pending):
                if task < job:
                    self._pending.insert(i, task)
                    break
            else:
                self._pending.append(task)

            dispatch('on_job_scheduled', self, task=task, position=self._pending.index(task))

    @subscribe('on_job_done')
    def job_done(self, job) -> None:
        """Event searching for job successful completion

        :param job: Incoming job
        :return: None
        """

        self._running.pop(job.id)
        self._completed[job.id] = job.result

        for other_job in self._pending + list(self._running.values()):
            if job in other_job.dependencies:
                LOG.debug(other_job.dependencies)
                other_job.dependencies.remove(job)

                if not other_job.dependencies:
                    other_job.dependency_event.set()

    @subscribe('on_job_failed')
    def job_failed(self, job) -> None:
        """Event searching for job failing

        :param job: Incoming job
        :return: None
        """

        self._running.pop(job.id)
        if job.tries > 0:
            job.restart()
            self.schedule(job)
            return

        self._completed[job.id] = job.error
        for other_job in self._pending + list(self._running.values()):
            if job in other_job.dependencies:
                other_job.failed(error=ex.JobDependencyFailError(job))
                other_job.dependency_event.set()

    def run(self) -> None:
        """Check if scheduler executor is ready for execute incoming job
        If no tasks to execute - make stop and dump executor state,
        send a job to executor otherwise

        :return: None
        """

        dispatch('on_scheduler_started', self)
        while self._is_active:
            try:
                job = self._pending.pop(0)
            except IndexError:
                time.sleep(1)
                if not any([self._pending, self._running]):
                    self.stop()
                    self.scheduler_state_dump()
            else:
                self._executor.send(job)
                time.sleep(.1)

    @coroutine
    def _executor(self) -> None:
        """Scheduler executor coroutine
        Yield next tasks and try to execute in thread

        :return: None
        """

        while True:
            job = yield

            if job.start_at > dt.datetime.now():
                thread = threading.Timer(
                    interval=job.start_at.timestamp() - time.time(),
                    function=job.run,
                )
            else:
                thread = threading.Thread(target=job.run)

            self._running[job.id] = job
            thread.start()

    def stop(self) -> None:
        """Stop an executor

        :return: None
        """

        dispatch('on_scheduler_stopping', self)

        self._is_active = False
        for job in self._pending + list(self._running.values()):
            job.stop()
        self._executor.close()
        del self._executor

    def scheduler_state_dump(self) -> None:
        """Dump an executor current state into a picle file

        :return: None
        """

        with open('scheduler.pickle', 'wb') as f:
            pickle.dump(self, f)
        dispatch('on_scheduler_stopped', self)
