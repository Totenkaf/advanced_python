"""
Multithread server project
Copyright 2022 by Artem Ustsov
"""

import argparse
import json
import logging
import socket
import threading
from collections import Counter
from time import sleep
import os

import requests
from bs4 import BeautifulSoup
from requests import ConnectionError, TooManyRedirects
from thread_pool.thread_pool import ThreadPool


class Server:
    """

    """
    def __init__(
        self, k_top=3, num_of_workers=2, ip_address="0.0.0.0", port=53210
    ):
        self._k_top = k_top
        self._num_of_workers = num_of_workers
        self._ip_address = ip_address
        self._port = port
        self._lock = threading.RLock()
        self._urls_processed = 0

    def run_server(self):
        """

        :return:
        """
        serv_sock = self.create_serv_sock()
        client_sock = self.accept_client_conn(serv_sock)

        with ThreadPool(self._num_of_workers) as pool:
            client_request = self.read_request(client_sock)
            while client_request:
                pool.add_task(self.handle_request, client_request, client_sock)
                client_request = self.read_request(client_sock)
        logging.info(f"Total amount of processed urls {self._urls_processed}")

        client_sock.close()
        logging.info(
            f"Client in {threading.current_thread().name} has been served"
        )

    def create_serv_sock(self):
        """

        :return:
        """
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        serv_sock.bind((self._ip_address, self._port))
        serv_sock.listen()
        return serv_sock

    @staticmethod
    def accept_client_conn(serv_sock):
        """

        :param serv_sock:
        :return:
        """
        client_sock, client_addr = serv_sock.accept()
        logging.info(
            f"Client connected "
            f"{client_addr[0]}:{client_addr[1]} "
            f"in {threading.current_thread().name}"
        )
        return client_sock

    @staticmethod
    def read_request(client_sock):
        """

        :param client_sock:
        :return:
        """
        logging.debug(f"{threading.current_thread().name} start read socket")
        try:
            request = client_sock.recv(1024)
            logging.info(f"{threading.current_thread().name} catch {request}")
            if not request:
                logging.debug(f"{threading.current_thread().name} break cycle")
                return None
        except ConnectionResetError:
            return None
        return request

    def handle_request(self, client_request, client_sock):
        """

        :param client_request:
        :param client_sock:
        :return:
        """
        with self._lock:
            try:
                logging.info(
                    f"{threading.current_thread().name} try handle the {client_request}"
                )
                url = client_request.decode(encoding="utf-8")
                server_response = requests.get(url, timeout=1)
                if server_response:
                    server_response = self.parse_url(server_response)
                    self.write_response(
                        client_request, client_sock, server_response
                    )
                else:
                    self.write_response(
                        client_request,
                        client_sock,
                        f"ERROR: {server_response.status_code}",
                    )
                sleep(0.1)
            except Exception as e:
                if isinstance(e, ConnectionError):
                    logging.debug(f"CONNECTION DENIED")
                    logging.debug(e)
                    self.write_response(
                        client_request, client_sock, "CONNECTION DENIED"
                    )
                elif isinstance(e, TooManyRedirects):
                    logging.debug(f"TOO MANY REDIRECTS")
                    logging.debug(e)
                    self.write_response(
                        client_request, client_sock, "TOO MANY REDIRECTS"
                    )
                else:
                    logging.debug(e)
                    self.write_response(
                        client_request, client_sock, "ERROR: OTHER"
                    )
            finally:
                self._urls_processed += 1
        logging.info(f"URLs processed: {self._urls_processed}")

    def parse_url(self, server_response, parser_type="lxml"):
        """

        :param server_response:
        :param parser_type:
        :return:
        """
        soup = BeautifulSoup(server_response.text, parser_type)
        bodies = soup.get_text("\n", strip=True)
        words = [word for word in bodies.split() if word.isalnum()]
        most_common_words = dict(Counter(words).most_common(self._k_top))
        return json.dumps(
            most_common_words, separators=(", ", ": "), ensure_ascii=False
        )

    @staticmethod
    def write_response(client_request, client_sock, server_response):
        """

        :param client_request:
        :param client_sock:
        :param server_response:
        :return:
        """
        logging.info(
            f"{threading.current_thread().name} sending {server_response}"
        )
        client_sock.sendall(f"{client_request}: {server_response}".encode())


if __name__ == "__main__":
    logging.info("=====PROGRAM START=====")

    parser = argparse.ArgumentParser()
    # parser.add_argument("-d", "--debug",  default='off')
    parser.add_argument("-i", "--ip_address", default="0.0.0.0")
    parser.add_argument("-k", "--ktop", type=int, default=3)
    parser.add_argument("-p", "--port", type=int, default=53210)
    parser.add_argument("-w", "--workers", type=int, default=2)

    args = parser.parse_args()

    if not os.path.isdir("logs"):
        os.mkdir("logs")

    fmt = "%(asctime)s: %(message)s"
    file_log = logging.FileHandler("logs/server.log")
    console_out = logging.StreamHandler()

    logging.basicConfig(
        handlers=(file_log, console_out),
        format=fmt,
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )

    # if args.debug == 'on':
    #     logging.getLogger().setLevel(logging.DEBUG)

    thread_server = Server(
        k_top=args.ktop,
        num_of_workers=args.workers,
        ip_address="0.0.0.0",
        port=53210,
    )

    thread_server.run_server()

    logging.info("=====PROGRAM STOP=====")
