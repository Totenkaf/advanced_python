# ==================== 2. Принцип открытости/закрытости (OCP) ====================

"""
OCP: Классы должны быть открыты для расширения, но закрыты для модификации.

Это означает, что мы можем добавлять новую функциональность,
не изменяя существующий код (через наследование, композицию и т.д.).

Нарушение приводит к:
- Постоянным изменениям существующего кода
- Риску сломать работающую функциональность
- Трудностям в расширении системы
"""


# Плохой пример (нарушение OCP)
class Discount:
    """При добавлении нового типа скидки нужно изменять этот класс"""

    def __init__(self, customer_type: str):
        self.customer_type = customer_type

    def give_discount(self):
        if self.customer_type == "regular":
            return 10
        elif self.customer_type == "premium":
            return 20
        # Для нового типа нужно добавлять еще один elif


# Хороший пример (соблюдение OCP)
from abc import ABC, abstractmethod


class Discount(ABC):
    """Базовый абстрактный класс, закрытый для модификации"""

    @abstractmethod
    def give_discount(self):
        """Каждый подкласс реализует свою логику расчета скидки"""
        pass


class RegularDiscount(Discount):
    """Реализация для обычных клиентов - можно добавлять новые классы, не меняя существующие"""

    def give_discount(self):
        return 10


class PremiumDiscount(Discount):
    """Реализация для премиум клиентов"""

    def give_discount(self):
        return 20


class NewYearDiscount(Discount):
    """Новый тип скидки - добавлен без изменения существующего кода"""

    def give_discount(self):
        return 30
