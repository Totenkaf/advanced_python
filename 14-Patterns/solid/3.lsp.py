# ==================== 3. Принцип подстановки Лисков (LSP) ====================

"""
LSP: Подклассы должны быть взаимозаменяемы с их базовыми классами без нарушения работы программы.

Нарушение приводит к:
- Неожиданным ошибкам при замене класса
- Нарушению контракта базового класса
- Проблемам при полиморфном использовании классов
"""


# Плохой пример (нарушение LSP)
class Rectangle:
    """Базовый класс прямоугольника"""

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def area(self):
        return self.width * self.height


class Square(Rectangle):
    """Квадрат - частный случай прямоугольника, но нарушает LSP"""

    def set_width(self, width):
        """У квадрата ширина и высота всегда равны - это изменяет ожидаемое поведение"""
        self.width = width
        self.height = width

    def set_height(self, height):
        self.width = height
        self.height = height


def test_rectangle(rect: Rectangle):
    """Функция ожидает, что изменение ширины не влияет на высоту"""
    rect.set_width(5)
    rect.set_height(4)
    assert rect.area() == 20  # Для Square будет 16 - нарушение контракта!


# Хороший пример (соблюдение LSP)
from abc import ABC, abstractmethod


class Shape(ABC):
    """Абстрактный базовый класс для всех фигур"""

    @abstractmethod
    def area(self):
        """Каждая фигура реализует свой расчет площади"""
        pass


class Rectangle(Shape):
    """Прямоугольник - независимая реализация"""

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Square(Shape):
    """Квадрат - независимая реализация, не нарушающая LSP"""

    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2
