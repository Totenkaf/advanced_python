"""
File generator package main file
Copyright 2022 by Artem Ustsov
"""

import os
import sys
import unittest

from my_file_generator import (
    Chunker,
    find_occurrence,
)

#  pylint: disable=too-many-public-methods
#  pylint: disable=attribute-defined-outside-init
#  pylint: disable=too-many-instance-attributes


class TestFileGenerator(unittest.TestCase):
    """Main test class for my_file_generator module"""

    def setUp(self) -> None:
        self.input_fd = "input.txt"
        self.output_fd = "output.txt"
        self.test_sentences = [
            "а роза упала на лапу азора",
            "розовая пантера надела розовые штаны и купила розу для Розы",
            "роза купленная вчера в магазине роз начала розоветь",
        ]

    def test_chunker_init(self):
        """Chunker init"""

        self.chunker = Chunker(self.input_fd, self.output_fd, chunk_size=32)
        self.assertEqual(self.chunker.input_fd, self.input_fd)
        self.assertEqual(self.chunker.output_fd, self.output_fd)
        self.assertEqual(self.chunker.chunk_size, 32)

    def test_chunker_init_wrong_buffer_size(self):
        """Chunker init with wrong buffer size for chunkify
        Expects value or type error.
        """

        self.assertRaises(
            ValueError,
            Chunker,
            self.input_fd,
            self.output_fd,
            chunk_size=0,
        )
        self.assertRaises(
            ValueError,
            Chunker,
            self.input_fd,
            self.output_fd,
            chunk_size=-234623,
        )
        self.assertRaises(
            TypeError,
            Chunker,
            self.input_fd,
            self.output_fd,
            chunk_size="0",
        )
        self.assertRaises(
            TypeError,
            Chunker,
            self.input_fd,
            self.output_fd,
            chunk_size={0},
        )

    def test_find_occurrence_returned_sentence(self):
        """Test the return values of parsing function"""

        self.search_values = ["розовая", "роза"]
        self.returned_sentences = []
        for returned_sentence in find_occurrence(
            self.test_sentences,
            self.search_values,
        ):
            self.returned_sentences.append(returned_sentence)

        self.assertEqual(self.returned_sentences[0], self.test_sentences[0])
        self.assertEqual(self.returned_sentences[1], self.test_sentences[1])
        self.assertEqual(self.returned_sentences[2], self.test_sentences[2])

        self.search_values_1 = ["Розы"]
        self.returned_sentences_1 = []
        for returned_sentence in find_occurrence(
            self.test_sentences,
            self.search_values_1,
        ):
            self.returned_sentences_1.append(returned_sentence)

        self.assertEqual(self.returned_sentences_1[0], self.test_sentences[1])

    def test_find_occurrence_call_count(self):
        """Test the call count of parsing function"""

        self.search_values_1 = ["розовая", "роза"]
        call_counter = 0
        for _ in find_occurrence(self.test_sentences, self.search_values_1):
            call_counter += 1
        self.assertEqual(call_counter, 3)

        self.search_values_2 = ["розовая"]
        call_counter = 0
        for _ in find_occurrence(self.test_sentences, self.search_values_2):
            call_counter += 1
        self.assertEqual(call_counter, 1)

        self.search_values_3 = ["роз"]
        call_counter = 0
        for _ in find_occurrence(self.test_sentences, self.search_values_3):
            call_counter += 1
        self.assertEqual(call_counter, 1)

        self.search_values_4 = [""]
        call_counter = 0
        for _ in find_occurrence(self.test_sentences, self.search_values_4):
            call_counter += 1
        self.assertEqual(call_counter, 0)

    def test_chunkify(self):
        """Test the chunkify methode of the Chunker class"""

        self.test_sentences = [
            "роза роза роза роза роза",
            "роза роза роза роза роза",
            "роза роза роза роза роза",
            "роза роза роза роза роза",
            "роза роза роза роза роза",
        ]
        self.test_sentence_len_in_bytes = len(
            (self.test_sentences[0] + "\n").encode("utf-8"),
        )
        self.test_sentences_len_in_bytes = len(
            (self.test_sentences[0] + "\n").encode("utf-8"),
        ) * len(self.test_sentences)

        self.chunkify_input_filename = "chunkify_input.txt"
        with open(
            self.chunkify_input_filename,
            "w",
            encoding="utf-8",
        ) as self.file:
            for sentence in self.test_sentences:
                self.file.write(sentence)
                self.file.write("\n")

        self.chunker_1 = Chunker(
            self.chunkify_input_filename,
            self.output_fd,
            chunk_size=self.test_sentence_len_in_bytes // 2,
        )
        for _, chunk_size in self.chunker_1.chunkify():
            self.assertEqual(chunk_size, self.test_sentence_len_in_bytes)

        self.chunker_2 = Chunker(
            self.chunkify_input_filename,
            self.output_fd,
            chunk_size=self.test_sentences_len_in_bytes,
        )
        for _, chunk_size in self.chunker_2.chunkify():
            self.assertEqual(chunk_size, self.test_sentences_len_in_bytes)

        try:
            os.remove(self.file.name)
        except OSError as why:
            print(why)

    def test_file_processing_with_different_chunk_size(self):
        """Check correct processing of sentences with set search_values"""

        search_values_list = ["роза"]
        chunk_stats = []

        #  process the input.txt file, get chunk stats
        #  and write the searched sentences into output_i.txt
        for i in range(1, 4):
            self.output_filename = f"output_{i}.txt"
            chunk_stat = []
            with open(
                self.output_filename,
                "w",
                encoding="utf-8",
            ) if self.output_filename != "stdout" \
                    else sys.stdout as output_file:
                self.chunker = Chunker(
                    self.input_fd,
                    output_file,
                    chunk_size=i * 16,
                )
                for (
                    chunk_start_pos,
                    chunk_offset,
                ) in self.chunker.chunkify():
                    chunk_stat.append((chunk_start_pos, chunk_offset))
                    self.chunker.parse_wrapper(
                        chunk_start=chunk_start_pos,
                        chunk_offset=chunk_offset,
                        search_values=search_values_list,
                        parser_func=find_occurrence,
                    )
            chunk_stats.append(chunk_stat)

        #  check the equality of found sentences
        found_sentences = []
        for i in range(1, 4):
            self.output_filename = f"output_{i}.txt"
            with open(
                self.output_filename,
                "r",
                encoding="utf-8",
            ) as output_file:
                found_sentences.append(output_file.read().splitlines())

        right_rose_sentences = [
            "а роза упала на лапу азора",
            "роза хуторянка",
            "роза всегда возвращает свои долги",
            "роза скоро",
            "проклятье роза",
            "роза ветров",
            "роза сябитова",
        ]
        self.assertEqual(found_sentences[0], right_rose_sentences)
        self.assertEqual(len(found_sentences[0]), 7)

        self.assertEqual(found_sentences[1], right_rose_sentences)
        self.assertEqual(len(found_sentences[1]), 7)

        self.assertEqual(found_sentences[0], right_rose_sentences)
        self.assertEqual(len(found_sentences[2]), 7)

        #  check file stats
        right_chunk_stats = [
            [
                (0, 48),
                (48, 116),
                (164, 37),
                (201, 70),
                (271, 52),
                (323, 63),
                (386, 138),
                (524, 56),
                (580, 89),
                (669, 48),
                (717, 50),
            ],
            [
                (0, 164),
                (164, 65),
                (229, 70),
                (299, 87),
                (386, 138),
                (524, 83),
                (607, 62),
                (669, 68),
                (737, 30),
            ],
            [
                (0, 164),
                (164, 107),
                (271, 115),
                (386, 138),
                (524, 145),
                (669, 98),
            ],
        ]

        self.assertEqual(chunk_stats[0], right_chunk_stats[0])
        self.assertEqual(chunk_stats[1], right_chunk_stats[1])
        self.assertEqual(chunk_stats[2], right_chunk_stats[2])

        #  remove artefact files
        for i in range(1, 4):
            self.output_filename = f"output_{i}.txt"
            try:
                os.remove(self.output_filename)
            except OSError as why:
                print(why)
