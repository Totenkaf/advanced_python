"""
Data-descriptor package unit testing
Copyright 2022 by Artem Ustsov
"""

import unittest
from unittest.mock import patch

from descriptor.my_descriptor import Data, Integer, PositiveInteger, String

from .my_descriptor_factory import DataFactory


class TestCustomDataDescriptors(unittest.TestCase):
    """Main test class for Data with data-descriptors"""

    @patch.object(Integer, "__set__")
    def test_integer_on_random_dataset(self, __set__mock):
        """Check the call of __set__ method in Integer-descr
        on random data"""

        data = []
        data.extend(DataFactory.create_batch(size=100))
        self.assertEqual(__set__mock.call_count, 100)

    @patch.object(String, "__set__")
    def test_string_on_random_dataset(self, __set__mock):
        """Check the call of __set__ method in String-descr
        on random data"""

        data = []
        data.extend(DataFactory.create_batch(size=100))
        self.assertEqual(__set__mock.call_count, 100)

    @patch.object(PositiveInteger, "__set__")
    def test_on_random_dataset(self, __set__mock):
        """Check the call of __set__ method in PositiveInteger-descr
        on random data"""

        data = []
        data.extend(DataFactory.create_batch(size=100))
        self.assertEqual(__set__mock.call_count, 100)

    def test_set_valid_data_fields(self):
        """Check the dataclass initialisations via descriptors
        with valid data
        """

        self.data = Data(0, "apple", 100)
        self.assertEqual(self.data.num, 0)
        self.assertEqual(self.data.name, "apple")
        self.assertEqual(self.data.price, 100)

    def test_set_invalid_data_fields(self):
        """Check the dataclass initialisations via descriptors
        with invalid data
        """

        # num-suite
        self.assertRaises(TypeError, Data, "abc", "orange", 100)
        self.assertRaises(TypeError, Data, "1", "orange", 100)
        self.assertRaises(TypeError, Data, [], "orange", 100)
        # name-suite
        self.assertRaises(TypeError, Data, 1, 50, 100)
        self.assertRaises(TypeError, Data, 1, {"key": 100}, 100)
        self.assertRaises(ValueError, Data, 1, "mag**ma", 100)
        self.assertRaises(ValueError, Data, 1, "*/-*/-+-*adsf", 100)
        self.assertRaises(ValueError, Data, 1, "123456", 100)
        # price-suite
        self.assertRaises(TypeError, Data, 1, "orange", "100")
        self.assertRaises(TypeError, Data, 1, "orange", "abc")
        self.assertRaises(ValueError, Data, 1, "orange", -100)
        self.assertRaises(ValueError, Data, 1, "orange", -50)
        self.assertRaises(ValueError, Data, 1, "orange", 0)
        self.assertRaises(TypeError, Data, 1, "orange", set())

    def test_reset_valid_data_fields(self):
        """Check the dataclass initialisations via descriptors
        with valid data
        """

        self.data = Data(0, "apple", 100)
        self.data.price = 10
        self.assertEqual(self.data.price, 10)

        self.data.num = 2
        self.assertEqual(self.data.num, 2)

        self.data.num = -10
        self.assertEqual(self.data.num, -10)

        self.data.name = "orange"
        self.assertEqual(self.data.name, "orange")

    def test_reset_invalid_data_fields(self):
        """Check the dataclass initialisations via descriptors
        with valid data
        """

        self.data = Data(0, "apple", 100)
        with self.assertRaises(TypeError):
            self.data.num = "apple"

        with self.assertRaises(TypeError):
            self.data.num = 10.87

        with self.assertRaises(ValueError):
            self.data.price = -10

        with self.assertRaises(ValueError):
            self.data.price = 0

        with self.assertRaises(TypeError):
            self.data.price = 10.87

        with self.assertRaises(TypeError):
            self.data.price = "apple"

        with self.assertRaises(TypeError):
            self.data.name = 10
