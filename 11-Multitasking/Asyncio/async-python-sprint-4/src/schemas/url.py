# Copyright (c) 2023 Artem Ustsov

from typing import List, Union

from pydantic import BaseModel, UUID4, HttpUrl, validator, Field

from common.config import SETTINGS
from schemas.url_click import UrlClickResponse


class UrlBase(BaseModel):
    full_url: HttpUrl


class UrlCreate(UrlBase):
    pass


class UrlUpdate(BaseModel):
    is_active: bool


class UrlResponse(BaseModel):
    id: UUID4 = Field(alias='shorten_url')
    full_url: HttpUrl
    is_active: bool

    @validator('id')
    def id_to_shorten_url(cls, v):
        return f'{SETTINGS.server_address}/{v}'

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UrlStatus(BaseModel):
    url: UrlResponse
    clicks: Union[List[UrlClickResponse], int]
