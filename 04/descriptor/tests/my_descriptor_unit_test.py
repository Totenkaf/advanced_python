"""
Data-descriptor package unit testing
Copyright 2022 by Artem Ustsov
"""

import unittest

from descriptor.my_descriptor import Data, Integer, String, PositiveInteger


class TestCustomDataDescriptors(unittest.TestCase):
    """
    Main test class for Data with data-descriptors
    """

    def setUp(self) -> None:
        """
        Setting up the work env
        """
        pass


if __name__ == "__main__":
    unittest.main()
