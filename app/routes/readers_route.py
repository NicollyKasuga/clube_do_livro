from flask import Blueprint

from app.controllers.readers_controller import (
    create_reader,
    signin,
    get_reader,
    update_reader,
    delete_reader,
    register_confirmed_reader
)

bp_readers = Blueprint("bp_readers", __name__, url_prefix="/api")

bp_readers.post("/cadastro")(create_reader)
bp_readers.post("/entrar")(signin)
bp_readers.post("/register_reader")(register_confirmed_reader)
bp_readers.get("")(get_reader)
bp_readers.put("")(update_reader)
bp_readers.delete("")(delete_reader)
