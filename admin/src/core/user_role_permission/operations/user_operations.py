from src.core.database import db
from src.core.bcrypt import bcrypt
from src.core.user_role_permission.upr_models import User
from src.core.user_role_permission.upr_models import Role
from src.core.user_role_permission.upr_models import UserRole
from src.core.user_role_permission.operations.role_operations import get_role_by_name

from sqlalchemy.types import String, Text

#################################################

# Métodos CRUD

def list_users()->list:
    """ Lista todos los usuarios guardados en la BD"""
    return User.query.all()
 
def user_new(**kwargs)->User:
    """ Crea un usuario, lo guarda en la BD y lo retorna """
    #encripto la contra antes de guardar el user
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs["password"] = hash.decode("utf-8")
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user


def user_update(user_id, **kwargs)->User:
    """ Recibe el id de un usuario y actualiza sus datos"""
    user = get_user_by_id(user_id)
    for attr, value in kwargs.items():
        setattr(user, attr, value)
    db.session.commit()
    return user


def user_update_password(user_email, new_password):
    """ Recibe el email de un usuario y actualiza su contraseña"""
    user = get_user_by_email(user_email)
    # Encripto la nueva contraseña
    hash = bcrypt.generate_password_hash(new_password.encode("utf-8"))
    user.password = hash.decode("utf-8")
    db.session.commit()
    return user


def delete_user(user_email)->User:
    """ Elimina un usuario de la BD """
    user = get_user_by_email(user_email)
    db.session.delete(user)
    db.session.commit()
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
    print(role_name)
    user = get_user_by_id(user_id)
    role = get_role_by_name(role_name)
    user.roles.append(role)
    db.session.commit()
    return user

#################################################

# Métodos de búsqueda

def get_user_by_id(id):
    """ busco usuario por id """
    user = User.query.filter_by(id=id).first()
    return user

def get_user_by_email(user_email)->User:
    """ Obtiene un usuario por su email """
    return User.query.filter_by(email=user_email).first()


def list_users_advance(filters: dict, page=1, per_page=25, sort_by=None, sort_direction='asc')->list:
    """Devuelve usuarios que coinciden con los filtros enviados como parámetro"""
    return _list(User, filters, page, per_page, sort_by, sort_direction)


def _list(model, filters: dict, page=1, per_page=25, sort_by=None, sort_direction='asc')->tuple:
    """Devuelve elementos de un modelo que coinciden con los campos y valores especificados, paginados y ordenados."""
    query = filter_sort_users(filters, sort_by, sort_direction)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.pages

def filter_sort_users(filters: dict, sort_by=None, sort_direction='asc'):
    """Recibe los criterios de filtrado, sort_by, sort_direction y ejecuta una consulta a la base 
    de datos para obtener los usuarios que cumplen con los criterios"""
    query = User.query
    # Aplicar filtros
    for field, value in filters.items():
        if value is not None and value != '':
            column = getattr(User, field)
            if field == 'roles':
                query = query.join(UserRole).join(Role).filter(Role.id == value)
            elif isinstance(column.type, (String, Text)):
                query = query.filter(column.ilike(f"%{value}%"))
            else:
                query = query.filter(column == value)
    if sort_by:
        column = getattr(User, sort_by)
        if sort_direction == 'desc':
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    return query



#####################################################

