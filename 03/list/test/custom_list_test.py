"""
CustomList project. Unit testing
Copyright 2022 by Artem Ustsov
"""

import unittest

from list.custom_list import CustomList


class TestCustomList(unittest.TestCase):
    """
    Main test class for CustomList
    """

    def setUp(self) -> None:
        """
        Setting up the work env
        """
        self.empty_cust_list = CustomList()
        self.empty_list_cust_list = CustomList([])
        self.full_cust_list_1 = CustomList([1, 2, 3, 4, 5])
        self.full_cust_list_2 = CustomList([-5, -4, -3, -2, -1])
        self.full_cust_list_3 = CustomList([6, 7, 8])

    def test_empty_custom_list_init(self) -> None:
        """
        Check the empty arg in CustomList initialisation
        """
        self.assertEqual(self.empty_cust_list, [])
        self.assertEqual(len(self.empty_cust_list), 0)
        self.assertEqual(type(self.empty_cust_list), CustomList)

    def test_empty_list_custom_list_init(self) -> None:
        """
        Check empty list arg in CustomList initialisation
        """
        self.assertEqual(self.empty_list_cust_list, [])
        self.assertEqual(len(self.empty_list_cust_list), 0)
        self.assertEqual(type(self.empty_list_cust_list), CustomList)

    def test_wrong_param_custom_list_init(self) -> None:
        """
        Check wrong input parameters in CustomList
        """
        # int_suite
        self.assertRaises(TypeError, CustomList, 2)
        # float_suite
        self.assertRaises(TypeError, CustomList, 2.0)
        # string_suite
        self.assertRaises(TypeError, CustomList, "test_str")
        # dict_suite
        self.assertRaises(TypeError, CustomList, {"key": "value"})
        # tuple_suite
        self.assertRaises(TypeError, CustomList, (1, 2, 3))
        # set_suite
        self.assertRaises(TypeError, CustomList, {1, 2, 3})

        # wrong_list_elements_suites
        self.assertRaises(ValueError, CustomList, [1, 2, "hello"])
        self.assertRaises(ValueError, CustomList, [2, 3, {"key": "value"}])
        self.assertRaises(ValueError, CustomList, [-20, {1, 2, 3}, 7])
        self.assertRaises(ValueError, CustomList, [(1, 2, 3), 2])

    def test_right_param_custom_list_init(self) -> None:
        """
        Check right input parameters in CustomList
        """
        self.assertEqual(self.full_cust_list_1, [1, 2, 3, 4, 5])
        self.assertEqual(len(self.full_cust_list_1), 5)
        self.assertEqual(type(self.full_cust_list_1), CustomList)

    def test_convert_to_list(self) -> None:
        """
        Check the converting to list
        """
        # pylint: disable=protected-access
        self.assertEqual(
            type(
                self.full_cust_list_1._CustomList__convert_to_list(
                    CustomList([1, 2, 3]),
                ),
            ),
            list,
        )
        self.assertEqual(
            type(
                self.full_cust_list_1._CustomList__convert_to_list([1, 2, 3]),
            ),
            list,
        )

    def test_custom_list_getter(self) -> None:
        """
        Check class getter
        """
        self.assertEqual(self.full_cust_list_1, [1, 2, 3, 4, 5])

    def test_custom_list_setter(self) -> None:
        """
        Check class setter
        """
        tmp_cust_list = self.full_cust_list_1
        self.assertEqual(tmp_cust_list, [1, 2, 3, 4, 5])

    def test_cust_list_add_(self) -> None:
        """
        Check all adding action in class
        """
        # custom_list self add suite compare with custom_list
        self.assertEqual(
            self.full_cust_list_1 + self.full_cust_list_1,
            CustomList([2, 4, 6, 8, 10]),
        )

        # custom_list self add suite compare with list
        self.assertEqual(
            self.full_cust_list_1 + self.full_cust_list_1,
            [2, 4, 6, 8, 10],
        )

        # different length of custom_list suite
        self.assertEqual(
            self.full_cust_list_1 + self.full_cust_list_3,
            CustomList([7, 9, 11, 4, 5]),
        )

        # custom_list and list suite
        self.assertEqual(
            self.full_cust_list_2 + [1, 2, 3], [-4, -2, 0, -2, -1],
        )

        # custom_list self add via __radd__
        self.assertEqual(
            [1, 2, 3] + self.full_cust_list_2, [-4, -2, 0, -2, -1],
        )

        # custom_list self add via __iadd__
        self.full_cust_list_2 += self.full_cust_list_2
        self.assertEqual(self.full_cust_list_2, [-10, -8, -6, -4, -2])

    def test_cust_list_sub_(self) -> None:
        """
        Check all substitution actions in class
        """
        # custom_list self add suite compare with custom_list
        self.assertEqual(
            self.full_cust_list_1 - self.full_cust_list_1,
            CustomList([0, 0, 0, 0, 0]),
        )

        # custom_list self add suite compare with list
        self.assertEqual(
            self.full_cust_list_1 - self.full_cust_list_1, [0, 0, 0, 0, 0],
        )

        # different length of custom_list suite
        self.assertEqual(
            self.full_cust_list_1 - self.full_cust_list_3,
            CustomList([-5, -5, -5, 4, 5]),
        )

        # custom_list and list suite
        self.assertEqual(
            self.full_cust_list_2 - [1, 2, 3], [-6, -6, -6, -2, -1],
        )

        # custom_list self add via __radd__
        self.assertEqual([1, 2, 3] - self.full_cust_list_2, [6, 6, 6, 2, 1])

        # custom_list self add via __iadd__
        self.full_cust_list_2 -= self.full_cust_list_2
        self.assertEqual(self.full_cust_list_2, [0, 0, 0, 0, 0])

    def test_cust_list_eq_(self) -> None:
        """
        Check the sum equality of the classes
        """
        self.assertNotEqual(self.full_cust_list_1, self.full_cust_list_2)
        self.assertEqual(self.full_cust_list_3, [6, 7, 8])

    def test_cust_list_str_(self) -> None:
        """
        Check the string format
        """
        self.assertEqual(str(self.full_cust_list_3), "[6, 7, 8], 21")

    def test_cust_list_len_(self) -> None:
        """
        Check the len of the class
        """
        self.assertEqual(len(self.full_cust_list_3), 3)


if __name__ == "__main__":
    unittest.main()
