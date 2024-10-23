from datetime import datetime
from src.core.database import db


class Tipo_pago(db.Model):
    __tablename__ = 'tipos'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)  

    def __repr__(self):
        return f'<Tipo_pago {self.tipo}>'


class Pago(db.Model):
    __tablename__ = 'pagos'
    id = db.Column(db.Integer, primary_key=True)
    
    # Clave foránea con User
    beneficiario_id = db.Column(db.Integer, db.ForeignKey('members.id', ondelete='SET NULL'), nullable=True)
    beneficiario = db.relationship('Member', backref='pagos')
    
    monto = db.Column(db.Integer, nullable=False)  
    fecha_pago = db.Column(db.DateTime,nullable=False)  
    
    # Clave foránea con Tipo_pago
    tipo_pago_id = db.Column(db.Integer, db.ForeignKey('tipos.id', ondelete='CASCADE'), nullable=False)
    tipo_pago = db.relationship('Tipo_pago', backref='pagos')
    
    descripcion = db.Column(db.String(255), nullable=False)
   
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<Pago {self.id}, Beneficiario: {self.beneficiario_id}, Monto: {self.monto}>'
