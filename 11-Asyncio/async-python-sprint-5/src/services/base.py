import os
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from typing import Any, Generic, Type, TypeVar
from zipfile import ZIP_DEFLATED, ZipFile

import aiofiles
from fastapi import File, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from sqlalchemy import and_, exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from common.config import app_settings
from db.db import Base
from models.users import Token, User
from services.utils import (
    DEFAULT_FOLDER,
    HTTP_400_BAD_REQUEST,
    HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    HTTP_422_UNPROCESSABLE_ENTITY,
    hash_password,
    validate_uuid,
)


class UserRepository(ABC):
    @abstractmethod
    def add_user(self, *args, **kwargs):
        raise NotImplementedError


class FileRepository(ABC):
    @abstractmethod
    def upload_file(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def download_file(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_files_list(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def search(self, *args, **kwargs):
        raise NotImplementedError


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
FileSchemaType = TypeVar("FileSchemaType", bound=BaseModel)


class RepositoryDBUser(UserRepository, Generic[ModelType, CreateSchemaType]):
    def __init__(self, user_model: Type[ModelType]):
        self._user_model = user_model

    async def add_user(
        self,
        db: AsyncSession,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        hashed_password = hash_password(obj_in_data.pop('password'))
        obj_in_data['hashed_password'] = hashed_password
        db_obj = self._user_model(**obj_in_data)
        db.add(db_obj)
        try:
            await db.commit()
            await db.refresh(db_obj)
        except exc.IntegrityError:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Input another name.'
            )
        except exc.SQLAlchemyError as error:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error
            )
        return db_obj

    async def get_user_by_name(
        self,
        db: AsyncSession,
        login: str,
    ) -> ModelType | None:
        statement = select(self._user_model).where(
            self._user_model.login == login
        )
        user = await db.execute(statement=statement)
        return user.scalar_one_or_none()

    async def get_user_by_token(
        self,
        db: AsyncSession,
        token: str,
    ) -> ModelType | None:
        query = select(self._user_model).join(Token).where(
            and_(Token.token == token, Token.expires > datetime.now())
        )
        user = await db.execute(query)
        return user.scalar_one_or_none()


class RepositoryDBToken(Generic[ModelType, CreateSchemaType]):
    def __init__(self, token_model: Type[ModelType]):
        self._token_model = token_model

    async def create_token(
        self,
        db: AsyncSession,
        id: int,
    ) -> ModelType:
        expires_time = datetime.now() + timedelta(
            minutes=app_settings.token_expires_min
        )
        db_obj = self._token_model(
            user_id=id,
            expires=expires_time)
        db.add(db_obj)
        try:
            await db.commit()
            await db.refresh(db_obj)
        except exc.SQLAlchemyError as error:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error
            )
        return db_obj


class RepositoryDBFile(FileRepository, Generic[ModelType, CreateSchemaType]):
    def __init__(
        self,
        model: Type[ModelType],
        schema: Type[FileSchemaType],
    ) -> None:
        self._model = model
        self._schema = schema

    @staticmethod
    async def get_ping_db(db: AsyncSession) -> float:
        start = time.time()
        statement = select(1)
        await db.execute(statement=statement)
        return time.time() - start

    @staticmethod
    async def save_file(
        user: User,
        path: str = '',
        file: UploadFile = File(),
    ) -> None:
        user_folder = os.path.join(DEFAULT_FOLDER, user.login)
        if path:
            user_folder = os.path.join(user_folder, path)
        folder = Path(user_folder)
        try:
            if not Path.exists(folder):
                Path(folder).mkdir(parents=True, exist_ok=True)
            file_size, max_size = 0, app_settings.max_file_size
            async with aiofiles.open(Path(folder, file.filename), 'wb') as f:
                while content := await file.read(1024):
                    file_size += len(content)
                    if file_size > max_size:
                        os.remove(Path(folder, file.filename))
                        raise HTTPException(
                            status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail=f'File exceeds maximum size of {max_size} '
                                   f'bytes'
                        )
                    await f.write(content)
        except Exception as error:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'File not saved: {error}'
            )
        finally:
            await file.close()

    @staticmethod
    async def get_folder_archive(
        user: User,
        path: str,
        compression_type: str,
    ) -> StreamingResponse:
        folder = os.path.join(DEFAULT_FOLDER, user.login, path)
        files = list(Path(folder).iterdir())
        zip_file = f'{str(datetime.now())}.{compression_type}'
        zip_io = BytesIO()
        with ZipFile(zip_io, mode='w', compression=ZIP_DEFLATED) as f:
            for file in files:
                _, file_name = os.path.split(file)
                f.write(file, file_name)
        return StreamingResponse(
            iter([zip_io.getvalue()]),
            media_type="application/x-zip-compressed",
            headers={'Content-Disposition': f'attachment filename={zip_file}'}
        )

    @staticmethod
    async def get_file_archive(
        path: str,
        compression_type: str,
    ):
        _, file_name = os.path.split(path)
        zip_file = f'{str(datetime.now())}.{compression_type}'
        zip_io = BytesIO()
        with ZipFile(zip_io, mode='w', compression=ZIP_DEFLATED) as f:
            f.write(path, file_name)
        return StreamingResponse(
            iter([zip_io.getvalue()]),
            media_type='application/x-zip-compressed',
            headers={'Content-Disposition': f'attachment; filename={zip_file}'}
        )

    async def create_in_db(
        self,
        size: int,
        db: AsyncSession,
        user: User,
        path: str,
        file: UploadFile = File(),
    ) -> ModelType:
        db_obj = self._model(
            name=file.filename,
            path=path,
            size=size,
            is_downloadable=True,
            author=user.id
        )
        db.add(db_obj)
        try:
            await db.commit()
            await db.refresh(db_obj)
        except exc.SQLAlchemyError as error:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error
            )
        return db_obj

    async def upload_file(
        self,
        db: AsyncSession,
        user: User,
        path: str,
        file: UploadFile = File(),
    ) -> dict:
        file_size = len(await file.read())
        await self.save_file(
            user=user,
            path=path,
            file=file
        )
        db_obj = await self.create_in_db(
            db=db,
            user=user,
            path=path,
            file=file,
            size=file_size
        )
        return jsonable_encoder(db_obj)

    async def get_files_list(
        self,
        db: AsyncSession,
        user: User,
        skip=0,
        limit=100,
    ) -> list[ModelType]:
        statement = select(self._model).where(
            self._model.author == user.id
        ).offset(skip).limit(limit)
        result = await db.execute(statement=statement)
        return result.scalars().all()

    async def get_file_by_path(
        self,
        db: AsyncSession,
        user: User,
        path: Path | str,
        compression_type: str,
    ) -> File:
        file_path = Path(path)
        statement = select(self._model).where(
            and_(
                self._model.path == str(file_path.parent),
                self._model.name == file_path.name,
                self._model.author == user.id
            )
        )
        result = await db.scalar(statement=statement)
        if not result:
            return None
        file_name = os.path.join(
            DEFAULT_FOLDER,
            user.login,
            result.path,
            result.name
        )
        if os.path.exists(file_name) and os.path.isfile(file_name):
            if compression_type:
                return await self.get_file_archive(
                    result.name,
                    compression_type
                )
            return FileResponse(path=file_name)
        return None

    async def get_file_by_id(
        self,
        db: AsyncSession,
        user: User,
        id: str,
        compression_type: str,
    ) -> File:
        statement = select(self._model).where(self._model.id == id)
        result = await db.scalar(statement=statement)
        if not result:
            return None
        path = os.path.join(DEFAULT_FOLDER, user.login, result.path)
        file_name = os.path.join(path, result.name)
        if os.path.exists(file_name) and os.path.isfile(file_name):
            if compression_type:
                return await self.get_file_archive(
                    file_name,
                    compression_type
                )
            return FileResponse(path=file_name)
        return None

    async def download_file(
        self,
        db: AsyncSession,
        user: User,
        path_or_id: str,
        compression_type: str,
    ) -> File:
        if validate_uuid(path_or_id):
            return await self.get_file_by_id(
                db=db,
                user=user,
                id=path_or_id,
                compression_type=compression_type
            )
        return await self.get_file_by_path(
            db=db,
            user=user,
            path=Path(path_or_id),
            compression_type=compression_type
        )

    async def search(
        self,
        db: AsyncSession,
        user: User,
        path,
        ext,
        order,
        limit,
    ) -> list[dict[str, Any]]:
        statement = select(self._model).where(self._model.author == user.id)
        if path:
            statement = statement.where(self._model.path == path)
        if ext:
            statement = statement.where(self._model.name.ilike(f'%{ext}%'))
        if limit:
            statement = statement.limit(limit)
        statement = statement.order_by(order)
        results = await db.execute(statement=statement)
        files = results.scalars().all()
        return [self._schema.from_orm(file).dict() for file in files]
