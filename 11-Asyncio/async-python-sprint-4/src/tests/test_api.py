# Copyright (c) 2023 Artem Ustsov

import asyncio
from http import HTTPStatus

from fastapi import FastAPI
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from services.url import Url
from services.url_click import UrlClick


@pytest.mark.asyncio
async def test_app_up_and_running(client: AsyncClient) -> None:
    response = await client.get(url='docs')

    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_db_is_up_and_running(fastapi_app: FastAPI, client: AsyncClient) -> None:
    response = await client.get(fastapi_app.url_path_for('ping'))

    assert response.status_code == HTTPStatus.OK
    assert 'status' in response.json()
    assert 'ping' in response.json()


@pytest.mark.asyncio
async def test_url_create(fastapi_app: FastAPI, session: AsyncSession, client: AsyncClient) -> None:
    response = await client.post(fastapi_app.url_path_for('create'), json={'full_url': 'https://google.com'})
    urls = await Url.filter(session, full_url='https://google.com')

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['full_url'] == 'https://google.com'
    assert response.json()['shorten_url'].startswith('http://')
    assert len(urls) == 1
    assert urls[0].full_url == 'https://google.com'


@pytest.mark.asyncio
async def test_duplicate_url_create(fastapi_app: FastAPI, session: AsyncSession, client: AsyncClient) -> None:
    response = await client.post(fastapi_app.url_path_for('create'), json={'full_url': 'https://google.com'})
    assert response.status_code == HTTPStatus.CREATED

    response = await client.post(fastapi_app.url_path_for('create'), json={'full_url': 'https://google.com'})
    assert response.status_code == HTTPStatus.CONFLICT

    urls = await Url.filter(session, full_url='https://google.com')
    assert len(urls) == 1


@pytest.mark.asyncio
async def test_url_get_redirect(fastapi_app: FastAPI, client: AsyncClient) -> None:
    response = await client.post(fastapi_app.url_path_for('create'), json={'full_url': 'https://google.com'})
    shorten_url = response.json()['shorten_url']
    redirect_response = await client.get(shorten_url)

    assert redirect_response.status_code == HTTPStatus.TEMPORARY_REDIRECT
    assert redirect_response.headers['Location'] == 'https://google.com'


@pytest.mark.asyncio
async def test_url_ban(fastapi_app: FastAPI, client: AsyncClient) -> None:
    response = await client.post(fastapi_app.url_path_for('create'), json={'full_url': 'https://google.com'})
    shorten_url = response.json()['shorten_url']
    url_id = shorten_url.split('/')[-1]
    await client.patch(f'/{url_id}', json={'is_active': False})
    redirect_response = await client.get(shorten_url)

    assert redirect_response.status_code != HTTPStatus.TEMPORARY_REDIRECT
    assert redirect_response.status_code == HTTPStatus.GONE


@pytest.mark.asyncio
async def test_url_get_unexisting(client: AsyncClient) -> None:
    random_uuid = 'f0d2c2b3-5f8a-4b0d-9b0c-3b2b9e4e9a6f'
    response = await client.get(f'/{random_uuid}')
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_url_status_full(fastapi_app: FastAPI, session: AsyncSession, client: AsyncClient) -> None:
    response = await client.post(fastapi_app.url_path_for('create'), json={'full_url': 'https://google.com'})
    shorten_url = response.json()['shorten_url']
    url_id = shorten_url.split('/')[-1]
    await asyncio.gather(*[client.get(shorten_url) for _ in range(5)])

    clicks = await UrlClick.filter(session, url_id=url_id)
    status_response = await client.get(f'/{url_id}/status')

    assert len(clicks) == 5
    assert status_response.status_code == HTTPStatus.OK
    assert status_response.json()['url']['full_url'] == 'https://google.com'
    assert len(status_response.json()['clicks']) == 5


@pytest.mark.asyncio
async def test_url_status_short(fastapi_app: FastAPI, session: AsyncSession, client: AsyncClient) -> None:
    response = await client.post(fastapi_app.url_path_for('create'), json={'full_url': 'https://google.com'})
    shorten_url = response.json()['shorten_url']
    url_id = shorten_url.split('/')[-1]
    await asyncio.gather(*[client.get(shorten_url) for _ in range(5)])

    clicks = await UrlClick.filter(session, url_id=url_id)
    status_response = await client.get(f'/{url_id}/status', params={'full_info': False})

    assert len(clicks) == 5
    assert status_response.status_code == HTTPStatus.OK
    assert status_response.json()['url']['full_url'] == 'https://google.com'
    assert status_response.json()['clicks'] == 5


@pytest.mark.asyncio
async def test_url_status_limit_and_offset(fastapi_app: FastAPI, session: AsyncSession, client: AsyncClient) -> None:
    response = await client.post(fastapi_app.url_path_for('create'), json={'full_url': 'https://google.com'})
    shorten_url = response.json()['shorten_url']
    url_id = shorten_url.split('/')[-1]
    await asyncio.gather(*[client.get(shorten_url) for _ in range(10)])

    clicks = await UrlClick.filter(session, url_id=url_id)
    status_response = await client.get(f'/{url_id}/status', params={'limit': 5, 'offset': 7})

    assert len(clicks) == 10
    assert status_response.status_code == HTTPStatus.OK
    assert len(status_response.json()['clicks']) == 3


@pytest.mark.asyncio
async def test_url_bulk_create(fastapi_app: FastAPI, session: AsyncSession, client: AsyncClient) -> None:
    links = ['https://google.com', 'https://github.com', 'https://www.youtube.com']
    response = await client.post(
        fastapi_app.url_path_for('bulk_create'),
        json=[
            {'full_url': links[0]},
            {'full_url': links[1]},
            {'full_url': links[2]},
        ],
    )
    urls = await Url.filter(session)

    assert response.status_code == HTTPStatus.CREATED
    assert len(urls) == 3
    assert len(response.json()) == 3
    assert [url.full_url for url in urls] == links
    assert [url['full_url'] for url in response.json()] == links
