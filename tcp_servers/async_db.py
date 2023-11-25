import asyncio

class DBConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @classmethod
    async def init(cls, host, port):
        self = cls(host, port)
        _ = await self.get_conn()
        return self

    async def get_conn(self):
        print("Init connection...")
        await asyncio.sleep(1)

    async def close(self):
        print("Closing connection...")
        await asyncio.sleep(1)

    async def do_(self):
        print("Do some work...")
        await asyncio.sleep(1)

    async def __aenter__(self):
        print("Starting context manager...")
        await DBConnection.init(self.host, self.port)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Exit from context manager...")
        await self.close()

async def main():
    async with DBConnection("localhost", 3001) as conn:
        task = asyncio.create_task(conn.do_())
        await task

if __name__ == "__main__":
    asyncio.run(main())
