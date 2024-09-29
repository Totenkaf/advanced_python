import asyncio

async def print_message():
    while True:
        print("Имитация работы функции")
        await asyncio.sleep(1)


async def interrupt_handler(interrupt_flag):
    while True:
        # Ждем установки флага.
        await interrupt_flag.wait()
        print("Произошло прерывание! В этом месте может быть установлен любой обработчик")
        # Очищаем флаг для следующего использования
        interrupt_flag.clear()


async def main():
    interrupt_flag = asyncio.Event()
    asyncio.create_task(print_message())
    asyncio.create_task(interrupt_handler(interrupt_flag))

    while True:
        await asyncio.sleep(3)
        # Устанавливаем флаг для прерывания
        interrupt_flag.set()


asyncio.run(main())
