from src.core.database import db

class Job(db.Model):
    """Modelo de trabajo en la institución"""
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    

    def __repr__(self):
        return f'Job {self.id}'
    
    def __str__(self):
        return f'{self.name}'
    