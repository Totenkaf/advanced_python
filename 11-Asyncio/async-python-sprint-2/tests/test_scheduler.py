# Copyright (c) 2023 Artem Ustsov

import datetime as dt
import os
import pytest
import random

import common.exceptions as ex
from client.schemas import Forecast, Weather, WeatherDetail
from scheduler.job import Job
from scheduler.scheduler import Scheduler
import scheduler.tasks as tsk


@pytest.mark.parametrize('scheduler', [1], indirect=True)
def test_handle_successful_job(scheduler: Scheduler) -> None:
    job = Job(lambda: 1)
    scheduler.schedule(job)
    scheduler.run()
    assert job.error is None
    assert job.status == Job.Status.DONE
    assert job.tries == 1
    assert scheduler._completed[job.id] == job.result
    assert len(scheduler._completed) == 1
    assert scheduler._pending == []
    assert scheduler._running == {}


@pytest.mark.parametrize('scheduler', [1], indirect=True)
def test_scheduler_pool_overhead(scheduler: Scheduler) -> None:
    job1 = Job(lambda: 1)
    job2 = Job(lambda: 1)
    with pytest.raises(ex.SchedulerPoolOverheadError) as e:
        scheduler.schedule(*[job1, job2])
        scheduler.run()
        assert e.value == 'Pool overhead. Only 1 tasks could be executed simultaneously'


@pytest.mark.parametrize('scheduler', [10], indirect=True)
def test_handle_failed_job(scheduler: Scheduler) -> None:
    job = Job(lambda: 1 / 0)
    scheduler.schedule(job)
    scheduler.run()
    assert isinstance(job.error, ZeroDivisionError)
    assert job.status == Job.Status.FAILED
    assert job.tries == 0
    assert job.result is None
    assert scheduler._completed[job.id] == job.error
    assert len(scheduler._completed) == 1
    assert scheduler._pending == []
    assert scheduler._running == {}


@pytest.mark.parametrize('scheduler', [10], indirect=True)
def test_handle_independent_jobs(scheduler: Scheduler) -> None:
    job_1 = Job(sum, args=([1, 2, 3],))
    job_2 = Job(sum, args=([2, 3, 4],))
    job_3 = Job(sum, args=([3, 4, 5],))
    jobs = [job_1, job_2, job_3]
    scheduler.schedule(*jobs)
    scheduler.run()
    assert all([job.status == Job.Status.DONE for job in jobs])
    assert all([job.tries == 1 for job in jobs])
    assert all([job_1.result == 6, job_2.result == 9, job_3.result == 12])
    assert all([job.error is None for job in jobs])
    assert all([scheduler._completed[job.id] == job.result for job in jobs])
    assert len(scheduler._completed) == 3
    assert scheduler._pending == []
    assert scheduler._running == {}


@pytest.mark.parametrize('scheduler', [10], indirect=True)
def test_handle_dependent_jobs(scheduler: Scheduler) -> None:
    job_1 = Job(lambda: 'hello ')
    job_2 = Job(lambda: 'world', dependencies=[job_1])
    job_3 = Job(lambda: '!', dependencies=[job_2, job_1])
    jobs = [job_1, job_2, job_3]
    random.shuffle(jobs)
    scheduler.schedule(*jobs)
    assert scheduler._pending == [job_1, job_2, job_3]
    scheduler.run()
    assert ''.join(scheduler._completed.values()) == 'hello world!'
    assert all([job.status == Job.Status.DONE for job in [job_1, job_2, job_3]])
    assert all([job.error is None for job in jobs])
    assert all([scheduler._completed[job.id] == job.result for job in jobs])
    assert len(scheduler._completed) == 3
    assert scheduler._pending == []
    assert scheduler._running == {}


@pytest.mark.parametrize('scheduler', [10], indirect=True)
def test_schedule_jobs_by_time(scheduler: Scheduler) -> None:
    job_1 = Job(lambda: 1, start_at=dt.datetime.now() + dt.timedelta(seconds=1))
    job_2 = Job(lambda: 2, start_at=dt.datetime.now() + dt.timedelta(seconds=2))
    job_3 = Job(lambda: 3, start_at=dt.datetime.now() + dt.timedelta(seconds=3))
    jobs = [job_1, job_2, job_3]
    random.shuffle(jobs)
    scheduler.schedule(*jobs)
    assert scheduler._pending == [job_1, job_2, job_3]
    scheduler.run()
    assert all([job.status == Job.Status.DONE for job in jobs])
    assert all([job.tries == 1 for job in jobs])
    assert all([job.error is None for job in jobs])
    assert all([scheduler._completed[job.id] == job.result for job in jobs])
    assert len(scheduler._completed) == 3
    assert scheduler._pending == []
    assert scheduler._running == {}


