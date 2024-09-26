from sqlalchemy.orm import joinedload

from src.core.database import db
from src.core.people.person import Person
from src.core.people.member import Member

def list_people():
    """Devuelve todas las personas de la BD"""
    people = Person.query.all()
    return people

def list_members():
    """Devuelve todos los miembros de la BD"""
    members = Member.query.options(joinedload(Member.person)).all()
    return members

def member_new(**kwargs):
    """Crea un miembro, lo guarda en la BD y lo devuelve"""
    member = Member(**kwargs)
    db.session.add(member)
    db.session.commit()
    return member
