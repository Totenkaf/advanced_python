"""
Multithread server project. Main
Copyright 2022 by Artem Ustsov
"""

import argparse
import os
import logging

from my_server import Server

if __name__ == "__main__":
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    FORMAT_LOG = "%(asctime)s: %(message)s"
    file_log = logging.FileHandler("logs/server.log")
    console_out = logging.StreamHandler()

    logging.basicConfig(
        handlers=(file_log, console_out),
        format=FORMAT_LOG,
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )

    logging.getLogger().info("=====PROGRAM START=====")

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip_address", default="0.0.0.0")
    parser.add_argument("-k", "--ktop", type=int, default=3)
    parser.add_argument("-p", "--port", type=int, default=53210)
    parser.add_argument("-w", "--workers", type=int, default=2)

    args = parser.parse_args()

    thread_server = Server(
        k_top=args.ktop,
        num_of_workers=args.workers,
        ip_address="0.0.0.0",
        port=53210,
    )

    thread_server.run_server()
    print(thread_server._urls_processed)

    logging.getLogger().info("=====PROGRAM STOP=====")
