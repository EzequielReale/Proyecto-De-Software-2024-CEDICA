from src.core.database import db
from src.core.bcrypt import bcrypt
from src.core.user_role_permission.upr_models import User
from src.core.user_role_permission.upr_models import UserRole
from src.core.user_role_permission.upr_models import Role

from sqlalchemy.types import String, Text

#################################################

# Métodos CRUD

def list_users()->list:
    """ Lista todos los usuarios guardados en la BD"""
    return User.query.all()

def list_users_advance(filters: dict, page=1, per_page=25, sort_by=None, sort_direction='asc')->list:
    """Devuelve usuarios que coinciden con los filtros enviados como parámetro"""
    return _list(User, filters, page, per_page, sort_by, sort_direction)

def get_user_by_id(id):
    """ busco usuario por id """
    user = User.query.filter_by(id=id).first()
    return user

def get_user_by_email(user_email)->User:
    """ Obtiene un usuario por su email """
    return User.query.filter_by(email=user_email).first()
 
def user_new(**kwargs)->User:
    """ Crea un usuario, lo guarda en la BD y lo retorna """
    #encripto la contra antes de guardar el user
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs["password"] = hash.decode("utf-8")
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user

def user_update(user_email, **kwargs)->User:
    """ Edita un usuario y guarda los cambios en la BD """
    user = get_user_by_email(user_email)
    for key, value in kwargs.items():
        setattr(user, key, value)
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

#################################################

# Métodos de búsqueda

def get_user_by_role(user_role):
    """ Obtiene usuarios por su rol """
    return User.query.filter_by(role=user_role).first()


def get_user_by_status(user_status):
    """ Obtiene usuarios por su estado """
    return User.query.filter_by(isActive=user_status).first()

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

