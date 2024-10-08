from src.core.database import db
from src.core.user_role_permission.upr_models import RolePermission
from src.core.user_role_permission.operations.user_operations import get_user_by_email
from src.core.user_role_permission.upr_models import User

def create_role_permission(**kwargs)->RolePermission:
    """ Recibe nombre del rol y permisos asociados
    crea el rol, lo guarda en la BD y lo retorna""" 
    role_permission = RolePermission(**kwargs)
    db.session.add(role_permission)
    db.session.commit()
    return role_permission

def get_permissions(user):
    """Retorna los permisos del Rol del Usuario"""
    # Obtenemos los roles del usuario y luego los permisos relacionados con esos roles
    permisos = set()  # Usamos un set para evitar duplicados
    for role in user.roles:
        for permission in role.permissions:
            permisos.add(permission.name)
    
    return list(permisos)  # Retornamos la lista de nombres de permisos

