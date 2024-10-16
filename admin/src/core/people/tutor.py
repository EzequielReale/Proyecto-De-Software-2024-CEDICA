from src.core.database import db
from sqlalchemy import Enum

class Tutor(db.Model):
    """Modelo de padre o tutor de un estudiante"""
    __tablename__ = "tutors"

    id = db.Column(db.Integer, primary_key=True)

    relationship = db.Column(db.Enum("Padre", "Madre", "Tutor", name="relationships"), nullable=False)
    # Tiene campos repetidos con persona. Pero considero que no vale la pena mantener una herencia para manejar una tabla opcional
    name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    dni = db.Column(db.String(9), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    education_level = db.Column(Enum("Primario", "Secundario", "Terciario", "Universitario", name="education_levels"), nullable=False)
    job = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"Parent {self.id}"