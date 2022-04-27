# import blueprints

from flask import Flask
from flask import Blueprint

bp_api = Blueprint("bp_api", __name__, url_prefix="/api")


def init_app(app: Flask):
    # register blueprints
    app.register_blueprint(bp_api)
