# put your python code here
import asyncio

counters = {
    "Counter 1": 0,
    "Counter 2": 0,
    "Counter 3": 0,
}

max_counts = {
    "Counter 1": 13,
    "Counter 2": 7,
    "Counter 3": 15,
}

delays = {
    "Counter 1": 1,
    "Counter 2": 2,
    "Counter 3": 0.5
}

async def counter(counter_name: str, delay: int):
    while counters[counter_name] < max_counts[counter_name]:
        counters[counter_name] += 1
        await asyncio.sleep(delay)
        print(f"{counter_name}: {counters[counter_name]}")

async def main():
    await asyncio.gather(*[asyncio.create_task(counter(counter_name, delays[counter_name])) for counter_name in counters.keys()])

asyncio.run(main())