@pytest.mark.parametrize('scheduler', [10], indirect=True)
def test_handle_failed_dependency(scheduler: Scheduler) -> None:
    job_1 = Job(lambda: 1 / 0)
    job_2 = Job(lambda: 1, dependencies=[job_1])
    job_3 = Job(lambda: 1, dependencies=[job_2])
    jobs = [job_1, job_2, job_3]
    scheduler.schedule(*jobs)
    scheduler.run()
    assert all([job.status == Job.Status.FAILED for job in jobs])
    assert all([job.tries == 0 for job in jobs])
    assert isinstance(job_1.error, ZeroDivisionError)
    assert isinstance(job_2.error, ex.JobDependencyFailError)
    assert isinstance(job_3.error, ex.JobDependencyFailError)
    assert all([scheduler._completed[job.id] == job.error for job in jobs])
    assert len(scheduler._completed) == 3
    assert scheduler._pending == []
    assert scheduler._running == {}


@pytest.mark.parametrize('scheduler', [10], indirect=True)
def test_handle_file_tasks(scheduler: Scheduler) -> None:
    job_1 = Job(tsk.create_file)
    job_2 = Job(tsk.write_to_file, dependencies=[job_1])
    job_3 = Job(tsk.read_from_file, dependencies=[job_2])
    job_4 = Job(tsk.delete_file, dependencies=[job_3])
    jobs = [job_1, job_2, job_3, job_4]
    scheduler.schedule(*jobs)
    scheduler.run()
    assert all([job.status == Job.Status.DONE for job in jobs])
    assert len(scheduler._completed) == 4
    assert scheduler._pending == []
    assert scheduler._running == {}
    assert not os.path.exists('some_file.txt')


@pytest.mark.parametrize('scheduler', [10], indirect=True)
def test_handle_dir_tasks(scheduler: Scheduler) -> None:
    job_1 = Job(tsk.create_dir)
    job_2 = Job(tsk.delete_dir, dependencies=[job_1])
    jobs = [job_1, job_2]
    scheduler.schedule(*jobs)
    scheduler.run()
    assert all([job.status == Job.Status.DONE for job in jobs])
    assert len(scheduler._completed) == 2
    assert scheduler._pending == []
    assert scheduler._running == {}
    assert not os.path.exists('some_dir')


