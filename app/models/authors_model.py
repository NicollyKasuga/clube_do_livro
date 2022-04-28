from uuid import uuid4
from dataclasses import dataclass
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.configs.database import db

@dataclass
class Author (db.Model):
    
    name: str

    __tablename__ = "authors"

    author_id = Column(UUID(as_uuid=True) ,primary_key = True, default=uuid4)
    name = Column(String(150), unique=True, nullable=False)
