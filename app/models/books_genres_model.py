from uuid import uuid4
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.configs.database import db


class BookGenre(db.Model):

    __tablename__ = "books_genres"

    books_genres_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    genre_id = Column(UUID(as_uuid=True), ForeignKey("genres.genre_id"), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.book_id"), nullable=False)
