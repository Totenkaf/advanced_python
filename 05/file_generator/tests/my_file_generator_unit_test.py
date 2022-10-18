"""
File generator package main file
Copyright 2022 by Artem Ustsov
"""

import os
import unittest
from unittest.mock import patch

from file_generator.my_file_generator import (
    Chunker,
    PositiveInteger,
    find_occurrence,
)

#  pylint: disable=too-many-public-methods
#  pylint: disable=attribute-defined-outside-init
#  pylint: disable=too-many-instance-attributes


class TestFileGenerator(unittest.TestCase):
    """
    Main test class for my_file_generator module
    """

    def setUp(self) -> None:
        self.input_fd = "input.txt"
        self.output_fd = "output.txt"
        self.test_sentences = [
            "а роза упала на лапу азора",
            "розовая пантера надела розовые штаны и купила розу для Розы",
            "роза купленная вчера в магазине роз начала розоветь",
        ]

    @patch.object(PositiveInteger, "__set__")
    def test_set_integer_descr(self, __set__mock):
        """Check the call of __set__ method in PositiveInteger-descr"""
        self.chunker = Chunker(self.input_fd, self.output_fd)
        self.assertTrue(__set__mock.called)

    @patch.object(PositiveInteger, "__get__")
    def test_get_integer_descr(self, __get__mock):
        """Check the call of __get__ method in PositiveInteger-descr"""
        __get__mock.return_value = None
        self.chunker = Chunker(self.input_fd, self.output_fd)
        self.assertEqual(self.chunker.buffer_size, None)
        self.assertTrue(__get__mock.called)

    @patch.object(Chunker, "__init__")
    def test_chunker_mock_init(self, __init__mock):
        """Chunker mock init"""
        __init__mock.return_value = None
        self.chunker = Chunker(self.input_fd, self.output_fd)
        self.assertTrue(__init__mock.called)

    def test_chunker_init(self):
        """Chunker init"""
        self.chunker = Chunker(self.input_fd, self.output_fd, buffer_size=32)
        self.assertEqual(self.chunker.input_fd, self.input_fd)
        self.assertEqual(self.chunker.output_fd, self.output_fd)
        self.assertEqual(self.chunker.buffer_size, 32)

    def test_chunker_init_wrong_buffer_size(self):
        """Chunker init with wrong buffer size for chunkify
        Expects value or type error.
        """

        self.assertRaises(
            ValueError, Chunker, self.input_fd, self.output_fd, buffer_size=0
        )
        self.assertRaises(
            ValueError,
            Chunker,
            self.input_fd,
            self.output_fd,
            buffer_size=-234623,
        )
        self.assertRaises(
            TypeError, Chunker, self.input_fd, self.output_fd, buffer_size="0"
        )
        self.assertRaises(
            TypeError, Chunker, self.input_fd, self.output_fd, buffer_size={0}
        )

    def test_find_occurrence_returned_sentence(self):
        """Test the return values of parsing function"""

        self.search_values = ["розовая", "роза"]
        self.returned_sentences = []
        for returned_sentence in find_occurrence(
            self.test_sentences, self.search_values
        ):
            self.returned_sentences.append(returned_sentence)

        self.assertEqual(self.returned_sentences[0], self.test_sentences[0])
        self.assertEqual(self.returned_sentences[1], self.test_sentences[1])
        self.assertEqual(self.returned_sentences[2], self.test_sentences[2])

        self.search_values_1 = ["Розы"]
        self.returned_sentences_1 = []
        for returned_sentence in find_occurrence(
            self.test_sentences, self.search_values_1
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
            (self.test_sentences[0] + "\n").encode("utf-8")
        )
        self.test_sentences_len_in_bytes = len(
            (self.test_sentences[0] + "\n").encode("utf-8")
        ) * len(self.test_sentences)

        self.chunkify_input_filename = "chunkify_input.txt"
        with open(
            self.chunkify_input_filename, "w", encoding="utf-8"
        ) as self.file:
            for sentence in self.test_sentences:
                self.file.write(sentence)
                self.file.write("\n")

        self.chunker_1 = Chunker(
            self.chunkify_input_filename,
            self.output_fd,
            buffer_size=self.test_sentence_len_in_bytes // 2,
        )
        for _, chunk_size in self.chunker_1.chunkify():
            self.assertEqual(chunk_size, self.test_sentence_len_in_bytes)

        self.chunker_2 = Chunker(
            self.chunkify_input_filename,
            self.output_fd,
            buffer_size=self.test_sentences_len_in_bytes,
        )
        for _, chunk_size in self.chunker_2.chunkify():
            self.assertEqual(chunk_size, self.test_sentences_len_in_bytes)

        try:
            os.remove(self.file.name)
        except OSError as why:
            print(why)


if __name__ == "__main__":
    unittest.main()
