"""
Json_parser.
Copyright 2022 by Artem Ustsov
"""
import json


def print_statistics(*args) -> None:
    """Prints the keyword symbol statistics"""
    print(f"Catch keyword is: {args[0]}")
    print("== Statistics ==")
    print(f"- {len(args[1])} characters with {len(set(args[1]))} "
          f"unique symbols\n"
          f"- {len(args[2])} digits with {len(set(args[2]))} "
          f"unique numbers\n"
          f"- {len(set(args[1])) + len(set(args[2]))} "
          f"symbols - total number of the uniques \n")


def keyword_handler(keyword: str) -> None:
    """
    Takes a string as an argument, calculates the number of letters
    and numbers in a word, finds the number of unique characters
    """
    word_schema = list(keyword)
    characters = []
    digits = []
    for char in word_schema:
        if char.isdigit():
            digits.append(char)
        elif char.isalpha():
            characters.append(char)
    print_statistics(keyword, characters, digits)


def parse_json(json_source: str, required_fields=None,
               keywords=None, keyword_callback=None) -> None:
    """
    Takes a string as an argument, calculates the number of letters
    and numbers in a word, finds the number of unique characters.
    If required_fields are not set - parsing is performed on all keys
    from the json dictionary
    If keywords are not set - parsing is performed on all words
    from the json dictionary
    If keyword_callback is not set - raising an Attribute error
    """
    json_dict = json.loads(json_source)
    keyword_parsed_values = []
    if required_fields is None:
        required_fields = json_dict.keys()
    if keywords is None:
        keywords = set()
        [keywords.update(values.split()) for values in json_dict.values()]
    if keyword_callback is None:
        raise AttributeError("Callback function is lost")

    for key, values in json_dict.items():
        if key in required_fields:
            parsed_values = values.split()
            for value in parsed_values:
                if value in keywords and value not in keyword_parsed_values:
                    keyword_callback(value)
                    keyword_parsed_values.append(value)
