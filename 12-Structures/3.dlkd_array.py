"""
Key Features
Bidirectional Traversal: Each node has both next and prev pointers

Efficient End Operations: O(1) time for head/tail insertions/deletions

Complete API:

- Insertion: append(), prepend(), insert_after(), insert_at_position()
- Deletion: delete_head(), delete_tail(), delete_value()
- Access: get_at_position(), search()
- Utility: reverse(), __iter__(), reverse_iter()

Complexity Summary
Operation	            Time Complexity	Description
append()	            O(1)	        Add to end
prepend()	            O(1)	        Add to beginning
insert_after()	        O(n)	        Insert after specific value
insert_at_position()	O(n)	        Insert at index
delete_head()	        O(1)	        Remove first element
delete_tail()	        O(1)	        Remove last element
delete_value()	        O(n)	        Remove first occurrence of value
search()	            O(n)	        Check if value exists
get_at_position()	    O(n)	        Get value by index
reverse()	            O(n)	        Reverse list in-place
Iteration	            O(n)           total	O(1) per element during traversal

When to Use
- When you need frequent insertions/deletions at both ends
- When bidirectional traversal is needed
- When random access is NOT a primary requirement (use arrays for that)

This implementation provides a robust foundation
that can be extended for specific use cases like LRU caches or deque implementations.
"""


class Node:
    """
    Node class for doubly linked list elements
    Each node contains:
    - data: the stored value
    - next: reference to next node
    - prev: reference to previous node
    """

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """
    Doubly Linked List implementation
    Usage: When you need efficient insertions/deletions at both ends and bidirectional traversal

    Time Complexity Analysis:
    - Access: O(n)
    - Search: O(n)
    - Insert at head/tail: O(1)
    - Delete at head/tail: O(1)
    - Insert/delete in middle: O(n) (need to traverse to position)

    Space Complexity: O(n)
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        """Return the number of elements: O(1)"""
        return self.size

    def is_empty(self):
        """Check if list is empty: O(1)"""
        return self.size == 0

    def append(self, data):
        """
        Add element at the end: O(1)
        1. Create new node
        2. If list is empty, set as head and tail
        3. Otherwise, adjust tail's next and new node's prev
        """
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def prepend(self, data):
        """
        Add element at the beginning: O(1)
        1. Create new node
        2. If list is empty, set as head and tail
        3. Otherwise, adjust head's prev and new node's next
        """
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def insert_after(self, target_data, new_data):
        """
        Insert new node after first occurrence of target_data: O(n)
        1. Find target node
        2. Handle cases: after tail, middle, or not found
        """
        current = self.head
        while current:
            if current.data == target_data:
                new_node = Node(new_data)

                # If inserting after tail
                if current == self.tail:
                    self.append(new_data)
                    return

                # Insert in middle
                new_node.next = current.next
                new_node.prev = current
                current.next.prev = new_node
                current.next = new_node
                self.size += 1
                return
            current = current.next
        raise ValueError(f"Target data {target_data} not found in list")

    def insert_at_position(self, position, data):
        """
        Insert at specific position (0-based index): O(n)
        1. Handle edge cases (position 0 or position == size)
        2. Traverse to position-1
        3. Insert new node
        """
        if position < 0 or position > self.size:
            raise IndexError("Position out of bounds")

        if position == 0:
            self.prepend(data)
            return
        if position == self.size:
            self.append(data)
            return

        new_node = Node(data)
        current = self.head
        for _ in range(position - 1):
            current = current.next

        new_node.next = current.next
        new_node.prev = current
        current.next.prev = new_node
        current.next = new_node
        self.size += 1

    def delete_head(self):
        """
        Remove first element: O(1)
        1. Handle empty list case
        2. Handle single element case
        3. Normal case with multiple elements
        """
        if self.is_empty():
            raise IndexError("List is empty")

        data = self.head.data
        if self.size == 1:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self.size -= 1
        return data

    def delete_tail(self):
        """
        Remove last element: O(1)
        1. Handle empty list case
        2. Handle single element case
        3. Normal case with multiple elements
        """
        if self.is_empty():
            raise IndexError("List is empty")

        data = self.tail.data
        if self.size == 1:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self.size -= 1
        return data

    def delete_value(self, value):
        """
        Delete first occurrence of value: O(n)
        1. Handle empty list case
        2. Special cases if value is at head or tail
        3. Normal case in middle
        """
        if self.is_empty():
            raise ValueError("List is empty")

        current = self.head

        # If head contains the value
        if current.data == value:
            return self.delete_head()

        # If tail contains the value
        if self.tail.data == value:
            return self.delete_tail()

        # Search in middle
        while current:
            if current.data == value:
                current.prev.next = current.next
                current.next.prev = current.prev
                self.size -= 1
                return current.data
            current = current.next

        raise ValueError(f"Value {value} not found in list")

    def search(self, value):
        """
        Search for value in list: O(n)
        Returns True if found, False otherwise
        """
        current = self.head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False

    def get_at_position(self, position):
        """
        Get value at specific position (0-based): O(n)
        """
        if position < 0 or position >= self.size:
            raise IndexError("Position out of bounds")

        current = self.head
        for _ in range(position):
            current = current.next
        return current.data

    def reverse(self):
        """
        Reverse the list in-place: O(n)
        1. Swap head and tail
        2. Reverse all next/prev pointers
        """
        if self.size <= 1:
            return

        current = self.head
        self.head, self.tail = self.tail, self.head

        while current:
            # Swap next and prev pointers
            current.next, current.prev = current.prev, current.next
            # Move to next node (which is now prev due to swap)
            current = current.prev

    def __iter__(self):
        """Iterator for forward traversal: O(n) total, O(1) per element"""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def reverse_iter(self):
        """Iterator for backward traversal: O(n) total, O(1) per element"""
        current = self.tail
        while current:
            yield current.data
            current = current.prev

    def __str__(self):
        """String representation of list: O(n)"""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        return " <-> ".join(elements)


if __name__ == "__main__":
    dll = DoublyLinkedList()
    for i in range(10):
        dll.append(i)
    print(dll)
