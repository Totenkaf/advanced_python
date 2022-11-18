"""
CustomClass with Meta package unit testing
Copyright 2022 by Artem Ustsov
"""

import unittest

from metaclass.my_metaclass import CustomClass


# pylint: disable=no-member
# pylint: disable=unnecessary-lambda
# pylint: disable=attribute-defined-outside-init
class TestCustomClass(unittest.TestCase):
    """
    Main test class for CustomList
    """

    def setUp(self) -> None:
        """
        Setting up the test environment
        """
        self.inst = CustomClass()
        self.inst_1 = CustomClass(-100)

    def test_custom_valid_class_attributes(self):
        """
        Check right custom_ methods and attributes
        """
        self.custom_class_attributes = [
            key
            for key in self.inst.__class__.__dict__
            if not key.startswith("__")
        ]
        self.magic_class_methods = [
            key
            for key in self.inst.__class__.__dict__
            if key.startswith("__")
        ]
        self.assertEqual(
            self.custom_class_attributes,
            ["custom_my_variable", "custom_line"],
        )
        self.assertEqual(
            self.magic_class_methods,
            [
                "__module__",
                "__doc__",
                "__init__",
                "__setattr__",
                "__str__",
                "__dict__",
                "__weakref__",
            ],
        )

    def test_custom_valid_object_attributes(self):
        """
        Check valid object custom_ attributes
        """
        self.test_custom_object_attributes = list(self.inst.__dict__)
        self.assertEqual(self.test_custom_object_attributes, ["custom_value"])

    def test_custom_invalid_attributes(self):
        """
        Check invalid object and class custom_ attributes and methods
        """
        self.assertRaises(AttributeError, lambda: CustomClass.my_variable)
        self.assertRaises(AttributeError, lambda: CustomClass.new_attribute)
        self.assertRaises(AttributeError, lambda: self.inst.new_attribute)
        self.assertRaises(AttributeError, lambda: self.inst.my_variable)
        self.assertRaises(AttributeError, lambda: self.inst.line())
        self.assertRaises(AttributeError, lambda: self.inst.value)

    def test_custom_attributes_value(self):
        """
        Check value of class custom_ attributes and methods
        """
        self.assertEqual(CustomClass.custom_my_variable, 50)
        self.assertEqual(CustomClass.custom_line(), 100)

        self.assertEqual(self.inst.custom_my_variable, 50)
        self.assertEqual(self.inst.custom_value, 99)
        self.assertEqual(self.inst_1.custom_value, -100)
        self.assertEqual(self.inst.custom_line(), 100)
        self.assertEqual(str(self.inst_1), "Custom_by_metaclass")

    def test_new_valid_custom_attributes(self):
        """
        Check the creation of new class and object attributes
        """
        CustomClass.static = "class_attribute"
        self.assertRaises(AttributeError, lambda: CustomClass.static)
        self.assertEqual(CustomClass.custom_static, "class_attribute")

        self.inst.dynamic = "object_attribute"
        self.assertRaises(AttributeError, lambda: self.inst.dynamic)
        self.assertEqual(self.inst.custom_dynamic, "object_attribute")
