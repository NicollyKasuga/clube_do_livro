from uuid import uuid4
from dataclasses import dataclass
from sqlalchemy import Column, ForeignKey, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
from app.configs.database import db


@dataclass
class ReaderBook(db.Model):

    review: str
    rating: float

    __tablename__ = "reviews"

    reader_book_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    reader_id = Column(UUID, ForeignKey("readers.reader_id"), nullable=False)
    book_id = Column(UUID, ForeignKey("books.book_id"), nullable=False)
    review = Column(String(200))
    rating = Column(Numeric)
