"""
Matrix chain miltiplication.
Calculations on Python
Copyright 2022 by Artem Ustsov
"""

# import argparse
import logging
import os
import random
import sys
from typing import List, Optional


# pylint: disable=redefined-outer-name
# pylint: disable=try-except-raise
def fill_matrix(
    num_rows: int,
    num_cols: int,
    randomize: bool,
    input_fd: Optional = sys.stdin,
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
        for rows in range(num_rows):
            for cols in range(num_cols):
                if randomize:
                    matrix[rows][cols] = random.randint(0, 5)
                else:
                    str_value = input_fd.readline()
                    matrix[rows][cols] = int(str_value)

    except ValueError:
        raise
    logging.getLogger().debug("Filled matrix %s", matrix)
    return matrix


def fill_matrix_chain(
    matrix_chain_pattern: List[int],
    filler: Optional,
    input_fd: Optional = sys.stdin,
    randomize: bool = False,
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
    try:
        filled_matrix_chain = []
        for num_rows, num_cols in zip(
            matrix_chain_pattern,
            matrix_chain_pattern[1:],
        ):
            if num_cols < 1 or num_rows < 1:
                raise IndexError("Matrix dims must be strong positive")
            filled_matrix_chain.append(
                filler(
                    num_rows=num_rows,
                    num_cols=num_cols,
                    randomize=randomize,
                    input_fd=input_fd,
                ),
            )
            logging.getLogger().debug(
                "Filled matrix chain %s",
                filled_matrix_chain,
            )
    except ValueError:
        raise
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
            "to second matrix col length",
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

    for rows in range(matrix_first_rows):
        for cols in range(matrix_second_cols):
            for _cols in range(matrix_first_cols):
                result_matrix[rows][cols] += (
                    matrix_first[rows][_cols] * matrix_second[_cols][cols]
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
        for index in range(1, len(matrix_chain_list)):
            result = multiply_two_matrixes(
                matrix_result_stack.pop(),
                matrix_chain_list[index],
            )
            matrix_result_stack.append(result)
    except ValueError:
        raise
    else:
        return matrix_result_stack.pop()


def multiply_matrix_chain_command(
    chain, is_random, input_fd=sys.stdin
) -> None or List[int]:
    """Fill matrix chain command

    :param chain: chain pattern
    :param is_random: True or False
    :param input_fd: file descriptor
    :return: None or result matrix
    """

    try:
        matrix_chain_pattern = list(map(int, chain.split(",")))
    except ValueError:
        logging.getLogger().info(
            "Matrix chain pattern should be a integer number"
        )
        return None
    else:
        try:
            if is_random == "False":
                matrix_chain_list = fill_matrix_chain(
                    matrix_chain_pattern,
                    fill_matrix,
                    randomize=False,
                    input_fd=input_fd,
                )
            else:
                matrix_chain_list = fill_matrix_chain(
                    matrix_chain_pattern,
                    fill_matrix,
                    randomize=True,
                    input_fd=input_fd,
                )
            result_matrix = multiply_matrix_chain(matrix_chain_list)
        except ValueError as error:
            logging.getLogger().info(error)
            return None
        except IndexError as error:
            logging.getLogger().info(error)
            return None
        else:
            logging.getLogger().info(
                "Result matrix shape: %ix%i",
                len(result_matrix),
                len(result_matrix[0]),
            )
            logging.getLogger().info("Result matrix")
            logging.getLogger().info(result_matrix)
            return result_matrix


# if __name__ == "__main__":
#     if not os.path.isdir("logs"):
#         os.mkdir("logs")
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
#
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-c", "--chain", default="2,3,2")
#     parser.add_argument("-r", "--is_random", default="True")
#     parser.add_argument("-i", "--input_fd", default="stdin")
#
#     args = parser.parse_args()
#
#     logging.getLogger().info("=====PROGRAM START=====")
#     with open(
#         args.input_fd, "r", encoding="utf-8"
#     ) if args.input_fd != "stdin" else sys.stdin as input_fd:
#         multiply_matrix_chain_command(args.chain, args.is_random, input_fd)
#     logging.getLogger().info("=====PROGRAM STOP=====")
