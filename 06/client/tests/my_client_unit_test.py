"""
Multithread client unit test
Copyright 2022 by Artem Ustsov
"""
import unittest
from unittest.mock import patch

from client.my_client import Client


#  pylint: disable=too-many-public-methods
#  pylint: disable=attribute-defined-outside-init
#  pylint: disable=too-many-instance-attributes
class TestClient(unittest.TestCase):
    """
    Main test class for my_client module
    """

    def test_kv_pair_init(self, __init__mock):
        """KV Pair mock init"""
        __init__mock.return_value = None
        self.pair = KVPair()
        self.assertTrue(__init__mock.called)


if __name__ == "__main__":
    unittest.main()
