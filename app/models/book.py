from app.configs.database import db
from uuid import uuid4
from dataclasses import dataclass
from sqlalchemy import Column, String
from sqlalchemy.orm import validates
from sqlalchemy.dialects.postgresql import UUID


@dataclass
class Book(db.Model):

    title: str
    synopsis: str
    edition: str
    ISBN: str
    publisher: str
    cover_img: str

    __tablename__ = "books"

    book_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(200), nullable=False)
    synopsis = Column(String)
    edition = Column(String(50))
    ISBN = Column(String(13), unique=True)
    publisher = Column(String(150))
    cover_img = Column(String)

    @validates("ISBN")
    def validate_ISB(self, key, val):
        if len(val) != 13:
            raise AttributeError
        return val
