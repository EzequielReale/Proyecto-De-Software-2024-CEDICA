from src.core.database import db
from src.core.models.user_role_permission.upr_models import Permission

def get_permission_by_name(permission_name):
    """ Recibe el nombre de un permiso y retorna el permiso correspondiente si existia"""
    return Permission.query.filter_by(name=permission_name).first()

<<<<<<< HEAD
def permiso_new(**kwargs):
    """ Crea un permiso, lo guarda en la BD y lo retorna """ 
    permiso = Permission(**kwargs)
    db.session.add(permiso)
    db.session.commit()
    return permiso
=======
def create_permission(**kwargs):
    """ Crea un permiso, lo guarda en la BD y lo retorna """ 
    permission = Permission(**kwargs)
    db.session.add(permission)
    db.session.commit()
    return permission
>>>>>>> development

def delete_permission(permission_name):
    """ Recibe el nombre de un permiso y lo elimina de la BD"""
    permission = get_permission_by_name(permission_name)
    db.session.delete(permission)
    db.session.commit()
    return permission

def add_role(permission, role):
    """ Recibe un permiso y el/los rol/es, agrega el/los rol/es 
    al permiso y lo actualiza en la BD"""
    permission.roles.append(role)
    db.session.commit()
    return permission