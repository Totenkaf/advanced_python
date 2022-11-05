"""
Matrix chain miltiplication.
Calculations on C++ via linking dll
Copyright 2022 by Artem Ustsov
"""

import ctypes
from typing import List
lib1 = ctypes.CDLL('matrix_chain_multiplication.so')
lib1.sum.multiply_matrix_chain_command = (ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int)


def multiply_matrix_chain_command(arr: List[int], edge: int) -> int:
    arr_len = len(arr)
    arr_type = ctypes.c_int * arr_len
    result = lib1.sum(arr_type(*arr), ctypes.c_int(arr_len), ctypes.c_int(edge))
    return result
