# Copyright (c) 2023 Artem Ustsov

from uuid import uuid4

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from db.db import Base


class Url(Base):
    __tablename__ = 'url'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    full_url = Column(String(255), nullable=False, unique=True, index=True)
    clicks = relationship("UrlClick", back_populates="url")
    is_active = Column(Boolean, nullable=False, default=True)
