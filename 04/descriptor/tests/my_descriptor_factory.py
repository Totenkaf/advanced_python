"""
Data-descriptor package factory
Copyright 2022 by Artem Ustsov
"""

from descriptor.my_descriptor import Data

from factory import Factory, Faker, Sequence, fuzzy


class DataFactory(Factory):
    """Factory creating test datasets"""

    class Meta:
        # pylint: disable=too-few-public-methods
        """Working meta module"""
        model = Data

    num = Sequence(lambda n: n)
    name = Faker("first_name")
    price = fuzzy.FuzzyInteger(1, 5000)
