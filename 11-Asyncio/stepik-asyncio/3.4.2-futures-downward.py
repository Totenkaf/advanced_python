import asyncio
import random

async def waiter(future):
    await future
    print(f"future выполнен, результат {future.result()}. Корутина waiter() может продолжить работу")

async def setter(future):
    await asyncio.sleep(random.randint(1, 3))
    future.set_result(True)

async def main():
    future = asyncio.Future()
    await asyncio.gather(waiter(future), setter(future))

asyncio.run(main())
