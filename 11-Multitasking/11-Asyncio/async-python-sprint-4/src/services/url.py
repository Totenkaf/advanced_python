# Copyright (c) 2023 Artem Ustsov

from uuid import UUID

from pydantic import HttpUrl, AnyUrl
from sqlalchemy.ext.asyncio import AsyncSession

from common.exceptions import UrlIsBanned
from models.url import Url as UrlModel
from schemas.url import UrlCreate, UrlUpdate
from schemas.url_click import UrlClickCreate
from services.base import RepositoryInterface
from services.url_click import UrlClick


class UrlRepository(RepositoryInterface[UrlModel, UrlCreate, UrlUpdate]):

    async def get_redirect_url(
        self,
        session: AsyncSession,
        client: AnyUrl,
        url_id: UUID,
    ) -> HttpUrl:
        url = await super().get(session, url_id)
        if not url.is_active:
            raise UrlIsBanned(url=url.full_url)
        await UrlClick.create(session, schema=UrlClickCreate(url_id=url.id, client=client))
        return url.full_url

    async def get_status(
        self,
        session: AsyncSession,
        url_id: UUID,
        full_info: bool,
        **options,
    ) -> dict:
        url = await super().get(session, url_id)
        if full_info:
            clicks = await UrlClick.filter(session, url_id=url.id, **options)
        else:
            clicks = len(await UrlClick.filter(session, url_id=url.id))
        return dict(url=url, clicks=clicks)


Url = UrlRepository(UrlModel)
