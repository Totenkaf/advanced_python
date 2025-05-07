# Copyright (c) 2023 Artem Ustsov

from fastapi import APIRouter

from api.url import url_router
from api.utils import utils_router


router = APIRouter()

router.include_router(utils_router)
router.include_router(url_router, tags=["url"])
