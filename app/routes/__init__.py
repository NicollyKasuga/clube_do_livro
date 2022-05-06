# import blueprints
from app.routes.readers_route import bp_readers
from app.routes.books_route import bp_books
from app.routes.chat_route import bp_chat

from flask import Flask
from flask import Blueprint
from app.routes.upload_images import bp_upload_images

bp_api = Blueprint("bp_api", __name__, url_prefix="/api")


def init_app(app: Flask):
    # register blueprints
    bp_api.register_blueprint(bp_readers)
    bp_api.register_blueprint(bp_chat)
    bp_api.register_blueprint(bp_books)
    app.register_blueprint(bp_api)
    app.register_blueprint(bp_upload_images)
