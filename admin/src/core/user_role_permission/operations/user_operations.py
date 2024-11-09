from src.core.database import db
from src.core.bcrypt import bcrypt
from src.core import database_functions as dbf
from src.core.people.member_rider import UserMember
from src.core.user_role_permission.upr_models import Role, User, UserRole
from src.core.user_role_permission.operations.role_operations import get_role_by_name

from sqlalchemy.types import String, Text

#################################################

# Métodos CRUD

def list_users_google()-> list:
    """ Devuelve una lista de usuarios parcialmente registrados con Google """
    return User.query.filter(User.google_id.isnot(None), User.confirmed == False).all()

def list_users()->list:
    """ Lista todos los usuarios guardados en la BD"""
    return User.query.all()
 
def user_new(**kwargs)->User:
    """ Crea un usuario, lo guarda en la BD y lo retorna """
    #encripto la contra antes de guardar el user
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs["password"] = hash.decode("utf-8")
    return dbf.new(User, **kwargs)


def user_update(user_id, **kwargs)->User:
    """ Recibe el id de un usuario y actualiza sus datos"""
    return dbf.update(User, user_id, **kwargs)


def user_update_password(user_email, new_password):
    """ Recibe el email de un usuario y actualiza su contraseña"""
    user = get_user_by_email(user_email)
    # Encripto la nueva contraseña
    hash = bcrypt.generate_password_hash(new_password.encode("utf-8"))
    user.password = hash.decode("utf-8")
    db.session.commit()
    return user


def user_unlink_member(email):
    """ Elimina la relación entre un usuario y un miembro """
    user = get_user_by_email(email)
    user_update(user.id, member=None)
    dbf.delete_by_field(UserMember, "user_id", user.id)
    return user


def delete_user(user_email)->User:
    """ Elimina un usuario de la BD """
    user = get_user_by_email(user_email)
    dbf.delete(User, user.id)
    return user


#################################################

# Métodos adicionales

def user_exists(email):
    """ Verifica si un usuario existe en la BD """
    return get_user_by_email(email) is not None


def find_user(email,password):
    """ Busca un usuario por email y contraseña """
    user = get_user_by_email(email)
    if user and bcrypt.check_password_hash(user.password,password):
        return user
    return None


def user_has_roles(user_email):
    """ Recibe el mail de un usuario y chequea si tiene al menos un rol"""
    user = get_user_by_email(user_email)
    return len(user.roles) > 0

def user_has_role(user_email, role_name):
    """ Recibe el mail de un usuario y un rol y chequea si el usuario tiene ese rol"""
    user = get_user_by_email(user_email)
    role = get_role_by_name(role_name)
    return role.id in user.roles

def get_roles_from_user(user_email):
    """ Obtiene los roles de un usuario """
    user = get_user_by_email(user_email)
    return user.roles

def delete_role_from_user(user_id, role_name):
    """ Elimina un rol de un usuario """
    user = get_user_by_id(user_id)
    role = get_role_by_name(role_name)
    user.roles.remove(role)
    db.session.commit()
    return user

def add_role_to_user(user_id, role_name):
    """ Agrega un rol a un usuario """
    user = get_user_by_id(user_id)
    role = get_role_by_name(role_name)
    user.roles.append(role)
    db.session.commit()
    return user

#################################################

# Métodos de búsqueda

def get_user_by_id(id):
    """ busco usuario por id """
    return dbf.get_by_field(User, "id", id)

def get_user_by_email(user_email)->User:
    """ Obtiene un usuario por su email """
    return dbf.get_by_field(User, "email", user_email)


def list_users_advance(filters: dict, page=1, per_page=25, sort_by=None, sort_direction='asc')->list:
    """Devuelve usuarios que coinciden con los filtros enviados como parámetro"""
    return dbf.list_paginated(User, filters, page, per_page, sort_by, sort_direction)



#####################################################

