# Copyright (c) 2023 Artem Ustsov

import asyncio

from config import SETTINGS
from server.server import Server
from utils import check_python_version


async def main() -> None:
    """Start the server"""

    server = Server(SETTINGS.SERVER_HOST, SETTINGS.SERVER_PORT)
    await server.start()
    await server.serve()
    await server.stop()


if __name__ == '__main__':
    check_python_version()
    asyncio.run(main())
