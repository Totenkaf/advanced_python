"""
Multithread server unit test
Copyright 2022 by Artem Ustsov
"""
import unittest
from unittest.mock import patch

from server.my_server import Server


#  pylint: disable=too-many-public-methods
#  pylint: disable=attribute-defined-outside-init
#  pylint: disable=too-many-instance-attributes
class TestServer(unittest.TestCase):
    """
    Main test class for my_server
    """

    @patch.object(KVPair, "__init__")
    def test_kv_pair_init(self, __init__mock):
        """KV Pair mock init"""
        __init__mock.return_value = None
        self.pair = KVPair()
        self.assertTrue(__init__mock.called)


if __name__ == "__main__":
    unittest.main()
