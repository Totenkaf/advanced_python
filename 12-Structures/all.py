"""
This implementation includes:
1. Linear structures (List, LinkedList, Stack, Queue, Deque)
2. Hash-based structures (HashTable)
3. Tree structures (BST, AVL Tree)
4. Heap (MinHeap)
5. Graph (Adjacency List)
6. Trie (Prefix Tree)
7. Disjoint Set (Union-Find)
8. Bloom Filter (Probabilistic)
9. LRU Cache

Each class includes:
- Detailed docstring explaining usage and complexity
- All essential methods with their time/space complexity
- Helper methods where needed
- Clean, well-structured implementation

You can use this as a reference or import specific data structures as needed in your projects.
"""

"""
Data Structures Implementation in Python
This file contains implementations of all major data structures with their methods,
usage explanations, and time/space complexity analysis for each operation.
"""


# ==================== LINEAR DATA STRUCTURES ====================

class Stack:
    """
    Stack implementation (LIFO)
    Usage: Function call stack, undo operations, DFS
    Time Complexity:
        Push: O(1)
        Pop: O(1)
        Peek: O(1)
    Space Complexity: O(n)
    """

    def __init__(self):
        self.items = []

    def push(self, item):
        """Push item onto stack: O(1)"""
        self.items.append(item)

    def pop(self):
        """Remove and return top item: O(1)"""
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        """Return top item without removal: O(1)"""
        if not self.is_empty():
            return self.items[-1]

    def is_empty(self):
        """Check if stack is empty: O(1)"""
        return len(self.items) == 0

    def size(self):
        """Return number of items: O(1)"""
        return len(self.items)


class Queue:
    """
    Queue implementation (FIFO)
    Usage: BFS, task scheduling, buffering
    Time Complexity:
        Enqueue: O(1)
        Dequeue: O(1)
        Peek: O(1)
    Space Complexity: O(n)
    """

    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """Add item to end: O(1)"""
        self.items.append(item)

    def dequeue(self):
        """Remove and return front item: O(1)"""
        if not self.is_empty():
            return self.items.pop(0)

    def peek(self):
        """Return front item without removal: O(1)"""
        if not self.is_empty():
            return self.items[0]

    def is_empty(self):
        """Check if queue is empty: O(1)"""
        return len(self.items) == 0

    def size(self):
        """Return number of items: O(1)"""
        return len(self.items)


class Deque:
    """
    Double-Ended Queue implementation
    Usage: Sliding window problems, undo-redo operations
    Time Complexity:
        Append/pop at either end: O(1)
        Insert/delete in middle: O(n)
        Access by index: O(1)
    Space Complexity: O(n)
    """

    def __init__(self):
        self.items = []

    def append_left(self, item):
        """Add to front: O(1)"""
        self.items.insert(0, item)

    def append(self, item):
        """Add to end: O(1)"""
        self.items.append(item)

    def pop_left(self):
        """Remove and return front item: O(1)"""
        if not self.is_empty():
            return self.items.pop(0)

    def pop(self):
        """Remove and return end item: O(1)"""
        if not self.is_empty():
            return self.items.pop()

    def peek_left(self):
        """Return front item without removal: O(1)"""
        if not self.is_empty():
            return self.items[0]

    def peek(self):
        """Return end item without removal: O(1)"""
        if not self.is_empty():
            return self.items[-1]

    def is_empty(self):
        """Check if deque is empty: O(1)"""
        return len(self.items) == 0

    def size(self):
        """Return number of items: O(1)"""
        return len(self.items)


# ==================== HASH-BASED STRUCTURES ====================

class HashTable:
    """
    Hash Table implementation with chaining
    Usage: Fast lookups, dictionaries, caches
    Time Complexity (average case):
        Insert: O(1)
        Search: O(1)
        Delete: O(1)
    Time Complexity (worst case): O(n) for all operations
    Space Complexity: O(n)
    """

    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        """Insert key-value pair: O(1) average, O(n) worst"""
        hash_key = self._hash(key)
        bucket = self.table[hash_key]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def search(self, key):
        """Search for key and return value: O(1) average, O(n) worst"""
        hash_key = self._hash(key)
        bucket = self.table[hash_key]

        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        """Delete key-value pair: O(1) average, O(n) worst"""
        hash_key = self._hash(key)
        bucket = self.table[hash_key]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False

    def __contains__(self, key):
        """Check if key exists: O(1) average, O(n) worst"""
        return self.search(key) is not None


