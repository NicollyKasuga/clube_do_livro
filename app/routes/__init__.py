# import blueprints
from app.routes.readers_route import bp_readers
from app.routes.books_route import bp_books
from flask import Flask
from flask import Blueprint

bp_api = Blueprint("bp_api", __name__, url_prefix="/api")


def init_app(app: Flask):
    # register blueprints
    
    app.register_blueprint(bp_api)
    app.register_blueprint(bp_readers)
    app.register_blueprint(bp_books)
