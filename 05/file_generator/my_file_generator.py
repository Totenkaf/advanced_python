"""
File generator package main file
Copyright 2022 by Artem Ustsov
"""

import argparse
import sys
import os
from typing import List, NoReturn, Tuple


class Chunker:
    """Chunker object for parsing"""

    def __init__(self, filename: str, output_fd, buffer_size: int = 1024*1024):
        self.filename = filename
        self.output_fd = output_fd
        self.buffer_size = buffer_size

    def chunkify(self) -> Tuple[int, int]:
        """Make chunks.
        Return tuple of chunk_start position and chunk_size in file to parse
        """

        if self.buffer_size < 1:
            raise ValueError("Buffer size must be strong positive")

        with open(self.filename, 'rb') as file:
            file_end = os.path.getsize(self.filename)
            chunk_end = file.tell()
            while True:
                chunk_start = chunk_end
                file.seek(self.buffer_size, 1)

                self.find_end_of_chunk(file)

                chunk_end = file.tell()
                chunk_offset = chunk_end - chunk_start

                yield chunk_start, chunk_offset
                if chunk_end >= file_end:
                    break

    @staticmethod
    def find_end_of_chunk(file) -> NoReturn:
        """Check the end of chunk with skipping incomplete line
        Incomplete means that line doesn't end with \n"""

        #  skip incomplete line
        file.readline()
        p = file.tell()
        line = file.readline()

        while line:
            p = file.tell()
            line = file.readline()

        #  revert one line
        file.seek(p)

    def process_wrapper(self, chunk_start: int, size: int, search_values: List[str]) -> NoReturn:
        """Takes the chunk_start position and size of the chunk (in bytes) and parse the line"""
        with open(self.filename, 'r', encoding='utf-8') as input_file:
            with open(self.output_fd, 'w', encoding='utf-8') \
                    if self.output_fd != 'stdout' \
                    else sys.stdout as output_file:

                input_file.seek(chunk_start)
                sentences = input_file.read(size).splitlines()
                for sentence in sentences:
                    sentence_with_occurrence = self.find_occurrence(sentence, search_values)
                    print(*sentence_with_occurrence, file=output_file)

    @staticmethod
    def find_occurrence(sentence: str, search_values: List[str]) -> str:
        """Tries to find exactly occurrence of the search value in sentence"""
        for search_value in search_values:
            #  set() for avoiding duplicate words in sentences
            for word in set(sentence.split()):
                if word == search_value:
                    yield sentence


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default="input.txt")
    parser.add_argument("-o", "--output", default="stdout")
    args = parser.parse_args()

    occurrences_list = ["роза", "всегда"]

    chunker = Chunker(args.input, args.output, buffer_size=32)

    for chunk_start_pos, chunk_size in chunker.chunkify():
        chunker.process_wrapper(chunk_start=chunk_start_pos,
                                size=chunk_size,
                                search_values=occurrences_list,
                                )
