"""
File generator package main file
Copyright 2022 by Artem Ustsov
"""

import os
from typing import Callable, List, NoReturn, Tuple


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

    chunk_size = PositiveInteger()

    def __init__(
        self,
        input_fd,
        output_fd,
        chunk_size: int = 1024 * 1024,
    ) -> None:
        self.input_fd = input_fd
        self.output_fd = output_fd
        self.chunk_size = chunk_size

    def chunkify(self) -> Tuple[int, int]:
        """Make chunks.
        Return tuple of chunk_start position and chunk_size in file to parse
        """

        with open(self.input_fd, "r", encoding="utf-8") as file:
            file_end = os.path.getsize(self.input_fd)
            while True:
                chunk_end = file.tell()
                chunk_start = chunk_end
                chunk = file.read(self.chunk_size)
                if not chunk:
                    break
                if chunk[-1] != "\n":
                    file.readline()

                chunk_end = file.tell()
                yield chunk_start, chunk_end - chunk_start
                if chunk_end > file_end:
                    break

    def parse_wrapper(
        self,
        chunk_start: int,
        chunk_offset: int,
        search_values: List[str],
        parser_func: Callable,
    ) -> NoReturn:
        """Takes the chunk_start position and size of the chunk (in bytes)
        and parse the line"""

        with open(self.input_fd, "rb") as input_file:
            #  set the file pointer into position according to chunk of data
            input_file.seek(chunk_start)
            #  make decoding binary sequence into utf-8
            sentences = (
                input_file.read(chunk_offset).decode("utf-8").splitlines()
            )
            for sentence in parser_func(sentences, search_values):
                print(sentence, file=self.output_fd)


def find_occurrence(sentences: List[str], search_values: List[str]) -> str:
    """Tries to find exactly occurrence of the search value in sentence.
    Found sentences are returned in their actual order in the file"""

    for sentence in sentences:
        #  if sentence contains simultaneously several search values
        #  flag prevents re-parse
        sentence_processed = False
        for search_value in search_values:
            #  set() for avoiding duplicate words in sentences
            if (
                search_value in set(sentence.split())
                and not sentence_processed
            ):
                sentence_processed = True
                yield sentence
