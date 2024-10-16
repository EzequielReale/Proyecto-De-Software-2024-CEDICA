from src.core.database import db
from src.core.user_role_permission.upr_models import Permission

def get_permission_by_name(permission_name):
    """ Recibe el nombre de un permiso y retorna el permiso correspondiente si existia"""
    return Permission.query.filter_by(name=permission_name).first()

def permiso_new(**kwargs):
    """ Crea un permiso, lo guarda en la BD y lo retorna """ 
    permiso = Permission(**kwargs)
    db.session.add(permiso)
    db.session.commit()
    return permiso