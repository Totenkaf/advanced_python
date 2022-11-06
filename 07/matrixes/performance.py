"""
Matrix chain miltiplication.
Executing programs time comparison test
Copyright 2022 by Artem Ustsov
"""

import random
import time

import click

import matrixes_ctypes
import matrixes_python

import numpy as np


# pylint: disable=no-value-for-parameter
@click.command("perf_test.py")
@click.option("-r", "--random_num", type=int, default=10)
@click.option("-s", "--chain_size", type=int, default=10)
def run_performance_tests(random_num, chain_size):
    """Run the performance test. Compare execution type
    of different ways of calculation matrix chain mul

    :param random_num: maximum value of a number in matrix
    :param chain_size: number of matrixes in chain
    :return: None
    """

    #  Python naive realisation
    matrix_chain = [random.randint(1, random_num) for _ in range(chain_size)]
    chain_python = ",".join(list(map(str, matrix_chain)))

    num_of_iteration = 100
    py_time = []
    result_py = []
    for _ in range(num_of_iteration):
        start = time.time()
        result_py = matrixes_python.multiply_matrix_chain_command(
            chain=chain_python,
            is_random="True",
        )
        end = time.time()
        py_time.append(end - start)

    print(f"Python av_time = {np.mean(py_time):0.3f}")
    print(f"Python matrix size {len(result_py)*len(result_py[0])}\n")

    #  C++ dll realisation
    cpp_time = []
    result_cpp = 0
    for _ in range(num_of_iteration):
        start = time.time()
        result_cpp = matrixes_ctypes.multiply_matrix_chain_command(
            matrix_chain,
            edge=5,
            verbose=False,
        )
        end = time.time()
        cpp_time.append(end - start)
    print(f"Ctypes av_time = {np.mean(cpp_time):0.3f}")
    print(f"Ctypes matrix size {result_cpp}\n")
    print(f"Speedup average = {(np.mean(py_time) / np.mean(cpp_time)):0.3f}")


if __name__ == "__main__":
    run_performance_tests()
