

def autenticacion(session):
    print("entre a autenticacion")
    print (session.get("user"))
    return session.get("user") is not None