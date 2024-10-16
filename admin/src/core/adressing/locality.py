from src.core.database import db


class Locality(db.Model):
    """Modelo de localidad"""

    __tablename__ = "localities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    province_id = db.Column(db.Integer, db.ForeignKey("provinces.id"), nullable=False)
    province = db.relationship("Province", backref="localities", lazy=True)
    persons = db.relationship("Person", back_populates="locality")


    def __repr__(self):
        return f"Locality {self.id}"

    def __str__(self):
        return f"{self.name}"
