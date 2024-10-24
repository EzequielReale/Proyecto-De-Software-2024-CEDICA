from src.core.database import db


class DisabilityDiagnosis(db.Model):
    """Modelo de diagnóstico de discapacidad"""

    __tablename__ = "disability_diagnoses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    type_id = db.Column(
        db.Integer, db.ForeignKey("disability_types.id", ondelete='CASCADE'), nullable=False
    )
    type = db.relationship("DisabilityType", back_populates="diagnoses")

    def __repr__(self):
        return f"DisabilityDiagnosis {self.id}"
