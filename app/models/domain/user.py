import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.core.db import Base


class User(Base, AsyncAttrs):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gender = Column(String, nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phone = Column(String(32), nullable=False)
    email = Column(String(128), nullable=False)
    location = Column(String(128), nullable=False)
    photo_url = Column(Text, nullable=False)
