from src.core.database import db
from src.core.people.member import Member


def list_members(page=1, per_page=25):
    """Devuelve los miembros paginados de la BD"""
    pagination = Member.query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.pages

def get_member_by_field(field: str, value, exclude_id=None) -> Member:
    """Devuelve un miembro por un campo específico y su valor"""
    query = Member.query.filter_by(**{field: value})
    if exclude_id is not None:
        query = query.filter(Member.id != exclude_id)
    return query.first()

def member_new(**kwargs)->Member:
    """Crea un miembro, lo guarda en la BD y lo devuelve"""
    member = Member(**kwargs)
    db.session.add(member)
    db.session.commit()
    return member

def member_update(member_id:int, **kwargs)->Member:
    """Actualiza un miembro por ID y lo devuelve"""
    member = get_member_by_field('id', member_id)
    for attr, value in kwargs.items():
        setattr(member, attr, value)
    db.session.commit()
    return member

def member_delete(member_id:int)->Member:
    """Elimina un miembro por ID"""
    member = get_member_by_field('id', member_id)
    db.session.delete(member)
    db.session.commit()
    return member
