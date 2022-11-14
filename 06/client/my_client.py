"""
Multithread client project
Copyright 2022 by Artem Ustsov
"""

import logging

import socket
import sys
import threading
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
        lock=threading.RLock,
    ):
        self._input_fd = None
        self._output_fd = None
        self._num_of_workers = num_of_workers
        self._ip_address = ip_address
        self._port = port
        self._lock = lock()
        self._urls_processed = 0

    # pylint: disable=broad-except
    # pylint: disable=try-except-raise
    def run_client(
        self,
        input_fd: Any = sys.stdin,
        output_fd: Any = sys.stdout,
    ) -> NoReturn:
        """Run the client. Create client socket and connect to it.

        :param input_fd: Input ile descriptor
        :param output_fd: Output ile descriptor
        :return: Nothing
        """

        self._input_fd = input_fd
        self._output_fd = output_fd

        client_sock = self.create_client_sock()

        with ThreadPool(self._num_of_workers) as pool:
            logging.getLogger().debug(
                "%s make pool",
                threading.current_thread().name,
            )
            while True:
                try:
                    line = self._input_fd.readline().strip("\n")
                    if not line:
                        break
                    logging.getLogger().debug(
                        "%s read %s from file",
                        threading.current_thread().name,
                        line,
                    )
                    pool.add_task(self.send_response, line, client_sock)
                    print(
                        self.read_response(client_sock),
                        file=self._output_fd,
                    )
                    logging.getLogger().debug(
                        "%s read after pool",
                        threading.current_thread().name,
                    )
                except Exception as error:
                    if isinstance(error, ConnectionError):
                        break
                    break

        logging.getLogger().debug(
            "%s close pool",
            threading.current_thread().name,
        )
        client_sock.close()
        logging.getLogger().debug(
            "%s close socket",
            threading.current_thread().name,
        )

    def create_client_sock(self) -> socket:
        """Create the socket on specific ip and port

        :return: Created socket
        """

        client_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            proto=0,
        )
        client_sock.connect((self._ip_address, self._port))
        return client_sock

    # pylint: disable=broad-except
    def send_response(
        self,
        server_request: Any,
        client_sock: socket,
    ) -> NoReturn:
        """Each thread send the response to server.

        :param server_request:
        :param client_sock: Client socket from
        what urls will be sent
        :return: Nothing
        """
        with self._lock:
            try:
                logging.getLogger().debug(
                    "%s close pool %s",
                    threading.current_thread().name,
                    server_request,
                )
                client_sock.sendall(server_request.encode())

            except Exception as error:
                if isinstance(error, ConnectionError):
                    logging.getLogger().debug("CONNECTION DENIED")
                    logging.debug(error)
                    raise
                logging.debug(error)
                raise

            finally:
                self._urls_processed += 1
                logging.getLogger().info(
                    "URLs processed: %i",
                    self._urls_processed,
                )

    @staticmethod
    def read_response(client_sock: socket) -> str:
        """Main thread read the response from the server and
        sent it to outpu_fd

        :param client_sock: Client socket what listen a response
        from the server
        :return: Nothing
        """

        try:
            logging.getLogger().debug(
                "%s send the request",
                threading.current_thread().name,
            )

            value = client_sock.recv(1024)
            server_response = (
                str(value.decode(encoding="utf-8"))
                .replace("'", "")
                .replace("bhttps://", "")
            )
            logging.getLogger().debug(
                "%s wait for server response",
                threading.current_thread().name,
            )
            logging.getLogger().debug("%s", server_response)
        except ConnectionResetError:
            raise
        else:
            return server_response
