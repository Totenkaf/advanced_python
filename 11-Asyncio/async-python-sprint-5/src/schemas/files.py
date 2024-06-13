from datetime import datetime
from typing import Optional

from pydantic import UUID1, BaseModel


class FileBase(BaseModel):
    name: str


class FileCreate(FileBase):
    pass


class FileUpload(BaseModel):
    path: str


class FileInDB(FileBase):
    id: UUID1
    created_at: datetime
    path: Optional[str]
    size: int
    is_downloadable: bool

    class Config:
        orm_mode = True


class FilesList(BaseModel):
    account_id: UUID1
    files: list[FileInDB]


class FileSearchMatches(BaseModel):
    matches: list[FileInDB]
