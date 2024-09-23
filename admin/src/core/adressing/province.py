from src.core.database import db

class Province(db.Model):
    """Modelo de provincia"""
    __tablename__ = 'provinces'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)


    def __repr__(self):
        return f'Province {self.id}'

    def __str__(self):
        return f'{self.name}'
    