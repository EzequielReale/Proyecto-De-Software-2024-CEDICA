from src.core.database import db

class School(db.Model):
    """Modelo de escuela para un j/a"""
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(64), nullable=False)
    school_address = db.Column(db.String(128), nullable=False)
    school_phone = db.Column(db.String(16), nullable=False)
    school_level = db.Column(
        db.Enum(
            "Inicial",
            "Primario",
            "Secundario",
            "Terciario",
            "Universitario",
            name="school_levels",
        ),
        nullable=False,
    )
    school_year = db.Column(db.Integer, nullable=False)
    school_observations = db.Column(db.Text, nullable=False)
    rider_id = db.Column(db.Integer, db.ForeignKey("riders.id"), nullable=False)
    rider = db.relationship("Rider", back_populates="school", lazy=True, overlaps="rider_school,school")
