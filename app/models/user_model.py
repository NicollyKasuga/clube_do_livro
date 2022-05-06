from app.configs.database import db

from sqlalchemy import Column, Integer, String
from dataclasses import dataclass

from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class UserModel(db.Model):
    id: int
    name: str
    email: str
    avatar: str
    password_hash: str

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    avatar = Column(String(511))
    password_hash = Column(String(511))

    @property
    def password(self):
        raise AttributeError("Password cannot be acessed")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
