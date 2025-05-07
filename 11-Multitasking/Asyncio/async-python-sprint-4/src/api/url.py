# Copyright (c) 2023 Artem Ustsov

from http import HTTPStatus
from typing import List, Union
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Path
from fastapi.responses import RedirectResponse, Response
from pydantic import HttpUrl, AnyUrl
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from common.dependencies import get_client
from schemas import url as url_schema
from services.url import Url

url_router = APIRouter()


@url_router.get(
    '/{url_id}',
    description='Get a short url for redirect',
)
async def get(
    *,
    session: AsyncSession = Depends(get_session),
    url_id: UUID = Path(..., example='3a8f7808-f12b-4599-8fbb-b72b67943463'),
    client: AnyUrl = Depends(get_client),
) -> RedirectResponse:
    full_url: HttpUrl = await Url.get_redirect_url(session, client, url_id)
    return RedirectResponse(url=full_url)


@url_router.get(
    '/{url_id}/status',
    response_model=Union[url_schema.UrlStatus],
    description='Get number of clicks for specific url',
)
async def get_status(
    *, session: AsyncSession = Depends(get_session),
    url_id: UUID = Path(..., example='3a8f7808-f12b-4599-8fbb-b72b67943463'),
    full_info: bool = Query(default=True),
    limit: int = Query(default=10),
    offset: int = Query(default=0)
) -> Response:
    status = await Url.get_status(session, url_id, full_info, limit=limit, offset=offset)
    return status


@url_router.post(
    '/',
    response_model=url_schema.UrlResponse,
    status_code=HTTPStatus.CREATED,
    description='Create shortcut for given url',
)
async def create(
    *,
    session: AsyncSession = Depends(get_session),
    schema: url_schema.UrlCreate,
) -> Response:
    url = await Url.create(session, schema=schema)
    return url


@url_router.patch(
    '/{url_id}',
    response_model=url_schema.UrlResponse,
    status_code=HTTPStatus.OK,
    description='Delete saved url',
)
async def ban(
    *,
    session: AsyncSession = Depends(get_session),
    url_id: UUID,
    schema: url_schema.UrlUpdate,
) -> Response:
    url = await Url.update(session, url_id, schema=schema)
    return url


@url_router.post(
    '/shorten', response_model=list[url_schema.UrlResponse],
    status_code=HTTPStatus.CREATED,
    description='Create urls by batch',
)
async def bulk_create(
    *,
    session: AsyncSession = Depends(get_session),
    schema: List[url_schema.UrlCreate],
) -> Response:
    urls = await Url.bulk_create(session, schema=schema)
    return urls
