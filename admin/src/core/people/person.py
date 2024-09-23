from datetime import datetime
from src.core.database import db

class Person(db.Model):
    """Modelo de persona generica"""
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    dni = db.Column(db.String(16), nullable=False)
    phone = db.Column(db.String(32), nullable=False)
    emergency_phone = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    
    province_id = db.Column(db.Integer, db.ForeignKey('provinces.id'), nullable=False)
    locality_id = db.Column(db.Integer, db.ForeignKey('localities.id'), nullable=False)

    created_at = db.Column(db.DateTime, default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return f'Person {self.id}'
    