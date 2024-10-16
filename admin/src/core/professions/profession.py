from src.core.database import db

class Profession(db.Model):
    """Modelo de profesion"""
    __tablename__ = 'professions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    

    def __repr__(self):
        return f'Profession {self.id}'
    
    def __str__(self):
        return f'{self.name}'
    