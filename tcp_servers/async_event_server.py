import logging
from socket import socket, AF_INET, SOCK_STREAM
from scheduler import NewTask, Scheduler

logger = logging.getLogger(__name__)


def handle_client(client, addr):
    logger.info("Connection from %s", addr)
    while True:
        data = client.recv(65536)
        if not data:
            break
        client.send(data)
    logger.info("Client closed")
    client.close()


def server(port):
    print("Server starting")
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("", port))
    sock.listen()
    try:
        while True:
            client, addr = sock.accept()
            NewTask(handle_client(client, addr))
            yield
    finally:
        sock.close()


if __name__ == "__main__":
    shed = Scheduler()
    shed.add_task(server(8000))
    shed.event_loop()
