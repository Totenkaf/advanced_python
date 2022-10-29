"""
Multithread server unit test
Copyright 2022 by Artem Ustsov
"""
import json
import socket
import unittest
from unittest.mock import Mock, patch

from requests import TooManyRedirects
from server.my_server import Server
from thread_pool.thread_pool import ThreadPool

#  pylint: disable=too-many-public-methods
#  pylint: disable=attribute-defined-outside-init
#  pylint: disable=too-many-instance-attributes
#  pylint: disable=protected-access


class TestServer(unittest.TestCase):
    """
    Main test class for my_server
    """

    def setUp(self) -> None:
        self.server = Server()

    def test_server_init(self):
        """Server init"""

        self.assertEqual(self.server._k_top, 3)
        self.assertEqual(self.server._num_of_workers, 2)
        self.assertEqual(self.server._ip_address, "0.0.0.0")
        self.assertEqual(self.server._port, 53210)
        self.assertEqual(self.server._urls_processed, 0)

    def test_serv_sock_create(self):
        """Server socket creation"""

        self.server_socket = self.server.create_serv_sock()
        self.assertEqual(self.server_socket.family, socket.AF_INET)
        self.assertEqual(self.server_socket.proto, 0)
        self.assertEqual(self.server_socket.type, socket.SOCK_STREAM)
        self.server_socket.close()

    @patch("server.my_server.socket.socket")
    def test_read_request(self, mock_socket):
        """Mock the client socket by list of values"""

        def fake_recv():
            return_values = [
                "url_1",
                "url_2",
                "url_3",
                "url_4",
                "url_5",
            ]
            for value in return_values:
                yield value

        self.server_socket = self.server.create_serv_sock()
        mock_socket.return_value.accept.return_value = (
            mock_socket,
            ["fake_ip", "fake_port"],
        )
        self.client_socket = self.server.accept_client_conn(
            self.server_socket,
        )
        mock_socket.recv.return_value = fake_recv()

        for fake_request, expected_request in zip(
            self.server.read_request(self.client_socket),
            ["url_1", "url_2", "url_3", "url_4", "url_5"],
        ):
            self.assertEqual(fake_request, expected_request)

        mock_socket.recv.return_value = None
        self.assertEqual(self.server.read_request(self.client_socket), None)

        self.server_socket.close()
        self.client_socket.close()

    @patch("server.my_server.socket.socket")
    def test_read_request_exception(self, mock_socket):
        """Mock the client socket and catch the exception"""

        self.server_socket = self.server.create_serv_sock()
        mock_socket.return_value.accept.return_value = (
            mock_socket,
            ["fake_ip", "fake_port"],
        )
        self.client_socket = self.server.accept_client_conn(
            self.server_socket,
        )
        mock_socket.recv = Mock(side_effect=ConnectionResetError)
        self.assertEqual(self.server.read_request(self.client_socket), None)

        self.server_socket.close()
        self.client_socket.close()

    @patch("server.my_server.socket.socket")
    def test_handle_valid_server_response(self, mock_socket):
        """Mock the requests.get"""

        mock_requests_get_patcher = patch("server.my_server.requests.get")
        mock_write_response_patcher = patch.object(Server, "write_response")
        mock_parse_response_patcher = patch.object(Server, "parse_response")

        self.server_socket = self.server.create_serv_sock()
        mock_socket.return_value.accept.return_value = (
            mock_socket,
            ["fake_ip", "fake_port"],
        )
        self.client_socket = self.server.accept_client_conn(
            self.server_socket,
        )
        mock_socket.recv.return_value = "fake request".encode()
        self.client_fake_request = self.server.read_request(
            self.client_socket,
        )

        mock_requests_get = mock_requests_get_patcher.start()
        mock_requests_get.return_value.text.return_value = "fake response"

        mock_parse_response = mock_parse_response_patcher.start()
        mock_parse_response.return_value = None

        mock_write_response = mock_write_response_patcher.start()
        mock_write_response.return_value = None

        self.server.handle_request(
            client_request=self.client_fake_request,
            client_sock=self.client_socket,
        )

        mock_requests_get_patcher.stop()
        mock_write_response_patcher.stop()
        mock_parse_response_patcher.stop()

        self.server_socket.close()
        self.client_socket.close()

        self.assertTrue(mock_requests_get.called)
        self.assertTrue(mock_parse_response.called)
        self.assertTrue(mock_write_response.called)

    @patch("server.my_server.socket.socket")
    def test_handle_exception_error(self, mock_socket):
        """Catch the raised exceptions"""

        mock_requests_patcher = patch("server.my_server.requests")

        self.server_socket = self.server.create_serv_sock()
        mock_socket.return_value.accept.return_value = (
            mock_socket,
            ["fake_ip", "fake_port"],
        )
        self.client_socket = self.server.accept_client_conn(
            self.server_socket,
        )
        mock_socket.recv.return_value = "fake request".encode()
        self.client_fake_request = self.server.read_request(
            self.client_socket,
        )

        mock_requests = mock_requests_patcher.start()
        mock_requests.get = Mock(side_effect=ConnectionError)
        self.assertRaises(
            ConnectionError,
            self.server.handle_request,
            self.client_fake_request,
            self.client_socket,
        )

        mock_requests = mock_requests_patcher.start()
        mock_requests.get = Mock(side_effect=TooManyRedirects)
        self.assertRaises(
            TooManyRedirects,
            self.server.handle_request,
            self.client_fake_request,
            self.client_socket,
        )

        mock_requests = mock_requests_patcher.start()
        mock_requests.get = Mock(side_effect=Exception)
        self.assertRaises(
            Exception,
            self.server.handle_request,
            self.client_fake_request,
            self.client_socket,
        )

        mock_requests_patcher.stop()

        self.server_socket.close()
        self.client_socket.close()

    @patch("server.my_server.socket.socket")
    def test_handle_invalid_server_response(self, mock_socket):
        """Mock the requests.get"""

        mock_requests_get_patcher = patch("server.my_server.requests.get")

        self.server_socket = self.server.create_serv_sock()
        mock_socket.return_value.accept.return_value = (
            mock_socket,
            ["fake_ip", "fake_port"],
        )
        self.client_socket = self.server.accept_client_conn(
            self.server_socket,
        )
        mock_socket.recv.return_value = "fake request".encode("utf-8")
        self.client_fake_request = self.server.read_request(
            self.client_socket,
        )

        mock_requests_get = mock_requests_get_patcher.start()
        mock_requests_get.return_value = None

        mock_socket.sendall = Mock(send=True)

        self.server.handle_request(
            client_request=self.client_fake_request,
            client_sock=self.client_socket,
        )

        mock_requests_get_patcher.stop()

        self.server_socket.close()
        self.client_socket.close()

        self.assertTrue(mock_requests_get.called)
        self.assertTrue(mock_socket.sendall.called)

    def test_parse_response(self):
        """Response parsing"""

        self.server_response = """<!DOCTYPE html>
                                <html>
                                  <head>
                                    <meta charset="utf-8">
                                    <title>Формула этанола</title>
                                  </head>
                                  <body>
                                    <p>Формула этанола
                                    С<sub>2</sub>Н<sub>5</sub>ОН</p>
                                  </body>
                                </html>"""

        self.json_response = self.server.parse_response(self.server_response)
        # only three because of default k_top=3 on server
        self.json_expected = json.dumps(
            {"Формула": 2, "этанола": 2, "С": 1},
            separators=(", ", ": "),
            ensure_ascii=False,
        )

        # json_tools.diff return empty list if no differences
        self.assertEqual(
            json_tools.diff(self.json_response, self.json_expected),
            [],
        )

    @patch("server.my_server.socket.socket")
    def test_num_of_processed_urls(self, mock_socket):
        """Response parsing"""

        mock_requests_get_patcher = patch("server.my_server.requests.get")
        mock_write_response_patcher = patch.object(Server, "write_response")
        mock_parse_response_patcher = patch.object(Server, "parse_response")

        self.num_of_fake_urls = 10

        def fake_recv():
            return_values = [
                str(i).encode("utf-8")
                for i in range(0, self.num_of_fake_urls)
            ]
            for value in return_values:
                yield value

        mock_socket.return_value.bind.return_value = None
        mock_socket.return_value.listen.return_value = None
        self.server_socket = self.server.create_serv_sock()
        mock_socket.return_value.accept.return_value = (
            mock_socket,
            ["fake_ip", "fake_port"],
        )
        self.client_socket = self.server.accept_client_conn(
            self.server_socket,
        )
        mock_socket.recv.return_value = fake_recv()

        mock_requests_get = mock_requests_get_patcher.start()
        mock_requests_get.return_value.text.return_value = "fake response"

        mock_parse_response = mock_parse_response_patcher.start()
        mock_parse_response.return_value = None

        mock_write_response = mock_write_response_patcher.start()
        mock_write_response.return_value = None

        with ThreadPool(self.server._k_top) as pool:
            for client_request in self.server.read_request(
                self.client_socket,
            ):
                pool.add_task(
                    self.server.handle_request,
                    client_request,
                    self.client_socket,
                )

        mock_requests_get_patcher.stop()
        mock_write_response_patcher.stop()
        mock_parse_response_patcher.stop()

        self.server_socket.close()
        self.client_socket.close()

        self.assertEqual(self.server._urls_processed, self.num_of_fake_urls)

    # @patch("server.my_server.socket.socket")
    # def test_run_server(self, mock_socket):
    #     """Response parsing"""
    #
    #     mock_requests_get_patcher = patch("server.my_server.requests.get")
    #     mock_write_response_patcher = patch.object(Server, 'write_response')
    #     mock_parse_response_patcher = patch.object(Server, 'parse_response')
    #     mock_read_response_patcher = patch.object(Server, 'read_request')
    #
    #     self.num_of_fake_urls = 10
    #
    #     mock_socket.return_value.bind.return_value = None
    #     mock_socket.return_value.listen.return_value = None
    #     self.server_socket = self.server.create_serv_sock()
    #
    #     mock_socket.return_value.accept.return_value = (
    #         socket.socket,
    #         ["fake_ip", "fake_port"],
    #     )
    #
    # self.client_socket = \
    #     self.server.accept_client_conn(self.server_socket)
    #     mock_read_response = mock_read_response_patcher.start()
    #     # mock_read_response.return_value = Mock(side_effect=test)
    #     mock_read_response.return_value = self.client_socket.test()
    #
    #     # mock_socket.recv.return_value = FIXME
    #
    #     mock_requests_get = mock_requests_get_patcher.start()
    #     mock_requests_get.return_value.text.return_value = "fake response"
    #
    #     mock_parse_response = mock_parse_response_patcher.start()
    #     mock_parse_response.return_value = None
    #
    #     mock_write_response = mock_write_response_patcher.start()
    #     mock_write_response.return_value = None
    #
    #     self.server.run_server()
    #
    #     mock_requests_get_patcher.stop()
    #     mock_write_response_patcher.stop()
    #     mock_parse_response_patcher.stop()
    #
    #     self.assertEqual(self.server._urls_processed, self.num_of_fake_urls)


if __name__ == "__main__":
    unittest.main()
