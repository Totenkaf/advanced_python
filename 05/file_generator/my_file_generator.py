"""
File generator package main file
Copyright 2022 by Artem Ustsov
"""

# import argparse
import os
import sys
from typing import Any, List, NoReturn, Tuple


# pylint: disable=attribute-defined-outside-init
class PositiveInteger:
    """
    Integer data-descriptor
    """

    @classmethod
    def is_integer(cls, value: int) -> None:
        """
        Checks if an incoming value is an int
        """
        if not isinstance(value, int):
            raise TypeError(f"Value must be a int-like not {type(value)}")

    @classmethod
    def is_positive(cls, value: int):
        """
        Checks if an incoming value is strong positive
        """
        if not value > 0:
            raise ValueError(
                f"Value must be a strong positive. You gave {value}",
            )

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        self.is_integer(value)
        self.is_positive(value)
        instance.__dict__[self.name] = value


class Chunker:
    """Chunker object for parsing"""

    buffer_size = PositiveInteger()

    def __init__(
        self, input_fd: str, output_fd, buffer_size: int = 1024 * 1024,
    ) -> None:
        self.input_fd = input_fd
        self.output_fd = output_fd
        self.buffer_size = buffer_size

    def chunkify(self) -> Tuple[int, int]:
        """Make chunks.
        Return tuple of chunk_start position and chunk_size in file to parse
        """

        with open(self.input_fd, "rb") as file:
            file_end = os.path.getsize(self.input_fd)
            chunk_end = file.tell()
            while True:
                chunk_start = chunk_end
                file.seek(self.buffer_size, 1)

                self.__class__.find_end_of_chunk(file)

                chunk_end = file.tell()
                chunk_offset = chunk_end - chunk_start

                yield chunk_start, chunk_offset
                if chunk_end >= file_end:
                    break

    @staticmethod
    def find_end_of_chunk(file_fd: Any) -> NoReturn:
        """Check the end of chunk with skipping incomplete line
        Incomplete means that line doesn't end with \n"""

        #  skip incomplete line
        file_fd.readline()
        file_pointer = file_fd.tell()
        file_fd.readline()

        # while line == '\n':
        #     file_pointer = file.tell()
        #     line = file.readline()

        #  revert one line
        file_fd.seek(file_pointer)

    def parse_wrapper(
        self,
        chunk_start: int,
        size: int,
        search_values: List[str],
        parser_func,
    ) -> NoReturn:
        """Takes the chunk_start position and size of the chunk (in bytes)
        and parse the line"""

        with open(self.input_fd, "r", encoding="utf-8") as input_file:
            with open(
                self.output_fd,
                "w",
                encoding="utf-8",
            ) if self.output_fd != "stdout" else sys.stdout as output_file:

                input_file.seek(chunk_start)
                for sentence in parser_func(
                    input_file.read(size).splitlines(), search_values,
                ):
                    print(sentence, file=output_file)


def find_occurrence(sentences: List[str], search_values: List[str]) -> str:
    """Tries to find exactly occurrence of the search value in sentence.
    Found sentences are returned in their actual order in the file"""

    for sentence in sentences:
        #  if sentence contains simultaneously several search values
        #  flag prevents re-parse
        sentence_processed = False
        for search_value in search_values:
            #  set() for avoiding duplicate words in sentences
            for word in set(sentence.split()):
                if word == search_value and not sentence_processed:
                    sentence_processed = True
                    yield sentence
