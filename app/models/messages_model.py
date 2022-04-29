from dataclasses import dataclass
from datetime import datetime
from email.policy import default
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.configs.database import db

@dataclass
class Messages(db.Model):

    message_text: str
    created_at: datetime
    
    __tablename__ = 'messages'

    message_id = Column(UUID(as_uuid=True), primary_key = True, default=uuid4)
    sender_id = Column(UUID , ForeignKey("readers.reader_id"), nullable=False)
    reciever_id = Column(UUID , ForeignKey("readers.reader_id"), nullable=False)
    message_text = Column(String(600))
    created_at = Column(DateTime)