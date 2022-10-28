"""Copyright 2022 by Artem Ustsov"""

from queue import Queue
from threading import Thread
from typing import Any, Callable, NoReturn


class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""

    def __init__(self, tasks: Queue):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        """Run the func in the worker

        :return: Nothing
        """
        # pylint: disable=broad-except
        while True:
            func, args = self.tasks.get()
            try:
                func(*args)
            except Exception as error:
                print(error)
            finally:
                self.tasks.task_done()


class ThreadPool:
    """Pool of threads consuming tasks from a queue"""

    def __init__(self, num_threads: int) -> NoReturn:
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def __enter__(self) -> Any:
        return self

    def add_task(self, func: Callable, *args: Any) -> NoReturn:
        """Add a task to the queue"""

        self.tasks.put((func, args))

    def wait_completion(self) -> NoReturn:
        """Wait for completion of all the tasks in the queue"""

        self.tasks.join()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> NoReturn:
        self.wait_completion()
