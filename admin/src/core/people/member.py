from src.core.database import db
from src.core.people.person import Person

class Member(Person):
    """Modelo de miembro del equipo"""
    __tablename__ = 'members'
    
    __mapper_args__ = {
        'polymorphic_identity': 'member'  # Identificador de la subclase
    }

    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    health_insurance = db.Column(db.String(32), nullable=False)
    health_insurance_number = db.Column(db.String(32), nullable=False)
    condition = db.Column(db.Enum('Voluntario', 'Personal Rentado', name='condition_types'), nullable=False)
    active = db.Column(db.Boolean, default=True)

    profession_id = db.Column(db.Integer, db.ForeignKey('professions.id'), nullable=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)

    def __repr__(self):
        return f'Member {self.id}'
    