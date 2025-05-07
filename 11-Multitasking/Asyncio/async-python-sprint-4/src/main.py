# Copyright (c) 2023 Artem Ustsov

import uvicorn
from fastapi import FastAPI

from api.routes import router
from common import exceptions as exc
from common.config import SETTINGS
from utils import check_python_version

app = FastAPI()
app.include_router(router)
app.add_exception_handler(exc.ObjectAlreadyExists, exc.obj_already_exists_handler)
app.add_exception_handler(exc.ObjectDoesNotExist, exc.obj_does_not_exist_handler)
app.add_exception_handler(exc.UrlIsBanned, exc.url_is_banned_handler)


if __name__ == '__main__':
    check_python_version()
    uvicorn.run(
        'main:app',
        host=SETTINGS.server_host,
        port=SETTINGS.server_port,
        loop='asyncio',
        reload=True,
    )
