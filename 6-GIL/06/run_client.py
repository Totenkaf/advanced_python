"""
Multithread client project. Main
Copyright 2022 by Artem Ustsov
"""

import argparse
import os
import logging
import sys

from my_client import Client


if __name__ == "__main__":
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    FORMAT_LOG = "%(asctime)s: %(message)s"
    file_log = logging.FileHandler("logs/client.log")
    console_out = logging.StreamHandler()

    logging.basicConfig(
        handlers=(file_log, console_out),
        format=FORMAT_LOG,
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )

    logging.getLogger().info("=====PROGRAM START=====")

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--input", default="data/urls_https.txt")
    parser.add_argument("-i", "--ip_address", default="0.0.0.0")
    parser.add_argument("-o", "--output", default="data/urls_requests.txt")
    parser.add_argument("-p", "--port", type=int, default=53210)
    parser.add_argument("-w", "--workers", type=int, default=2)

    args = parser.parse_args()

    thread_client = Client(
        num_of_workers=args.workers,
        ip_address=args.ip_address,
        port=args.port,
    )
    with open(
        args.input, "r", encoding="utf-8"
    ) if args.input != "stdin" else sys.stdin as input_file, open(
        args.output, "w", encoding="utf-8"
    ) if args.output != "stdout" else sys.stdin as output_file:
        thread_client.run_client(input_fd=input_file, output_fd=output_file)
    print(thread_client._urls_processed)

    logging.getLogger().info("=====PROGRAM STOP=====")
