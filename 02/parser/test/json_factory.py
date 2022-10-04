"""
Json_factory.
Copyright 2022 by Artem Ustsov
"""
import json
import random

import factory
from factory import Factory, Faker


class JsonStr:
    """Initialize class of json_string"""
    # pylint: disable=too-few-public-methods
    def __init__(self, name, colors):
        self.name = name
        self.colors = colors

    def make_str(self):
        """Concatenate class attributes and make the string"""
        return json.dumps(({self.name: ' '.join(self.colors)}))


class JsonStrFactory(Factory):
    """Factory creating test datasets"""

    class Meta:
        # pylint: disable=too-few-public-methods
        """Working meta module"""
        model = JsonStr

    name = Faker("first_name")
    colors = factory.List([Faker("color_name")
                           for i in range(random.randint(1, 5))])
