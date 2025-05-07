import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from db.db import Base


class File(Base):
    __tablename__ = 'files'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid1)
    name = Column(String(50))
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    size = Column(Integer)
    path = Column(String(100))
    is_downloadable = Column(Boolean)
    author = Column(
        UUIDType,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    user = relationship('User', back_populates='file')
