import logging
import selectors
import socket
import sys

HOST, PORT = '', 8000  # Порт сервера

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

def new_connection(selector: selectors.BaseSelector, sock: socket.socket):
    new_conn, address = sock.accept()
    logger.info('accepted new_conn from %s', address)
    new_conn.setblocking(False)

    selector.register(new_conn, selectors.EVENT_READ, read_callback)

def read_callback(selector: selectors.BaseSelector, sock: socket.socket):
    data = sock.recv(1024)
    if data:
        sock.send(data)
    else:
        logger.info('closing connection %s', sock)
        selector.unregister(sock)
        sock.close()

def run_iteration(selector: selectors.BaseSelector):
    events = selector.select()
    for key, mask in events:
        callback = key.data
        callback(selector, key.fileobj)

def serve_forever():
    """
    Метод запускает сервер на постоянное прослушивание новых сообщений
    """
    with selectors.SelectSelector() as selector:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            server_socket.setblocking(False)
            logger.info('Server started on port %s', PORT)

            selector.register(server_socket, selectors.EVENT_READ, new_connection)

            while True:
                run_iteration(selector)

if __name__ == '__main__':
    serve_forever()
