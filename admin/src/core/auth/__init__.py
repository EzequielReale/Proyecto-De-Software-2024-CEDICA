from src.core.database import db
from src.core.bcrypt import bcrypt
from src.core.auth.user import User,Role


def list_users():
    """Devuelve todos los registros de la BD"""
    users = User.query.all()
    return users 

def user_new(**kwargs):
    """Crea un user, lo guarda en la BD y lo devuelve"""
    #encripto la contra antes de guardar el user
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs["password"] = hash.decode("utf-8")
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user


def role_new(**kwargs):
    user = Role(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user


def find_user_email(email):
    """ busco usuario por email """
    user = User.query.filter_by(email=email).first()
    return user

def find_user(email,password):
    user = find_user_email(email)
    if user and bcrypt.check_password_hash(user.password,password):
        return user
    return None

