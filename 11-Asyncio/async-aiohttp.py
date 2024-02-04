import asyncio
import aiohttp
from util.util import async_timed, fetch_status


@async_timed()
async def main():
    # no more than 100 sessions simultaneously
    conn = aiohttp.TCPConnector(limit=1, limit_per_host=1)
    session_timeout = aiohttp.ClientTimeout(total=1, connect=1)
    async with aiohttp.ClientSession(connector=conn, timeout=session_timeout) as session:
        url = 'https://www.example.com'
        status = await fetch_status(session, url)
        print(f'Состояние для {url} было равно {status}')

asyncio.run(main())
