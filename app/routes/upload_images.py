from flask import Blueprint
from app.controllers.upload_images_controller import upload_images

bp_upload_images = Blueprint("bp_upload_images", __name__, url_prefix="/api")

bp_upload_images.post("/upload")(upload_images)