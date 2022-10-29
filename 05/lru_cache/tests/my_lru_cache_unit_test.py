"""
LRUCache package main file
Copyright 2022 by Artem Ustsov
"""


import unittest
from unittest.mock import patch

from lru_cache.my_lru_cache import CircledDoubleLinkedList, KVPair, LimitException, LRUCache, Node

#  pylint: disable=too-many-public-methods
#  pylint: disable=attribute-defined-outside-init
#  pylint: disable=too-many-instance-attributes


class TestLRUCache(unittest.TestCase):
    """
    Main test class for my_lru_cache module
    Test contains: Node test, ircledDoubleLinkedList (CDLL) test,
    LRUCache test
    """

    @patch.object(KVPair, "__init__")
    def test_kv_pair_init(self, __init__mock):
        """KV Pair mock init"""
        __init__mock.return_value = None
        self.pair = KVPair()
        self.assertTrue(__init__mock.called)

    def test_kv_pair_special_init(self):
        """KV Pair special init"""
        self.pair = KVPair("key", "value")
        self.assertEqual(self.pair.key, "key")
        self.assertEqual(self.pair.value, "value")

    @patch.object(Node, "__init__")
    def test_node_init(self, __init__mock):
        """Node mock init"""
        __init__mock.return_value = None
        self.node = Node()
        self.assertTrue(__init__mock.called)

    def test_node_default_init_values(self):
        """Node default init"""
        self.node = Node()
        self.assertIsNone(self.node.data)
        self.assertIsNone(self.node.next)
        self.assertIsNone(self.node.prev)

    def test_node_special_init_values(self):
        """Node special init"""
        self.pair = KVPair("key", "value")
        self.node = Node(self.pair)
        self.assertEqual(self.node.data.key, "key")
        self.assertEqual(self.node.data.value, "value")

        self.assertIsNone(self.node.next)
        self.assertIsNone(self.node.prev)

    @patch.object(CircledDoubleLinkedList, "__init__")
    def test_cdll_init(self, __init__mock):
        """CDLL mock init"""
        __init__mock.return_value = None
        self.cdll = CircledDoubleLinkedList()
        self.assertTrue(__init__mock.called)

    def test_cdll_default_init_values(self):
        """CDLL default init"""
        self.cdll = CircledDoubleLinkedList()
        self.assertIsNone(self.cdll.root.data)

        self.assertEqual(self.cdll.len, 0)
        self.assertEqual(self.cdll.root.next, self.cdll.root)
        self.assertEqual(self.cdll.root.prev, self.cdll.root)

    def test_cdll_move_front(self):
        """Check move_front behaviour"""
        self.cdll = CircledDoubleLinkedList()
        self.assertEqual(self.cdll.move_front(None), None)

        self.node = Node()
        self.cdll.move_front(self.node)

        self.assertEqual(self.cdll.len, 0)
        self.assertEqual(self.node.prev, self.cdll.root)
        self.assertEqual(self.node.next, self.cdll.root)

        self.assertEqual(self.cdll.root.next, self.node)
        self.assertEqual(self.cdll.root.prev, self.node)

    def test_cdll_add_data(self):
        """Check add_data behaviour"""
        self.cdll = CircledDoubleLinkedList()
        self.node = self.cdll.add_data(KVPair("key_1", "value_1"))

        self.assertEqual(self.cdll.len, 1)

        self.assertEqual(self.node.data.key, "key_1")
        self.assertEqual(self.node.data.value, "value_1")

    def test_cdll_move_several_nodes(self):
        """Check the LRU strategy"""
        self.cdll = CircledDoubleLinkedList()

        self.node_1 = self.cdll.add_data(KVPair("key_1", "value_1"))
        self.assertEqual(self.node_1.prev, self.cdll.root)
        self.assertEqual(self.node_1.next, self.cdll.root)

        self.node_2 = self.cdll.add_data(KVPair("key_2", "value_2"))
        self.assertEqual(self.node_2.prev, self.cdll.root)
        self.assertEqual(self.node_2.next, self.node_1)
        self.assertEqual(self.node_1.next, self.cdll.root)
        self.assertEqual(self.node_1.prev, self.node_2)

        self.assertEqual(self.cdll.len, 2)

    def test_isolate_nodes(self):
        """Check the isolate method"""
        self.cdll = CircledDoubleLinkedList()

        self.node_1 = self.cdll.add_data(KVPair("key_1", "value_1"))
        self.node_2 = self.cdll.add_data(KVPair("key_2", "value_2"))

        self.isolated_node = self.cdll.isolate(self.node_2)

        self.assertEqual(self.node_1.next, self.cdll.root)
        self.assertEqual(self.node_1.prev, self.cdll.root)

        # node_1 must refer to root
        self.assertEqual(self.cdll.root.next, self.node_1)
        self.assertEqual(self.cdll.root.prev, self.node_1)

        # return data of isolated node must be the same as node_2
        self.assertEqual(self.isolated_node.data.key, self.node_2.data.key)
        self.assertEqual(
            self.isolated_node.data.value, self.node_2.data.value
        )

        # isolated node doesn't have any references
        self.assertIsNone(self.node_2.next)
        self.assertIsNone(self.node_2.prev)

    def test_remove_node_with_empty_cdll(self):
        """Check remove empty CDLL behaviour"""
        self.cdll = CircledDoubleLinkedList()
        self.node = Node(KVPair("key_1", "value_1"))
        self.assertIsNone(self.cdll.remove(self.node))

    def test_remove_node_cdll(self):
        """Check remove node from CDLL behaviour"""
        self.cdll = CircledDoubleLinkedList()
        self.node_1 = self.cdll.add_data(KVPair("key_1", "value_1"))
        self.node_2 = self.cdll.add_data(KVPair("key_3", "value_3"))
        self.node_3 = self.cdll.add_data(KVPair("key_2", "value_2"))
        self.assertEqual(self.cdll.len, 3)

        self.removed_node = self.cdll.remove(self.node_2)
        self.assertEqual(self.cdll.len, 2)

    def test_remove_tail_node_cdll(self):
        """Check remove tail from CDLL behaviour"""
        self.cdll = CircledDoubleLinkedList()
        self.node_1 = self.cdll.add_data(KVPair("key_1", "value_1"))
        self.node_2 = self.cdll.add_data(KVPair("key_3", "value_3"))
        self.node_3 = self.cdll.add_data(KVPair("key_2", "value_2"))
        self.assertEqual(self.cdll.len, 3)

        self.tail_node = self.cdll.remove_tail()
        self.assertIsNone(self.node_1.next)
        self.assertIsNone(self.node_1.prev)
        self.assertEqual(self.tail_node.data.key, self.node_1.data.key)
        self.assertEqual(self.tail_node.data.value, self.node_1.data.value)
        self.assertEqual(self.cdll.len, 2)

        self.assertEqual(self.node_2.next, self.cdll.root)
        self.assertEqual(self.cdll.root.prev, self.node_2)

    @patch.object(LRUCache, "__init__")
    def test_lru_cache_init(self, __init__mock):
        """LRUCache mock init"""
        __init__mock.return_value = None
        self.lru_cache = LRUCache()
        self.assertTrue(__init__mock.called)

    def test_default_lru_cache_init(self):
        """LRUCache default init"""
        self.lru_cache = LRUCache()
        self.assertEqual(self.lru_cache.limit, 42)
        self.assertEqual(self.lru_cache.cdl_list.len, 0)
        self.assertEqual(self.lru_cache.nodes, {})

    def test_special_valid_lru_cache_init(self):
        """LRUCache special valid limit"""
        self.lru_cache = LRUCache(2)
        self.assertEqual(self.lru_cache.limit, 2)

    def test_special_invalid_lru_cache_init(self):
        """LRUCache special invalid limit"""
        self.assertRaises(LimitException, LRUCache, -10)

    @patch.object(LRUCache, "set_value")
    def test_lru_cache_set_value_call(self, set_value_mock):
        """Set several value with mocked set_value method"""
        self.lru_cache = LRUCache(2)
        set_value_mock.return_value = None
        self.lru_cache.set_value("k1", "val1")
        self.lru_cache.set_value("k2", "val2")
        self.lru_cache.set_value("k3", "val3")

        self.assertEqual(set_value_mock.call_count, 3)

    def test_lru_cache_get_value(self):
        """LRUCache get_value check"""
        self.lru_cache = LRUCache(2)
        self.lru_cache.set_value("k1", "val1")
        self.lru_cache.set_value("k2", "val2")
        self.assertEqual(self.lru_cache.get_value("k1"), "val1")
        self.assertEqual(self.lru_cache.get_value("k2"), "val2")
        self.assertIsNone(self.lru_cache.get_value("k3"))

    def test_lru_cache_over_limit_value(self):
        """Check the behaviour with over limit of cache"""
        self.lru_cache = LRUCache(2)
        self.lru_cache.set_value("k1", "val1")
        self.lru_cache.set_value("k2", "val2")
        self.lru_cache.set_value("k3", "val3")
        self.assertEqual(self.lru_cache.get_value("k3"), "val3")
        self.assertEqual(self.lru_cache.get_value("k2"), "val2")
        self.assertIsNone(self.lru_cache.get_value("k1"))

    def test_lru_cache_set_same_key(self):
        """Check the behaviour and LRU strategy with similar keys"""
        self.lru_cache = LRUCache()
        self.lru_cache.set_value("k1", "val1")
        self.lru_cache.set_value("k2", "val2")
        self.lru_cache.set_value("k3", "val3")

        #  check the LRU strategy
        self.assertEqual(self.lru_cache.cdl_list.root.next.data.key, "k3")
        self.assertEqual(self.lru_cache.get_value("k1"), "val1")

        #  add same key with another value
        self.lru_cache.set_value("k1", "val4")
        self.assertEqual(self.lru_cache.get_value("k1"), "val4")

        #  check the LRU strategy
        self.assertEqual(self.lru_cache.cdl_list.root.next.data.key, "k1")


if __name__ == "__main__":
    unittest.main()
