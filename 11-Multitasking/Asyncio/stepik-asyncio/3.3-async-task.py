# import asyncio
#
# # Список поваров.
# chef_list = ['', 'Франсуа', 'Жан', 'Марсель']
#
#
# async def cook_order(order_number, dish):
#     # Повар готовит блюдо
#     print(f"Повар {chef_list[order_number]} начинает готовить заказ №{order_number}: {dish}")
#     await asyncio.sleep(2)  # Имитация времени на готовку
#     print(f"Заказ №{order_number}: {dish} готов!")
#     return f"{dish} для заказа №{order_number}"
#
#
# async def serve_order(order_number, dish):
#     # Официант подает блюдо
#     await cook_order(order_number, dish)
#     print(f"Официант подает {dish}")
#
#
# async def manager():
#     # Менеджер (событийный цикл) назначает задачи
#     orders = [(1, 'Салат'), (2, 'Стейк'), (3, 'Суп')]
#     tasks = [asyncio.create_task(serve_order(order_number, dish)) for order_number, dish in orders]
#
#     # Ожидаем завершения всех задач
#     await asyncio.gather(*tasks)
#
#
# # Запуск событийного цикла
# asyncio.run(manager())

"""
Важно! Сохраняйте ссылку на результат функции asyncio.create_task(), чтобы задача не исчезла в процессе выполнения.
Цикл событий сохраняет только слабые ссылки на задачи (тип ссылки в Python, которая не препятствует удалению объекта,
на который она ссылается). Задача, на которую больше нигде нет ссылок, кроме слабых ссылок цикла событий,
может быть удалена сборщиком мусора в любое время, даже до того, как она будет выполнена.
Для надежных фоновых задач типа "запустил и забыл" нужно собрать их в коллекцию (множество, список или кортеж),
как мы это делали в примерах выше.
"""

# import asyncio
#
# async def my_task():
#     print(f"{'-' * 10}\nRunning my task")
#     await asyncio.sleep(1)
#     print(f"Task complete\n{'-' * 10}")
#
# async def main():
#     # Создаем задачу без сохранения ссылки на нее
#     await asyncio.create_task(my_task())
#     # Здесь произойдет запуск задачи, однако стоит помнить,
#     # что эта задача может быть удалена сборщиком мусора в любой момент.
#     await asyncio.sleep(2)
#
# asyncio.run(main())
