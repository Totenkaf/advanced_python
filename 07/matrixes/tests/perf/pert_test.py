"""
Matrix chain miltiplication.
Executing programs time comparison test
Copyright 2022 by Artem Ustsov
"""

import random
import time

from matrixes import matrixes_python
from matrixes import matrixes_ctypes



if __name__ == "__main__":
    start = time.time()
    matrix_chain = ','.join([str(random.randint(0, 10)) for item in range(1000)])


    matrixes_python.multiply_matrix_chain_command(
        chain=matrix_chain, is_random="True",
    )
    end = time.time()

    py_time = end - start
    print(f"Python time = {py_time}")

    EDGE = 5
    start = time.time()
    matrixes_ctypes.multiply_matrix_chain_command(matrix_chain, EDGE)
    end = time.time()

    cy_time = end - start
    print(f"Ctypes time = {cy_time}")

    print(f"Speedup = {py_time / cy_time}")
