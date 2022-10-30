"""
Data-descriptor package factory
Copyright 2022 by Artem Ustsov
"""

# pylint: disable=wrong-import-order
from descriptor.my_descriptor import Data
from factory import Factory, Faker, Sequence, fuzzy


# pylint: disable=too-few-public-methods
class DataFactory(Factory):
    """Factory creating test datasets"""

    class Meta:
        """Working meta module"""

        model = Data

    num = Sequence(lambda n: n)
    name = Faker("first_name")
    price = fuzzy.FuzzyInteger(1, 5000)
