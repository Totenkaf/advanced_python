# Copyright (c) 2023 Artem Ustsov

from models.url_click import UrlClick as UrlClickModel
from schemas.url_click import UrlClickCreate, UrlClickUpdate
from services.base import RepositoryInterface


class UrlClickRepository(RepositoryInterface[UrlClickModel, UrlClickCreate, UrlClickUpdate]):
    pass


UrlClick = UrlClickRepository(UrlClickModel)
