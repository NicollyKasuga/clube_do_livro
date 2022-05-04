import os
from flask_jwt_extended import JWTManager


def init_app(app):
    app.config["SECRET_KEY"] = os.getenv("SECRET")
    JWTManager(app)
