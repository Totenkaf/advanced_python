"""
Matrix chain miltiplication.
Calculations on python unit test
Copyright 2022 by Artem Ustsov
"""

import os
import sys
import unittest

from matrixes.matrixes_python import (
    fill_matrix,
    fill_matrix_chain,
    multiply_matrix_chain,
    multiply_matrix_chain_command,
    multiply_two_matrixes,
)


# pylint: disable=too-many-instance-attributes
# pylint: disable=consider-using-enumerate
# pylint: disable=too-many-branches
# pylint: disable=attribute-defined-outside-init
class TestClient(unittest.TestCase):
    """Main test class for my_client module"""

    def setUp(self) -> None:
        """Prepare ENV
        :return: None
        """

        self.matrix_chain_pattern = [3, 2, 3]
        self.matrix_2x2 = [[1, 2], [3, 4]]
        self.result_matrix_2x2 = [[7, 10], [15, 22]]
        self.matrix_3x2 = [[1, 2], [3, 4], [5, 6]]
        self.matrix_2x4 = [[1, 2, 3, 4], [5, 6, 7, 8]]

        self.result_matrix_3x4 = [
            [11, 14, 17, 20],
            [23, 30, 37, 44],
            [35, 46, 57, 68],
        ]

        # 3x2 2x2 2x4
        self.result_matrix_3x2x4 = [
            [57, 74, 91, 108],
            [125, 162, 199, 236],
            [193, 250, 307, 364],
        ]

        self.input_2x2_matrix_filename = "input_2x2_matrix.txt"
        self.input_3x2_matrix_filename = "input_3x2_matrix.txt"
        self.input_2x4_matrix_filename = "input_2x4_matrix.txt"
        self.input_3x4_matrix_filename = "input_3x4_matrix.txt"

        if not os.path.isdir(self.input_2x2_matrix_filename):
            with open(
                self.input_2x2_matrix_filename,
                "w",
                encoding="utf-8",
            ) as file:
                for rows in range(len(self.matrix_2x2)):
                    for cols in range(len(self.matrix_2x2[0])):
                        file.write(str(self.matrix_2x2[rows][cols]) + "\n")

        if not os.path.isdir(self.input_3x2_matrix_filename):
            with open(
                self.input_3x2_matrix_filename,
                "w",
                encoding="utf-8",
            ) as file:
                for rows in range(len(self.matrix_3x2)):
                    for cols in range(len(self.matrix_3x2[0])):
                        file.write(str(self.matrix_3x2[rows][cols]) + "\n")

        if not os.path.isdir(self.input_2x4_matrix_filename):
            with open(
                self.input_2x4_matrix_filename,
                "w",
                encoding="utf-8",
            ) as file:
                for rows in range(len(self.matrix_2x4)):
                    for cols in range(len(self.matrix_2x4[0])):
                        file.writelines(
                            str(self.matrix_2x4[rows][cols]) + "\n",
                        )

        if not os.path.isdir(self.input_3x4_matrix_filename):
            with open(
                self.input_3x4_matrix_filename,
                "w",
                encoding="utf-8",
            ) as file:
                for rows in range(len(self.matrix_3x2)):
                    for cols in range(len(self.matrix_3x2[0])):
                        file.writelines(
                            str(self.matrix_3x2[rows][cols]) + "\n",
                        )
                for rows in range(len(self.matrix_2x4)):
                    for cols in range(len(self.matrix_2x4[0])):
                        file.writelines(
                            str(self.matrix_2x4[rows][cols]) + "\n",
                        )

    def tearDown(self) -> None:
        """Clear ENV

        :return: None
        """

        try:
            os.remove(self.input_2x2_matrix_filename)
            os.remove(self.input_3x2_matrix_filename)
            os.remove(self.input_2x4_matrix_filename)
            os.remove(self.input_3x4_matrix_filename)
        except OSError as why:
            print(why)

    def test_fill_matrix(self) -> None:
        """Test filling via file
        Test filling via random

        :return: None
        """

        with open(
            self.input_2x2_matrix_filename,
            "r",
            encoding="utf-8",
        ) as file:
            self.matrix = fill_matrix(
                num_rows=len(self.matrix_2x2),
                num_cols=len(self.matrix_2x2[0]),
                input_fd=file,
                randomize=False,
            )

            for rows in range(len(self.matrix)):
                for cols in range(len(self.matrix[0])):
                    self.assertEqual(
                        self.matrix[rows][cols],
                        self.matrix_2x2[rows][cols],
                    )

            self.random_matrix = fill_matrix(
                num_rows=len(self.matrix_2x2),
                num_cols=len(self.matrix_2x2[0]),
                input_fd=file,
                randomize=True,
            )

            self.assertEqual(len(self.random_matrix), len(self.matrix_2x2))
            self.assertEqual(
                len(self.random_matrix[0]),
                len(self.matrix_2x2[0]),
            )

            self.assertRaises(
                ValueError,
                fill_matrix,
                "1",
                1,
                sys.stdin,
                False,
            )
            self.assertRaises(
                ValueError,
                fill_matrix,
                1,
                [1],
                sys.stdin,
                False,
            )

    def test_fill_matrix_chain(self) -> None:
        """Fill matrix chain

        :return: None
        """

        with open(
            self.input_3x2_matrix_filename,
            "r",
            encoding="utf-8",
        ) as file:
            filled_matrix_chain = fill_matrix_chain(
                matrix_chain_pattern=[3, 2],
                filler=fill_matrix,
                randomize=False,
                input_fd=file,
            )

            self.assertEqual(len(filled_matrix_chain), 1)
            for rows in range(len(filled_matrix_chain[0])):
                for cols in range(len(filled_matrix_chain[0][0])):
                    self.assertEqual(
                        filled_matrix_chain[0][rows][cols],
                        self.matrix_3x2[rows][cols],
                    )

    def test_fill_matrix_chain_wrong_dim(self) -> None:
        """Test wrong matrix_hain_patter dim

        :return: None
        """

        self.assertRaises(
            IndexError,
            fill_matrix_chain,
            [2, 0, 2],
            fill_matrix,
        )
        self.assertRaises(IndexError, fill_matrix_chain, [1, -1], fill_matrix)

    def test_multiply_two_matrixes(self) -> None:
        """Test multiplying

        :return: None
        """

        result_quadratic_matrix = multiply_two_matrixes(
            self.matrix_2x2,
            self.matrix_2x2,
        )
        for rows in range(len(result_quadratic_matrix)):
            for cols in range(len(result_quadratic_matrix[0])):
                self.assertEqual(
                    result_quadratic_matrix[rows][cols],
                    self.result_matrix_2x2[rows][cols],
                )

        self.assertEqual(
            len(result_quadratic_matrix),
            len(self.result_matrix_2x2),
        )
        self.assertEqual(
            len(result_quadratic_matrix[0]),
            len(self.result_matrix_2x2[0]),
        )

        result_rectangle_matrix = multiply_two_matrixes(
            self.matrix_3x2,
            self.matrix_2x4,
        )
        for rows in range(len(result_rectangle_matrix)):
            for cols in range(len(result_rectangle_matrix[0])):
                self.assertEqual(
                    result_rectangle_matrix[rows][cols],
                    self.result_matrix_3x4[rows][cols],
                )

        self.assertEqual(
            len(result_rectangle_matrix),
            len(self.result_matrix_3x4),
        )
        self.assertEqual(
            len(result_rectangle_matrix[0]),
            len(self.result_matrix_3x4[0]),
        )

    def test_multiply_two_matrixes_wrong_dim(self) -> None:
        """Test wron multiplying

        :return: None
        """

        self.assertRaises(
            ValueError,
            multiply_two_matrixes,
            self.matrix_2x2,
            self.matrix_3x2,
        )
        self.assertRaises(
            ValueError,
            multiply_two_matrixes,
            self.matrix_3x2,
            self.matrix_3x2,
        )

    def test_multiply_matrix_chain(self) -> None:
        """Test multiplying chain of matrixes

        :return: None
        """

        matrix_chain_list = [
            self.matrix_3x2,
            self.matrix_2x2,
            self.matrix_2x4,
        ]
        result_matrix = multiply_matrix_chain(matrix_chain_list)

        self.assertEqual(len(result_matrix), len(self.result_matrix_3x2x4))
        self.assertEqual(
            len(result_matrix[0]),
            len(self.result_matrix_3x2x4[0]),
        )

        for rows in range(len(result_matrix)):
            for cols in range(len(result_matrix[0])):
                self.assertEqual(
                    result_matrix[rows][cols],
                    self.result_matrix_3x2x4[rows][cols],
                )

    def test_multiply_random_matrix_chain_command(self) -> None:
        """Test matrix chain command

        :return: None
        """

        chain, is_random, verbose = "2,3,10,7", "True", 0
        result_matrix = multiply_matrix_chain_command(chain, is_random, verbose)
        self.assertEqual(len(result_matrix), 2)
        self.assertEqual(len(result_matrix[0]), 7)

    def test_multiply_input_matrix_chain_command(self) -> None:
        """Test matrix chain command

        :return: None
        """

        chain, is_random = "3,2,4", "False"
        with open(
            self.input_3x4_matrix_filename,
            "r",
            encoding="utf-8",
        ) as file:
            result_matrix = multiply_matrix_chain_command(
                chain,
                is_random,
                file,
            )

        self.assertEqual(len(result_matrix), 3)
        self.assertEqual(len(result_matrix[0]), 4)

        for rows in range(len(result_matrix)):
            for cols in range(len(result_matrix[0])):
                self.assertEqual(
                    result_matrix[rows][cols],
                    self.result_matrix_3x4[rows][cols],
                )

    def test_multiply_wrong_matrix_chain_command(self) -> None:
        """Test matrix chain command

        :return: None
        """

        chain, is_random, verbose = "2,3,abc,7", "True", 0
        result_matrix = multiply_matrix_chain_command(chain, is_random, verbose)
        self.assertIsNone(result_matrix)

        chain, is_random = "2,3,-1,7", "True"
        result_matrix = multiply_matrix_chain_command(chain, is_random, verbose)
        self.assertIsNone(result_matrix)
