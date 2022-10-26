"""
Multithread client project
Copyright 2022 by Artem Ustsov
"""

import argparse
import logging
import socket
import sys
import threading
from time import sleep
import os

from thread_pool.thread_pool import ThreadPool


class Client:
    """

    """
    def __init__(
        self,
        num_of_workers=2,
        ip_address="0.0.0.0",
        port=53210,
    ):
        self._input_fd = None
        self._output_fd = None
        self._num_of_workers = num_of_workers
        self._ip_address = ip_address
        self._port = port
        self._lock = threading.RLock()

    def run_client(self, input_fd=sys.stdin, output_fd=sys.stdout):
        """

        :param input_fd:
        :param output_fd:
        :return:
        """
        self._input_fd = input_fd
        self._output_fd = output_fd
        client_sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM, proto=0
        )
        client_sock.connect((self._ip_address, self._port))

        with ThreadPool(self._num_of_workers) as pool:
            logging.debug(f"{threading.current_thread().name} make pool")
            while True:
                line = self._input_fd.readline().strip("\n")
                if not line:
                    break
                logging.debug(
                    f"{threading.current_thread().name} read from file {line}"
                )
                pool.add_task(self.handle_response, line, client_sock)
                self.read_response(client_sock)
                logging.debug(f"{threading.current_thread().name} after pool")

        logging.debug(f"{threading.current_thread().name} close pool")
        client_sock.close()
        logging.debug(f"{threading.current_thread().name} close socket")

    def handle_response(self, server_request, client_sock):
        """

        :param server_request:
        :param client_sock:
        :return:
        """
        with self._lock:
            logging.debug(
                f"{threading.current_thread().name} ready to send {server_request}"
            )
            client_sock.sendall(server_request.encode())
            sleep(0.1)

    def read_response(self, client_sock):
        """

        :param client_sock:
        :return:
        """
        logging.debug(f"{threading.current_thread().name} send the request")
        logging.debug(
            f"{threading.current_thread().name} wait for server response"
        )
        server_response = (
            str(client_sock.recv(1024).decode(encoding="utf-8"))
            .replace("'", "")
            .replace("bhttps://", "")
        )
        logging.info(f"{server_response}")
        print(
            f"{server_response}",
            file=self._output_fd,
        )


if __name__ == "__main__":
    logging.info("=====PROGRAM START=====")

    parser = argparse.ArgumentParser()
    # parser.add_argument("-d", "--debug", default='off')
    parser.add_argument("-f", "--input", default="data/urls_https.txt")
    parser.add_argument("-i", "--ip_address", default="0.0.0.0")
    parser.add_argument("-o", "--output", default="data/urls_requests.txt")
    parser.add_argument("-p", "--port", type=int, default=53210)
    parser.add_argument("-w", "--workers", type=int, default=2)

    args = parser.parse_args()

    # if not os.path.isdir("logs"):
    #     os.mkdir("logs")

    fmt = "%(asctime)s: %(message)s"
    file_log = logging.FileHandler("logs/client.log")
    console_out = logging.StreamHandler()

    logging.basicConfig(
        handlers=(file_log, console_out),
        format=fmt,
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )

    # if args.debug == 'on':
    #     logging.getLogger().setLevel(logging.DEBUG)

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

    logging.info("=====PROGRAM STOP=====")