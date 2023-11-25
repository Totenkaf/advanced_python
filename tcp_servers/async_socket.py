from __future__ import annotations
from socket import socket
from typing import Tuple
from . import SystemCall

# Wait for writing
class WriteWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self, sched, task):
        fd = self.f.fileno()
        sched.wait_for_write(task, fd)

# Wait for reading
class ReadWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self, sched, task):
        fd = self.f.fileno()
        sched.wait_for_read(task, fd)

class AsyncSocket:
    def __init__(self, sock: socket):
        self.sock = sock

    def accept(self) -> Tuple['AsyncSocket', str]:
        yield ReadWait(self.sock)
        client, addr = self.sock.accept()
        return AsyncSocket(client), addr

    def send(self, buffer: bytes):
        while buffer:
            yield WriteWait(self.sock)
            len = self.sock.send(buffer)
            buffer = buffer[len:]

    def recv(self, maxbytes: int) -> bytes:
        yield ReadWait(self.sock)
        return self.sock.recv(maxbytes)

    def close(self):
        yield self.sock.close()
