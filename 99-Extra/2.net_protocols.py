"""
Комплексный пример работы с сетевыми протоколами в Python
Уровни модели OSI и примеры использования каждого протокола
"""

import socket
import requests
from ftplib import FTP
from scapy.all import *
from ping3 import ping
import paramiko


def http_example():
    """
    HTTP/HTTPS (Уровень приложений - 7)
    Цель: Передача гипертекста (веб-страницы, API)
    Используется библиотека requests
    """
    print("\n=== HTTP/HTTPS Example ===")

    # GET-запрос к публичному API
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

    # Выводим статус код и данные
    print(f"Status Code: {response.status_code}")
    print(f"Response Data: {response.json()}")

    # POST-запрос с данными
    post_data = {"title": "foo", "body": "bar", "userId": 1}
    response = requests.post("https://jsonplaceholder.typicode.com/posts", json=post_data)
    print(f"POST Response: {response.json()}")


def ftp_example():
    """
    FTP (Уровень приложений - 7)
    Цель: Передача файлов
    Используется ftplib (для FTPS нужно использовать ftplib.FTP_TLS)
    """
    print("\n=== FTP Example ===")

    try:
        # Подключение к тестовому FTP-серверу (работает только если есть доступ)
        with FTP("ftp.dlptest.com") as ftp:
            # Аутентификация
            ftp.login(user="dlpuser", passwd="rNrKYTX9g7z3RgJRmxWuGHbeu")
            print("FTP Login Successful")

            # Получаем список файлов
            print("Directory Listing:")
            ftp.retrlines('LIST')

            # Пример загрузки файла (если бы он существовал)
            # with open('local_file.txt', 'wb') as f:
            #     ftp.retrbinary('RETR remote_file.txt', f.write)

    except Exception as e:
        print(f"FTP Error: {e}")


def dns_example():
    """
    DNS (Уровень приложений - 7)
    Цель: Преобразование доменных имен в IP
    Используется socket для простых запросов
    """
    print("\n=== DNS Example ===")

    # Прямое преобразование имени в IP
    hostname = "google.com"
    ip_address = socket.gethostbyname(hostname)
    print(f"{hostname} has IP: {ip_address}")

    # Обратное преобразование IP в имя (не всегда работает)
    try:
        host = socket.gethostbyaddr("8.8.8.8")
        print(f"8.8.8.8 is {host[0]}")
    except socket.herror:
        print("Reverse DNS lookup failed")


def tcp_example():
    """
    TCP (Уровень транспорта - 4)
    Цель: Надежная передача данных с установкой соединения
    """
    print("\n=== TCP Example ===")

    # Создаем TCP-клиент для подключения к веб-серверу
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Устанавливаем соединение с HTTP-сервером (порт 80)
            s.connect(("example.com", 80))

            # Отправляем HTTP-запрос вручную
            request = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
            s.sendall(request.encode())

            # Получаем ответ (первые 1024 байта)
            response = s.recv(1024)
            print("TCP Response (first 1024 bytes):")
            print(response.decode())

    except Exception as e:
        print(f"TCP Error: {e}")


def udp_example():
    """
    UDP (Уровень транспорта - 4)
    Цель: Быстрая передача данных без установки соединения
    """
    print("\n=== UDP Example ===")

    # Создаем UDP-сокет
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Отправляем сообщение на локальный UDP-сервер (если бы он был)
        server_address = ("127.0.0.1", 9999)
        message = b"Hello UDP Server!"

        try:
            print(f"Sending {message} to {server_address}")
            s.sendto(message, server_address)

            # Ждем ответа (таймаут 2 секунды)
            s.settimeout(2.0)
            data, server = s.recvfrom(4096)
            print(f"Received {data} from {server}")
        except socket.timeout:
            print("No response received (expected for this demo)")


def icmp_example():
    """
    ICMP (Уровень сетевой - 3)
    Цель: Диагностика сети (ping)
    Используется ping3 для простого ping
    """
    print("\n=== ICMP Example ===")

    target = "google.com"
    response_time = ping(target, unit='ms')

    if response_time is not None:
        print(f"Ping to {target}: {response_time:.2f} ms")
    else:
        print(f"Ping to {target} failed")


def arp_example():
    """
    ARP (Уровень канала данных - 2)
    Цель: Сопоставление IP и MAC-адресов в локальной сети
    Используется scapy для отправки ARP-запросов
    """
    print("\n=== ARP Example ===")

    # Определяем сетевой интерфейс (может потребоваться изменение)
    interface = conf.iface

    # Создаем ARP-запрос
    arp_request = ARP(pdst="192.168.1.1/24")
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether_frame / arp_request

    print(f"Sending ARP requests to local network via {interface}")

    # Отправляем пакет и получаем ответы
    answered, unanswered = srp(packet, timeout=2, verbose=0)

    # Выводим результаты
    print("Discovered devices:")
    for sent, received in answered:
        print(f"IP: {received.psrc} - MAC: {received.hwsrc}")


def ssh_example():
    """
    SSH (Уровень приложений - 7)
    Цель: Безопасный удаленный доступ
    Используется paramiko
    """
    print("\n=== SSH Example ===")

    # Параметры подключения (замените на реальные)
    host = "test.rebex.net"
    port = 22
    username = "demo"
    password = "password"

    try:
        # Создаем SSH-клиент
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Подключаемся к серверу
        client.connect(host, port=port, username=username, password=password)
        print("SSH Connection Established")

        # Выполняем команду
        stdin, stdout, stderr = client.exec_command("ls")
        print("Directory Listing:")
        print(stdout.read().decode())

        # Закрываем соединение
        client.close()
    except Exception as e:
        print(f"SSH Error: {e}")


def main():
    # Запускаем все примеры
    http_example()
    ftp_example()
    dns_example()
    tcp_example()
    udp_example()
    icmp_example()
    arp_example()
    ssh_example()


if __name__ == "__main__":
    main()
