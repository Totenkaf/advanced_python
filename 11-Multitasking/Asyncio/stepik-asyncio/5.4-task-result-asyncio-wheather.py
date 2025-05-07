import asyncio
import random

random.seed(0)


async def fetch_weather(source, city):
    delay = random.randint(1, 5)
    temperature = random.randint(-10, 35)
    await asyncio.sleep(delay)
    return f"Данные о погоде получены из источника {source} для города {city}: {temperature}°C"


async def main():
    city = "Москва"
    sources = [
        'http://api.weatherapi.com',
        'http://api.openweathermap.org',
        'http://api.weatherstack.com',
        'http://api.weatherbit.io',
        'http://api.meteostat.net',
        'http://api.climacell.co'
    ]

    tasks = [asyncio.create_task(fetch_weather(src, city)) for src in sources]

    while tasks:
        finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for x in finished:
            if result := x.result():
                print(f"Finished task produced {result!r}")

                # Cancel the other tasks, we have a result. Apply only on next loop iteration
                print(f"Cancelling {len(unfinished)} remaining tasks")
                for task in unfinished:
                    task.cancel()

                # So wait for the cancellations to propagate.
                await asyncio.wait(unfinished)
                return result

        tasks = unfinished

    # while tasks:
    #     finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    #     for x in finished:
    #         if result := x.result():
    #             # Cancel the other tasks, we have a result. Apply only on next loop iteration
    #             for task in unfinished:
    #                 task.cancel()
    #
    #             # So wait for the cancellations to propagate.
    #             await asyncio.wait(unfinished)
    #             print(result)
    #             tasks = []
    #             break
    #     else:
    #         tasks = unfinished

asyncio.run(main())
