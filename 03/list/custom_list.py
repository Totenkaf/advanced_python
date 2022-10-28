"""
CustomList project.
Copyright 2022 by Artem Ustsov
"""
from itertools import zip_longest


class CustomList(list):
    """
    Inherits the built-in type list and
    provides work with a collection of integer elements
    """

    def __init__(self, array=None):
        if array is None:
            array = []
        if not isinstance(array, list):
            raise TypeError
        if not all(map(lambda x: isinstance(x, int), array)):
            raise ValueError

        super().__init__(array)
        self.__array = array

    @property
    def array(self):
        """
        Gets the array of CustList
        """
        return self.__array

    @array.setter
    def array(self, array):
        self.__array = array

    @classmethod
    def __convert_to_list(cls, other: object):
        # pylint: disable=protected-access
        other_array = other
        if isinstance(other, cls):
            other_array = other.__array
        return other_array

    @classmethod
    def __arithmetic_action(
        cls,
        r_array: list,
        l_array: list,
        operator: str,
        fill_value=0,
    ):
        """
        Provides arithmetic operations on collections.
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
                x + y for x, y in zip_longest(r_array, l_array, fillvalue=fill_value)
            ]
        if operator == "-":
            return [
                x - y for x, y in zip_longest(r_array, l_array, fillvalue=fill_value)
            ]
        return None

    def __sub__(self, other: object):
        result_list = self.__arithmetic_action(
            self.__array,
            self.__convert_to_list(other),
            operator="-",
        )
        return CustomList(result_list)

    def __isub__(self, other: object):
        result_list = self.__arithmetic_action(
            self.__array,
            self.__convert_to_list(other),
            operator="-",
        )
        return CustomList(result_list)

    def __rsub__(self, other: object):
        result_list = self.__arithmetic_action(
            self.__convert_to_list(other),
            self.__array,
            operator="-",
        )
        return CustomList(result_list)

    def __add__(self, other: object):
        result_list = self.__arithmetic_action(
            self.__array,
            self.__convert_to_list(other),
            operator="+",
        )
        return CustomList(result_list)

    def __iadd__(self, other: object):
        result_list = self.__arithmetic_action(
            self.__array,
            self.__convert_to_list(other),
            operator="+",
        )
        return CustomList(result_list)

    def __radd__(self, other: object):
        result_list = self.__arithmetic_action(
            self.__convert_to_list(other),
            self.__array,
            operator="+",
        )
        return CustomList(result_list)

    def __eq__(self, other: object):
        return sum(self.__array) == sum(self.__convert_to_list(other))

    def __str__(self):
        return f"{self.__array}, {sum(self.__array)}"

    def __len__(self):
        return len(self.__array)
