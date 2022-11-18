"""
LRUCache package main file
Copyright 2022 by Artem Ustsov
"""

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

        if node is None:
            return None

        # if node is already in the linked list,
        # remove it from its current position
        if node.prev is not None and node.next is not None:
            node.next.prev = node.prev
            node.prev.next = node.next

        node.prev = self.root
        node.next = self.root.next

        #  make linked list looped
        self.root.next.prev = node
        self.root.next = node

        return node

    def add_data(self, data: KVPair) -> Node:
        """Fill new node with data and
        move it at the beginning of the list
        """

        node = Node(data)
        self.move_front(node)
        self.increase_len()
        return node

    def remove_tail(self) -> Any:
        """Remove tail from linked list"""
        return self.remove(self.root.prev)

    def remove(self, node: Node) -> Any:
        """Remove node from linked list"""
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
        node.next.prev = node.prev
        node.prev.next = node.next
        node.next = None
        node.prev = None
        return node

    def increase_len(self) -> NoReturn:
        """Increase CircledDoubleLinkedList length"""
        self.len += 1

    def decrease_len(self) -> NoReturn:
        """Decrease CircledDoubleLinkedList length"""
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
            raise LimitException("Max size must be larger than zero")
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

        node = self.__nodes.get(key, None)
        # If key doesn't exist return None
        if node is None:
            return None

        # make the key to the front of linked list (most recently used)
        self.__list.move_front(node)
        return node.data.value

    def set_value(self, key: str, value: Any) -> None:
        """Set the new key, value pair into linked list"""

        node = self.__nodes.get(key, None)

        # if the key already exists, update the value
        if node is not None:
            node.data.value = value
            self.__list.move_front(node)
            return

        # if the cache has reached its limit,
        # remove the least recently used key
        if self.__list.len == self.__limit:
            expired_node = self.__list.remove_tail()
            del self.__nodes[expired_node.data.key]

        self.__nodes[key] = self.__list.add_data(KVPair(key, value))
