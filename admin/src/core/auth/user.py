from datetime import datetime
from src.core.database import db

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True, unique=True)

    
    created_at = db.Column(db.DateTime,default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return f'{self.name}'



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    
    role = db.relationship('Role', backref='users')


    created_at = db.Column(db.DateTime,default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return f'User {self.id}'