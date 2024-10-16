from src.core.database import db

class HorseDocumentType(db.Model):
    """Modelo para los tipos de documentos"""
    __tablename__ = 'horse_document_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return f'HorseDocumentType {self.id} - {self.name}'

    def __str__(self):
        return self.name