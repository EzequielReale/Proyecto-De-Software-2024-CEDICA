from datetime import datetime
from src.core.database import db


class Person(db.Model):
    """Modelo de persona generica con herencia de SQLAlchemy -joined table inheritance-"""

    __tablename__ = "persons"

    __mapper_args__ = {
        "polymorphic_identity": "person",  # Identificador de la clase base
        "polymorphic_on": "type",  # Campo que define el tipo de subclase
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    dni = db.Column(db.String(16), nullable=False)
    phone = db.Column(db.String(32), nullable=False)
    emergency_phone = db.Column(db.String(32), nullable=False)
    street = db.Column(db.String(128), nullable=False)
    number = db.Column(db.String(8), nullable=False)
    floor = db.Column(db.String(8), nullable=True)
    department = db.Column(db.String(8), nullable=True)
    health_insurance = db.Column(db.String(32), nullable=False)
    health_insurance_number = db.Column(db.String(32), nullable=False)
    locality_id = db.Column(db.Integer, db.ForeignKey("localities.id"), nullable=False)
    locality = db.relationship(
        "Locality", back_populates="persons", lazy=True, overlaps="riders"
    )
    documents = db.relationship("PersonDocument", back_populates="person")
    type = db.Column(
        db.String(16)
    )  # Campo utilizado para la discriminación de la herencia

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"Person {self.id}"
