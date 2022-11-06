"""
Acynsio fetcher project
Copyright 2022 by Artem Ustsov
"""

import logging
from typing import List, NoReturn, Optional, TextIO
import asyncio
import aiohttp

from bs4 import BeautifulSoup
import json
from collections import Counter


class UrlStats:
    """

    """

    def __init__(self):
        self.url_processed = 0
        self.url_correct = 0
        self.url_wrong = 0

    def print_stat(self):
        """

        """

        print("Number of processed URL: ", self.url_processed)
        print("With correctly processed URL: ", self.url_correct)
        print("With error URL: ", self.url_wrong)


class AsyncioFetcher:
    """

    """

    def __init__(self, connections: int, k_top: int = 3) -> NoReturn:
        self.connections = connections
        self.k_top = k_top
        self.url_stat = UrlStats()

    async def fetch(self, session: Optional, queue: Optional, file: TextIO) -> NoReturn:
        while True:
            url = await queue.get()
            logging.getLogger().info(f"Got {url} from queue")

            try:
                logging.getLogger().info(f"Send a request by url {url}")
                async with session.get(url) as resp:
                    logging.getLogger().info(f"Response status for {url} is {resp.status}")
                    logging.getLogger().info(f"Read data")
                    data = await resp.read()
                    logging.getLogger().info(f"URL {self.url_stat.url_processed}: {url} with data len as {len(data)}")
                    parsed_data = await self.parse_data(data)
                    logging.getLogger().info(f"URL {self.url_stat.url_processed}: {url} with parsed {parsed_data}")
                    file.write(f"{url} : {parsed_data}\n")
            except Exception as error:
                if isinstance(error, ConnectionError):
                    logging.getLogger().info(f"URL {self.url_stat.url_processed}: {url} with {error}")
                    file.write(f"{url} : {error}\n")
                logging.getLogger().info(f"URL {self.url_stat.url_processed}: {url} with other ERROR")
                file.write(f"{url} : other ERROR\n")
                self.url_stat.url_wrong += 1
                continue
            else:
                self.url_stat.url_correct += 1
            finally:
                logging.getLogger().info(f"Task done")
                queue.task_done()
                self.url_stat.url_processed += 1

    async def fill_queue(self):
        pass

    async def batch_fetch(self, urls: List[str], file: TextIO) -> NoReturn:
        queue = asyncio.Queue()
        for url in urls:
            logging.getLogger().info(f"Put the url {url} in a queue")
            await queue.put(url)

        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout, trust_env=True) as session:
            logging.getLogger().info("Make a client session")
            workers = [
                asyncio.create_task(self.fetch(session, queue, file))
                for _ in range(self.connections)
            ]
            await queue.join()

            for worker in workers:
                worker.cancel()

    async def parse_data(self, data, parser_type="lxml"):
        soup = BeautifulSoup(data, parser_type)
        bodies = soup.get_text("\n", strip=True)
        words = [word for word in bodies.split() if word.isalnum()]
        most_common_words = dict(Counter(words).most_common(self.k_top))
        return json.dumps(
            most_common_words,
            separators=(", ", ": "),
            ensure_ascii=False,
        )
