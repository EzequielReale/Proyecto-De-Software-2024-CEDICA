from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.orm.query import Query
from sqlalchemy.types import Enum, Integer, String, Text

from src.core.database import db


def __apply_filters(model, query:Query, field:any, value:any) -> Query:
    """Aplica los filtros respectivos a una consulta"""
    column = getattr(model, field)
            
    # Comprobar si es una relación de muchos a muchos (por ejemplo, members en Rider)
    if hasattr(column, "property") and isinstance(column.property, RelationshipProperty):
        related_model = column.property.mapper.class_
        query = query.join(column)
        # Si hay más de un valor (o sea, un getlist), convertirlo en una lista
        print(f"Field: {field}, Value: {value}, Type: {type(value)}")
        if isinstance(value, list):
            query = query.filter(getattr(related_model, 'id').in_(value))
        else:
            query = query.filter(getattr(related_model, 'id') == value)
    # Comprobar si es un entero o un enum
    elif isinstance(column.type, (Integer, Enum)):
        query = query.filter(column == value)
    # Comprobar si es un tipo de columna string
    elif isinstance(column.type, (String, Text)):
        query = query.filter(column.ilike(f"%{value}%"))
    
    return query


def filter(model, filters: dict) -> Query:
    """Aplica filtros y ordenación a una consulta"""
    query = model.query
    for field, value in filters.items():
        if value and value != "":
            query = __apply_filters(model, query, field, value)

    return query


def order_by(model, query:Query, sort_by=None, sort_direction="asc") -> Query:
    """Aplica ordenación a una consulta"""
    if sort_by:
        column = getattr(model, sort_by)
        if sort_direction == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    return query


def list_all(model) -> list:
    """Devuelve todos los elementos de un modelo"""
    return model.query.all()


def list_paginated(model, filters: dict, page=1, per_page=25, sort_by=None, sort_direction="asc") -> tuple:
    """Devuelve elementos de un modelo que coinciden con los campos y valores especificados, paginados y ordenados."""
    query = filter(model, filters)
    query = order_by(model, query, sort_by, sort_direction) 
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.pages


def get_by_field(model, field: str, value, exclude_id=None) -> object:
    """Devuelve un elemento de un modelo por un campo específico y su valor"""
    query = model.query.filter_by(**{field: value})
    if exclude_id is not None:
        query = query.filter(model.id != exclude_id)
    return query.first()


def new(model, **kwargs) -> object:
    """Crea un nuevo elemento, lo guarda en la BD y lo devuelve"""
    item = model(**kwargs)
    db.session.add(item)
    db.session.commit()
    return item


def update(model, item_id: int, **kwargs) -> object:
    """Actualiza un elemento por ID y lo devuelve"""
    item = get_by_field(model, "id", item_id)
    for attr, value in kwargs.items():
        setattr(item, attr, value)
    db.session.commit()
    return item


def delete(model, item_id: int) -> object:
    """Elimina un elemento por ID"""
    item = get_by_field(model, "id", item_id)
    db.session.delete(item)
    db.session.commit()
    return item
