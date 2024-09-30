from src.core.database import db

class Activity(db.Model):
    """Modelo para las actividades asignadas a los caballos"""
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'Activity {self.id} - {self.name}'
    
    def __str__(self):
        return f'{self.name}'