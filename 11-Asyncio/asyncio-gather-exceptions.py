import asyncio
import aiohttp
from util.util import async_timed, fetch_status

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com', 'python://example.com']
        tasks = [fetch_status(session, url) for url in urls]

        # Проблемы
        # [1] если возникло исключение остальные задачи не будут отменены
        # [2] если один запрос выполняется дольше, чем другие
        # будем дожидаться выполнения всех, а не выполнять их по мере поступления
        results = await asyncio.gather(*tasks, return_exceptions=True)

        exceptions = [res for res in results if isinstance(res, Exception)]
        successful_results = [res for res in results if not isinstance(res, Exception)]

        print(f'Все результаты: {results}')
        print(f'Завершились успешно: {successful_results}')
        print(f'Завершились с исключением: {exceptions}')

asyncio.run(main())
