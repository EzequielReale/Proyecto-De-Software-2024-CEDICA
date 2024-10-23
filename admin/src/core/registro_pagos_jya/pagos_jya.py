from datetime import datetime
from src.core.database import db


class MediosDePago(db.Model):
    __tablename__ = 'medios_de_pago'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), unique=True, nullable=False)  

    def __repr__(self):
        return f'<Medio_de_pago {self.tipo}>'

class PagoJineteAmazona(db.Model):
    __tablename__ = 'pagos_jinetes_amazonas'

    id = db.Column(db.Integer, primary_key=True)
    
    jinete_amazona_id = db.Column(db.Integer, db.ForeignKey('riders.id', ondelete='CASCADE'), nullable=False)
    jinete_amazona = db.relationship('Rider', back_populates='payments')
    
    medio_de_pago_id = db.Column(db.Integer, db.ForeignKey('medios_de_pago.id', ondelete='CASCADE'), nullable=False) 
    medio_de_pago = db.relationship('MediosDePago', backref='pagos', uselist=False)

    fecha_pago = db.Column(db.DateTime,nullable=False)
    monto = db.Column(db.Integer, nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('members.id', ondelete='CASCADE'), nullable=False) 
    receptor = db.relationship('Member', back_populates='payments')

    en_deuda = db.Column(db.Boolean, default=False)
    observaciones = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now) 