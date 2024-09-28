from src.core.auth import User

def autenticacion(session):
    print("entre a autenticacion")
    print (session.get("user"))
    return session.get("user") is not None


def rol(session, rol):
    # id del usuario  en la sesión
    print("enrte a verificar el rol")
    user_email = session.get("user")
    if not user_email:
         return False  
    user = User.query.filter_by(email=user_email).first()  #tomo user, (las sesiones se guardan por el email, guarda con eso)
    if not user:
         return False  
    print(user.role.name == rol)
    return user.role.name == rol