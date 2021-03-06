from flask import Blueprint

from app.controllers.books_controller import (
    create_book,
    get_book,
    patch_book,
    get_book_by_isbn,
    create_review,
    update_review,
    get_reviews_by_book,
)

bp_books = Blueprint("bp_books", __name__, url_prefix="/books")

bp_books.post("")(create_book)
bp_books.get("")(get_book)
bp_books.get("/<isbn>")(get_book_by_isbn)
bp_books.patch("/<isbn>")(patch_book)
bp_books.get("/<isbn>/reviews")(get_reviews_by_book)
bp_books.post("/review")(create_review)
bp_books.patch("/review/<review_id>")(update_review)
