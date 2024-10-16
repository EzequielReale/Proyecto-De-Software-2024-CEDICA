from src.core.database import db
from core.user_role_permission.upr_models import Role

#################################################

# Métodos CRUD

def list_roles()->list:
    """ Lista todos los roles guardados en la BD"""
    return Role.query.all()

def role_new(**kwargs)->Role:
    """ Recibe nombre del rol y permisos asociados
    crea el rol, lo guarda en la BD y lo retorna""" 
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()
    return role

#################################################

# Métodos adicionales

def role_exists(role_name)->bool:
    """ Recibe el nombre de un rol y retorna True si existe"""
    return get_role_by_name(role_name) is not None

def roles_exists(roles)->bool:
    """ Recibe una lista de roles y retorna True si todos existen"""
    for role in roles:
        if role_exists(role) is False:
            return False
    return True

#################################################

# Métodos de búsqueda

def get_role_by_name(role_name)->Role:
    """ Recibe el nombre de un role y retorna el role correspondiente si existia"""
    return Role.query.filter_by(name=role_name).first()



