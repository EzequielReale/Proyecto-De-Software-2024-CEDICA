from functools import wraps

from flask import abort
from flask import redirect
from flask import session

from src.core import auth
from src.web.handlers.error import unauthorized

def autenticacion(session):
    print("entre a autenticacion")
    print (session.get("user"))
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
    user = auth.find_user_email(user_email)
    permissions = auth.get_permissions(user) #permissos del user
    return user is not None and permission in permissions 
