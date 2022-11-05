import json
import socket
from collections import Counter

import requests
from bs4 import BeautifulSoup
from requests import ConnectionError, HTTPError, ReadTimeout, TooManyRedirects

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(("", 53210))
serv_sock.listen(10)

while True:
    client_sock, client_addr = serv_sock.accept()
    print("Connected by", client_addr)

    while True:
        data = client_sock.recv(1024)
        answer = None
        if not data:
            break

        try:
            url = data.decode(encoding="utf-8")
            response = requests.get(url, timeout=1)

        except Exception as e:
            if isinstance(e, ConnectionError):
                print("CONNECTION DENIED")
            elif isinstance(e, TooManyRedirects):
                print("TOO MANY REDIRECTS")
            elif isinstance(e, HTTPError):
                print("HTTP ERROR")
            elif isinstance(e, ReadTimeout):
                print("READ TIMEOUT ERROR")
            else:
                print(e)

        else:
            soup = BeautifulSoup(response.text, "lxml")
            bodies = soup.get_text("\n", strip=True)
            words = [word for word in bodies.split() if word.isalnum()]
            most_common_words = dict(Counter(words).most_common(3))
            answer = json.dumps(
                most_common_words, separators=(", ", ": "), ensure_ascii=False
            )

        if answer:
            client_sock.sendall(answer.encode())
        else:
            client_sock.sendall("-1".encode())

    client_sock.close()
