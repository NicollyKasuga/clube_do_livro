from typing import Collection
from app.configs.database import db
from uuid import uuid4
from dataclasses import dataclass
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

class Readers(db.Model):

    name: str
    email: str
    avatar: str

    __tablename__ = "readers"

    reader_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False)
    email = Column(String(70), nullable=False, unique=True)
    avatar = Column(String)
    password_hash = Column(String)