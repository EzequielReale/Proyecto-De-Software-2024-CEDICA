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

def _person_new(**kwargs):
    """Crea una persona, la guarda en la BD y la devuelve"""
    
    person_data = {
        "name": kwargs.get("name"),
        "last_name": kwargs.get("last_name"),
        "dni": kwargs.get("dni"),
        "phone": kwargs.get("phone"),
        "emergency_phone": kwargs.get("emergency_phone"),
        "address": kwargs.get("address"),
        "province_id": kwargs.get("province_id"),
        "locality_id": kwargs.get("locality_id")
    }
    person = Person(**person_data)
    db.session.add(person)
    db.session.commit()

    return person


def member_new(**kwargs):
    """Crea un miembro, lo guarda en la BD y lo devuelve"""
    
    # Crear la instancia de Person
    person = _person_new(**kwargs)
    
    # Crear la instancia de Member usando el ID de la persona recién creada
    member_data = {
        "email": kwargs.get("email"),
        "start_date": kwargs.get("start_date"),
        "end_date": kwargs.get("end_date"),
        "health_insurance": kwargs.get("health_insurance"),
        "health_insurance_number": kwargs.get("health_insurance_number"),
        "condition": kwargs.get("condition"),
        "active": kwargs.get("active", True),
        "profession_id": kwargs.get("profession_id"),
        "person_id": person.id
    }
    
    member = Member(**member_data)
    db.session.add(member)
    db.session.commit()

    return member
