"""
Multithread pool unit test
Copyright 2022 by Artem Ustsov
"""
import threading
import unittest
from queue import Queue
from time import sleep
from typing import Any, NoReturn
from unittest.mock import patch

from thread_pool import ThreadPool, Worker


#  pylint: disable=too-many-public-methods
#  pylint: disable=attribute-defined-outside-init
#  pylint: disable=too-many-instance-attributes
#  pylint: disable=too-few-public-methods


class TestThreadPool(unittest.TestCase):
    """
    Main test class for thread_pool
    """

    @patch.object(Worker, "__init__")
    def test_worker_init(self, __init__mock) -> Any:
        """Worker mock init"""

        __init__mock.return_value = None
        self.queue = Queue(1)
        self.worker = Worker(self.queue)
        self.assertTrue(__init__mock.called)

    @patch.object(Worker, "run")
    def test_worker_run(self, run_mock) -> Any:
        """run method mock"""

        run_mock.return_value = None
        self.queue = Queue(1)
        self.queue.put(("func", 2))
        self.worker = Worker(self.queue)
        self.assertEqual(self.worker.daemon, True)
        self.assertEqual(self.worker.tasks.get(), ("func", 2))
        self.assertTrue(run_mock.called)

    @patch.object(ThreadPool, "__init__")
    def test_thread_pool_init(self, __init__mock) -> Any:
        """Thread pool mock init"""

        __init__mock.return_value = None
        self.num_of_threads = 0
        self.thread_pool = ThreadPool(self.num_of_threads)
        self.assertTrue(__init__mock.called)

    @patch.object(Worker, "__init__")
    def test_multi_pool_init(self, worker_mock) -> Any:
        """Thread pool with several workers
        mock init"""

        worker_mock.return_value = None
        self.num_of_workers = 5
        self.pool = ThreadPool(self.num_of_workers)
        self.assertEqual(self.pool.tasks.maxsize, self.num_of_workers)
        self.assertEqual(worker_mock.call_count, 5)

    @patch.object(Worker, "__init__")
    def test_pool_add_task(self, worker_mock) -> Any:
        """Thread pool with several workers
        mock init"""

        worker_mock.return_value = None
        self.num_of_workers = 3
        self.pool = ThreadPool(self.num_of_workers)

        def func() -> NoReturn:
            pass

        self.pool.add_task(func, 2, 3)
        self.pool.add_task(func, "test")
        self.pool.add_task(func, [1, 2, 3], (4, 5), {6, 7, 8}, {"9": "10"})
        self.assertEqual(self.pool.tasks.maxsize, self.num_of_workers)
        self.assertEqual(self.pool.tasks.get(), (func, (2, 3)))
        self.assertEqual(self.pool.tasks.get(), (func, ("test",)))
        self.assertEqual(
            self.pool.tasks.get(),
            (func, ([1, 2, 3], (4, 5), {6, 7, 8}, {"9": "10"})),
        )

    @patch.object(ThreadPool, "__enter__")
    @patch.object(ThreadPool, "__exit__")
    def test_thread_pool_context_manager(
        self,
        __enter__mock,
        __exit__mock,
    ) -> Any:
        """

        :param __enter__mock:
        :param __exit__mock:
        :return:
        """

        __enter__mock.return_value = ThreadPool
        __exit__mock.return_value = None

        def func() -> NoReturn:
            pass

        self.num_of_workers = 3
        with ThreadPool(self.num_of_workers) as pool:
            for i in range(self.num_of_workers):
                pool.add_task(func, i)

        self.assertTrue(__enter__mock.called)
        self.assertTrue(__exit__mock.called)

    def test_thread_pool_work(self) -> Any:
        """Checks the fool work of thread pool
        :return: Nothing
        """

        class FakeStat:
            """Fake class for saving condition"""

            def __init__(self):
                self.counter = 0
                self.sums = []
                self._lock = threading.Lock()

            def func(self, summand_1: int, summand_2: int) -> NoReturn:
                """Add a to b

                :param summand_1: summand
                :param summand_2: summand
                :return: sum of two summands
                """

                with self._lock:
                    local_copy = self.counter
                    local_copy += 1
                    self.sums.append(summand_1 + summand_2)
                    sleep(0.01)
                    self.counter = local_copy

        self.num_of_threads = 10
        self.num_to_sum = 100
        self.fake_stat = FakeStat()

        with ThreadPool(self.num_of_threads) as pool:
            for i in range(self.num_to_sum):
                pool.add_task(self.fake_stat.func, i, i + 1)

        self.assertEqual(
            sorted(self.fake_stat.sums),
            [2 * num + 1 for num in range(self.num_to_sum)],
        )
        self.assertEqual(self.fake_stat.counter, self.num_to_sum)
