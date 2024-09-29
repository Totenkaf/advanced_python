import asyncio
import aiohttp
import logging
from util.util import fetch_status, async_timed

@async_timed()
async def main():
    # Обработка исключений при использовании wait
    async with aiohttp.ClientSession() as session:
        good_request = fetch_status(session, 'https://www.example.com')
        bad_request = fetch_status(session, 'python://bad')
        fetchers = [asyncio.create_task(good_request), asyncio.create_task(bad_request)]

        done, pending = await asyncio.wait(fetchers)

        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')

        """
        Функция done_task.exception() проверяет, имело ли место исключение.
        Если нет, то можно получить результат из done_task методом result. 
        Здесь также было бы безопасно написать result = await done_task, 
        хотя при этом может возникнуть исключение, чего мы, возможно, не желаем. 
        
        Если результат exception() не равен None, то в допускающем ожидание объекте возникло исключение 
        и его можно обработать, как нам угодно. 
        В данном случае просто печатаем трассу стека в момент исключения.
        """

        for done_task in done:
            # result = await done_task возбудит исключение
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("При выполнении запроса возникло исключение", exc_info=done_task.exception())

asyncio.run(main())
