"""
CustomClass with Meta package main file
Copyright 2022 by Artem Ustsov
"""


class CustomMeta(type):
    """
    MetaClass adds the "custom_"
    to the CustomClass methods (not magic) and attributes
    """

    def __new__(cls, name, bases, attrs):
        customized_attrs = {
            attr if attr.startswith("__") else "_".join(["custom", attr]): v
            for attr, v in attrs.items()
        }
        return super().__new__(cls, name, bases, customized_attrs)

    def __setattr__(cls, key, value):
        type.__setattr__(cls, "_".join(["custom", key]), value)


class CustomClass(metaclass=CustomMeta):
    """Class adds the "custom_" to the CustomClass object attributes"""

    my_variable = 50

    def __init__(self, value=99):
        self.value = value

    def __setattr__(self, key, value):
        object.__setattr__(self, "_".join(["custom", key]), value)

    @staticmethod
    def line():
        """
        Just return the fixed value
        """
        return 100

    def __str__(self):
        return "Custom_by_metaclass"


if __name__ == "__main__":
    my_class = CustomClass()
    print(my_class.__class__.__dict__)
