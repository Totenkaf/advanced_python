import asyncio


"""
Pending (ожидание) -  в этом состоянии операция, связанная с объектом Future, еще не выполнена. 
Это начальное состояние для всех объектов Future/Task. При попытке получить результат операции, 
будет вызвано исключение InvalidStateError. 
"""
async def main():
    future = asyncio.Future()
    if not future.done():
        print("Состояние: Pending (ожидание)")
    try:
        result = future.result()
        print(result)
    except asyncio.InvalidStateError:
        print('Задача еще не выполнена. Доступа к результатам нет!')

asyncio.run(main())

"""
Completed (завершён) - когда операция завершена, объект Future переходит в состояние "завершено". 
В этом состоянии вы можете получить результат операции, вызвав метод result() объекта Future. 
Если операция завершилась с ошибкой, вызов метода result() приведет к возникновению исключения. 
"""
async def main():
    future = asyncio.Future()
    future.set_result('Задача завершена')
    result = future.result()

    if future.done():
        print("Состояние: Completed (завершено)")
        print("Результат:", result)


asyncio.run(main())


"""
Cancelled (отменён) - если операция была отменена, объект Future переходит в состояние "отменено". 
Операция может быть отменена вызовом метода cancel() объекта Future. 
Для проверки отмены операции можно использовать метод future.cancelled(). 
Отменить можно только незавершенную задачу. Если операция была отменена, вызов result() вызовет исключение CancelledError
"""
async def main():
    future = asyncio.Future()
    future.cancel()
    if future.cancelled():
        print("Состояние: Cancelled (отменено)")
    try:
        result = future.result()
        print(result)
    except asyncio.CancelledError:
        print('Задача отменена. Доступа к результатам нет!')

asyncio.run(main())