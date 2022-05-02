from flask import Blueprint

from app.controllers.books_controller import (
    create_book,
    get_book,
    patch_book,
    get_book_by_isbn
)

bp_books = Blueprint("bp_books", __name__, url_prefix="/api")

bp_books.post("/livros")(create_book)
bp_books.get("/livros")(get_book)
bp_books.get("/livros/<isbn>")(get_book_by_isbn)
bp_books.patch("/livros/<isbn>")(patch_book)
