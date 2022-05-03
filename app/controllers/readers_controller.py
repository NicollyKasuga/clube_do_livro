from flask import request, current_app, jsonify
from regex import E
from requests import session
from app.models import Reader
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, decode_token
from app.models.email_model import Email


def create_reader():
        
    reader_data = request.get_json()

    found_reader = Reader.query.filter(Reader.email == reader_data["email"]).first()

    if found_reader:
        return jsonify({"msg": "Email already exists"}), 409
    print(found_reader)

    new_reader = Reader(**reader_data)

    token = create_access_token(new_reader)

    send_user_email = Email(new_reader.email, token)

    send_user_email.send_email()

    return {"msg": "Confirmation email sent",
            "token": token}, 200

def register_confirmed_reader(token):

    print(token)

    reader = decode_token(token)['sub']

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
    print(reader)

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
