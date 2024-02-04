import asyncio
import aiohttp
from util.util import async_timed, fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com' for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls]

        # каждая корутина обертывается в задачу
        # запускаются последоательно, но выполняются конкурентно
        # запросы могут выполниться в разный момент времени
        # однако gather гарантирует детерминорованный порядок возвращения результатов
        status_codes = await asyncio.gather(*requests)
        print(status_codes)

asyncio.run(main())
