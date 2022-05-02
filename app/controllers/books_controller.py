from http import HTTPStatus
from http.client import OK
from flask import current_app, jsonify, request
import psycopg2
from app.models.book import Book
from sqlalchemy.exc import IntegrityError

def create_book():
    data = request.get_json()

    try:
        new_book = Book(**data)
    except AttributeError:
        return {"msg": "Invalid ISBN"},HTTPStatus.BAD_REQUEST
    except TypeError:
        return {"msg": "Wrong fields added"}, HTTPStatus.BAD_REQUEST
    try:
        current_app.db.session.add(new_book)
        current_app.db.session.commit()
    except IntegrityError as e:
        if isinstance(e.orig, psycopg2.errors.UniqueViolation):
            return {"msg": "ISBN already registred"},HTTPStatus.CONFLICT
        else:
            return {"msg": "Missing fields"},HTTPStatus.BAD_REQUEST
    return jsonify(new_book), HTTPStatus.CREATED


def get_book():
    books = (Book.query.all())

    serializer = [{
    "book_id":book.book_id,
    "title": book.title,
    "synopsis": book.synopsis,
    "edition": book.edition,
    "ISBN": book.ISBN,
    "publisher": book.publisher,
    "cover_img": book.cover_img,
    } for book in books]
    return {"data": serializer},HTTPStatus.OK

def patch_book(isbn):
    data = request.get_json()
    book = Book.query.filter_by(ISBN=isbn).first()
    if not book:
        return {"msg": "Livro não encontrado"}
    for key, val in data.items():
        setattr(book, key, val)
    
    current_app.db.session.add(book)
    current_app.db.session.commit()
    return jsonify(book),HTTPStatus.OK
def get_book_by_isbn(isbn):
    book = Book.query.filter_by(ISBN=isbn).first()
    if not book:
        return {"msg": "Livro não encontrado"}
    return jsonify(book),HTTPStatus.OK