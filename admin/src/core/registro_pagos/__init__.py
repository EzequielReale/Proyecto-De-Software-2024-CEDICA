from src.core.database import db
from src.core.registro_pagos.Pagos import Pago, Tipo_pago



def tipo_new(**kwargs):
    """Crea un tipo de pago, lo guarda en la BD y lo devuelve"""
    tipo = Tipo_pago(**kwargs)
    db.session.add(tipo)
    db.session.commit()
    return tipo

def get_tipo_pago(id):
    """ obtiene un tipo de pago mediante el id y lo devuelve"""
    return Tipo_pago.query.filter_by(id=id).first()

####------------

def pago_create(**kwargs):
    """Crea un pago, lo guarda en la BD y lo devuelve"""
    pago = Pago(**kwargs)
    db.session.add(pago)
    db.session.commit()
    return pago


#mod
def administracion_index(request):
    """devuelvo todos los registros de pagos con los filtros necesarios si lo requiere"""   
    #filtros
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    tipo_pago = request.args.get('tipo_pago')
    
     #orden
    order_by = request.args.get('order_by', 'fecha_pago')  # por defecto, ordenar por fecha_pago
    order = request.args.get('order', 'desc')  # por defecto, de más nuevo a más viejo

    # consulta base
    query = Pago.query
    
    # rango de fechas
    if fecha_inicio:
        query = query.filter(Pago.fecha_pago >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Pago.fecha_pago <= fecha_fin)
    
    # tipo de pago
    if tipo_pago and tipo_pago != "Todos los tipos":
        print("tipo pago: ",tipo_pago)
        query = query.join(Pago.tipo_pago).filter(Tipo_pago.tipo == tipo_pago)
    
    #orden de las fechas
    if order_by == 'fecha_pago':
        if order == 'asc':
            query = query.order_by(Pago.fecha_pago.asc())
        else:
            query = query.order_by(Pago.fecha_pago.desc())


    pagos = query.all()
    return pagos 
    
    


def administracion_destroy(id):
    """busco el registro de pago mediante el id y si existe lo borro fisicamente de la BD"""
    pago = Pago.query.get(id)  
    print(pago.beneficiario)
    if pago:
        db.session.delete(pago)
        db.session.commit()
        return True
    else:
        return False
    

def administracion_tipoPagos():
    """devuelvo todos los registos de Tipo de pago"""
    return Tipo_pago.query.all() 

def administracion_getPago(id):
    """obtengo un registro de pago mediante el id y lo devuelvo"""
    return Pago.query.get_or_404(id)

def administracion_update(id,monto,tipo_pago,fecha_pago,des,beneficiario):
     """obtengo un registro de pago mediante el id , actualizo sus campos y lo guardo en la BD"""
     pago= administracion_getPago(id) 
     pago.monto = monto
     pago.tipo_pago = tipo_pago
     pago.tipo_pago_id = tipo_pago.id
     pago.fecha_pago = fecha_pago
     pago.descripcion = des
     pago.beneficiario = beneficiario
     pago.beneficiario_id = beneficiario.id
     db.session.commit() #guardo cambios
     



def administracion_create(**kwargs):
    """creo un nuevo registro de pago, lo guardo en la BD y lo devuelvo"""
    pago = Pago(**kwargs)
    db.session.add(pago)
    db.session.commit()
    return pago