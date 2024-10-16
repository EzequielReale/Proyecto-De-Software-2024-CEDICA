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
    beneficiario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    beneficiario = db.relationship('User', backref='pagos')
    
    monto = db.Column(db.Integer, nullable=False)  
    fecha_pago = db.Column(db.DateTime,nullable=False)  
    
    # Clave foránea con Tipo_pago
    tipo_pago_id = db.Column(db.Integer, db.ForeignKey('tipos.id'), nullable=False)  # Tipo de pago, no permite nulos
    tipo_pago = db.relationship('Tipo_pago', backref='pagos')  # Relación con el tipo de pago
    
    descripcion = db.Column(db.String(255), nullable=False)  # Descripción del pago
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # Actualización automática

    def __repr__(self):
        return f'<Pago {self.id}, Beneficiario: {self.beneficiario_id}, Monto: {self.monto}>'
