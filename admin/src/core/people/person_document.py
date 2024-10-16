from datetime import datetime

from src.core.database import db


class PersonDocument(db.Model):
    """Modelo para almacenar documentos de las personas"""

    __tablename__ = "person_documents"

    id = db.Column(db.Integer, primary_key=True)
    document_name = db.Column(db.String(255), nullable=False)
    document_path = db.Column(db.String(255), nullable=False) # Path en MinIO o URL
    document_type = db.Column(
        db.Enum("Entrevista", "Evaluación", "Planificaciones", "Evolución", "Crónicas", "Documental", name="document_type_enum"),
        nullable=True
    )
    its_a_link = db.Column(db.Boolean, default=False)

    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"), nullable=False)
    person = db.relationship("Person", back_populates="documents")

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<PersonDocument {self.id}>"
