"""
Multithread server project
Copyright 2022 by Artem Ustsov
"""

import json
import logging
import socket
import threading
from collections import Counter
from typing import Any, NoReturn

import requests
from bs4 import BeautifulSoup
from requests import TooManyRedirects
from thread_pool.thread_pool import ThreadPool


class Server:
    """Threadpool server.
    Main thread listen the socket, take requests (urls)
    and give it to worker.
    Worker is a thread from the pool that send request (url)
    to the external server (by url),
    response the answer and parse it, then sent to client socket.
    Circle continue.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        k_top=3,
        num_of_workers=2,
        ip_address="0.0.0.0",
        port=53210,
        lock=threading.RLock,
    ):
        self._k_top = k_top
        self._num_of_workers = num_of_workers
        self._ip_address = ip_address
        self._port = port
        self._lock = lock()
        self._urls_processed = 0

    # pylint: disable=broad-except
    def run_server(self) -> NoReturn:
        """Run the server

        :return: Nothing
        """

        serv_sock = self.create_serv_sock()
        client_sock = self.accept_client_conn(serv_sock)

        with ThreadPool(self._num_of_workers) as pool:
            client_request = self.read_request(client_sock)
            while client_request:
                pool.add_task(
                    self.handle_request,
                    client_request,
                    client_sock,
                )
                client_request = self.read_request(client_sock)

        serv_sock.close()
        client_sock.close()
        logging.getLogger().info(
            "Total amount of processed urls: %i",
            self._urls_processed,
        )

    def create_serv_sock(self) -> socket:
        """Create the socket on specific ip and port

        :return: Created socket
        """

        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        serv_sock.bind((self._ip_address, self._port))
        serv_sock.listen()
        return serv_sock

    @staticmethod
    def accept_client_conn(serv_sock: socket) -> socket:
        """Accept the new client connection

        :param serv_sock: Socket to be listened
        :return: client socket
        """

        client_sock, client_addr = serv_sock.accept()
        logging.getLogger().info(
            "Client connected %s:%s in %s",
            client_addr[0],
            client_addr[1],
            threading.current_thread().name,
        )
        return client_sock

    @staticmethod
    def read_request(client_sock: socket) -> Any:
        """Read the request from client

        :param client_sock: Socket to be listened
        :return: Request bytesarray or None
        """

        logging.getLogger().debug(
            "%s start read socket",
            threading.current_thread().name,
        )
        try:
            request = client_sock.recv(1024)
            logging.getLogger().debug(
                "%s catch %s",
                threading.current_thread().name,
                request,
            )
            if not request:
                logging.getLogger().debug(
                    "%s break cycle",
                    threading.current_thread().name,
                )
                return None
        except ConnectionResetError as error:
            logging.getLogger().debug(error)
            return None
        return request

    def handle_request(
        self,
        client_request: Any,
        client_sock: socket,
    ) -> NoReturn:
        """Send the request to external server. Take back the response,
        partse it's html body, make counts the number
        of occurrences of words.
        Then send it to writing on a client

        :param client_request: Requested from client url to be processed
        :param client_sock: Socket to be listened
        :return: Nothing
        """

        with self._lock:
            try:
                logging.getLogger().debug(
                    "%s try handle the %s",
                    threading.current_thread().name,
                    client_request,
                )
                url = client_request.decode(encoding="utf-8")
                server_response = requests.get(url, timeout=1)
                if server_response:
                    server_response = self.parse_response(
                        server_response.text,
                    )
                    self.write_response(
                        client_request,
                        client_sock,
                        server_response,
                    )
                else:
                    self.write_response(
                        client_request,
                        client_sock,
                        f"ERROR: {server_response}",
                    )

            # pylint: disable=broad-except
            except Exception as error:
                if isinstance(error, ConnectionError):
                    logging.getLogger().debug("CONNECTION DENIED")
                    logging.getLogger().debug(error)
                    self.write_response(
                        client_request,
                        client_sock,
                        "CONNECTION DENIED",
                    )
                    raise
                if isinstance(error, TooManyRedirects):
                    logging.getLogger().debug("TOO MANY REDIRECTS")
                    logging.getLogger().debug(error)
                    self.write_response(
                        client_request,
                        client_sock,
                        "TOO MANY REDIRECTS",
                    )
                    raise
                logging.getLogger().debug(error)
                self.write_response(
                    client_request,
                    client_sock,
                    "ERROR: OTHER",
                )
                raise

            finally:
                self._urls_processed += 1
                logging.getLogger().info(
                    "URLs processed: %i",
                    self._urls_processed,
                )

    def parse_response(
        self,
        server_response: Any,
        parser_type: str = "lxml",
    ) -> json:
        """Parse the url

        :param server_response: Response html from external server
        :param parser_type: Parser scheme
        :return: Json with most common words statistics
        """

        soup = BeautifulSoup(server_response, parser_type)
        bodies = soup.get_text("\n", strip=True)
        words = [word for word in bodies.split() if word.isalnum()]
        most_common_words = dict(Counter(words).most_common(self._k_top))
        return json.dumps(
            most_common_words,
            separators=(", ", ": "),
            ensure_ascii=False,
        )

    @staticmethod
    def write_response(
        client_request: Any,
        client_sock: socket,
        server_response: Any,
    ) -> NoReturn:
        """Send back the parsed statistics to client

        :param client_request: Client requested url
        :param client_sock: Client socket to send
        :param server_response: Parsed response from external server
        :return: Nothing
        """

        logging.getLogger().debug(
            "%s sending %s",
            threading.current_thread().name,
            server_response,
        )
        client_sock.sendall(f"{client_request}: {server_response}".encode())
