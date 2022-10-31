"""
Matrix chain miltiplication.
Calculations on python
Copyright 2022 by Artem Ustsov
"""

import sys
from typing import List

# Функция для поиска наиболее эффективного способа умножения
# заданная последовательность матриц
# Функция для поиска наиболее эффективного способа умножения
# заданная последовательность матриц
def matrixChainMultiplication(dims, i, j, lookup):
    # Базовый случай: одна матрица
    if j <= i + 1:
        return 0

    # хранит минимальное количество скалярных умножений (т.е. стоимость)
    # требуется для вычисления матрицы `M[i+1] … M[j] = M[i…j]`
    min = sys.maxsize

    # , если подзадача видится впервые, решите ее и
    # сохраняет результат в таблице поиска
    if lookup[i][j] == 0:

        # берут минимум по каждому возможному положению, в котором
        # Последовательность матриц # может быть разделена

        '''
            (M[i+1]) × (M[i+2]………………M[j])
            (M[i+1]M[i+2]) × (M[i+3…………M[j])
            …
            …
            (M[i+1]M[i+2]…………M[j-1]) × (M[j])
        '''

        for k in range(i + 1, j):

            # повторяется для `M[i+1]…M[k]`, чтобы получить матрицу `i × k`
            cost = matrixChainMultiplication(dims, i, k, lookup)

            # повторяется для `M[k+1]…M[j]`, чтобы получить матрицу `k × j`
            cost += matrixChainMultiplication(dims, k, j, lookup)

            # стоимость умножения двух матриц `i × k` и `k × j`
            print(dims[i], dims[k], dims[j])
            cost += dims[i] * dims[k] * dims[j]

            if cost < min:
                min = cost

        lookup[i][j] = min
        print(lookup)

    # возвращает минимальную стоимость умножения `M[j+1]…M[j]`
    return lookup[i][j]


# if __name__ == '__main__':
#     # Матрица `M[i]` имеет размерность `dims[i-1] × dims[i]` для `i=1…n`
#     # Вход #: матрица 10 × 30, матрица 30 × 5, матрица 5 × 60
#     dims = [10, 30, 5, 60]
#
#     # Таблица поиска # для хранения решения уже вычисленных подзадач
#     lookup = [[0 for x in range(len(dims))] for y in range(len(dims))]
#
#     n = len(dims)
#     print('The minimum cost is', matrixChainMultiplication(dims, 0, n - 1, lookup))


def fill_matrix(rows: int, cols: int, input_fd=sys.stdin) -> List[List[int]]:
    if not isinstance(rows, int) or not isinstance(cols, int):
        raise ValueError

    print(f'Fill maxtrix {rows} x {cols}:\n')
    matrix = []

    try:
        for i in range(rows):
            array = []
            for j in range(cols):
                array.append(int(input_fd.readline()))
            matrix.append(array)

    except ValueError:
        raise ValueError("Value in matrix must be a number")

    return matrix


def fill_matrix_chain(matrix_chain_pattern: List[int]) -> List[List[List[int]]]:
    filled_matrix_chain = []
    for num_rows, num_cols in zip(matrix_chain_pattern, matrix_chain_pattern[1:]):
        filled_matrix_chain.append(fill_matrix(rows=num_rows, cols=num_cols))
    return filled_matrix_chain


# def multiply_matrix_chain(matrix_chain: List[List[int]]) -> List[List[int]]:
#     result_matrix = [[0 for i in range(length)] for i in range(length)]


if __name__ == "__main__":
    matrix_chain_pattern = [2, 2, 2]
    print(fill_matrix_chain(matrix_chain_pattern))
