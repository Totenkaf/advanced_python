from pathlib import Path
import pytest

from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import app

from tests.utils import (
    TEST_FILE,
    TEST_FOLDER,
    TEST_PASSWORD,
    TEST_USER1,
    UPLOAD_FILES,
)


@pytest.mark.asyncio
async def test_ping(client: AsyncClient, async_session: AsyncSession) -> None:
    response = await client.get(app.url_path_for('check_db'))
    assert response.status_code == status.HTTP_200_OK
    res = response.json()
    assert 'db' in res
    assert 'cache' in res
    assert res['db'] > 0
    assert res['cache'] > 0


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, async_session: AsyncSession) -> None:
    response = await client.post(
        app.url_path_for('register_user'),
        json={
            'login': TEST_USER1,
            'password': TEST_PASSWORD
        }
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_auth_user(client: AsyncClient, async_session: AsyncSession) -> None:
    response = await client.post(
        app.url_path_for('auth_user'),
        data={
            'username': TEST_USER1,
            'password': TEST_PASSWORD,
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access_token' in response.json()


@pytest.mark.asyncio
async def test_get_files_list_unauthorized(client: AsyncClient, async_session: AsyncSession) -> None:
    response = await client.get(app.url_path_for('get_files_list'))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_empty_file_list(client_authorized: AsyncClient, async_session: AsyncSession) -> None:
    response = await client_authorized.get(app.url_path_for("get_files_list"))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'files' in data
    assert isinstance(data['files'], list)
    assert len(data['files']) == 0
    assert 'account_id' in data


@pytest.mark.asyncio
async def test_upload_file_unauthorized(client: AsyncClient, async_session: AsyncSession) -> None:
    response = await client.post(app.url_path_for('upload_file'))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_upload_file(client_authorized: AsyncClient, async_session: AsyncSession) -> None:
    path_file = Path(TEST_FILE)
    if not path_file.exists():
        with open(path_file, 'w'):
            pass
    file = {'file': path_file.open('rb')}
    response = await client_authorized.post(
        app.url_path_for('upload_file'),
        params={'path': TEST_FOLDER + '/'},
        files=file
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data.get('id')
    UPLOAD_FILES[TEST_FILE] = data.get('id')


@pytest.mark.asyncio
async def test_get_file_list(client_authorized: AsyncClient, async_session: AsyncSession) -> None:
    response = await client_authorized.get(app.url_path_for('get_files_list'))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'files' in data
    assert isinstance(data['files'], list)
    assert len(data['files']) == 1
    file = data['files'][0]
    assert file['name'] == TEST_FILE


@pytest.mark.asyncio
async def test_download_file_unauthorized(client: AsyncClient, async_session: AsyncSession) -> None:
    response = await client.get(app.url_path_for('download_file_or_folder'))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_download_file(client_authorized: AsyncClient, async_session: AsyncSession) -> None:
    response = await client_authorized.get(
        app.url_path_for('download_file_or_folder'),
        params={'path_to_file': UPLOAD_FILES[TEST_FILE]}
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_download_zip_file(client_authorized: AsyncClient, async_session: AsyncSession) -> None:
    response = await client_authorized.get(
        app.url_path_for('download_file_or_folder'),
        params={'path_to_folder': TEST_FOLDER, 'compression_type': 'zip'}
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_search_file_unauthorized(client: AsyncClient, async_session: AsyncSession) -> None:
    response = await client.get(app.url_path_for('files_search'))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_file_search(client_authorized: AsyncClient, async_session: AsyncSession) -> None:
    response = await client_authorized.get(
        app.url_path_for('files_search'),
        params={'extension': 'txt'}
    )
    assert response.status_code == status.HTTP_200_OK
    res = response.json()
    assert len(res['matches']) == 1
    file = res['matches'][0]
    assert file['name'] == TEST_FILE
