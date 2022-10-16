"""
File generator package main file
Copyright 2022 by Artem Ustsov
"""

from typing import Any, NoReturn
import os


# def chunkify(filename, size=1024*1024):
#     file_end = os.path.getsize(filename)
#     with open(filename, mode='r') as file:
#         chunk_end = file.tell()
#
#         while True:
#             chunk_start = chunk_end
#
#             #  set the shift from the current pointer position
#             # file.seek(size, 1)
#             file.read(size)
#             chunk_end = file.tell()
#             chunk_size = chunk_end - chunk_start
#
#             yield chunk_start, chunk_size
#
#             if chunk_end > file_end:
#                 break
#
#
def find_occurrences(line: list, occurrences_list: list):
    for occurrences in occurrences_list:
        if occurrences in line:
            print(''.join(line))
#
#
# def process_wrapper(chunk_start, chunk_size, filename, process_job, occurrences_list):
#     with open(filename, 'r') as file:
#         file.seek(chunk_start)
#         # lines = file.read(chunk_size).splitlines()
#         lines = file.read(chunk_size)
#         for line in lines:
#             process_job(line, occurrences_list)
#
#

class Chunker:
    """

    """
    @classmethod
    def chunkify(cls, fname, size=1024*1024):
        """

        """
        file_end = os.path.getsize(fname)
        with open(fname, 'r') as f:
            chunk_end = f.tell()
            while True:
                chunk_start = chunk_end
                f.read(size)
                cls._EOC(f)
                chunk_end = f.tell()

                yield chunk_start, chunk_end - chunk_start
                if chunk_end >= file_end:
                    break

    @staticmethod
    def _EOC(f):
        """

        """
        l = f.readline()  # incomplete line
        p = f.tell()
        l = f.readline()
        while l and l[0] != '\n':
            p = f.tell()
            l = f.readline()
        f.seek(p)  # revert one line

    @staticmethod
    def read(fname, chunk):
        """

        """
        with open(fname,'r') as f:
            f.seek(chunk[0])
            return f.read(chunk[1])

    @staticmethod
    def parse(chunk):
        """

        """
        for line in chunk.splitlines():
            yield line


if __name__ == '__main__':
    filename_ = 'input.txt'
    search_values = ["роза"]
    chunker = Chunker()
    for ch_st, ch_size in chunker.chunkify(filename_):
        pass
    # for chunk_start_, chunk_size_ in chunkify(filename_, size=48):
    #     process_wrapper(chunk_start_, chunk_size_, filename_, find_occurrences, search_values)
