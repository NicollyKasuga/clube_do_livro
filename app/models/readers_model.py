from app.configs.database import db
from uuid import uuid4
from dataclasses import dataclass

# from typing import uuid4 as UUID4
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class Reader(db.Model):

    reader_id: str
    name: str
    email: str
    avatar: str
    password_hash: str

    __tablename__ = "readers"

    reader_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False)
    email = Column(String(70), nullable=False, unique=True)
    avatar = Column(String)
    password_hash = Column(String)

    @property
    def password(self):
        raise AttributeError("Password cannot be accessed")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
