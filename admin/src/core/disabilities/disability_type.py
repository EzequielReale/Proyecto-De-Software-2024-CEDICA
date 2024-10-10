from src.core.database import db


class DisabilityType(db.Model):
    """Modelo de tipo de discapacidad"""

    __tablename__ = "disability_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    diagnoses = db.relationship("DisabilityDiagnosis", back_populates="type")

    def __repr__(self):
        return f"DisabilityType {self.id}"
