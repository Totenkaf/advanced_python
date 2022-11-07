"""
Asyncio fetcher unit test
Copyright 2022 by Artem Ustsov
"""

import json
from unittest.mock import Mock, patch
import pytest
from fetcher.fetcher import AsyncioFetcher, UrlStats
import asyncio
import json_tools

#  pylint: disable=too-many-public-methods
#  pylint: disable=attribute-defined-outside-init
#  pylint: disable=too-many-instance-attributes
#  pylint: disable=protected-access


def test_create_url_stat():
    url_stat = UrlStats()
    assert url_stat.url_processed == 0
    assert url_stat.url_correct == 0
    assert url_stat.url_wrong == 0


@patch('builtins.print')
def test_print_stats(mock_print):
    url_stat = UrlStats()
    url_stat.print_stat()
    assert mock_print.called


def test_create_fetcher():
    fetcher = AsyncioFetcher(connections=3, k_top=3)
    assert fetcher.connections == 3
    assert fetcher.k_top == 3
    assert isinstance(fetcher.url_stat, UrlStats)


@pytest.mark.asyncio
async def test_parse_url():
    """Response async parsing"""
    fetcher = AsyncioFetcher(connections=3, k_top=3)

    server_response = """<!DOCTYPE html>
                                    <html>
                                      <head>
                                        <meta charset="utf-8">
                                        <title>Формула этанола</title>
                                      </head>
                                      <body>
                                        <p>Формула этанола
                                        С<sub>2</sub>Н<sub>5</sub>ОН</p>
                                      </body>
                                    </html>"""

    json_response = await fetcher.parse_data(server_response)
    # only three because of default k_top=3 on server
    json_expected = json.dumps(
        {"Формула": 2, "этанола": 2, "С": 1},
        separators=(", ", ": "),
        ensure_ascii=False,
    )
    # json_tools.diff return empty list if no differences
    assert json_tools.diff(json_response, json_expected) == []
