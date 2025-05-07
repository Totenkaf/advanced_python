# Copyright (c) 2023 Artem Ustsov

from common.log import get_logger
from common.utils import subscribe, EVENTS

LOG = get_logger()


def dispatch(event, *args, **kwargs) -> None:
    """

    :param event:
    :param args:
    :param kwargs:
    :return:
    """

    handlers = EVENTS.get(event)
    if handlers is None:
        raise ValueError(f'Event {event} is not registered')
    for handler in handlers:
        handler(*args, **kwargs)


@subscribe('on_scheduler_started')
def scheduler_started(*args) -> None:
    """

    :param args:
    :return:
    """

    scheduler = args[0]
    LOG.debug(
        'Scheduler has started. Current queue: %s, max size: %s',
        len(scheduler._pending),
        scheduler._pool_size,
    )


@subscribe('on_job_scheduled')
def job_scheduled(*args, **kwargs) -> None:
    """

    :param args:
    :param kwargs:
    :return:
    """

    job = kwargs.get('task')
    position = kwargs.get('position') + 1
    scheduler = args[0]
    LOG.debug(
        'Job %s is scheduled at position %s/%s',
        job,
        position,
        len(scheduler._pending),
    )


@subscribe('on_job_started')
def job_started(*args, **kwargs) -> None:
    """

    :param args:
    :param kwargs:
    :return:
    """

    job = kwargs.get('job')
    LOG.info('Job %s has started', job)


@subscribe('on_job_done')
def job_done(*args, **kwargs) -> None:
    """

    :param args:
    :param kwargs:
    :return:
    """

    job = kwargs.get('job')
    LOG.info('Job %s is done, result: %s', job, job.result)


@subscribe('on_job_failed')
def job_failed(*args, **kwargs) -> None:
    """

    :param args:
    :param kwargs:
    :return:
    """

    job = kwargs.get('job')
    if job.tries > 0:
        LOG.warning(
            'Job %s is failed, error: %s. Restarting job... (%s tries left)',
            job,
            job.error,
            job.tries,
        )
    else:
        LOG.warning('Job %s is failed, error: %s. No more tries left', job, job.error)
