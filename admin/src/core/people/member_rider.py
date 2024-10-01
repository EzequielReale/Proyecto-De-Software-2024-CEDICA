from src.core.database import db
from src.core.people.person import Person

class RiderMember(db.Model):
    __tablename__ = 'rider_member'
    
    rider_id = db.Column(db.Integer, db.ForeignKey('riders.id'), primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), primary_key=True)

class Member(Person):
    """Modelo de miembro del equipo"""
    __tablename__ = 'members'
    
    __mapper_args__ = {
        'polymorphic_identity': 'member'  # Identificador de la subclase
    }

    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    health_insurance = db.Column(db.String(32), nullable=False)
    health_insurance_number = db.Column(db.String(32), nullable=False)
    condition = db.Column(db.Enum('Voluntario', 'Personal Rentado', name='condition_types'), nullable=False)
    active = db.Column(db.Boolean, default=True)

    profession_id = db.Column(db.Integer, db.ForeignKey('professions.id'), nullable=True)
    profession = db.relationship('Profession', backref='members', lazy=True)    
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    job = db.relationship('Job', backref='members', lazy=True)
    riders = db.relationship('Rider', secondary='rider_member', back_populates='members')

    def __repr__(self):
        return f'Member {self.id}'
    
class Rider(Person):
    """Modelo de miembro del equipo"""
    __tablename__ = 'riders'
    
    __mapper_args__ = {
        'polymorphic_identity': 'rider'  # Identificador de la subclase
    }

    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    birth_date = db.Column(db.Date, nullable=False)
    grant_owner = db.Column(db.Boolean, default=False)
    grant_percentage = db.Column(db.Float, default=0.0)

    city_of_birth = db.Column(db.Integer, db.ForeignKey('localities.id'), nullable=False)
    city_of_birth = db.relationship('Locality', back_populates='riders', lazy=True, overlaps="locality,persons")
    members = db.relationship('Member', secondary='rider_member', back_populates='riders')

    def __repr__(self):
        return f'Rider {self.id}'
    