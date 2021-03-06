from http import HTTPStatus
from flask import jsonify, request
from app.models import Room, Messages
from sqlalchemy.orm import Session, Query
from sqlalchemy.sql import or_
from flask_sqlalchemy import BaseQuery
from datetime import datetime
from flask_jwt_extended import jwt_required

from app.configs.database import db


@jwt_required()
def create_room():
    session: Session = db.session
    first_reader_id = request.args.get("first_reader_id")
    second_reader_id = request.args.get("second_reader_id")

    data = {"first_reader_id": first_reader_id, "second_reader_id": second_reader_id}

    room = Room(**data)

    session.add(room)
    session.commit()

    return jsonify(room), HTTPStatus.CREATED


@jwt_required()
def get_room():
    session: Session = db.session
    first_reader_id = request.args.get("first_reader_id")
    second_reader_id = request.args.get("second_reader_id")

    first_query: Query = (
        session.query(Room.room_id)
        .select_from(Room)
        .where(
            or_(
                Room.first_reader_id == first_reader_id,
                Room.first_reader_id == second_reader_id,
            )
        )
    )

    second_query: Query = (
        session.query(Room.room_id)
        .select_from(Room)
        .where(
            or_(
                Room.second_reader_id == first_reader_id,
                Room.second_reader_id == second_reader_id,
            )
        )
    )

    print(first_query)

    room_query: Query = first_query.intersect(second_query)

    found_room = room_query.first()

    if found_room:
        return {"room_id": found_room[0]}, 200
    else:
        return {"room_id": found_room}, 200


@jwt_required()
def send_message():
    session: Session = db.session
    data = request.get_json()

    data["created_at"] = datetime.now()

    message = Messages(**data)
    message.created_at = datetime.now()

    session.add(message)
    session.commit()

    return jsonify(message), 200


@jwt_required()
def get_messages():
    session: Session = db.session
    room_id = request.args.get("room_id")

    messages = (
        session.query(Messages)
        .filter(Messages.room_id == room_id)
        .order_by(Messages.created_at)
        .all()
    )

    return jsonify(messages), 200
