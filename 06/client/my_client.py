"""
Multithread client project
Copyright 2022 by Artem Ustsov
"""

import argparse
import logging
import os
import socket
import sys
import threading
from time import sleep
from typing import Any, NoReturn

from thread_pool.thread_pool import ThreadPool


class Client:
    """Threadpool client.
    Main thread listen the socket, take urls from the file
    and give it to worker.
    Worker is a thread from the pool that send request (url)
    to the server, response the answer and print the parsed result
    into stdout (or file)
    Circle continue
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

    def run_client(
        self, input_fd: Any = sys.stdin, output_fd: Any = sys.stdout
    ) -> NoReturn:
        """Run the client. Create client socket and connect to it.

        :param input_fd: Input ile descriptor
        :param output_fd: Output ile descriptor
        :return: Nothing
        """

        self._input_fd = input_fd
        self._output_fd = output_fd
        client_sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM, proto=0
        )
        client_sock.connect((self._ip_address, self._port))

        with ThreadPool(self._num_of_workers) as pool:
            logging.getLogger().debug(
                "%s make pool", threading.current_thread().name
            )
            while True:
                line = self._input_fd.readline().strip("\n")
                if not line:
                    break
                logging.getLogger().debug(
                    "%s read %s from file",
                    threading.current_thread().name,
                    line,
                )
                pool.add_task(self.send_response, line, client_sock)
                self.read_response(client_sock)
                logging.getLogger().debug(
                    "%s read after pool", threading.current_thread().name
                )

        logging.getLogger().debug(
            "%s close pool", threading.current_thread().name
        )
        client_sock.close()
        logging.getLogger().debug(
            "%s close socket", threading.current_thread().name
        )

    def send_response(
        self, server_request: Any, client_sock: socket
    ) -> NoReturn:
        """Each thread send the response to server.

        :param server_request:
        :param client_sock: Client socket from
        what urls will be sent
        :return: Nothing
        """

        with self._lock:
            logging.getLogger().debug(
                "%s close pool %s",
                threading.current_thread().name,
                server_request,
            )
            client_sock.sendall(server_request.encode())
            sleep(0.1)

    def read_response(self, client_sock: socket) -> NoReturn:
        """Main thread read the response from the server and
        sent it to outpu_fd

        :param client_sock: Client socket what listen a response
        from the server
        :return: Nothing
        """

        logging.getLogger().debug(
            "%s send the request", threading.current_thread().name
        )
        logging.getLogger().debug(
            "%s wait for server response", threading.current_thread().name
        )

        server_response = (
            str(client_sock.recv(1024).decode(encoding="utf-8"))
            .replace("'", "")
            .replace("bhttps://", "")
        )
        logging.getLogger().debug("%s", server_response)
        print(
            f"{server_response}",
            file=self._output_fd,
        )


if __name__ == "__main__":
    logging.getLogger().info("=====PROGRAM START=====")

    parser = argparse.ArgumentParser()
    # parser.add_argument("-d", "--debug", default='off')
    parser.add_argument("-f", "--input", default="data/urls_https.txt")
    parser.add_argument("-i", "--ip_address", default="0.0.0.0")
    parser.add_argument("-o", "--output", default="data/urls_requests.txt")
    parser.add_argument("-p", "--port", type=int, default=53210)
    parser.add_argument("-w", "--workers", type=int, default=2)

    args = parser.parse_args()

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

    logging.getLogger().info("=====PROGRAM STOP=====")
