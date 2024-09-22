from src.core.database import db
from src.core.auth.user import User


def list_users():
    """Devuelve todos los registros de la BD"""
    users = User.query.all()
    return users 

def create_user(**kwargs):
    """Crea un user, lo guarda en la BD y lo devuelve"""
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

def find_user(email,password):
    """ busco usuario por email y contraseña"""
    user = User.query.filter_by(email=email,password = password).first()
    return user