from src.core.database import db
from src.core.user_role_permission.upr_models import RolePermission

def create_role_permission(**kwargs)->RolePermission:
    """ Recibe nombre del rol y permisos asociados
    crea el rol, lo guarda en la BD y lo retorna""" 
    role_permission = RolePermission(**kwargs)
    db.session.add(role_permission)
    db.session.commit()
    return role_permission