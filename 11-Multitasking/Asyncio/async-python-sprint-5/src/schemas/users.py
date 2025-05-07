from datetime import datetime
from typing import Optional

from pydantic import UUID1, UUID4, BaseModel, Field


class UserBase(BaseModel):
    login: str

    class Config:
        orm_model = True


class UserCreate(UserBase):
    password: str


class DBUser(UserBase):
    hashed_password: str


class UserID(UserBase):
    id: UUID1


class UserToken(BaseModel):
    token: UUID4 = Field(..., alias='access_token')
    token_type: Optional[str] = 'Bearer'
    expires: datetime

    class Config:
        orm_model = True
        allow_population_by_field_name = True
