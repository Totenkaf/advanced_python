# Copyright (c) 2023 Artem Ustsov

from queue import Queue


class QueueMixin:
    """Queue mixin"""

    def __init__(self):
        self._queue = Queue()

    @property
    def queue(self):
        return self._queue

    @queue.setter
    def queue(self, task):
        self._queue.put(task)

    @property
    def get(self):
        return self._queue.get().result()
