import logging
import sys
from socket import socket, AF_INET, SOCK_STREAM
from async_socket import AsyncSocket
from scheduler import NewTask, Scheduler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


def handle_client(client, addr):
    print("Connection from", addr)
    while True:
        data = yield from client.recv(65536)
        if not data:
            break
        yield from client.send(data)
    print("Client closed")
    client.close()


def server(port):
    print("Server starting")
    rawsock = socket(AF_INET, SOCK_STREAM)
    rawsock.bind(("", port))
    rawsock.listen()
    sock = AsyncSocket(rawsock)
    try:
        while True:
            client, addr = yield from sock.accept()
            yield NewTask(handle_client(client, addr))
    finally:
        sock.close()


if __name__ == "__main__":
    shed = Scheduler()
    shed.add_task(server(8000))
    shed.event_loop()
