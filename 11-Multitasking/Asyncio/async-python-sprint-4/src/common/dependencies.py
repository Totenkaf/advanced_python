# Copyright (c) 2023 Artem Ustsov

from fastapi import Request
from pydantic import AnyUrl


def get_client(request: Request) -> str:
    host, port = request.client.host, str(request.client.port)
    return AnyUrl.build(scheme='http', host=host, port=port)
