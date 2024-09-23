from src.core.database import db
from src.core.professions.profession import Profession


def get_professions():
    """Obtiene todas las profesiones"""
    return Profession.query.all()

def get_profession_by_id(profession_id):
    """Obtiene una profesion por ID"""
    return Profession.query.filter_by(id=profession_id).first()

def profession_new(**kwargs):
    """Crea una profesion, la guarda en la BD y la devuelve"""
    profession = Profession(**kwargs)
    db.session.add(profession)
    db.session.commit()
    return profession
