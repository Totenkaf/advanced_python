# Copyright (c) 2023 Artem Ustsov

import datetime as dt

from pydantic import BaseModel, UUID4, AnyUrl


class UrlClickBase(BaseModel):
    pass


class UrlClickCreate(UrlClickBase):
    url_id: UUID4
    client: AnyUrl


class UrlClickUpdate(UrlClickBase):
    pass


class UrlClickResponse(BaseModel):
    datetime: dt.datetime
    client: AnyUrl

    class Config:
        orm_mode = True
