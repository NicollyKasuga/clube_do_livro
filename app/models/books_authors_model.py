from uuid import uuid4
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.configs.database import db


class BookAuthor(db.Model):

    __tablename__ = "books_authors"

    books_authors_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    author_id = Column(
        UUID(as_uuid=True), ForeignKey("authors.author_id"), nullable=False
    )
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.book_id"), nullable=False)
