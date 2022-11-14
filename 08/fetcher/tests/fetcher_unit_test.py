"""
Asyncio fetcher unit test
Copyright 2022 by Artem Ustsov
"""

import asyncio
import json
import sys
from unittest.mock import AsyncMock, patch
import pytest
import json_tools
import aiohttp
from fetcher.fetcher import AsyncioFetcher, UrlStats


#  pylint: disable=too-many-public-methods
#  pylint: disable=attribute-defined-outside-init
#  pylint: disable=too-many-instance-attributes
#  pylint: disable=protected-access


def test_create_url_stat():
    """Test init stats"""
    url_stat = UrlStats()
    assert url_stat.url_processed == 0
    assert url_stat.url_correct == 0
    assert url_stat.url_wrong == 0


@patch("builtins.print")
def test_print_stats(mock_print):
    """Test print stats"""

    url_stat = UrlStats()
    url_stat.print_stat()
    assert mock_print.called


def test_create_fetcher():
    """Fetcher creating"""

    fetcher = AsyncioFetcher(connections=3, k_top=3)
    assert fetcher.connections == 3
    assert fetcher.k_top == 3
    assert isinstance(fetcher.url_stat, UrlStats)


@pytest.mark.asyncio
async def test_parse_data():
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
    assert not json_tools.diff(json_response, json_expected)


@pytest.mark.asyncio
async def test_batch_fetch_data():
    """Test asyncio batch fetching"""

    fetcher = AsyncioFetcher(connections=5, k_top=3)
    urls = ["url_1", "url_2", "url_3"]
    file = AsyncMock()

    mock_async_queue_patcher = patch.object(
        asyncio.Queue, "join", new=AsyncMock()
    )
    mock_async_queue = mock_async_queue_patcher.start()
    mock_async_queue.return_value = None

    with patch.object(
        AsyncioFetcher, "fetch", new=AsyncMock()
    ) as async_fetch_mock:
        await fetcher.batch_fetch(urls, file)
        assert async_fetch_mock.call_count == fetcher.connections

    mock_async_queue_patcher.stop()


@pytest.mark.asyncio
@patch("sys.stdout.write")
async def test_fetch_data(mock_out):
    """Fetch the correct urls"""

    mock_out.return_value = None
    fetcher = AsyncioFetcher(connections=5, k_top=3)

    mock_aiohttp_get_patcher = patch.object(aiohttp.ClientSession, "get")
    mock_aiohttp_get = mock_aiohttp_get_patcher.start()
    mock_aiohttp_get.return_value = AsyncMock()

    mock_url_parse_patcher = patch.object(
        AsyncioFetcher, "parse_data", new=AsyncMock()
    )
    mock_url_parse = mock_url_parse_patcher.start()
    mock_url_parse.return_value = None

    urls = ["url_1", "url_2", "url_3", "url_4"]

    await fetcher.batch_fetch(urls, sys.stdout)
    assert fetcher.url_stat.url_processed == len(urls)
    assert fetcher.url_stat.url_correct == len(urls)
    assert fetcher.url_stat.url_wrong == 0

    mock_aiohttp_get_patcher.stop()
    mock_url_parse_patcher.stop()


@pytest.mark.asyncio
@patch("sys.stdout.write")
async def test_fetch_bad_data(mock_out):
    """Try to process an error during the url fetching"""

    mock_out.return_value = None
    fetcher = AsyncioFetcher(connections=5, k_top=3)

    mock_aiohttp_get_patcher = patch.object(aiohttp.ClientSession, "get")
    mock_aiohttp_get = mock_aiohttp_get_patcher.start()
    mock_aiohttp_get.return_value = AsyncMock()

    mock_url_parse_patcher = patch.object(
        AsyncioFetcher, "parse_data", new=AsyncMock()
    )
    mock_url_parse = mock_url_parse_patcher.start()

    async def connection_error():
        raise ConnectionError

    mock_url_parse.side_effect = connection_error

    urls = ["url_1"]

    await fetcher.batch_fetch(urls, sys.stdout)
    assert fetcher.url_stat.url_processed == 1
    assert fetcher.url_stat.url_correct == 0
    assert fetcher.url_stat.url_wrong == 1

    mock_aiohttp_get_patcher.stop()
    mock_url_parse_patcher.stop()
