"""
Asyncio fetcher unit test
Copyright 2022 by Artem Ustsov
"""
import json
import socket
import unittest
from unittest.mock import Mock, patch

import json_tools
from requests import TooManyRedirects
from fetcher.fetcher import AsyncioFetcher

#  pylint: disable=too-many-public-methods
#  pylint: disable=attribute-defined-outside-init
#  pylint: disable=too-many-instance-attributes
#  pylint: disable=protected-access


class TestServer(unittest.IsolatedAsyncioTestCase):
    """
    Main test class for asyncio_server
    """


if __name__ == "__main__":
    unittest.main()
