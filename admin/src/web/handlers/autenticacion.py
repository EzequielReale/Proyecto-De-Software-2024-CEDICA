from functools import wraps
from flask import session

from src.core.user_role_permission.operations.role_permissions_operations import get_permissions
from src.core.user_role_permission.operations.user_operations import get_user_by_email
from src.web.handlers.error import unauthorized

import secrets
from werkzeug.security import generate_password_hash

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


def generate_random_hash():
    """generar una cadena aleatoria de 16 bytes y luego la hashea"""
    random_string = secrets.token_hex(16)  
    hashed_password = generate_password_hash(random_string, method='pbkdf2:sha256', salt_length=16)
    return hashed_password