from datetime import datetime
from src.core.database import db

class Issue(db.Model):
    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime,default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return f'Issue {self.id}'