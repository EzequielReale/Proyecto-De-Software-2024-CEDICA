from src.core.database import db

class HorseDocument(db.Model):
    """Modelo para almacenar documentación de los caballos"""
    __tablename__ = 'horse_documents'

    id = db.Column(db.Integer, primary_key=True)
    horse_id = db.Column(db.Integer, db.ForeignKey('horses.id'), nullable=False)
    document_type = db.Column(db.String(64), nullable=False)
    url = db.Column(db.String(256), nullable=True)
    file_path = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f'HorseDocument {self.id} - {self.document_type}'

    def __str__(self):
        return f'{self.document_type}'