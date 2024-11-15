from functools import wraps
from flask import session

from src.core.user_role_permission.operations.role_permissions_operations import get_permissions
from src.core.user_role_permission.operations.user_operations import get_user_by_email
from src.web.handlers.error import unauthorized

def autenticacion(session):
    return session.get("user") is not None


def login_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if not autenticacion(session):
            return unauthorized()
        return f(*args,**kwargs)
    return wrapper


def check_permission(session, permission):
    user_email = session.get("user")
    user = get_user_by_email(user_email)
    permissions = get_permissions(user) # Permissos del user
    return user is not None and permission in permissions 
