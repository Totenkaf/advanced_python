from fastapi import APIRouter, Depends
from fastapi_cache.backends.redis import RedisCacheBackend
from sqlalchemy.ext.asyncio import AsyncSession

from middleware.redis import ping_cache, redis_cache
from common.logger import get_logger
from db.db import get_session
from schemas.services import Ping
from services.files import files_crud

router = APIRouter()
LOG = get_logger()

@router.get(
    '/ping',
    response_model=Ping,
    description='Execute a database ping.',
)
async def check_db(
    db: AsyncSession = Depends(get_session),
    cache: RedisCacheBackend = Depends(redis_cache)
) -> Ping:

    LOG.info('Get ping from the Redis cache.')
    from_cache = await ping_cache(cache=cache)
    LOG.info('Get ping from the DB.')
    from_db = await files_crud.get_ping_db(db=db)
    return Ping(
        db="{:.4f}".format(from_db),
        cache="{:.4f}".format(from_cache)
    )
