from src.core.database import db
from src.core.people.member import Member


def list_members()->list:
    """Devuelve todos los miembros de la BD"""
    return Member.query.all()

def get_member_by_id(member_id:int)->Member:
    """Devuelve un miembro por ID"""
    return Member.query.filter_by(id=member_id).first()

def member_new(**kwargs)->Member:
    """Crea un miembro, lo guarda en la BD y lo devuelve"""
    member = Member(**kwargs)
    db.session.add(member)
    db.session.commit()
    return member

def member_update(member_id:int, **kwargs)->Member:
    """Actualiza un miembro por ID y lo devuelve"""
    member = get_member_by_id(member_id)
    for attr, value in kwargs.items():
        setattr(member, attr, value)
    db.session.commit()
    return member

def member_delete(member_id:int)->Member:
    """Elimina un miembro por ID"""
    member = get_member_by_id(member_id)
    db.session.delete(member)
    db.session.commit()
    return member
