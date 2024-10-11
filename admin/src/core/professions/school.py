from src.core.database import db

class School(db.Model):
    """Modelo de escuela para un j/a"""
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    level = db.Column(
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
    year = db.Column(db.Integer, nullable=False)
    observations = db.Column(db.Text, nullable=False)
    rider_id = db.Column(db.Integer, db.ForeignKey("riders.id"), nullable=False)
    rider = db.relationship("Rider", back_populates="school", lazy=True, overlaps="rider_school,school")
