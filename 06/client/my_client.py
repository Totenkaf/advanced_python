import socket
import threading
import logging
from thread_pool.thread_pool import ThreadPool
import argparse
import sys


class Client:
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
        self._input_fd = input_fd
        self._output_fd = output_fd
        client_sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM, proto=0
        )
        client_sock.connect((self._ip_address, self._port))

        with ThreadPool(self._num_of_workers) as pool:
            logging.debug(
                f"Thread {threading.current_thread().name} make pool"
            )
            for line in self._input_fd.read().splitlines():
                logging.debug(
                    f"Thread {threading.current_thread().name} read from file {line}"
                )
                logging.info(
                    f"For {line} in thread {threading.current_thread().name}: "
                )
                pool.add_task(self.handle_request, line, client_sock)
                # line = self._input_fd.readline().strip('\n')
                logging.debug(
                    f"Thread {threading.current_thread().name} after pool"
                )

        logging.debug(f"Thread {threading.current_thread().name} close pool")
        client_sock.close()
        logging.debug(f"Thread {threading.current_thread().name} close socket")

    def handle_request(self, server_request, client_sock):
        logging.debug(
            f"Thread {threading.current_thread().name} ready to send {server_request}"
        )
        client_sock.sendall(server_request.encode())

        with self._lock:
            logging.debug(
                f"Thread {threading.current_thread().name} send the request"
            )
            logging.debug(
                f"Thread {threading.current_thread().name} wait for server response"
            )

            server_response = client_sock.recv(1024)
            logging.info(
                f"Received {server_response.decode(encoding='utf-8')}"
            )
            print(
                f"Received {server_request}",
                file=self._output_fd,
            )
            print(
                f"Received {server_response.decode(encoding='utf-8')}",
                file=self._output_fd,
            )


if __name__ == "__main__":
    fmt = "%(asctime)s: %(message)s"
    file_log = logging.FileHandler("logs/client.log")
    console_out = logging.StreamHandler()

    # logging.basicConfig(
    #     handlers=(file_log, console_out),
    #     format=fmt,
    #     level=logging.INFO,
    #     datefmt="%H:%M:%S",
    # )
    # logging.getLogger().setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", default="stdout")
    parser.add_argument("-f", "--input", default="client/urls_https.txt")
    parser.add_argument("-w", "--workers", type=int, default=2)
    parser.add_argument("-i", "--ip_address", default="0.0.0.0")
    parser.add_argument("-p", "--port", default=53210)
    args = parser.parse_args()

    thread_client = Client(
        num_of_workers=args.workers,
        ip_address=args.ip_address,
        port=args.port,
    )
    with open(
        args.input, "r", encoding="utf-8"
    ) if args.input != "stdin" else sys.stdin as input_file:
        thread_client.run_client(input_fd=input_file)
