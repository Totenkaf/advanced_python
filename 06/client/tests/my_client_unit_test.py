"""
Multithread client unit test
Copyright 2022 by Artem Ustsov
"""
import socket
import unittest
from unittest.mock import Mock, patch

from client.my_client import Client

#  pylint: disable=too-many-public-methods
#  pylint: disable=attribute-defined-outside-init
#  pylint: disable=too-many-instance-attributes
#  pylint: disable=protected-access


class TestClient(unittest.TestCase):
    """
    Main test class for my_client module
    """

    def setUp(self) -> None:
        self.client = Client()

    def test_client_init(self):
        """Client init"""

        self.assertEqual(self.client._num_of_workers, 2)
        self.assertEqual(self.client._ip_address, "0.0.0.0")
        self.assertEqual(self.client._output_fd, None)
        self.assertEqual(self.client._input_fd, None)
        self.assertEqual(self.client._port, 53210)

    @patch("client.my_client.socket.socket")
    def test_client_sock_create(self, mock_socket):
        """Client socket creation"""

        mock_socket.connect.return_value = True

        self.client_socket = self.client.create_client_sock()
        self.assertTrue(mock_socket.called)
        self.client_socket.close()

    @patch("client.my_client.socket.socket")
    def test_read_response(self, mock_socket):
        """socket.recv mocking"""
        mock_create_socket_patcher = patch.object(
            Client, "create_client_sock"
        )

        mock_create_socket = mock_create_socket_patcher.start()
        mock_create_socket.return_value = socket.socket

        self.client_socket = self.client.create_client_sock()
        self.values = [
            "bhttps://url_1",
            "bhttps://url_2",
            "bhttps://url_3",
            "bhttps://url_4",
            "bhttps://url_5",
        ]
        self.expected_values = [
            "url_1",
            "url_2",
            "url_3",
            "url_4",
            "url_5",
        ]

        for value, expected_value in zip(self.values, self.expected_values):
            mock_socket.recv.return_value = value.encode(encoding="utf-8")
            fake_response = self.client.read_response(self.client_socket)
            self.assertEqual(fake_response, expected_value)
        self.assertEqual(
            mock_socket.recv.call_count, len(self.expected_values)
        )

        mock_socket.recv = Mock(side_effect=ConnectionResetError)
        self.assertRaises(
            ConnectionResetError,
            self.client.read_response,
            self.client_socket,
        )
        self.assertEqual(mock_socket.recv.call_count, 1)
        mock_create_socket.stop()

    @patch("client.my_client.socket.socket")
    def test_send_response(self, mock_socket):
        """socket.senddall mock"""

        mock_create_socket_patcher = patch.object(
            Client, "create_client_sock"
        )

        mock_socket.sendall.return_value = True
        mock_create_socket = mock_create_socket_patcher.start()
        mock_create_socket.return_value = socket.socket

        self.client_socket = self.client.create_client_sock()
        self.server_request = "fake request"

        self.client.send_response(self.server_request, self.client_socket)
        self.assertTrue(mock_create_socket.called)

    @patch("client.my_client.socket.socket")
    def test_send_response_exception(self, mock_socket):
        """socket.senddall mock"""

        mock_create_socket_patcher = patch.object(
            Client, "create_client_sock"
        )

        mock_create_socket = mock_create_socket_patcher.start()
        mock_create_socket.return_value = socket.socket

        self.client_socket = self.client.create_client_sock()
        self.server_request = "fake request"

        mock_socket.sendall = Mock(side_effect=ConnectionError)
        self.assertRaises(
            ConnectionError,
            self.client.send_response,
            self.server_request,
            self.client_socket,
        )
        self.assertTrue(mock_socket.sendall.called)

        mock_socket.sendall = Mock(side_effect=Exception)
        self.assertRaises(
            Exception,
            self.client.send_response,
            self.server_request,
            self.client_socket,
        )
        self.assertTrue(mock_socket.sendall.called)
        mock_create_socket_patcher.stop()

    @patch("client.my_client.socket.socket")
    def test_run_client(self, mock_socket):
        """socket.senddall mock"""

        mock_send_response_patcher = patch.object(Client, "send_response")
        mock_read_response_patcher = patch.object(Client, "read_response")

        mock_socket.connect.return_value = True

        mock_send_response = mock_send_response_patcher.start()
        mock_send_response.return_value = None

        mock_read_response = mock_read_response_patcher.start()
        mock_read_response.return_value = "response"

        self.input_filename = "data/urls_https.txt"
        self.output_filename = "data/urls_requests.txt"
        self.client_1 = Client()

        with open(
            self.input_filename, "r", encoding="utf-8"
        ) as input_file, open(
            self.output_filename, "w", encoding="utf-8"
        ) as output_file:
            self.client_1.run_client(
                input_fd=input_file, output_fd=output_file
            )

        with open(self.output_filename, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
            self.assertEqual(len(lines), 100)
            self.assertEqual(lines[0], "response")
            self.assertTrue(all(x == y for x, y in zip(lines, lines[1:])))

        mock_send_response_patcher.stop()
        mock_read_response_patcher.stop()


if __name__ == "__main__":
    unittest.main()
