import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from db.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid1)
    login = Column(String(75), unique=True, index=True)
    hashed_password = Column(String())
    token = relationship(
        'Token',
        back_populates="user",
        passive_deletes=True
    )
    active = Column(
        Boolean(),
        default=True,
        nullable=False,
    )
    file = relationship(
        'File',
        back_populates="user",
        passive_deletes=True
    )


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid1)
    token = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    user = relationship('User', back_populates='token')
    user_id = Column(
        UUIDType,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    expires = Column(DateTime())
