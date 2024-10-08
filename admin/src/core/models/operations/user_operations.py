from src.core.database import db
from src.core.bcrypt import bcrypt
from src.core.models.user_role_permission.upr_models import User

#################################################

# Métodos CRUD

def list_users()->list:
    """ Lista todos los usuarios guardados en la BD"""
    return User.query.all()

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

#################################################

# Métodos de búsqueda


def get_user_by_role(user_role):
    """ Obtiene usuarios por su rol """
    return User.query.filter_by(role=user_role).first()


def get_user_by_status(user_status):
    """ Obtiene usuarios por su estado """
    return User.query.filter_by(isActive=user_status).first()

<<<<<<< HEAD
#####################################################

# Metodos agregados por Giu

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
=======
def find_user(email,password):
    user = get_user_by_email(email)
>>>>>>> development
    if user and bcrypt.check_password_hash(user.password,password):
        return user
    return None

<<<<<<< HEAD

def get_permissions(user):
    """Retorna los permisos del rol del usuario"""
    # Obtenemos los roles del usuario y luego los permisos relacionados con esos roles
    permisos = set()  # Usamos un set para evitar duplicados
    for role in user.roles:
        for permission in role.permissions:
            permisos.add(permission.name)
    
    return list(permisos)  # Retornamos la lista de nombres de permisos
=======
>>>>>>> development
