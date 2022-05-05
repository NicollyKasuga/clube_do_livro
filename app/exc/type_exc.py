from http import HTTPStatus


class TypeValueError(Exception):
    def __init__(self, message):
        self.message = {"msg": message}
        self.status_code = HTTPStatus.BAD_REQUEST
