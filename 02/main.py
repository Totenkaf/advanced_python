"""
Json_parser.
Copyright 2022 by Artem Ustsov
"""

from parser.json_parser import keyword_handler, parse_json


if __name__ == "__main__":
    JSON_SOURCE_1 = (
        "{"
        '"key1": "word1 word2 word3", '
        '"key2": "word2 word6 word4 abracadabra",'
        '"key3": "word1",'
        '"key4": ""'
        "}"
    )

    FIELDS = ["key1", "key2"]
    WORDS = ["word1", "word6"]
    try:
        parse_json(
            JSON_SOURCE_1,
            required_fields=FIELDS,
            keywords=WORDS,
            keyword_callback=keyword_handler,
        )
    except AttributeError as error:
        print(error)