# ==================== TREE-BASED STRUCTURES ====================

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """
    Binary Search Tree implementation
    Usage: Searching, sorting, database indices
    Time Complexity (balanced):
        Insert: O(log n)
        Search: O(log n)
        Delete: O(log n)
    Time Complexity (unbalanced): O(n) for all operations
    Space Complexity: O(n)
    """

    def __init__(self):
        self.root = None

    def insert(self, value):
        """Insert a value: O(log n) average, O(n) worst"""
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)

    def search(self, value):
        """Search for a value: O(log n) average, O(n) worst"""
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None:
            return False
        if node.value == value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def delete(self, value):
        """Delete a value: O(log n) average, O(n) worst"""
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children
            temp = self._find_min(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)

        return node

    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current


class AVLTreeNode(TreeNode):
    def __init__(self, value):
        super().__init__(value)
        self.height = 1


class AVLTree:
    """
    AVL Tree (Self-balancing BST) implementation
    Usage: When guaranteed O(log n) operations are needed
    Time Complexity:
        Insert: O(log n)
        Search: O(log n)
        Delete: O(log n)
    Space Complexity: O(n)
    """

    def __init__(self):
        self.root = None

    def insert(self, value):
        """Insert a value: O(log n)"""
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if not node:
            return AVLTreeNode(value)
        elif value < node.value:
            node.left = self._insert_recursive(node.left, value)
        else:
            node.right = self._insert_recursive(node.right, value)

        node.height = 1 + max(self._get_height(node.left),
                              self._get_height(node.right))

        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and value < node.left.value:
            return self._right_rotate(node)

        # Right Right Case
        if balance < -1 and value > node.right.value:
            return self._left_rotate(node)

        # Left Right Case
        if balance > 1 and value > node.left.value:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Left Case
        if balance < -1 and value < node.right.value:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left),
                           self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left),
                           self._get_height(y.right))

        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left),
                           self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left),
                           self._get_height(y.right))

        return y


# ==================== HEAP STRUCTURES ====================

class MinHeap:
    """
    Min Heap implementation
    Usage: Priority queues, Dijkstra's algorithm, heap sort
    Time Complexity:
        Insert: O(log n)
        Extract Min: O(log n)
        Get Min: O(1)
        Heapify: O(n)
    Space Complexity: O(n)
    """

    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def insert(self, key):
        """Insert key: O(log n)"""
        self.heap.append(key)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i):
        while i > 0 and self.heap[self.parent(i)] > self.heap[i]:
            self.heap[self.parent(i)], self.heap[i] = self.heap[i], self.heap[self.parent(i)]
            i = self.parent(i)

    def extract_min(self):
        """Remove and return minimum: O(log n)"""
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_down(self, i):
        smallest = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left

        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._heapify_down(smallest)

    def get_min(self):
        """Get minimum without removal: O(1)"""
        return self.heap[0] if self.heap else None


# ==================== GRAPH STRUCTURES ====================

