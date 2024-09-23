from src.core.database import db

class Member(db.Model):
    """Modelo de miembro del equipo"""
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    health_insurance = db.Column(db.String(32), nullable=False)
    health_insurance_number = db.Column(db.String(32), nullable=False)
    condition = db.Column(db.Enum('Voluntario', 'Personal Rentado'), nullable=False)
    active = db.Column(db.Boolean, default=True)

    profession_id = db.Column(db.Integer, db.ForeignKey('professions.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)

    def __repr__(self):
        return f'Member {self.id}'
    