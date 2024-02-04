import aiohttp
import asyncio
import logging
from util.util import fetch_status, async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:

        # Здесь мы отправляем один плохой запрос и два хороших, по 3 с каждый.
        fetchers = [
            asyncio.create_task(fetch_status(session, 'python://bad.com')),
            asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=3)),
            asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=3)),
        ]

        """
        CASE I:

        Если ни в одной задаче не было исключений, то этот режим эквивалентен ALL_COMPLETED. 
        Мы дождемся завершения всех задач, после чего множество done будет содержать все задачи, 
        а множество pending останется пустым.
        
        CASE II:
        Если хотя бы в одной задаче возникло исключение, то wait немедленно возвращается. 
        Множество done будет содержать как задачи, завершившиеся успешно, так и те, в которых имело место исключение. 
        Гарантируется, что done будет содержать как минимум одну задачу – завершившуюся ошибкой, 
        но может содержать и какие-то успешно завершившиеся задачи. 

        Множество pending может быть пустым, а может содержать задачи, 
        которые продолжают выполняться. 
        Мы можем использовать его для управления выполняемыми задачами по своему усмотрению.
        """

        # У режимов ALL_COMPLETED и FIRST_EXCEPTION есть недостаток:
        # Если задачи не возбуждают исключений, то мы должны ждать, пока все они завершатся.

        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_EXCEPTION)
        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')
        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("При выполнении запроса возникло исключение", exc_info=done_task.exception())

        for pending_task in pending:
            pending_task.cancel()

asyncio.run(main())