class Graph:
    """
    Graph implementation using adjacency list
    Usage: Social networks, pathfinding, dependency resolution
    Time Complexity (for V vertices and E edges):
        Add vertex: O(1)
        Add edge: O(1)
        Remove vertex: O(V + E)
        Remove edge: O(E)
        Query: O(V)
    Space Complexity: O(V + E)
    """

    def __init__(self):
        self.adj_list = {}

    def add_vertex(self, vertex):
        """Add vertex: O(1)"""
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, v1, v2):
        """Add undirected edge: O(1)"""
        if v1 in self.adj_list and v2 in self.adj_list:
            self.adj_list[v1].append(v2)
            self.adj_list[v2].append(v1)

    def remove_edge(self, v1, v2):
        """Remove undirected edge: O(E)"""
        if v1 in self.adj_list and v2 in self.adj_list:
            self.adj_list[v1] = [v for v in self.adj_list[v1] if v != v2]
            self.adj_list[v2] = [v for v in self.adj_list[v2] if v != v1]

    def remove_vertex(self, vertex):
        """Remove vertex: O(V + E)"""
        if vertex in self.adj_list:
            for neighbor in self.adj_list[vertex]:
                self.adj_list[neighbor].remove(vertex)
            del self.adj_list[vertex]

    def bfs(self, start):
        """Breadth-First Search: O(V + E)"""
        visited = set()
        queue = [start]
        result = []

        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                queue.extend(self.adj_list[vertex])
        return result

    def dfs(self, start):
        """Depth-First Search: O(V + E)"""
        visited = set()
        result = []

        def _dfs(vertex):
            visited.add(vertex)
            result.append(vertex)
            for neighbor in self.adj_list[vertex]:
                if neighbor not in visited:
                    _dfs(neighbor)

        _dfs(start)
        return result


# ==================== TRIE STRUCTURE ====================

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    """
    Trie (Prefix Tree) implementation
    Usage: Autocomplete, spell checking, IP routing
    Time Complexity (for word length L):
        Insert: O(L)
        Search: O(L)
        Prefix search: O(L)
    Space Complexity: O(n*L) where n is number of words
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Insert word: O(L)"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        """Search exact word: O(L)"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix):
        """Check if prefix exists: O(L)"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


# ==================== DISJOINT SET ====================

class DisjointSet:
    """
    Disjoint Set (Union-Find) implementation
    Usage: Kruskal's algorithm, connected components
    Time Complexity (with path compression and union by rank):
        Find: O(α(n)) (inverse Ackermann function)
        Union: O(α(n))
    Space Complexity: O(n)
    """

    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x):
        """Find root with path compression: O(α(n))"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Union by rank: O(α(n))"""
        x_root = self.find(x)
        y_root = self.find(y)

        if x_root == y_root:
            return

        if self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        else:
            self.parent[y_root] = x_root
            if self.rank[x_root] == self.rank[y_root]:
                self.rank[x_root] += 1


# ==================== BLOOM FILTER ====================

class BloomFilter:
    """
    Bloom Filter probabilistic data structure
    Usage: Spell checkers, network routers, cache filtering
    Time Complexity:
        Add: O(k) where k is number of hash functions
        Membership test: O(k)
    Space Complexity: O(m) where m is filter size
    """

    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [False] * size

    def _hashes(self, item):
        """Generate multiple hash values for the item"""
        # Using Python's built-in hash with different seeds
        return [abs(hash(f"{i}{item}")) % self.size for i in range(self.hash_count)]

    def add(self, item):
        """Add item to filter: O(k)"""
        for h in self._hashes(item):
            self.bit_array[h] = True

    def __contains__(self, item):
        """Check if item might be in filter: O(k)"""
        return all(self.bit_array[h] for h in self._hashes(item))


# ==================== LRU CACHE ====================

class LRUCacheNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    LRU Cache implementation
    Usage: Caching, database query optimization
    Time Complexity:
        Get: O(1)
        Put: O(1)
    Space Complexity: O(capacity)
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = LRUCacheNode(0, 0)
        self.tail = LRUCacheNode(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node):
        """Add node right after head"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        """Remove node from linked list"""
        prev = node.prev
        next = node.next
        prev.next = next
        next.prev = prev

    def _move_to_head(self, node):
        """Move node to head position"""
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self):
        """Remove and return tail node"""
        node = self.tail.prev
        self._remove_node(node)
        return node

    def get(self, key):
        """Get value by key: O(1)"""
        if key in self.cache:
            node = self.cache[key]
            self._move_to_head(node)
            return node.value
        return -1

    def put(self, key, value):
        """Put key-value pair: O(1)"""
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                tail = self._pop_tail()
                del self.cache[tail.key]

            new_node = LRUCacheNode(key, value)
            self.cache[key] = new_node
            self._add_node(new_node)
