from flask import Blueprint

from app.controllers import chat_controllers

# bp_chat = Blueprint("chat", __name__, url_prefix="/chat")
bp_chat = Blueprint("bp_chat", __name__, url_prefix="/chat")


bp_chat.post("/rooms")(chat_controllers.create_room)
bp_chat.post("/rooms/messages")(chat_controllers.send_message)
bp_chat.get("/rooms")(chat_controllers.get_room)
bp_chat.get("/rooms/messages")(chat_controllers.get_messages)
