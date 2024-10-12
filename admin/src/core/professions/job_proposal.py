from src.core.database import db

class JobProposal(db.Model):
    """Modelo de propuesta de trabajo para un j/a"""

    __tablename__ = "job_proposals"

    id = db.Column(db.Integer, primary_key=True)
    institutional_work_proposal = db.Column(
        db.Enum(
            "Hipoterapia",
            "Monta Terapéutica",
            "Deporte Ecuestre Adaptado",
            "Actividades Recreativas",
            "Equitación",
            name="institutional_work_proposals",
        ),
        nullable=False,
    )
    condition = db.Column(
        db.Enum("Regular", "De baja", name="conditions"),
        nullable=False,
    )
    headquarters = db.Column(
        db.Enum("CASJ", "HLP", "OTRO", name="headquarters"),
        nullable=False,
    )
    days = db.Column(
        db.ARRAY(
            db.Enum(
                "Lunes",
                "Martes",
                "Miércoles",
                "Jueves",
                "Viernes",
                "Sábado",
                "Domingo",
                name="days_of_week",
            )
        ),
        nullable=False,
    )
    rider_id = db.Column(db.Integer, db.ForeignKey("riders.id"), nullable=False)
    rider = db.relationship("Rider", back_populates="job_proposal", lazy=True)
    professor_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    professor = db.relationship("Member", foreign_keys=[professor_id], lazy=True)
    member_horse_rider_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    member_horse_rider = db.relationship("Member", foreign_keys=[member_horse_rider_id], lazy=True)
    horse_id = db.Column(db.Integer, db.ForeignKey("horses.id"), nullable=False)
    horse = db.relationship("Horse", backref="riders", lazy=True)
    assistant_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    assistant = db.relationship("Member", foreign_keys=[assistant_id], lazy=True)

    def __repr__(self):
        return f"Job Proposal {self.id}"