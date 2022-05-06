from http import HTTPStatus
from operator import and_
from flask import current_app, jsonify, request, url_for
import psycopg2
from app.models import Author, Book, Review, Genre
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Session
from app.configs.database import db
from werkzeug.exceptions import NotFound
from psycopg2.errors import InvalidTextRepresentation
from flask_jwt_extended import jwt_required
from app.services.books_services import define_authors_or_genres
from flask_jwt_extended import decode_token


@jwt_required()
def create_book():
    session: Session = db.session
    data = request.get_json()

    authors = []
    genres = []

    if data.get("authors"):
        authors = data.pop("authors")
        authors = define_authors_or_genres(authors, session, Author)

    if data.get("genres"):
        genres = data.pop("genres")
        genres = define_authors_or_genres(genres, session, Genre)

    try:
        new_book = Book(**data)
    except AttributeError:
        return {"msg": "Invalid ISBN"}, HTTPStatus.BAD_REQUEST
    except TypeError:
        return {"msg": "Wrong fields added"}, HTTPStatus.BAD_REQUEST

    if authors:
        for author in authors:
            new_book.authors.append(author)

    if genres:
        for genre in genres:
            new_book.genres.append(genre)

    try:
        session.add(new_book)
        session.commit()
    except IntegrityError as e:
        if isinstance(e.orig, psycopg2.errors.UniqueViolation):
            return {"msg": "ISBN already registred"}, HTTPStatus.CONFLICT
        else:
            return {"msg": "Missing fields"}, HTTPStatus.BAD_REQUEST
    return (
        jsonify(
            {
                "book_id": new_book.book_id,
                "title": new_book.title,
                "synopsis": new_book.synopsis,
                "edition": new_book.edition,
                "ISBN": new_book.ISBN,
                "publisher": new_book.publisher,
                "cover_img": new_book.cover_img,
                "reviews": url_for(".get_reviews_by_book", isbn=new_book.ISBN),
                "authors": [author.name for author in new_book.authors],
                "genres": [genre.name for genre in new_book.genres],
            }
        ),
        HTTPStatus.CREATED,
    )


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
            "reviews": url_for(".get_reviews_by_book", isbn=book.ISBN),
            "authors": [author.name for author in book.authors],
            "genres": [genre.name for genre in book.genres],
        }
        for book in books
    ]
    return {"data": serializer}, HTTPStatus.OK


@jwt_required()
def patch_book(isbn):
    session: Session = db.session
    data = request.get_json()
    book = Book.query.filter_by(ISBN=isbn).first()

    authors = []
    genres = []

    if data.get("authors"):
        authors = data.pop("authors")
        authors = define_authors_or_genres(authors, session, Author)

    if data.get("genres"):
        genres = data.pop("genres")
        genres = define_authors_or_genres(genres, session, Genre)

    if not book:
        return {"msg": "Livro não encontrado"}

    for key, val in data.items():
        setattr(book, key, val)

    if authors:
        for author in authors:
            book.authors.append(author)

    if genres:
        for genre in genres:
            book.genres.append(genre)

    current_app.db.session.add(book)
    current_app.db.session.commit()
    return (
        jsonify(
            {
                "book_id": book.book_id,
                "title": book.title,
                "synopsis": book.synopsis,
                "edition": book.edition,
                "ISBN": book.ISBN,
                "publisher": book.publisher,
                "cover_img": book.cover_img,
                "reviews": url_for(".get_reviews_by_book", isbn=book.ISBN),
                "authors": [author.name for author in book.authors],
                "genres": [genre.name for genre in book.genres],
            }
        ),
        HTTPStatus.OK,
    )


def get_book_by_isbn(isbn):
    book = Book.query.filter_by(ISBN=isbn).first()
    if not book:
        return {"msg": "Livro não encontrado"}

    return (
        jsonify(
            {
                "book_id": book.book_id,
                "title": book.title,
                "synopsis": book.synopsis,
                "edition": book.edition,
                "ISBN": book.ISBN,
                "publisher": book.publisher,
                "cover_img": book.cover_img,
                "reviews": url_for(".get_reviews_by_book", isbn=book.ISBN),
                "authors": [author.name for author in book.authors],
                "genres": [genre.name for genre in book.genres],
            }
        ),
        HTTPStatus.OK,
    )


def get_reviews_by_book(isbn: str):
    session: Session = db.session

    book = session.query(Book).filter_by(ISBN=isbn).first()

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
                for review in book.reviews
            ]
        ),
        HTTPStatus.OK,
    )


@jwt_required()
def create_review():
    session: Session = db.session
    data = request.get_json()

    token = request.headers["Authorization"].split()[1]
    reader_id = decode_token(token)["sub"]["reader_id"]

    review_already_exists = (
        session.query(Review)
        .filter(and_(Review.book_id == data["book_id"], Review.reader_id == reader_id))
        .first()
    )

    if review_already_exists:
        return {
            "msg": "Reader already have a review for this book"
        }, HTTPStatus.CONFLICT

    data["reader_id"] = reader_id

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


@jwt_required()
def update_review(review_id: str):
    session: Session = db.session
    data: dict = request.get_json()

    token = request.headers["Authorization"].split()[1]
    reader_id = decode_token(token)["sub"]["reader_id"]

    try:
        found_review = (
            session.query(Review).filter_by(review_id=review_id).first_or_404()
        )
    except NotFound:
        return {"msg": "Review not found"}, HTTPStatus.NOT_FOUND
    except DataError as e:
        if type(e.orig) == InvalidTextRepresentation:
            return {"msg": "Review id is not in uuid4 format"}, HTTPStatus.BAD_REQUEST

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
