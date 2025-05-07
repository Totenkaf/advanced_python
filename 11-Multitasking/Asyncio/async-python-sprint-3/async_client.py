# Copyright (c) 2023 Artem Ustsov

import asyncio

from config import SETTINGS
from client.client import Client
from utils import check_python_version


async def main() -> None:
    """Start the client"""

    async with Client(SETTINGS.SERVER_HOST, SETTINGS.SERVER_PORT) as client:
        await client.handle_input()


if __name__ == '__main__':
    check_python_version()
    asyncio.run(main())
