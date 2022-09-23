"""
Json_parser project. Unit testing
Copyright 2022 by Artem Ustsov
"""

import unittest
from parser.json_parser import keyword_handler, parse_json
from unittest.mock import patch

# from .factory_boy_example import JsonStrFactory


class TestJsonParser(unittest.TestCase):
    """
        Main testing class of json_parser
    """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=consider-using-with
    def setUp(self) -> None:
        self.test_json_source = '{' \
                        '"key1": "word1 word2 word3", ' \
                        '"key2": "word2 word6 word4 abracadabra",' \
                        '"key3": "word1",' \
                        '"key4": ""' \
                        '}'

        self.test_fields = ["key1", "key2"]
        self.test_words = ["word1", "word6"]

    @patch("parser.json_parser.keyword_handler")
    def test_keyword_handler_with_all_args(self, keyword_handler_mock):
        """
        Test the keyword_handler with giving all arguments
        """
        parse_json(self.test_json_source, self.test_fields,
                   self.test_words, keyword_handler_mock)
        self.assertEqual(keyword_handler_mock.call_count, 2)

    @patch("parser.json_parser.keyword_handler")
    def test_keyword_handler_with_no_required_fields(self,
                                                     keyword_handler_mock):
        """
        Test the keyword_handler missing the required_fields
        """
        parse_json(self.test_json_source,
                   keywords=self.test_words,
                   keyword_callback=keyword_handler_mock)
        self.assertEqual(keyword_handler_mock.call_count, 2)

    @patch("parser.json_parser.keyword_handler")
    def test_keyword_handler_with_no_keywords(self, keyword_handler_mock):
        """
        Test the keyword_handler missing the keywords
        """
        parse_json(self.test_json_source, required_fields=self.test_fields,
                   keyword_callback=keyword_handler_mock)
        self.assertEqual(keyword_handler_mock.call_count, 6)

    @patch("parser.json_parser.keyword_handler")
    def test_keyword_handler_with_no_args(self, keyword_handler_mock):
        """
        Test the keyword_handler missing all arguments
        but with keyword_Callback function
        """
        parse_json(self.test_json_source,
                   keyword_callback=keyword_handler_mock)
        self.assertEqual(keyword_handler_mock.call_count, 6)

    def test_parse_json_with_no_keyword_callback(self):
        """
        Test the parse_json without callback function
        """
        self.assertRaises(AttributeError, parse_json, self.test_json_source)

    # @patch("parser.json_parser.print_statistics")
    # def test_print_statistics(self, print_statistics_mock):
    #     """
    #     Test the print_statistics via mocking
    #     """
    #     parse_json(self.test_json_source,
    #                keyword_callback=keyword_handler)
    #     self.assertEqual(print_statistics_mock.call_count, 6)


if __name__ == '__main__':
    unittest.main()
