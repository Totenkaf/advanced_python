"""
Acynsio fetcher project
Copyright 2022 by Artem Ustsov
"""

import asyncio
import json
import logging
from typing import List, NoReturn, Optional, TextIO
from collections import Counter

import aiohttp

from bs4 import BeautifulSoup


# pylint:disable=too-few-public-methods
class UrlStats:
    """Class for collecting statistics"""

    def __init__(self) -> NoReturn:
        self.url_processed = 0
        self.url_correct = 0
        self.url_wrong = 0

    def print_stat(self) -> None:
        """Print the url stats into stdout"""

        print("Number of processed URL: ", self.url_processed)
        print("With correctly processed URL: ", self.url_correct)
        print("With error URL: ", self.url_wrong)


# pylint:disable=broad-except
class AsyncioFetcher:
    """Asyncio URL fetcher"""

    def __init__(self, connections: int, k_top: int = 3) -> NoReturn:
        self.connections = connections
        self.k_top = k_top
        self.url_stat = UrlStats()

    async def fetch(
        self,
        session: Optional,
        queue: Optional,
        file: TextIO,
    ) -> None:
        """Event loop. Fetch the data from url in ClientSession.
        Send the data from url to parse method
        """

        while True:
            url = await queue.get()
            logging.getLogger().info("Got %s from queue", url)

            try:
                logging.getLogger().info("Send a request by %s", url)
                async with session.get(url) as resp:
                    logging.getLogger().info(
                        "Response status for %s is %s",
                        url,
                        resp.status,
                    )
                    logging.getLogger().info("Read data")
                    data = await resp.read()
                    logging.getLogger().info(
                        "URL %s: %s with data len as %d",
                        self.url_stat.url_processed,
                        url,
                        len(data),
                    )
                    parsed_data = await self.parse_data(data)
                    logging.getLogger().info(
                        "URL %s: %s with parsed %d",
                        self.url_stat.url_processed,
                        url,
                        parsed_data,
                    )
                    file.write(f"{url} : {parsed_data}\n")

            except Exception as error:
                if isinstance(error, ConnectionError):
                    logging.getLogger().info(
                        "URL %s: %s with %s",
                        self.url_stat.url_processed,
                        url,
                        error,
                    )
                    file.write(f"{url} : {error}\n")
                logging.getLogger().info(
                    "URL %s: %s with other ERROR",
                    self.url_stat.url_processed,
                    url,
                )
                file.write(f"{url} : other ERROR\n")
                self.url_stat.url_wrong += 1
                continue

            else:
                self.url_stat.url_correct += 1

            finally:
                logging.getLogger().info("Task done")
                queue.task_done()
                self.url_stat.url_processed += 1

    async def batch_fetch(self, urls: List[str], file: TextIO) -> None:
        """Gets the urls from queue, create new task to process
        url, synchronize workers
        """

        queue = asyncio.Queue()
        for url in urls:
            logging.getLogger().info("Put the %s in a queue", url)
            await queue.put(url)

        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(
            timeout=timeout, trust_env=True
        ) as session:
            logging.getLogger().info("Make a client session")
            workers = [
                asyncio.create_task(self.fetch(session, queue, file))
                for _ in range(self.connections)
            ]
            await queue.join()

            for worker in workers:
                worker.cancel()

    async def parse_data(self, data, parser_type="lxml"):
        """Parse url, create the most common words json"""

        soup = BeautifulSoup(data, parser_type)
        bodies = soup.get_text("\n", strip=True)
        words = [word for word in bodies.split() if word.isalnum()]
        most_common_words = dict(Counter(words).most_common(self.k_top))
        return json.dumps(
            most_common_words,
            separators=(", ", ": "),
            ensure_ascii=False,
        )
