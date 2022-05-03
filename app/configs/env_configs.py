from flask import Flask
from os import getenv
from dotenv import load_dotenv


def init_app(app: Flask):
    load_dotenv()

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False
    app.config["SECRET_KEY"] = getenv("JWT_SECRET_KEY")