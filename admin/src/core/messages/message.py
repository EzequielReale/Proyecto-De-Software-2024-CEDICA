from sqlalchemy import Enum as SQLAlchemyEnum
from datetime import datetime
from src.core.database import db
from src.core.messages.message_status_enum import MessageStatus

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    body_message = db.Column(db.String(400), nullable=False)

    state = db.Column(SQLAlchemyEnum(MessageStatus), nullable=False)
    comment = db.Column(db.String(400), nullable=True)
   

    created_at = db.Column(db.DateTime,default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate=datetime.now)
    closed_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'{self.name}, {self.email}, {self.body_message}, {self.state}, {self.comment}'