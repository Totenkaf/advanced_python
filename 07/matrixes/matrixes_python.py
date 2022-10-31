"""
Matrix chain miltiplication.
Calculations on python
Copyright 2022 by Artem Ustsov
"""

# import argparse
import logging

# import os
import random
import sys
from typing import List, Optional


def fill_matrix(
    num_rows: int,
    num_cols: int,
    randomize: bool,
    input_fd,
) -> List[List[int]]:
    """

    :param num_rows: Matrix number of rows
    :param num_cols: Matrix number of columns
    :param randomize: If true allow to fill with random numbers
    :param input_fd: Input file descriptor
    :return: Matrix of numbers
    """

    if not isinstance(num_rows, int) or not isinstance(num_cols, int):
        raise ValueError

    logging.getLogger().info("Fill matrix %i x %i:", num_rows, num_cols)
    matrix = [[0 for _ in range(num_cols)] for _ in range(num_rows)]
    try:
        for i in range(num_rows):
            for j in range(num_cols):
                if randomize:
                    matrix[i][j] = random.randint(0, 5)
                else:
                    str_value = input_fd.readline()
                    if not str_value:
                        break
                    matrix[i][j] = int(str_value)

    except ValueError:
        logging.getLogger().debug("Value in matrix must be a number")
    logging.getLogger().debug("Filled matrix %s", matrix)
    return matrix


def fill_matrix_chain(
    matrix_chain_pattern: List[int],
    filler: Optional,
    randomize: bool = False,
    input_fd=sys.stdin,
) -> List[List[List[int]]]:
    """Fill the matrix with specific values

    :param matrix_chain_pattern: list with matrix dimensions like:
    [2, 5, 4, 3] means 2x5 5x4 4x3
    :param filler: function to fill matrix
    :param randomize: allow to produce random numbers
    to fill the matrix
    :param input_fd: input file descriptor
    :return: filled matrix with number
    """

    filled_matrix_chain = []
    for num_rows, num_cols in zip(
        matrix_chain_pattern, matrix_chain_pattern[1:]
    ):
        if num_cols < 1 or num_rows < 1:
            raise IndexError("Must be a strong positive")
        filled_matrix_chain.append(
            filler(
                num_rows=num_rows,
                num_cols=num_cols,
                randomize=randomize,
                input_fd=input_fd,
            )
        )
        logging.getLogger().debug(
            "Filled matrix chain %s", filled_matrix_chain
        )
    return filled_matrix_chain


def multiply_two_matrixes(matrix_first, matrix_second):
    """Check matrix dimensions and multiply on by another

    :param matrix_first: matrix with integers
    :param matrix_second: matrix with integers
    :return: result of two matrix multiplication
    """
    matrix_first_rows = len(matrix_first)
    matrix_first_cols = len(matrix_first[0])
    matrix_second_rows = len(matrix_second)
    matrix_second_cols = len(matrix_second[0])

    if matrix_first_cols != matrix_second_rows:
        raise ValueError(
            "First matrix row length should be equal "
            "to second matrix col length"
        )

    result_matrix = [
        [0 for _ in range(matrix_second_cols)]
        for _ in range(matrix_first_rows)
    ]
    logging.getLogger().debug(
        "Result matrix dimensions: %ix%i",
        len(result_matrix),
        len(result_matrix[0]),
    )

    for i in range(matrix_first_rows):
        for j in range(matrix_second_cols):
            for k in range(matrix_first_cols):
                result_matrix[i][j] += (
                    matrix_first[i][k] * matrix_second[k][j]
                )

    return result_matrix


def multiply_matrix_chain(
    matrix_chain_list: List[List[List[int]]],
) -> List[List[int]]:
    """Store result in stack and pop it for multiplication with another matrix

    :param matrix_chain_list: list of matrix dimensions like [2, 3, 3]
    :return: result of chain of matrix multiplication
    """

    try:
        matrix_result_stack = [matrix_chain_list[0]]
        for i in range(1, len(matrix_chain_list)):
            result = multiply_two_matrixes(
                matrix_result_stack.pop(), matrix_chain_list[i]
            )
            matrix_result_stack.append(result)
    except ValueError as error:
        raise error
    else:
        return matrix_result_stack.pop()


# if __name__ == "__main__":
#     if not os.path.isdir("../logs"):
#         os.mkdir("../logs")
#
#     FORMAT_LOG = "%(asctime)s: %(message)s"
#     file_log = logging.FileHandler("logs/matrix.log")
#     console_out = logging.StreamHandler()
#
#     logging.basicConfig(
#         handlers=(file_log, console_out),
#         format=FORMAT_LOG,
#         level=logging.INFO,
#         datefmt="%H:%M:%S",
#     )
#     logging.getLogger().info("=====PROGRAM START=====")
#
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-c", "--chain", default="2,4,3,1")
#     parser.add_argument("-r", "--random", default="True")
#
#     args = parser.parse_args()
#
#     try:
#         matrix_chain_pattern = list(map(int, args.chain.split(",")))
#     except ValueError(
#         "Matrix chain pattern should be a integer number"
#     ) as error:
#         logging.getLogger().info(error)
#     else:
#         try:
#             if args.random == "False":
#                 matrix_chain_list = fill_matrix_chain(
#                     matrix_chain_pattern, fill_matrix
#                 )
#             else:
#                 matrix_chain_list = fill_matrix_chain(
#                     matrix_chain_pattern, fill_matrix, randomize=True
#                 )
#             result_matrix = multiply_matrix_chain(matrix_chain_list)
#         except ValueError as error:
#             logging.getLogger().info(error)
#         except IndexError as error:
#             logging.getLogger().info(error)
#         else:
#             logging.getLogger().info(
#                 "Result matrix shape: %ix%i",
#                 len(result_matrix),
#                 len(result_matrix[0]),
#             )
#             logging.getLogger().info("Result matrix")
#             logging.getLogger().info(result_matrix)
#     logging.getLogger().info("=====PROGRAM STOP=====")
