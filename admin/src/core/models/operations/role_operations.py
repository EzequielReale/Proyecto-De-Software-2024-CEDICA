from src.core.database import db
from src.core.models.user_role_permission.upr_models import Role

def get_role_by_name(role_name)->Role:
    """ Recibe el nombre de un role y retorna el role correspondiente si existia"""
    return Role.query.filter_by(name=role_name).first()


<<<<<<< HEAD
def role_new(**kwargs):
    """ Recibe nombre del rol y permisos asociados
    crea el rol, lo guarda en la BD y lo retorna""" 
    user = Role(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user
=======
def create_role(**kwargs)->Role:
    """ Recibe nombre del rol y permisos asociados
    crea el rol, lo guarda en la BD y lo retorna""" 
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()
    return role
>>>>>>> development


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

