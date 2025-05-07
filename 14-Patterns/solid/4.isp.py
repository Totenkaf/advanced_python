# ==================== 4. Принцип разделения интерфейса (ISP) ====================

"""
ISP: Клиенты не должны зависеть от интерфейсов, которые они не используют.

Создавайте узкоспециализированные интерфейсы вместо одного "толстого" интерфейса.

Нарушение приводит к:
- Зависимостям от ненужных методов
- Пустым или выброшенным NotImplementedError
- Трудностям при повторном использовании кода
"""


# Плохой пример (нарушение ISP)
class Machine(ABC):
    """"Толстый" интерфейс с методами для всех возможных устройств"""

    @abstractmethod
    def print(self, document):
        pass

    @abstractmethod
    def fax(self, document):
        pass

    @abstractmethod
    def scan(self, document):
        pass


class OldPrinter(Machine):
    """Старый принтер вынужден реализовывать ненужные методы"""

    def print(self, document):
        print("Печать документа")

    def fax(self, document):
        """Принтер не поддерживает факс, но вынужден иметь этот метод"""
        raise NotImplementedError("Факс не поддерживается")

    def scan(self, document):
        """Принтер не поддерживает сканирование"""
        raise NotImplementedError("Сканер не поддерживается")


# Хороший пример (соблюдение ISP)
class Printer(ABC):
    """Узкий интерфейс только для печати"""

    @abstractmethod
    def print(self, document):
        pass


class Scanner(ABC):
    """Узкий интерфейс только для сканирования"""

    @abstractmethod
    def scan(self, document):
        pass


class SimplePrinter(Printer):
    """Простой принтер реализует только нужные ему методы"""

    def print(self, document):
        print("Печать документа")


class Photocopier(Printer, Scanner):
    """Копировальный аппарат реализует несколько интерфейсов"""

    def print(self, document):
        print("Печать документа")

    def scan(self, document):
        print("Сканирование документа")
