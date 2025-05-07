from contextlib import contextmanager
import logging
import time
import sys
import wrapt

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


@contextmanager
def timing_context(operation_name):
    """Этот контекст менеджер замеряет время выполнения произвольной операции"""
    start_time = time.time()
    try:
        yield
    finally:
        logger.debug(
            'Operation "%s" completed in %0.2f seconds',
            operation_name,
            time.time() - start_time,
        )


@wrapt.decorator
def timing(func, instance, args, kwargs):
    """
    Замеряет время выполнения произвольной фукнции или метода.
    Здесь мы используем библиотеку https://wrapt.readthedocs.io/en/latest/
    чтобы безболезненно декорировать методы класса и статические методы
    """
    with timing_context(func.__name__):
        return func(*args, **kwargs)


class DebugMeta(type):
    def __new__(mcs, name, bases, attrs):
        for attr, method in attrs.items():
            if not attr.startswith('_'):
                # оборачиваем все методы декоратором
                attrs[attr] = timing(method)
        return super().__new__(mcs, name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        with timing_context(f'{cls.__name__} instance creation'):
            # замеряем время выполнения создания экземпляра
            return super().__call__(*args, **kwargs)

    # Параметризуем наш `DebugMeta` метакласс из примера выше
    # class DebugMetaParametrized(type):
    #     def __new__(mcs, name, bases, attrs, **extra_kwargs):
    #         debug_methods = extra_kwargs.get('debug_methods', ())
    #
    #         for attr, value in attrs.items():
    #             # Замеряем время исполнения только для методов, имена которых
    #             # переданы в параметре `debug_methods`:
    #             if attr in debug_methods:
    #                 attrs[attr] = timing(value)
    #         return super().__new__(mcs, name, bases, attrs)
    #


if __name__ == '__main__':
    class User(metaclass=DebugMeta):
        def __init__(self, name):
            self.name = name
            time.sleep(.7)

        def login(self):
            time.sleep(1)

        def logout(self):
            time.sleep(2)

        @classmethod
        def create(cls):
            time.sleep(.5)


    user = User('Michael')
    user.login()
    user.logout()
    user.create()

    # class User(metaclass=DebugMetaParametrized, debug_methods=('login', 'create')):
    #     ...
    #
    # user = User('Oleg')
    # user.login()
    # # Метод "logout" залогирован не будет.
    # user.logout()
    # user.create()
