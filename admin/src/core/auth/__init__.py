from src.core.database import db
from src.core.bcrypt import bcrypt
from src.core.user_role_permission.upr_models import User, Role, Permission


def get_permissions(user):
    """Retorna los permisos del rol del usuario"""
    # Obtenemos los roles del usuario y luego los permisos relacionados con esos roles
    permisos = set()  # Usamos un set para evitar duplicados
    for role in user.roles:
        for permission in role.permissions:
            permisos.add(permission.name)
    
    return list(permisos)  # Retornamos la lista de nombres de permisos




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


def permiso_new(**kwargs):
    permiso = Permission(**kwargs)
    db.session.add(permiso)
    db.session.commit()
    return permiso

def find_user_email(email):
    """ busco usuario por email """
    user = User.query.filter_by(email=email).first()
    return user


def find_user_id(id):
    """ busco usuario por id """
    user = User.query.filter_by(id=id).first()
    return user


def find_user(email,password):
    user = find_user_email(email)
    if user and bcrypt.check_password_hash(user.password,password):
        return user
    return None

