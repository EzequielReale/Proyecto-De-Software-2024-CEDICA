from datetime import datetime
from sqlalchemy import Enum as SQLAlchemyEnum
from src.core.content_admin.article_status_enum import ArticleStatus
from src.core.database import db

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(SQLAlchemyEnum(ArticleStatus), nullable=False, default=ArticleStatus.BORRADOR)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime, nullable=True)

    author = db.relationship('User', back_populates='articles')