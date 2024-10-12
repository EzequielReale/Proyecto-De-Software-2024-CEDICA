from os import fstat
import uuid

from flask import current_app
from minio.error import S3Error
from sqlalchemy.types import String, Text, Integer
from sqlalchemy.orm import RelationshipProperty

from src.core.database import db
from src.core.people.member_rider import Member
from src.core.people.member_rider import Rider
from src.core.people.tutor import Tutor
from src.core.people.member_rider import RiderMember
from src.core.people.person_document import PersonDocument as Document


def __apply_filters(model, query:tuple, field:any, value:any, filters: dict) -> tuple:
    """Aplica los filtros respectivos a una consulta"""
    column = getattr(model, field)
            
    # Comprobar si es una relación de muchos a muchos (por ejemplo, members en Rider)
    if hasattr(column, "property") and isinstance(column.property, RelationshipProperty):
        related_model = column.property.mapper.class_
        query = query.join(column)
        # Si hay más de un valor (o sea, un getlist), convertirlo en una lista
        if isinstance(value, list):
            query = query.filter(getattr(related_model, 'id').in_(value))
        else:
            query = query.filter(getattr(related_model, 'id') == value)
    # Comprobar si es un tipo de columna string
    elif isinstance(column.type, (String, Text)):
        query = query.filter(column.ilike(f"%{value}%"))
    # Comprobar si es un entero
    elif isinstance(column.type, Integer):
        query = query.filter(column == value)
    
    return query


def _filter_and_sort(model, filters: dict, sort_by=None, sort_direction="asc") -> tuple:
    """Aplica filtros y ordenación a una consulta"""
    query = model.query

    # Aplicar filtros
    for field, value in filters.items():
        if value and value != "":
            query = __apply_filters(model, query, field, value, filters)

    # Aplicar ordenación
    if sort_by:
        column = getattr(model, sort_by)
        if sort_direction == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    return query


def _list(model, filters: dict, page=1, per_page=25, sort_by=None, sort_direction="asc") -> tuple:
    """Devuelve elementos de un modelo que coinciden con los campos y valores especificados, paginados y ordenados."""
    query = _filter_and_sort(model, filters, sort_by, sort_direction)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.pages


def _get_by_field(model, field: str, value, exclude_id=None) -> object:
    """Devuelve un elemento de un modelo por un campo específico y su valor"""
    query = model.query.filter_by(**{field: value})
    if exclude_id is not None:
        query = query.filter(model.id != exclude_id)
    return query.first()


def _new(model, **kwargs) -> object:
    """Crea un nuevo elemento, lo guarda en la BD y lo devuelve"""
    item = model(**kwargs)
    db.session.add(item)
    db.session.commit()
    return item


def _update(model, item_id: int, **kwargs) -> object:
    """Actualiza un elemento por ID y lo devuelve"""
    item = _get_by_field(model, "id", item_id)
    for attr, value in kwargs.items():
        setattr(item, attr, value)
    db.session.commit()
    return item


def _delete(model, item_id: int) -> object:
    """Elimina un elemento por ID"""
    item = _get_by_field(model, "id", item_id)
    db.session.delete(item)
    db.session.commit()
    return item


def _add_document(person_id: int, file: bytes, path: str) -> Document:
    """Añade un documento a un elemento por ID y lo guarda en MinIO"""
    size = fstat(file.fileno()).st_size
    try:
        document = current_app.storage.client.put_object(
            "grupo04", path, file, size, file.content_type
        )
    except S3Error as e:
        raise RuntimeError(f"Error subiendo el documento: {e}")

    document = Document(
        person_id=person_id, document_path=path, document_name=file.filename
    )
    db.session.add(document)
    db.session.commit()
    return document


def list_documents(person_id: int) -> list:
    """Devuelve los documentos de una persona por ID con URLs descargables"""
    docs_db = Document.query.filter_by(person_id=person_id).all()
    files = []
    for doc in docs_db:
        file_url = current_app.storage.client.presigned_get_object(
            "grupo04", doc.document_path
        )
        files.append({"id": doc.id, "name": doc.document_name, "url": file_url})
    return files


def delete_document(document_id: int) -> Document:
    """Elimina un documento por ID"""
    document = _get_by_field(Document, "id", document_id)
    current_app.storage.client.remove_object("grupo04", document.document_path)
    db.session.delete(document)
    db.session.commit()
    return document


"""Funciones de miembros"""


def list_members(filters: dict, page=1, per_page=25, sort_by=None, sort_direction="asc") -> tuple:
    """Devuelve miembros que coinciden con los filtros enviados como parámetro"""
    return _list(Member, filters, page, per_page, sort_by, sort_direction)


def list_professionals() -> list:
    """Devuelve todos los miembros de la BD"""
    return Member.query.all()


def get_member_by_field(field: str, value, exclude_id=None) -> Member:
    """Devuelve un miembro por un campo específico y su valor"""
    return _get_by_field(Member, field, value, exclude_id)


def member_new(**kwargs) -> Member:
    """Crea un miembro, lo guarda en la BD y lo devuelve"""
    return _new(Member, **kwargs)


def member_update(member_id: int, **kwargs) -> Member:
    """Actualiza un miembro por ID y lo devuelve"""
    return _update(Member, member_id, **kwargs)


def member_delete(member_id: int) -> Member:
    """Elimina un miembro por ID"""
    return _delete(Member, member_id)


def member_add_document(member_id: int, file: bytes) -> Document:
    """Añade un documento a un miembro por ID y lo guarda en MinIO"""
    ulid = uuid.uuid4().hex
    path = f"members/{member_id}/{ulid}_{file.filename}"
    return _add_document(member_id, file, path)


"""Funciones de j/a"""

def list_riders(filters: dict, page=1, per_page=25, sort_by=None, sort_direction="asc") -> tuple:
    """Devuelve los jinetes paginados de la BD"""
    return _list(Rider, filters, page, per_page, sort_by, sort_direction)


def get_rider_by_field(field: str, value, exclude_id=None) -> Rider:
    """Devuelve un jinete por un campo específico y su valor"""
    return _get_by_field(Rider, field, value, exclude_id)


def rider_new(**kwargs) -> Rider:
    """Crea un jinete, lo guarda en la BD y lo devuelve"""
    return _new(Rider, **kwargs)


def rider_update(rider_id: int, **kwargs) -> Rider:
    """Actualiza un jinete por ID y lo devuelve"""
    return _update(Rider, rider_id, **kwargs)


def rider_delete(rider_id: int) -> Rider:
    """Elimina un jinete por ID"""
    return _delete(Rider, rider_id)


def rider_add_document(rider_id: int, file: bytes) -> Document:
    """Añade un documento a un jinete por ID y lo guarda en MinIO"""
    ulid = uuid.uuid4().hex
    path = f"riders/{rider_id}/{ulid}_{file.filename}"
    return _add_document(rider_id, file, path)

def tutor_new(**kwargs) -> Tutor:
    """Crea un tutor, lo guarda en la BD y lo devuelve"""
    return _new(Tutor, **kwargs)

# def rider_member_new(rider_id: int, member_id: int) -> Rider:
#     """Crea una relación entre un jinete y un miembro"""
#     rider = _get_by_field(Rider, "id", rider_id)
#     member = _get_by_field(Member, "id", member_id)
#     rider.members.append(member)
#     member.riders.append(rider)
#     db.session.commit()
#     return rider

def rider_member_new(**kwargs) -> Rider:
    """Crea una relación entre un jinete y un miembro"""
    return _new(RiderMember, **kwargs)