@pytest.mark.parametrize('scheduler', [10], indirect=True)
def test_handle_web_tasks(scheduler: Scheduler) -> None:
    job_1 = Job(tsk.get_whether)
    jobs = [job_1]
    scheduler.schedule(*jobs)
    scheduler.run()
    assert all([job.status == Job.Status.DONE for job in jobs])
    assert len(scheduler._completed) == 1
    assert scheduler._pending == []
    assert scheduler._running == {}
    expected = [Forecast(
        forecasts=[Weather(
            date='2022-05-26', hours=[WeatherDetail(hour='0', temp=10, condition='overcast'),
                                      WeatherDetail(hour='1', temp=10, condition='overcast'),
                                      WeatherDetail(hour='2', temp=9, condition='overcast'),
                                      WeatherDetail(hour='3', temp=8, condition='overcast'),
                                      WeatherDetail(hour='4', temp=7, condition='overcast'),
                                      WeatherDetail(hour='5', temp=8, condition='overcast'),
                                      WeatherDetail(hour='6', temp=9, condition='overcast'),
                                      WeatherDetail(hour='7', temp=11, condition='cloudy'),
                                      WeatherDetail(hour='8', temp=13, condition='cloudy'),
                                      WeatherDetail(hour='9', temp=15, condition='cloudy'),
                                      WeatherDetail(hour='10', temp=17, condition='cloudy'),
                                      WeatherDetail(hour='11', temp=18, condition='cloudy'),
                                      WeatherDetail(hour='12', temp=19, condition='cloudy'),
                                      WeatherDetail(hour='13', temp=20, condition='overcast'),
                                      WeatherDetail(hour='14', temp=20, condition='overcast'),
                                      WeatherDetail(hour='15', temp=19, condition='overcast'),
                                      WeatherDetail(hour='16', temp=18, condition='light-rain'),
                                      WeatherDetail(hour='17', temp=17, condition='light-rain'),
                                      WeatherDetail(hour='18', temp=17, condition='light-rain'),
                                      WeatherDetail(hour='19', temp=15, condition='light-rain'),
                                      WeatherDetail(hour='20', temp=14, condition='light-rain'),
                                      WeatherDetail(hour='21', temp=13, condition='light-rain'),
                                      WeatherDetail(hour='22', temp=13, condition='light-rain'),
                                      WeatherDetail(hour='23', temp=12, condition='light-rain')]
        ), Weather(
            date='2022-05-27', hours=[WeatherDetail(hour='0', temp=12, condition='light-rain'),
                                      WeatherDetail(hour='1', temp=12, condition='light-rain'),
                                      WeatherDetail(hour='2', temp=11, condition='light-rain'),
                                      WeatherDetail(hour='3', temp=11, condition='light-rain'),
                                      WeatherDetail(hour='4', temp=11, condition='light-rain'),
                                      WeatherDetail(hour='5', temp=11, condition='light-rain'),
                                      WeatherDetail(hour='6', temp=11, condition='light-rain'),
                                      WeatherDetail(hour='7', temp=11, condition='light-rain'),
                                      WeatherDetail(hour='8', temp=11, condition='light-rain'),
                                      WeatherDetail(hour='9', temp=12, condition='light-rain'),
                                      WeatherDetail(hour='10', temp=12, condition='light-rain'),
                                      WeatherDetail(hour='11', temp=12, condition='light-rain'),
                                      WeatherDetail(hour='12', temp=13, condition='light-rain'),
                                      WeatherDetail(hour='13', temp=13, condition='light-rain'),
                                      WeatherDetail(hour='14', temp=13, condition='light-rain'),
                                      WeatherDetail(hour='15', temp=14, condition='showers'),
                                      WeatherDetail(hour='16', temp=14, condition='showers'),
                                      WeatherDetail(hour='17', temp=14, condition='showers'),
                                      WeatherDetail(hour='18', temp=14, condition='light-rain'),
                                      WeatherDetail(hour='19', temp=13, condition='light-rain'),
                                      WeatherDetail(hour='20', temp=13, condition='light-rain'),
                                      WeatherDetail(hour='21', temp=12, condition='cloudy'),
                                      WeatherDetail(hour='22', temp=11, condition='cloudy'),
                                      WeatherDetail(hour='23', temp=10, condition='cloudy')]
        ), Weather(
            date='2022-05-28', hours=[WeatherDetail(hour='0', temp=10, condition='overcast'),
                                      WeatherDetail(hour='1', temp=10, condition='overcast'),
                                      WeatherDetail(hour='2', temp=10, condition='overcast'),
                                      WeatherDetail(hour='3', temp=9, condition='light-rain'),
                                      WeatherDetail(hour='4', temp=9, condition='light-rain'),
                                      WeatherDetail(hour='5', temp=9, condition='light-rain'),
                                      WeatherDetail(hour='6', temp=9, condition='light-rain'),
                                      WeatherDetail(hour='7', temp=10, condition='light-rain'),
                                      WeatherDetail(hour='8', temp=11, condition='showers'),
                                      WeatherDetail(hour='9', temp=11, condition='showers'),
                                      WeatherDetail(hour='10', temp=11, condition='light-rain'),
                                      WeatherDetail(hour='11', temp=11, condition='light-rain'),
                                      WeatherDetail(hour='12', temp=12, condition='light-rain'),
                                      WeatherDetail(hour='13', temp=12, condition='showers'),
                                      WeatherDetail(hour='14', temp=13, condition='showers'),
                                      WeatherDetail(hour='15', temp=13, condition='showers'),
                                      WeatherDetail(hour='16', temp=13, condition='light-rain'),
                                      WeatherDetail(hour='17', temp=13, condition='showers'),
                                      WeatherDetail(hour='18', temp=13, condition='light-rain'),
                                      WeatherDetail(hour='19', temp=12, condition='light-rain'),
                                      WeatherDetail(hour='20', temp=11, condition='light-rain'),
                                      WeatherDetail(hour='21', temp=11, condition='cloudy'),
                                      WeatherDetail(hour='22', temp=10, condition='cloudy'),
                                      WeatherDetail(hour='23', temp=9, condition='cloudy')]
        ), Weather(
            date='2022-05-29', hours=[WeatherDetail(hour='0', temp=9, condition='clear'),
                                      WeatherDetail(hour='1', temp=8, condition='clear'),
                                      WeatherDetail(hour='2', temp=8, condition='clear'),
                                      WeatherDetail(hour='3', temp=8, condition='clear'),
                                      WeatherDetail(hour='4', temp=7, condition='clear'),
                                      WeatherDetail(hour='5', temp=8, condition='cloudy'),
                                      WeatherDetail(hour='6', temp=9, condition='cloudy'),
                                      WeatherDetail(hour='7', temp=10, condition='cloudy'),
                                      WeatherDetail(hour='8', temp=11, condition='light-rain'),
                                      WeatherDetail(hour='9', temp=12, condition='cloudy')]
        ), Weather(date='2022-05-30', hours=[])]
    )]

    assert list(scheduler._completed.values()) == expected
