from dataclasses import dataclass
from uuid import uuid4
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from app.configs.database import db


@dataclass
class Room(db.Model):

    room_id: str

    __tablename__ = "rooms"

    room_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
