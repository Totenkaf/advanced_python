# Copyright (c) 2023 Artem Ustsov

from http import HTTPStatus

from fastapi import Request
from fastapi.responses import ORJSONResponse


class ObjectAlreadyExists(Exception):
    pass


def obj_already_exists_handler(request: Request, exc: ObjectAlreadyExists) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=HTTPStatus.CONFLICT,
        content={'detail': str(exc)},
    )


class ObjectDoesNotExist(Exception):
    pass


def obj_does_not_exist_handler(request: Request, exc: ObjectDoesNotExist) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={'detail': str(exc)},
    )


class UrlIsBanned(Exception):
    def __init__(self, url: str):
        self.url = url


def url_is_banned_handler(request: Request, exc: UrlIsBanned) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=HTTPStatus.GONE,
        content={'detail': f'"{exc.url}" is banned'},
    )
