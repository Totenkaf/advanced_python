from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from fastapi_cache.backends.redis import RedisCacheBackend
from sqlalchemy.ext.asyncio import AsyncSession

from middleware.redis import get_cache, get_key_by_pattern, redis_cache, set_cache
from common.logger import get_logger
from db.db import get_session
from models.users import User
from schemas.files import FileInDB, FileSearchMatches, FilesList
from services.files import files_crud

from .utils import current_user

router = APIRouter()
LOG = get_logger()


@router.post(
    '/upload',
    status_code=status.HTTP_201_CREATED,
    response_model=FileInDB,
    response_model_exclude_unset=True,
    description='Uploading user file.',
)
async def upload_file(
    path: str = Query(
        example='my_path',
        max_length=450,
        min_length=1,
    ),
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
    file: UploadFile = File(),
    cache: RedisCacheBackend = Depends(redis_cache)
) -> FileInDB:
    LOG.info('Uploading a new file.')
    await cache.delete(f'files_{user.id}')
    keys = await get_key_by_pattern(cache, pattern=f'search-user:{user.id}*')
    for key in keys:
        await cache.delete(key)
    file_upload = await files_crud.upload_file(
        db=db,
        file=file,
        user=user,
        path=path)
    LOG.info('A new file successfully uploaded.')
    return FileInDB(**file_upload)


@router.get(
    '/list',
    response_model=FilesList,
    description='Getting the file list.',
)
async def get_files_list(
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
    cache: RedisCacheBackend = Depends(redis_cache)
) -> FilesList | dict:
    LOG.info('Getting a file list.')
    result = await get_cache(cache, f'files_{user.id}')
    if not result:
        files = await files_crud.get_files_list(db=db, user=user)
        files_list = [FileInDB.from_orm(file).dict() for file in files]
        await set_cache(
            cache,
            redis_key=f'files_{user.id}',
            data={
                'account_id': user.id,
                'files': files_list,
            }
        )
        LOG.info('The file list is taken from the DB.')
        return FilesList(account_id=user.id, files=files_list)
    LOG.info('The file list is taken from the Redis cache.')
    return result


@router.get(
    '/download',
    response_class=FileResponse,
    description='Download file or archived folder.',
)
async def download_file_or_folder(
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
    path_or_id: str = Query(
        default='',
        alias='path_to_file',
        description='Path to file or file id',
    ),
    path_to_folder: str = Query(
        default='',
        description='Path to folder',
    ),
    compression_type: str = Query(
        default='',
        description='Archive type: zip | tar | 7z',
    )
) -> FileResponse:
    if compression_type and compression_type not in ('zip', 'tar', '7z'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Wrong compression type.',
        )
    if path_to_folder:
        return await files_crud.get_folder_archive(
            user=user,
            path=path_to_folder,
            compression_type=compression_type,
        )
    file = await files_crud.download_file(
        db=db,
        user=user,
        path_or_id=path_or_id,
        compression_type=compression_type,
    )
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found.",
        )
    return file


@router.get(
    '/search',
    response_model=FileSearchMatches,
    description='Searching for an uploaded file.'
)
async def files_search(
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
    path: str = Query(
        default='',
        example='my_path',
        max_length=500,
        description='Folder id to search',
    ),
    extension: str = Query(
        default='',
        max_length=10,
        description='File extension',
    ),
    order_by: str = Query(
        default='id',
        max_length=50,
        description=f"Field to order search result: "
                    f"{', '.join(list(FileInDB.__fields__.keys()))}"),
    limit: int = Query(
        default=100,
        ge=1,
        description='Max number of result.',
    ),
    cache: RedisCacheBackend = Depends(redis_cache)
) -> FileSearchMatches | dict:
    if order_by not in FileInDB.__fields__:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order_by field should be in {FileInDB.__fields__}"
        )
    LOG.info('Starting a file search.')
    cache_key = (f'search-user:{user.id}-path:{path}-ext:{extension}-'
                 f'ord:{order_by}-limit:{limit}')
    result = await get_cache(cache, cache_key)
    if not result:
        new_result = await files_crud.search(
            db=db,
            user=user,
            path=path,
            ext=extension,
            order=order_by,
            limit=limit,
        )
        new_result = FileSearchMatches(matches=new_result)
        await set_cache(cache, redis_key=cache_key, data=new_result.dict())
        LOG.info('Searching for files in the DB.')
        return new_result
    LOG.info('Searching for files in the Redis cache.')
    return result
