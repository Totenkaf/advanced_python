import asyncio
import aiohttp
from aiohttp import ClientSession
from util.util import fetch_status, async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, 'https://www.example.com', 2),
            fetch_status(session, 'https://www.example.com', 1),
            fetch_status(session, 'https://www.example.com', 1),
            fetch_status(session, 'https://www.example.com', 10),
        ]

        # as_completed возвращает список допускающих ожидание объектов
        # функция немедленно возвращает итератор
        # в await выполнение приостанавливается до получения первого ответа

        # по истечении timeout будет возбуждено TimeoutError

        # Problems:
        # [1] Порядок возврата недетерминирован, невозможно понять, что именно
        # мы начнем обрабатывать в первую очередь
        # [2] Как и у gather при возбуждении исключения - все оставшиеся задачи не будут сняты
        for finished_task in asyncio.as_completed(fetchers, timeout=2):
            print(await finished_task)

asyncio.run(main())
