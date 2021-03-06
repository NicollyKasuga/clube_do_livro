from dataclasses import asdict
from http import HTTPStatus
from flask import request, current_app, jsonify
from regex import E, R
from requests import session
from app.models import Reader
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, decode_token
from sqlalchemy.orm import Session
from app.configs.database import db
from app.models import Reader
from datetime import timedelta
from app.models.email_model import Email
from app.models import Review


def create_reader():

    reader_data = request.get_json()

    found_reader = Reader.query.filter(Reader.email == reader_data["email"]).first()

    if found_reader:
        return jsonify({"msg": "Email already exists"}), 409

    new_reader = Reader(**reader_data)

    token = create_access_token(new_reader)

    send_user_email = Email(new_reader.email, token)

    send_user_email.send_email()

    return {"msg": "Confirmation email sent", "token": token}, 200


def register_confirmed_reader(token):


    reader = decode_token(token)["sub"]

    found_reader = Reader.query.filter(Reader.email == reader["email"]).first()

    if found_reader:
        return jsonify({"msg": "Email already exists"}), 409

    new_reader = Reader(**reader)

    current_app.db.session.add(new_reader)
    current_app.db.session.commit()

    return jsonify(new_reader), 201


def signin():
    reader_data = request.get_json()

    found_reader = Reader.query.filter(Reader.email == reader_data["email"]).first()


    if not found_reader:
        return jsonify({"msg": "email not registered"}), 404

    if found_reader.check_password(reader_data["password"]):
        token = create_access_token(found_reader, expires_delta=timedelta(hours=24))
        return jsonify({"access_token": token}), 200

    return jsonify({"msg": "reader not found"}), 404


@jwt_required()
def get_reader():
    token = request.headers["Authorization"].split()[1]
    reader = decode_token(token)["sub"]

    return (
        jsonify(
            {
                "reader_id": reader["reader_id"],
                "name": reader["name"],
                "email": reader["email"],
            }
        ),
        200,
    )


@jwt_required()
def get_all_readers():
    session: Session = db.session
    readers = session.query(Reader).all()

    return jsonify(readers), 200


@jwt_required()
def update_reader():
    data = request.get_json()
    token = request.headers["Authorization"].split()[1]
    email = decode_token(token)["sub"]["email"]

    reader = Reader.query.filter_by(email=email).first()

    for key, value in data.items():
        setattr(reader, key, value)

    current_app.db.session.add(reader)
    current_app.db.session.commit()

    return jsonify({"name": reader.name, "email": reader.email}), 200


@jwt_required()
def delete_reader():
    token = request.headers["Authorization"].split()[1]
    email = decode_token(token)["sub"]["email"]
    reader = Reader.query.filter_by(email=email).first()

    current_app.db.session.delete(reader)
    current_app.db.session.commit()

    return jsonify({"msg": f"Reader {reader.name} has been deleted"}), 200


def get_reviews_by_reader():
    session: Session = db.session

    token = request.headers["Authorization"].split()[1]
    reader_id = decode_token(token)["sub"]["reader_id"]

    book_reviews = session.query(Review).filter_by(reader_id=reader_id).all()

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
