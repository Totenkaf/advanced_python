import json
import time
from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import HTTPException, status
from fastapi_cache import caches
from fastapi_cache.backends.base import BaseCacheBackend
from fastapi_cache.backends.redis import CACHE_KEY


def redis_cache() -> BaseCacheBackend | None:
    return caches.get(CACHE_KEY)


def convert_value(value: Any) -> Any:
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    return value


async def get_cache(cache: BaseCacheBackend, redis_key: str) -> dict | None:
    result = await cache.get(redis_key)
    if result:
        return json.loads(result)
    return None


async def get_key_by_pattern(
    cache: BaseCacheBackend,
    pattern: str
) -> list:
    client = await cache._client
    return await client.keys(pattern=pattern)


async def set_cache(cache, redis_key, data, expire: int = 0) -> None:
    await cache.set(
        key=redis_key,
        value=json.dumps(data, default=convert_value),
        expire=expire
    )


async def ping_cache(cache: BaseCacheBackend) -> float | str:
    key, value = 'test_key', 'Simple value'
    start_time = time.time()
    await cache.set(key=key, value=value, expire=5)
    get_value = await cache.get(key)
    if value == get_value:
        return time.time() - start_time
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Failed to get test value from cache.'
    )
