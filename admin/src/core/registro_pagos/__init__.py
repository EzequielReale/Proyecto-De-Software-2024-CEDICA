from src.core import database_functions as dbf
from src.core.database import db
from src.core.registro_pagos.Pagos import Pago, Tipo_pago



def tipo_new(tipo: str) -> Tipo_pago:
    """Crea un tipo de pago, lo guarda en la BD y lo devuelve"""
    return dbf.new(Tipo_pago, tipo=tipo)

def get_tipo_pago(id):
    """ obtiene un tipo de pago mediante el id y lo devuelve"""
    return dbf.get_by_field(Tipo_pago, "id", id)

####------------

def administracion_index(filtros: dict, page: int, per_page: int, order_by: str, orden: str) -> tuple:
    """Devuelvo todos los registros de pagos con los filtros necesarios si lo requiere"""
    query = Pago.query

    # Rango de fechas
    fecha_inicio = filtros.get("fecha_inicio")
    fecha_fin = filtros.get("fecha_fin")
    if fecha_inicio:
        query = query.filter(Pago.fecha_pago >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Pago.fecha_pago <= fecha_fin)

    # Tipo de pago
    tipo_pago = filtros.get("tipo_pago")
    if tipo_pago and tipo_pago != "Todos los tipos":
        query = query.join(Pago.tipo_pago).filter(Tipo_pago.tipo == tipo_pago)

    # Orden de las fechas
    query = dbf.order_by(Pago, query, order_by, orden)

    # Paginación
    query_paginada = query.paginate(page=page, per_page=per_page, error_out=False)
    pagos = query_paginada.items
    total_paginas = query_paginada.pages

    return pagos, total_paginas
    


def administracion_destroy(id):
    """busco el registro de pago mediante el id y si existe lo borro fisicamente de la BD"""
    pago = Pago.query.get(id)  
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
    return dbf.new(Pago, **kwargs)