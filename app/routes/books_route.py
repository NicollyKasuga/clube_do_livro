from flask import Blueprint

from app.controllers.books_controller import (
    create_book,
    get_book,
    patch_book,
)

bp_books = Blueprint("bp_books", __name__, url_prefix="/api")

bp_books.post("/livros")(create_book)
bp_books.get("/livros")(get_book)
bp_books.get("/livros/<id>")(get_book)
bp_books.patch("/livros/<isbn>")(patch_book)
