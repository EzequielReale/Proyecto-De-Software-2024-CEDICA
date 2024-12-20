from datetime import datetime

from src.core.database import db
from src.core.people.person import Person


class RiderMember(db.Model):
    __tablename__ = "rider_member"

    rider_id = db.Column(db.Integer, db.ForeignKey("riders.id"), primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Member(Person):
    """Modelo de miembro del equipo"""

    __tablename__ = "members"

    __mapper_args__ = {"polymorphic_identity": "member"}  # Identificador de la subclase

    id = db.Column(db.Integer, db.ForeignKey("persons.id"), primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    condition = db.Column(
        db.Enum("Voluntario", "Personal Rentado", name="condition_types"),
        nullable=False,
    )
    active = db.Column(db.Boolean, default=True)

    # carrera universitaria
    profession_id = db.Column(db.Integer, db.ForeignKey("professions.id"), nullable=True)
    profession = db.relationship("Profession", backref="members", lazy=True)

    # puesto laboral
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    job = db.relationship("Job", backref="members", lazy=True)

    # j/a asignados
    riders = db.relationship("Rider", secondary="rider_member", back_populates="members")

    # usuario vinculado
    user = db.relationship("User", secondary="user_member", back_populates="member", uselist=False, lazy=True)

    # cobros
    payments = db.relationship("PagoJineteAmazona", back_populates="receptor",  cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f"Member {self.id}"
    

class UserMember(db.Model):
    __tablename__ = "user_member"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'))
    member_id = db.Column(db.Integer, db.ForeignKey("members.id", ondelete='CASCADE'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Rider(Person):
    """Modelo de miembro del equipo"""

    __tablename__ = "riders"

    __mapper_args__ = {"polymorphic_identity": "rider"}  # Identificador de la subclase

    # personal data
    id = db.Column(db.Integer, db.ForeignKey("persons.id", ondelete='CASCADE'), primary_key=True)
    birth_date = db.Column(db.Date, nullable=False)
    grant_percentage = db.Column(db.Float, default=0.0, nullable=True)
    family_allowance = db.Column(
        db.Enum(
            "Asignación universal por hijo",
            "Asignación universal por hijo con discapacidad",
            "Asignación por ayuda escolar anual",
            name="family_allowances",
        ),
        nullable=True,
    )
    pension_benefit = db.Column(db.Enum("Nacional", "Provincial", name="pension_benefits"), nullable=True)
    has_guardianship = db.Column(db.Boolean, default=False)

    disability_id = db.Column(db.Integer, db.ForeignKey("disability_diagnoses.id", ondelete='SET NULL'), nullable=True)
    disability = db.relationship("DisabilityDiagnosis", backref="riders", lazy=True)
    city_of_birth_id = db.Column(db.Integer, db.ForeignKey("localities.id", ondelete='CASCADE'), nullable=False)
    city_of_birth = db.relationship("Locality", foreign_keys=[city_of_birth_id], lazy=True)

    # profesionales que lo atienden
    members = db.relationship("Member", secondary="rider_member", back_populates="riders")

    # escuela
    school = db.relationship("School", backref="rider", uselist=False, cascade="all, delete-orphan", lazy=True, overlaps="rider_school,school")

    # tutores
    tutor_1_id = db.Column(db.Integer, db.ForeignKey("tutors.id", ondelete='SET NULL'), nullable=True)
    tutor_1 = db.relationship("Tutor", backref="rider_tutor_1", lazy=True, foreign_keys=[tutor_1_id])
    tutor_2_id = db.Column(db.Integer, db.ForeignKey("tutors.id", ondelete='SET NULL'), nullable=True)
    tutor_2 = db.relationship("Tutor", backref="rider_tutor_2", lazy=True, foreign_keys=[tutor_2_id])

    # trabajo
    job_proposal = db.relationship("JobProposal", uselist=False, backref="rider", cascade="all, delete-orphan", lazy=True)

    # pagos
    payments = db.relationship("PagoJineteAmazona", back_populates="jinete_amazona", cascade='all, delete-orphan', lazy=True)

    
    def __repr__(self):
        return f"Rider {self.id}"
