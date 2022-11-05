"""
Matrix chain miltiplication.
Executing programs time comparison test
Copyright 2022 by Artem Ustsov
"""

import random
import time

import click

from matrixes import matrixes_python
from matrixes import matrixes_ctypes


@click.command("perf_test.py")
@click.option("-r", "--random_num", type=int, default=10)
@click.option("-s", "--chain_size", type=int, default=1000)
def run_performance_tests(random_num, chain_size):
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


if __name__ == "__main__":
    run_performance_tests()
