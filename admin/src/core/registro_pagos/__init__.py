from src.core.database import db
from src.core.registro_pagos.Pagos import Tipo_pago,Pago 
from src.core.auth import User


def tipo_new(**kwargs):
    """Crea un tipo de pago, lo guarda en la BD y lo devuelve"""
    tipo = Tipo_pago(**kwargs)
    db.session.add(tipo)
    db.session.commit()
    return tipo

####------------

def pago_create(**kwargs):
    """Crea un pago, lo guarda en la BD y lo devuelve"""
    pago = Pago(**kwargs)
    db.session.add(pago)
    db.session.commit()
    return pago



def administracion_index():
     """devuelvo todos los registros de pagos"""
     pagos = Pago.query.all()  
     return pagos 


def administracion_destroy(id):
    pago = Pago.query.get(id)  
    print(pago.beneficiario)
    if pago:
        db.session.delete(pago)
        db.session.commit()
        return True
    else:
        return False
    

def administracion_tipoPagos():
    return Tipo_pago.query.all() 

def administracion_getPago(id):
    return Pago.query.get_or_404(id)

def administracion_update(request,id):
     pago= administracion_getPago(id)
     if request.method == 'POST':

        beneficiario_id = request.form['beneficiario']
        beneficiario = User.query.filter_by(id=beneficiario_id).first()##agarro el benef(object)
        pago.beneficiario = beneficiario
        pago.beneficiario_id = beneficiario_id

        pago.monto = request.form['monto']

        tipo_pago_id = request.form['tipo_pago'] 
        tipo_pago_obj = Tipo_pago.query.filter_by(id=tipo_pago_id).first()
        pago.tipo_pago = tipo_pago_obj
        pago.tipo_pago_id = tipo_pago_id

        pago.fecha_pago = request.form['fecha_pago']

        des=  request.form['descripcion']
        pago.descripcion =des
        db.session.commit() #guardo cambios
        return True
     else:
         return False
     

def administracion_create(request):
     if request.method == 'POST':

        monto = request.form['monto']

        tipo_pago_id = request.form['tipo_pago'] 
        tipo_pago_obj = Tipo_pago.query.filter_by(id=tipo_pago_id).first()
       
        fecha_pago = request.form['fecha_pago']

        des=  request.form['descripcion']

        beneficiario_id = request.form['beneficiario']
        if beneficiario_id:
             beneficiario = User.query.filter_by(id=beneficiario_id).first()##agarro el benef(object)
             pago = Pago(beneficiario=beneficiario,monto=monto,tipo_pago=tipo_pago_obj,fecha_pago=fecha_pago,descripcion=des)
        else:
            pago = Pago(monto=monto,tipo_pago=tipo_pago_obj,fecha_pago=fecha_pago,descripcion=des)
        db.session.add(pago)
        db.session.commit() #guardo cambios
        return True
     else:
         return False