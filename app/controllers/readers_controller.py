from flask import request, current_app, jsonify
from app.models import Reader
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, decode_token


def create_reader():
    try:
        reader_data = request.get_json()

        new_reader = Reader(**reader_data)

        current_app.db.session.add(new_reader)
        current_app.db.session.commit()

        response = jsonify(
            {
                "id": new_reader.reader_id,
                "name": new_reader.name,
                "email": new_reader.email,
            }
        )

        return response, 201
    except IntegrityError:
        return jsonify({"msg": "Email already exists"}), 409


def signin():
    reader_data = request.get_json()

    found_reader = Reader.query.filter(Reader.email == reader_data["email"]).first()

    print(found_reader)

    if not found_reader:
        return jsonify({"msg": "email not registered"}), 404

    if found_reader.check_password(reader_data["password"]):
        token = create_access_token(found_reader)
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
