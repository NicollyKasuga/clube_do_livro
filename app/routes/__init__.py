# import blueprints
from app.routes.user_route import bp_users

from flask import Flask
from flask import Blueprint

bp_api = Blueprint("bp_api", __name__, url_prefix="/api")


def init_app(app: Flask):
    # register blueprints
    app.register_blueprint(bp_api)
    app.register_blueprint(bp_users)
