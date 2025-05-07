class LinkedListNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    """
    Singly Linked List implementation
    Usage: When frequent insertions/deletions at beginning are needed
    Time Complexity:
        Access: O(n)
        Search: O(n)
        Insert at head: O(1)
        Insert at any position: O(n) in general
        Insert at tail: O(1) with tail pointer, O(n) without
        Delete at head: O(1)
        Delete at any position: O(n) in general
        Delete at tail: O(n)
    Space Complexity: O(n)
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def push_back(self, value):
        """Add to end: O(1)"""
        new_node = LinkedListNode(value)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def push_front(self, value):
        """Add to beginning: O(1)"""
        new_node = LinkedListNode(value)
        new_node.next = self.head
        self.head = new_node
        if not self.tail:
            self.tail = new_node
        self.length += 1

    def pop_front(self):
        # nothing to delete
        if self.head is None:
            return

        # single elem linked list
        if self.head == self.tail:
            self.tail = self.head = None
            self.length = 0

        tmp = self.head
        # head as second elem
        self.head = tmp.next
        # init GC
        del tmp
        self.length -= 1

    def pop_back(self):
        if not self.tail:
            return

        if self.head == self.tail:
            self.head = self.tail = None
            self.length = 0
            return

        tmp = self.head
        # search for the end of linked list
        while tmp.next != self.tail:
            tmp = tmp.next

        # make end as None
        tmp.next = None
        # make new tail
        self.tail = tmp
        self.length -= 1

    def get_at(self, idx: int):
        """Get the value at position idx"""

        if idx < 0:
            return None

        # any current node
        tmp = self.head
        # idx counter
        n = 0

        while tmp and idx != n and tmp.next:
            tmp = tmp.next
            n += 1

        return tmp if n == idx else None

    def insert(self, idx: int, value):
        """Insert value at position idx: O(n)"""
        left = self.get_at(idx)
        if not left:
            return

        right = left.next
        new = LinkedListNode(value)

        left.next = new
        new.next = right

        # insert at the end of list situation
        if right is None:
            self.head = new
        self.length += 1

    def erase(self, idx: int):
        """Delete value at position idx: O(n)"""
        if idx < 0:
            return None

        # first for deleting
        if idx == 0:
            self.pop_front()
            self.length -= 1
            return None

        # before deleting
        left = self.get_at(idx - 1)
        tmp = left.next

        # nothing to delete
        if tmp is None:
            return None

        # after deleting
        right = tmp.next
        left.next = right

        # deleting last, so tail should be as previous one
        if tmp == self.tail:
            self.tail = left

        del tmp
        self.length -= 1

    def delete(self, value):
        """Delete first occurrence: O(n)"""
        current = self.head
        prev = None
        while current:
            if current.value == value:
                if prev:
                    prev.next = current.next
                    if not current.next:  # Deleting tail
                        self.tail = prev
                else:
                    self.head = current.next
                    if not current.next:  # List becomes empty
                        self.tail = None
                self.length -= 1
                return True
            prev = current
            current = current.next
        return False

    def __len__(self):
        """Get length: O(1)"""
        return self.length

    def __iter__(self):
        """Iterate through list: O(n)"""
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __str__(self):
        """Pretty print: O(n)"""
        return f"[{', '.join(str(elem) for elem in self)}]"


if __name__ == '__main__':
    ll = LinkedList()
    ll.push_front(1)
    ll.push_front(2)
    ll.push_front(3)
    print(ll, len(ll))

    ll.pop_back()
    print(ll, len(ll))

    ll.push_back(2)
    ll.erase(1)
    ll.erase(1)
    ll.erase(0)
    print(ll, len(ll))
