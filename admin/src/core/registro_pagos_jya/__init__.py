from src.core import database_functions as dbf
from src.core.registro_pagos_jya.pagos_jya import PagoJineteAmazona, MediosDePago
from src.core.people.member_rider import Member

from sqlalchemy.orm.query import Query


##### Operaciones sobre Medios de Pago ####

def medio_de_pago_new(**kwargs) -> MediosDePago:
    """Recibe un String que define al Medio de Pago,
    lo crea, lo guarda en la BD y lo devuelve"""
    return dbf.new(MediosDePago, **kwargs)


def pago_jya_new(**kwargs) -> PagoJineteAmazona:
    """Recibe los datos de un Pago de Jinete o Amazona, lo crea, lo guarda en la BD y lo devuelve"""
    return dbf.new(PagoJineteAmazona, **kwargs)


def get_pagos_jya() -> list:
    """Devuelve una lista con todos los Pagos de Jinetes y Amazonas"""
    return dbf.list_all(PagoJineteAmazona)


def get_medio_de_pago(id:int) -> MediosDePago:
    """Recibe un id de Medio de Pago y lo devuelve"""
    return dbf.get_by_field(MediosDePago, "id", id)


def get_pago_jya(id:int) -> PagoJineteAmazona:
    """Recibe un id de Pago de Jinete o Amazona y lo devuelve"""
    return dbf.get_by_field(PagoJineteAmazona, "id", id)


def pago_jya_update(id:int, **kwargs) -> PagoJineteAmazona:
    """Recibe un id de Pago de Jinete o Amazona, los datos a actualizar y los actualiza"""
    return dbf.update(PagoJineteAmazona, id, **kwargs)


def pago_jya_delete(id:int) -> PagoJineteAmazona:
    """Recibe un id de Pago de Jinete o Amazona y lo elimina"""
    return dbf.delete(PagoJineteAmazona, id)


#### Operaciones adicionales sobre Pagos de Jinetes y Amazonas ####

def list_paginated(model, filters: dict, page=1, per_page=25, sort_by=None, sort_direction="asc") -> tuple:
    """Devuelve elementos de un modelo que coinciden con los campos y valores especificados, paginados y ordenados."""
    query = filter_pagos_jya(model, filters)
    query = dbf.order_by(model, query, sort_by, sort_direction) 
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.pages


def filter_pagos_jya(model, filters: dict) -> Query:
    """Aplica filtros y ordenación a una consulta"""
    query = model.query

    # Agrego filtrado por Member
    if filters["receptor_name"] or filters["receptor_last_name"]:
        query = query.join(Member)
        if filters["receptor_name"]:
            query = query.filter(Member.name.ilike(f"%{filters['receptor_name']}%"))
        if filters["receptor_last_name"]:
            query = query.filter(Member.last_name.ilike(f"%{filters['receptor_last_name']}%"))

    # Elimino los campos de receptor_name y receptor_last_name
    del filters["receptor_name"]
    del filters["receptor_last_name"]

    # Agrego filtrado por fecha
    if filters['fecha_inicio']:
        query = query.filter(PagoJineteAmazona.fecha_pago >= filters['fecha_inicio'])
    if filters['fecha_fin']:
        query = query.filter(PagoJineteAmazona.fecha_pago <= filters['fecha_fin'])

    # Elimino los campos de fecha para no interferir con los filtros
    del filters['fecha_inicio']
    del filters['fecha_fin']

    for field, value in filters.items():
        if value and value != "":
            query = __apply_filters(model, query, field, value)

    return query


# rompe el principio de responsabilidad única? Si. Es mejor que tener un código repetido en varios lugares? También.
def __apply_filters(model, query:Query, field:any, value:any) -> Query:
    """Aplica los filtros respectivos a la consulta del cobro"""
    return dbf.__apply_filters(model, query, field, value)
