"""
Matrix chain miltiplication.
Executing programs time comparison test
Copyright 2022 by Artem Ustsov
"""

import random
import time

import click

from matrixes import matrixes_ctypes
from matrixes import matrixes_python


# pylint: disable=no-value-for-parameter
@click.command("perf_test.py")
@click.option("-r", "--random_num", type=int, default=10)
@click.option("-s", "--chain_size", type=int, default=1000)
def run_performance_tests(random_num, chain_size):
    """Run the performance test. Compare execution type
    of different ways of calculation matrix chain mul

    :param random_num: maximum value of a number in matrix
    :param chain_size: number of matrixes in chain
    :return: None
    """

    #  Python naive realisation
    start = time.time()
    matrix_chain = [random.randint(0, random_num) for _ in range(chain_size)]

    matrixes_python.multiply_matrix_chain_command(
        chain=",".join(list(map(str, matrix_chain))),
        is_random="True",
    )
    end = time.time()
    py_time = end - start
    print(f"Python time = {py_time}")

    #  C++ dll realisation
    start = time.time()
    matrixes_ctypes.multiply_matrix_chain_command(matrix_chain, edge=5)
    end = time.time()
    cy_time = end - start
    print(f"Ctypes time = {cy_time}")

    print(f"Speedup = {py_time / cy_time}")
