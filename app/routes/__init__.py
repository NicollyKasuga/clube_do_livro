# import blueprints

from flask import Flask
from flask import Blueprint
from app.routes.upload_images import bp_upload_images

bp_api = Blueprint("bp_api", __name__, url_prefix="/api")


def init_app(app: Flask):
    # register blueprints
    app.register_blueprint(bp_api)
    app.register_blueprint(bp_upload_images)
