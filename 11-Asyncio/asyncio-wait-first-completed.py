import aiohttp
import asyncio
from util.util import fetch_status, async_timed

@async_timed()
async def main():
    """
    Здесь мы создаем множество pending и инициализируем его задачами, которые хотим выполнить.
    Цикл while выполняется, пока в pending остаются элементы, и на каждой итерации мы вызываем
    wait для этого множества.
    Получив результат от wait, мы обновляем множества done и pending,
    а затем печатаем завершившиеся задачи.

    Получается поведение, похожее на as_completed, с тем отличием, что теперь мы лучше знаем,
    какие задачи завершились, а какие продолжают работать.
    """
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'
        pending = [asyncio.create_task(fetch_status(session, url)),
        asyncio.create_task(fetch_status(session, url)), asyncio.create_task(fetch_status(session, url))]
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            print(f'Число завершившихся задач: {len(done)}')
            print(f'Число ожидающих задач: {len(pending)}')
            for done_task in done:
                print(await done_task)

asyncio.run(main())
