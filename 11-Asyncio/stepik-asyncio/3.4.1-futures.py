import asyncio

# async def callee():
#     print('Hello')
#
# async def caller():
#     await callee()
#     print('World')
#
#
# async def callee():
#     print('Hello')
#
# async def caller():
#     asyncio.create_task(callee())
#     print('World')
#
#
# async def callee():
#     return 'Hello'
#
# async def caller():
#     loop = asyncio.get_event_loop()
#     future = loop.create_task(callee())
#     result = await future
#     print(result + ' World')
#
#
# async def caller():
#     loop = asyncio.get_event_loop()
#     future = loop.create_task(callee())
#     while not future.done():
#         # Какие-нибудь циклические дела
#     print(future.result() + ' World')
#
# async def caller():
#     loop = asyncio.get_event_loop()
#     future = loop.create_task(callee())
#     future.add_done_callback(lambda f: print(f.result() + ' World'))
#     # какие-нибудь другие важные дела
#
# asyncio.run(caller())


async def do_some_work_1(x, future: asyncio.Future):
    print(f"Выполняется работа 1: {x}")
    await asyncio.sleep(x)
    future.set_result(x * 2)


async def do_some_work_2(x, future: asyncio.Future):
    print(f"Выполняется работа 2: {x}")
    await asyncio.sleep(x)
    future.set_result(x + 2)


async def main():
    # Создаем объекты Future для каждой задачи
    future_1 = asyncio.Future()
    future_2 = asyncio.Future()

    # Запускаем первую задачу и передаем ей Future
    asyncio.create_task(do_some_work_1(2, future_1))

    # Дожидаемся завершения первой задачи
    await future_1
    result_1 = future_1.result()

    # Запускаем вторую задачу, передавая результат первой и объект Future
    asyncio.create_task(do_some_work_2(result_1, future_2))

    # Дожидаемся завершения второй задачи
    await future_2
    result_2 = future_2.result()

    print(f"Результат future_1: {result_1}")  # Выводим результат первой задачи
    print(f"Результат future_2: {result_2}")  # Выводим результат второй задачи


asyncio.run(main())
