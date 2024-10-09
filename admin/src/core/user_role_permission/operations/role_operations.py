from src.core.database import db
from src.core.user_role_permission.upr_models import Role

def list_roles()->list:
    """ Lista todos los roles guardados en la BD"""
    return Role.query.all()

def get_role_by_name(role_name)->Role:
    """ Recibe el nombre de un role y retorna el role correspondiente si existia"""
    return Role.query.filter_by(name=role_name).first()

def role_new(**kwargs)->Role:
    """ Recibe nombre del rol y permisos asociados
    crea el rol, lo guarda en la BD y lo retorna""" 
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()
    return role

def delete_role(role_name)->Role:
    """ Recibe el nombre de un rol y lo elimina de la BD"""
    role = get_role_by_name(role_name)
    db.session.delete(role)
    db.session.commit()
    return role

def add_permission(role, permission)->Role:
    """ Recibe un rol y el/los permiso/s, agrega el/los permiso/s 
    al rol y lo actualiza en la BD"""
    role.permissions.append(permission)
    db.session.commit()
    return role

