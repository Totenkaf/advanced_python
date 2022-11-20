"""
Matrix chain miltiplication.
Calculations on C++ via linking dll
Copyright 2022 by Artem Ustsov
"""

import ctypes
from typing import List

lib1 = ctypes.CDLL("./matrix_chain_multiplication.so")
lib1.multiply_matrix_chain_command.argtypes = (
    ctypes.POINTER(ctypes.c_int),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
)


def multiply_matrix_chain_command(
    arr: List[int],
    edge: int,
    verbose: int,
) -> int:
    """Realize dll linkage and work in python code

        :param arr: matrix chain pattern
        :param edge: seed for random generator
        :param verbose: If true print result matrix into stdout
        :return: Result matrix size
    )
    """

    arr_len = len(arr)
    arr_type = ctypes.c_int * arr_len
    result = lib1.multiply_matrix_chain_command(
        arr_type(*arr),
        ctypes.c_int(arr_len),
        ctypes.c_int(edge),
        ctypes.c_int(verbose),
    )
    return result
