# ==================== 5. Принцип инверсии зависимостей (DIP) ====================

"""
DIP:
1. Модули верхнего уровня не должны зависеть от модулей нижнего уровня.
   Оба должны зависеть от абстракций.
2. Абстракции не должны зависеть от деталей.
   Детали должны зависеть от абстракций.

Нарушение приводит к:
- Жесткой связанности компонентов
- Трудностям при тестировании
- Проблемам при замене реализации
"""


# Плохой пример (нарушение DIP)
class LightBulb:
    """Класс нижнего уровня (деталь реализации)"""

    def turn_on(self):
        print("Лампочка включена")

    def turn_off(self):
        print("Лампочка выключена")


class ElectricPowerSwitch:
    """Класс верхнего уровня напрямую зависит от LightBulb"""

    def __init__(self, bulb: LightBulb):
        self.bulb = bulb  # Прямая зависимость от конкретного класса
        self.on = False

    def press(self):
        if self.on:
            self.bulb.turn_off()
            self.on = False
        else:
            self.bulb.turn_on()
            self.on = True


# Хороший пример (соблюдение DIP)
from abc import ABC, abstractmethod


class Switchable(ABC):
    """Абстракция, от которой зависят оба уровня"""

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass


class LightBulb(Switchable):
    """Реализация абстракции для лампочки"""

    def turn_on(self):
        print("Лампочка включена")

    def turn_off(self):
        print("Лампочка выключена")


class Fan(Switchable):
    """Реализация абстракции для вентилятора"""

    def turn_on(self):
        print("Вентилятор включен")

    def turn_off(self):
        print("Вентилятор выключен")


class ElectricPowerSwitch:
    """Зависит от абстракции, а не от конкретной реализации"""

    def __init__(self, device: Switchable):  # Зависимость от абстракции
        self.device = device
        self.on = False

    def press(self):
        if self.on:
            self.device.turn_off()
            self.on = False
        else:
            self.device.turn_on()
            self.on = True

