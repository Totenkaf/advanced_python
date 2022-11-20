"""
Acynsio fetcher project. Enter point
Copyright 2022 by Artem Ustsov
"""

from fetcher import AsyncioFetcher
import asyncio
import os
import argparse
import logging
import time
import sys

if __name__ == "__main__":
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    FORMAT_LOG = "%(asctime)s: %(message)s"
    file_log = logging.FileHandler("logs/fetcher.log")
    console_out = logging.StreamHandler()

    logging.basicConfig(
        handlers=(file_log, console_out),
        format=FORMAT_LOG,
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )

    logging.getLogger().info("=====PROGRAM START=====")

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--connections", type=int, default=5)
    parser.add_argument("-k", "--ktop", type=int, default=3)
    parser.add_argument("-i", "--input", default="data/urls_https.txt")
    parser.add_argument("-o", "--output", default="stdout")
    args = parser.parse_args()

    with open(
        args.input, "r", encoding="utf-8"
    ) if args.input != "stdin" else sys.stdin as file:
        URLS = file.read().splitlines()

    fetcher = AsyncioFetcher(connections=args.connections, k_top=args.ktop)

    with open(
        args.output, "w", encoding="utf-8"
    ) if args.output != "stdout" else sys.stdout as file:
        t1 = time.time()
        asyncio.run(fetcher.batch_fetch(URLS, file))
        t2 = time.time()
        print(f"Execution time {(t2-t1):0.3f} secs")
        fetcher.url_stat.print_stat()

    logging.getLogger().info("=====PROGRAM STOP=====")
