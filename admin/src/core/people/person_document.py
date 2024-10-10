from src.core.database import db


class PersonDocument(db.Model):
    """Modelo para almacenar documentos de las personas"""

    __tablename__ = "person_documents"

    id = db.Column(db.Integer, primary_key=True)
    document_name = db.Column(db.String(255), nullable=False)
    document_path = db.Column(db.String(255), nullable=False)

    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"), nullable=False)
    person = db.relationship("Person", back_populates="documents")

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __repr__(self):
        return f"<PersonDocument {self.id}>"

    def __str__(self):
        return f"{self.document_type} {self.document_number}"
