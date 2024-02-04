import asyncio
import functools
import time
from typing import Callable, Any
from aiohttp import ClientSession


def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'выполняется {func} с аргументами {args} {kwargs}')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'{func} завершилась за {total:.4f} с')
        return wrapped
    return wrapper


@async_timed()
async def fetch_status(session: ClientSession, url: str, delay: int = 0) -> int:
    # ten_millis = ClientTimeout(total=1)
    # async with session.get(url, timeout=ten_millis) as result:

    # emulate long response
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status


async def delay(delay_seconds: int) -> int:
    print(f'засыпаю на {delay_seconds} с')
    await asyncio.sleep(delay_seconds)
    print(f'сон в течение {delay_seconds} с закончился')
    return delay_seconds
