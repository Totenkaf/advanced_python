# Список - динамический массив, содержащий ССЫЛКИ на объекты с конкретным типом
# Под капотом - обычный статический массив, а точнее массив указателей
a = [1, "True", (1, 2, 3), False]
b = list()

# Append O(1)
a.append("False")

# Insert/Delete O(n)
# Add new place for elem at the end
# Make circle move right for all elems
# Add new link before 1 index
a.insert(1, "False")
a.pop(1)
a.remove("True")

# Delete last elem O(1)
a.pop(-1)

# Get by index O(1)
# Используя адресную арифметику
# p = a + (j - 1) * k
# k - байт на хранение
# j - элемент
a[0]

# Concatenate O(n+m)
a + b

# Slice O(n)
# Slice make a new array, then copy data from array to slice
c = a[1:3]

# Использование:
# хорош для частого обращения к элементам коллекции произвольной длины (получение и перезапись)
# добавления и удаления элемента с конца коллекции

# Недостатки:
# плохо хранить большие непрерывные куски данных

import ctypes


class OhMyList:
    def __init__(self):
        self.length = 0
        self.capacity = 8
        self.array = (self.capacity * ctypes.py_object)()

    def append(self, item):
        self.array[self.length] = item
        self.length += 1

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        return self.array[idx]


class List:
    """
    Dynamic Array implementation (Python's built-in list)
    Usage: General-purpose sequential storage, stacks, queues
    Time Complexity:
        Access: O(1)
        Search: O(n)
        Insert at end: O(1) amortized
        Insert at beginning/middle: O(n)
        Delete at end: O(1)
        Delete at beginning/middle: O(n)
    Space Complexity: O(n)
    """

    def __init__(self):
        self.data = []

    def append(self, item):
        """Add item to end of list: O(1) amortized"""
        self.data.append(item)

    def insert(self, index, item):
        """Insert item at index: O(n)"""
        self.data.insert(index, item)

    def remove(self, item):
        """Remove first occurrence of item: O(n)"""
        self.data.remove(item)

    def pop(self, index=-1):
        """Remove and return item at index: O(1) at end, O(n) otherwise"""
        return self.data.pop(index)

    def __getitem__(self, index):
        """Get item at index: O(1)"""
        return self.data[index]

    def __len__(self):
        """Return length: O(1)"""
        return len(self.data)

    def __contains__(self, item):
        """Check if item in list: O(n)"""
        return item in self.data
