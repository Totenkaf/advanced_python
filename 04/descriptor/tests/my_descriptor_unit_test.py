"""
Data-descriptor package unit testing
Copyright 2022 by Artem Ustsov
"""

import unittest
from unittest.mock import patch

from descriptor.my_descriptor import Data, Integer, PositiveInteger, String

from .my_descriptor_factory import DataFactory


class TestCustomDataDescriptors(unittest.TestCase):
    """
    Main test class for Data with data-descriptors
    """

    def setUp(self) -> None:
        """Setup the basis dataclass"""
        self.data = Data(0, "apple", 100)

    @patch.object(Integer, "__set__")
    def test_set_integer_descr(self, __set__mock):
        """Check the call of __set__ method in Integer-descr"""
        Data(0, "apple", 100)
        self.assertTrue(__set__mock.called)

    @patch.object(Integer, "__get__")
    def test_get_integer_descr(self, __get__mock):
        """Check the call of __get__ method in Integer-descr"""
        __get__mock.return_value = None
        self.assertEqual(self.data.num, None)
        self.assertTrue(__get__mock.called)

    @patch.object(String, "__set__")
    def test_set_str_descr(self, __set__mock):
        """Check the call of __set__ method in String-descr"""
        Data(0, "apple", 100)
        self.assertTrue(__set__mock.called)

    @patch.object(String, "__get__")
    def test_get_str_descr(self, __get__mock):
        """Check the call of __get__ method in Integer-descr"""
        __get__mock.return_value = None
        self.assertEqual(self.data.name, None)
        self.assertTrue(__get__mock.called)

    @patch.object(PositiveInteger, "__set__")
    def test_set_pos_integer_descr(self, __set__mock):
        """Check the call of __set__ method in PositiveInteger-descr"""
        Data(0, "apple", 100)
        self.assertTrue(__set__mock.called)

    @patch.object(PositiveInteger, "__get__")
    def test_get_pos_integer_descr(self, __get__mock):
        """Check the call of __get__ method in PositiveInteger-descr"""
        __get__mock.return_value = None
        self.assertEqual(self.data.price, None)
        self.assertTrue(__get__mock.called)

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


if __name__ == "__main__":
    unittest.main()
