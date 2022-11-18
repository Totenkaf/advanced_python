"""
CustomList project.
Copyright 2022 by Artem Ustsov
"""
from itertools import zip_longest
from typing import Iterable


class CustomList(list):
    """Inherits the built-in type list and
    provides work with a collection of integer elements
    """

    def __init__(self, iterable: Iterable):
        if not isinstance(iterable, list):
            raise TypeError
        if not all(map(lambda x: isinstance(x, int), iterable)):
            raise ValueError

        super().__init__(iterable)

    @classmethod
    def __arithmetic_action(
        cls,
        r_array: Iterable,
        l_array: Iterable,
        operator: str,
        fill_value=0,
    ):
        """Provides arithmetic operations on collections.
        If the lengths of the collections are different,
        pads the smaller one with zeros
        """

        if not isinstance(l_array, (list, cls)) or not isinstance(
            r_array,
            (list, cls),
        ):
            raise TypeError
        if operator == "+":
            return [
                x + y
                for x, y in zip_longest(
                    r_array, l_array, fillvalue=fill_value
                )
            ]
        if operator == "-":
            return [
                x - y
                for x, y in zip_longest(
                    r_array, l_array, fillvalue=fill_value
                )
            ]

    def __sub__(self, other: Iterable):
        result_list = self.__arithmetic_action(
            self,
            other,
            operator="-",
        )
        return CustomList(result_list)

    def __isub__(self, other: Iterable):
        result_list = self.__arithmetic_action(
            self,
            other,
            operator="-",
        )
        return CustomList(result_list)

    def __rsub__(self, other: Iterable):
        result_list = self.__arithmetic_action(
            other,
            self,
            operator="-",
        )
        return CustomList(result_list)

    def __add__(self, other: Iterable):
        result_list = self.__arithmetic_action(
            self,
            other,
            operator="+",
        )
        return CustomList(result_list)

    def __iadd__(self, other: Iterable):
        result_list = self.__arithmetic_action(
            self,
            other,
            operator="+",
        )
        return CustomList(result_list)

    def __radd__(self, other: Iterable):
        result_list = self.__arithmetic_action(
            other,
            self,
            operator="+",
        )
        return CustomList(result_list)

    def __eq__(self, other: Iterable):
        return sum(self) == sum(other)

    def __ne__(self, other: Iterable):
        return sum(self) != sum(other)

    def __gt__(self, other: Iterable):
        return sum(self) > sum(other)

    def __ge__(self, other: Iterable):
        return sum(self) >= sum(other)

    def __lt__(self, other: Iterable):
        return sum(self) < sum(other)

    def __le__(self, other: Iterable):
        return sum(self) <= sum(other)

    def __str__(self):
        return f"{[item for item in self]}, {sum(self)}"
