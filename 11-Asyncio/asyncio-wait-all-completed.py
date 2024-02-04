import asyncio
import aiohttp
from aiohttp import ClientSession
from util.util import fetch_status, async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        """
        Когда wait передаются просто сопрограммы, они автоматически обертываются задачами, 
        а возвращенные множества done и pending будут содержать эти задачи. 
        Это значит, что сравнения на предмет присутствия задачи в множестве pending, как в предложении if task is api_b, 
        неправомерны, потому что мы сравниваем разные объекты: сопрограмму и задачу. 
        
        Но если обернуть fetch_status задачей, то новые объекты не создаются и сравнение 
        if task is api_b будет работать, как мы и ожидаем.
        """

        fetchers = [
            asyncio.create_task(fetch_status(session, 'https://example.com')),
            asyncio.create_task(fetch_status(session, 'https://example.com')),
        ]

        """
        Функция wait в asyncio похожа на gather, но дает более точный контроль над ситуацией. 
        У нее есть несколько параметров, позволяющих решить, когда мы хотим получить результаты. 
        Кроме того, она возвращает два множества: задачи, завершившиеся успешно или в результате исключения, 
        а также задачи, которые продолжают выполняться. 
        Еще эта функция позволяет задать тайм-аут, который, однако, ведет себя не так, как в других функциях API: 
        он не возбуждает исключений. 

        Базовая сигнатура wait – список допускающих ожидание объектов, за которым следует 
        факультативный тайм-аут и факультативный параметр return_when, 
        который может принимать значения:
        ALL_COMPLETED, FIRST_EXCEPTION и FIRST_COMPLETED, а по умолчанию равен ALL_COMPLETED. 

        В будущих версиях Python она бу-дет принимать только объекты task
        """

        done, pending = await asyncio.wait(fetchers)
        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')
        for done_task in done:
            result = await done_task
            print(result)

asyncio.run(main())
