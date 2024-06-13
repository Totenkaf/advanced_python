from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend
import uvicorn

from api.v1 import files, services, users
from common.config import app_settings
from common.logger import setup_logging
from utils import check_python_version


app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    redoc_url=None
)


@app.on_event('startup')
async def on_startup() -> None:
    rc = RedisCacheBackend(
        f'redis://{app_settings.redis_host}:{app_settings.redis_port}'
    )
    caches.set(CACHE_KEY, rc)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()


app.include_router(services.router, prefix="/api/v1", tags=['Services'])
app.include_router(users.router, prefix='/api/v1', tags=['Users'])
app.include_router(files.router, prefix='/api/v1/files', tags=['Files'])


if __name__ == '__main__':
    check_python_version()
    setup_logging()
    uvicorn.run(
        'main:app',
        host=app_settings.project_host,
        port=app_settings.project_port,
        reload=True,
        log_level='info',
    )
