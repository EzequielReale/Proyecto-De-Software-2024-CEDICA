from src.core.database import db


class Locality(db.Model):
    """Modelo de localidad"""
    __tablename__ = 'localities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    postal_code = db.Column(db.String(8), nullable=False)
    province_id = db.Column(db.Integer, db.ForeignKey('provinces.id'), nullable=False)


    def __repr__(self):
        return f'Locality {self.id}'

    def __str__(self):
        return f'{self.name}'
    