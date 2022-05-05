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
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import DataError
from psycopg2.errors import InvalidTextRepresentation


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


def get_reviews_by_book(book_id: str):
    session: Session = db.session

    book_reviews = session.query(Review).filter_by(book_id=book_id).all()

    return (
        jsonify(
            [
                {
                    "review_id": review.review_id,
                    "book_id": review.book_id,
                    "reader_id": review.reader_id,
                    "review": review.review,
                    "rating": str(review.rating),
                }
                for review in book_reviews
            ]
        ),
        HTTPStatus.OK,
    )


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


def update_review(review_id: str):
    session: Session = db.session
    data: dict = request.get_json()

    try:
        found_review = (
            session.query(Review).filter_by(review_id=review_id).first_or_404()
        )
    except NotFound:
        return {"msg": "Review not found"}, HTTPStatus.NOT_FOUND
    except DataError as e:
        if type(e.orig) == InvalidTextRepresentation:
            return {"msg": "Review id is not in uuid4 format"}, HTTPStatus.BAD_REQUEST

    reader_id = data.pop("reader_id")

    reader_is_review_owner = found_review.reader_id == reader_id

    if not reader_is_review_owner:
        return {
            "msg": "This reader is not owner of the review"
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    for key, value in data.items():
        setattr(found_review, key, value)

    session.commit()

    return (
        jsonify(
            {
                "review_id": found_review.review_id,
                "review": found_review.review,
                "rating": str(found_review.rating),
            }
        ),
        HTTPStatus.OK,
    )
