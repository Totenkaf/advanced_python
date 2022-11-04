"""
Matrix chain miltiplication.
Calculations on Python
Copyright 2022 by Artem Ustsov
"""

import time

from matrixes import matrixes_cpython
from matrixes import matrixes_python


NUMBER = 10
start = time.time()
matrixes_python.multiply_matrix_chain_command(
    chain="100,200,1000,1,5,10,11", is_random="True",
)
end = time.time()

py_time = end - start
print(f"Python time = {py_time}")

start = time.time()
matrixes_cpython.test(NUMBER)
end = time.time()

cy_time = end - start
print(f"Cython time = {cy_time}")

print(f"Speedup = {py_time / cy_time}")
