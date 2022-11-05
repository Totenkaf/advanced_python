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
)


def multiply_matrix_chain_command(arr: List[int], edge: int):
    """Call C++ dll lib and run the multiplying command

    :param arr: matrix_chain_pattern
    :param edge: seed for random generator inside dll
    :return: the shape of result array
    """

    arr_len = len(arr)
    arr_type = ctypes.c_int * arr_len
    result = lib1.multiply_matrix_chain_command(
        arr_type(*arr),
        ctypes.c_int(arr_len),
        ctypes.c_int(edge),
    )
    return result
