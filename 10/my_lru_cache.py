"""
LRUCache package main file
Copyright 2022 by Artem Ustsov
"""

import argparse
import logging.config
from typing import Any, NoReturn


class LimitException(Exception):
    # pylint: disable=too-few-public-methods
    """Inherited from Exception limit exception"""


class KVPair:
    # pylint: disable=too-few-public-methods
    """Pair realisation"""

    def __init__(self, key: Any = None, value: Any = None) -> NoReturn:
        self.key = key
        self.value = value


class Node:
    # pylint: disable=too-few-public-methods
    """Simple node with data in double linked list"""

    def __init__(self, data: KVPair = None) -> NoReturn:
        self.data = data
        self.next = None
        self.prev = None


class CircledDoubleLinkedList:
    """The pointer to the previous node of the list root
    contains the address of the last node.

    The pointer to the next node of the last node
    contains the address of the root of the list."""

    def __init__(self) -> NoReturn:
        self.root = Node()
        self.len = 0

        # the root node should point to itself when the linked list is empty
        self.root.next = self.root
        self.root.prev = self.root

    def move_front(self, node: Node or None) -> Any:
        """Whenever a key is retrieved from our cache,
        makes that key the last one used.
        """
        root_logger.info("Do LRU strategy")

        if node is None:
            root_logger.debug("Node is empty")
            return None

        # if node is already in the linked list,
        # remove it from its current position
        root_logger.debug("Remove node from its current position")
        if node.prev is not None and node.next is not None:
            node.next.prev = node.prev
            node.prev.next = node.next

        node.prev = self.root
        node.next = self.root.next

        #  make linked list looped
        root_logger.debug("Make linked list looped")
        self.root.next.prev = node
        self.root.next = node

        return node

    def add_data(self, data: KVPair) -> Node:
        """Fill new node with data and
        move it at the beginning of the list
        """

        root_logger.debug("Fill new node")
        node = Node(data)
        self.move_front(node)
        self.increase_len()
        return node

    def remove_tail(self) -> Any:
        """Remove tail from linked list"""

        root_logger.debug("Remove tail from linked list")
        return self.remove(self.root.prev)

    def remove(self, node: Node) -> Any:
        """Remove node from linked list"""
        root_logger.debug("Remove node from linked list")
        if self.len == 0:
            return None

        self.decrease_len()
        return self.isolate(node)

    @staticmethod
    def isolate(node: Node) -> Node:
        """Removes a node from its current position
        It also sets its next and prev pointers to None
        to prevent memory leaks
        """

        root_logger.debug("Removes a node from its current position")
        node.next.prev = node.prev
        node.prev.next = node.next
        node.next = None
        node.prev = None
        return node

    def increase_len(self) -> NoReturn:
        """Increase CircledDoubleLinkedList length"""
        root_logger.debug("Increase CDLL len")
        self.len += 1

    def decrease_len(self) -> NoReturn:
        """Decrease CircledDoubleLinkedList length"""
        root_logger.debug("Decrease CDLL len")
        self.len -= 1


class LRUCache:
    """Main class. Store the data in nodes with key-value structure (KVPair).
    Use the double-linked list to realize the
    last-recently used strategy for caching.

    Whenever a key is retrieved or updated, it becomes the last used one
    When the maximum cache size is reached, delete the least recently used key
    """

    def __init__(self, limit: int = 42) -> None:
        if limit <= 0:
            root_logger.warning("Max size must be larger than zero. Given %d", limit)
            raise LimitException(f"Max size must be larger than zero. Given {limit}")
        self.__limit = limit
        self.__list = CircledDoubleLinkedList()
        self.__nodes = {}

    @property
    def limit(self):
        """Getter of LRUCache limit value"""
        return self.__limit

    @property
    def cdl_list(self):
        """Getter of LRUCache CDLL"""
        return self.__list

    @property
    def nodes(self):
        """Getter of LRUCache mapped nodes"""
        return self.__nodes

    def get_value(self, key: str) -> Any:
        """Return the necessary key"""

        root_logger.debug("Get node")
        node = self.__nodes.get(key, None)
        # If key doesn't exist return None
        if node is None:
            root_logger.info("Key %s doesn't exist", key)
            return None

        # make the key to the front of linked list (most recently used)
        self.__list.move_front(node)
        root_logger.info("Get %s by key: %s", node.data.value, key)
        return node.data.value

    def set_value(self, key: str, value: Any) -> None:
        """Set the new key, value pair into linked list"""

        root_logger.debug("Get node to set %s", key)
        node = self.__nodes.get(key, None)

        # if the key already exists, update the value
        if node is not None:
            root_logger.info("Key %s already exists, update the %s by %s",
                             key, node.data.value,
                             value,
                             )
            node.data.value = value
            self.__list.move_front(node)
            return

        # if the cache has reached its limit,
        # remove the least recently used key
        if self.__list.len == self.__limit:
            root_logger.warning("Cache limit exceeded")
            expired_node = self.__list.remove_tail()
            root_logger.warning("Del expired node")
            del self.__nodes[expired_node.data.key]

        self.__nodes[key] = self.__list.add_data(KVPair(key, value))
        root_logger.info("Set %s to %s", value, key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", default="file")
    parser.add_argument("-c", "--capacity", type=int, default=5)

    args = parser.parse_args()

    log_config = {
        "version": 1,
        "formatters": {
            "simple": {
                "format": "%(asctime)s: %(message)s",
                "datefmt": "%H:%M:%S",
            },
            "smart": {
                "format": "%(asctime)s: %(levelname)s: %(message)s",
                "datefmt": "%H:%M:%S",
            },
            "ultimate": {
                "format": "%(asctime)s: %(name)s: %(levelname)s: %(message)s",
                "datefmt": "%H:%M:%S",
            },
        },
        "handlers": {
            "stdout_log": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
            "warning_log": {
                "level": "WARNING",
                "filename": "warning_cache.log",
                "class": "logging.FileHandler",
                "formatter": "smart",
            },
            "debug_log": {
                "level": "DEBUG",
                "filename": "debug_cache.log",
                "class": "logging.FileHandler",
                "formatter": "ultimate",
            },
        },
        "loggers": {
            "": {
                "level": "DEBUG",
                "handlers": ["stdout_log", "warning_log", "debug_log"]
                if args.s == "stdout"
                else ["warning_log", "debug_log"],
            },
        },
    }

    logging.config.dictConfig(log_config)
    root_logger = logging.getLogger(__name__)

    root_logger.info("=====PROGRAM START=====")

    cache = LRUCache(args.capacity)
    cache.set_value("k1", "val1")
    cache.set_value("k2", "val2")

    cache.get_value("k3")
    cache.get_value("k2")
    cache.get_value("k1")

    cache.set_value("k3", "val3")
    cache.set_value("k4", "val4")
    cache.set_value("k5", "val5")
    cache.set_value("k6", "val6")

    cache.get_value("k3")
    cache.get_value("k2")
    cache.get_value("k1")

    cache.set_value("k6", "new_val_6")
    cache.get_value("k3")
    cache.get_value("k8")

    root_logger.info("=====PROGRAM STOP=====")
