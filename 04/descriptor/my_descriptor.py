"""
Data-descriptors package main file
Copyright 2022 by Artem Ustsov
"""


# pylint: disable=attribute-defined-outside-init
class Integer:
    """
    Integer data-descriptor
    """

    @classmethod
    def is_integer(cls, value: int) -> None:
        """
        Checks if an incoming value is an int
        """
        if not isinstance(value, int):
            raise TypeError(f"Value must be a int-like not {type(value)}")

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        self.is_integer(value)
        instance.__dict__[self.name] = value


# pylint: disable=attribute-defined-outside-init
class String:
    """
    String data-descriptor
    """

    @classmethod
    def is_string(cls, value: str) -> None:
        """
        Checks if an incoming value is an str
        """
        if not isinstance(value, str):
            raise TypeError(f"Value must be a string-like not {type(value)}")

    @classmethod
    def is_alpha_string(cls, value: str) -> None:
        """
        Checks if an incoming value is an str with letters
        """
        if not value.isalpha():
            raise ValueError("Value must consists of only ascii letters")

    def __set_name__(self, owner, name):
        self.name = "".join(["_", name])

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        self.is_string(value)
        self.is_alpha_string(value)
        instance.__dict__[self.name] = value


# pylint: disable=attribute-defined-outside-init
class PositiveInteger(Integer):
    """
    Positive Integer data-descriptor. Inherits Integer class
    """

    @classmethod
    def is_positive(cls, value: int):
        """
        Checks if an incoming value is strong positive
        """
        if not value > 0:
            raise ValueError(
                f"Value must be a strong positive. You gave {value}",
            )

    def __set__(self, instance, value):
        self.is_integer(value)
        self.is_positive(value)
        instance.__dict__[self.name] = value


# pylint: disable=too-few-public-methods
class Data:
    """
    Main Data class
    """

    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price
