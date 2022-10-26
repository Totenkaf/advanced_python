"""Copyright 2022 by Artem Ustsov"""

from queue import Queue
from threading import Thread


class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        """

        :return:
        """

        while True:
            func, args = self.tasks.get()
            try:
                func(*args)
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()


class ThreadPool:
    """Pool of threads consuming tasks from a queue"""

    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def __enter__(self):
        return self

    def add_task(self, func, *args):
        """Add a task to the queue"""

        self.tasks.put((func, args))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""

        self.tasks.join()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wait_completion()
