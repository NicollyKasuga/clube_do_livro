from hashlib import new
from http import HTTPStatus
from http.client import OK
from operator import and_
from flask import current_app, jsonify, request
import psycopg2
from app.models import Author, Book, Review
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.services.books_services import define_authors_or_genres
from app.configs.database import db


def create_book():
    session: Session = db.session
    data = request.get_json()

    try:
        new_book = Book(**data)
    except AttributeError:
        return {"msg": "Invalid ISBN"}, HTTPStatus.BAD_REQUEST
    except TypeError:
        return {"msg": "Wrong fields added"}, HTTPStatus.BAD_REQUEST

    try:
        session.add(new_book)
        session.commit()
    except IntegrityError as e:
        if isinstance(e.orig, psycopg2.errors.UniqueViolation):
            return {"msg": "ISBN already registred"}, HTTPStatus.CONFLICT
        else:
            return {"msg": "Missing fields"}, HTTPStatus.BAD_REQUEST
    return jsonify(new_book), HTTPStatus.CREATED


def get_book():
    books = Book.query.all()

    serializer = [
        {
            "book_id": book.book_id,
            "title": book.title,
            "synopsis": book.synopsis,
            "edition": book.edition,
            "ISBN": book.ISBN,
            "publisher": book.publisher,
            "cover_img": book.cover_img,
        }
        for book in books
    ]
    return {"data": serializer}, HTTPStatus.OK


def patch_book(isbn):
    data = request.get_json()
    book = Book.query.filter_by(ISBN=isbn).first()
    if not book:
        return {"msg": "Livro não encontrado"}
    for key, val in data.items():
        setattr(book, key, val)

    current_app.db.session.add(book)
    current_app.db.session.commit()
    return jsonify(book), HTTPStatus.OK


def get_book_by_isbn(isbn):
    book = Book.query.filter_by(ISBN=isbn).first()
    if not book:
        return {"msg": "Livro não encontrado"}
    return jsonify(book), HTTPStatus.OK


def create_review():
    session: Session = db.session
    data = request.get_json()

    review_already_exists = (
        session.query(Review)
        .filter(
            and_(
                Review.book_id == data["book_id"], Review.reader_id == data["reader_id"]
            )
        )
        .first()
    )

    if review_already_exists:
        return {
            "msg": "Reader already have a review for this book"
        }, HTTPStatus.CONFLICT

    new_review = Review(**data)

    session.add(new_review)
    session.commit()

    return (
        jsonify(
            {
                "review_id": new_review.review_id,
                "book_id": new_review.book_id,
                "reader_id": new_review.reader_id,
                "review": new_review.review,
                "rating": str(new_review.rating),
            }
        ),
        HTTPStatus.OK,
    )
