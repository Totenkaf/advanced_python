# Copyright (c) 2023 Artem Ustsov


class SchedulerPoolOverheadError(Exception):
    def __init__(self, max_pool_size):
        self.message = f'Pool overhead. Only {max_pool_size} tasks could be executed simultaneously'
        super().__init__(self.message)


class JobDependencyFailError(Exception):
    def __init__(self, job):
        self.message = f'Job {job} dependency has failed.'
        super().__init__(self.message)
