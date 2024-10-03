from sqlalchemy.types import String, Text

from src.core.database import db
from core.people.member_rider import Member
from core.people.member_rider import Rider

def _list(model, filters: dict, page=1, per_page=25)->tuple:
    """Devuelve elementos de un modelo que coinciden con los campos y valores especificados, paginados."""
    query = model.query

    for field, value in filters.items():
        if value is not None and value != '': # Ignora campos con valores nulos o vacíos
            column = getattr(model, field)
            if isinstance(column.type, (String, Text)): # Esto es una comprobación de tipo, dado que sqlalchemy no permite usar ilike en campos de tipo Integer
                query = query.filter(column.ilike(f"%{value}%"))
            else:
                query = query.filter(column == value)

    # Aplica la paginación
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.pages

def _get_by_field(model, field: str, value, exclude_id=None):
    """Devuelve un elemento de un modelo por un campo específico y su valor"""
    query = model.query.filter_by(**{field: value})
    if exclude_id is not None:
        query = query.filter(model.id != exclude_id)
    return query.first()

def _new(model, **kwargs):
    """Crea un nuevo elemento, lo guarda en la BD y lo devuelve"""
    item = model(**kwargs)
    db.session.add(item)
    db.session.commit()
    return item

def _update(model, item_id: int, **kwargs):
    """Actualiza un elemento por ID y lo devuelve"""
    item = _get_by_field(model, 'id', item_id)
    for attr, value in kwargs.items():
        setattr(item, attr, value)
    db.session.commit()
    return item

def _delete(model, item_id: int):
    """Elimina un elemento por ID"""
    item = _get_by_field(model, 'id', item_id)
    db.session.delete(item)
    db.session.commit()
    return item

#Funciones de miembros
def list_members(filters: dict, page=1, per_page=25)->tuple:
    """Devuelve miembros que coinciden con los filtros enviados como parámetro"""
    return _list(Member, filters, page, per_page)

def get_member_by_field(field: str, value, exclude_id=None) -> Member:
    """Devuelve un miembro por un campo específico y su valor"""
    return _get_by_field(Member, field, value, exclude_id)

def member_new(**kwargs)->Member:
    """Crea un miembro, lo guarda en la BD y lo devuelve"""
    return _new(Member, **kwargs)

def member_update(member_id:int, **kwargs)->Member:
    """Actualiza un miembro por ID y lo devuelve"""
    return _update(Member, member_id, **kwargs)

def member_delete(member_id:int)->Member:
    """Elimina un miembro por ID"""
    return _delete(Member, member_id)

#Funciones de jinetes
def list_riders(filters:dict, page=1, per_page=25)->tuple:
    """Devuelve los jinetes paginados de la BD"""
    return _list(Rider, filters, page, per_page)

def get_rider_by_field(field: str, value, exclude_id=None)->Rider:
    """Devuelve un jinete por un campo específico y su valor"""
    return _get_by_field(Rider, field, value, exclude_id)

def rider_new(**kwargs)->Rider:
    """Crea un jinete, lo guarda en la BD y lo devuelve"""
    return _new(Rider, **kwargs)

def rider_update(rider_id:int, **kwargs)->Rider:
    """Actualiza un jinete por ID y lo devuelve"""
    return _update(Rider, rider_id, **kwargs)

def rider_delete(rider_id:int)->Rider:
    """Elimina un jinete por ID"""
    return _delete(Rider, rider_id)