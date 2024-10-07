from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    """Inicializa la BD con la app"""
    db.init_app(app)
    config(app)
    return app


def config(app):
    """Config. de hooks para la BD"""
    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()
    return app


def reset():
    """Resetea la bd"""

    db.drop_all() #Borra toda la BD
    print("BD borrada con exito") 
    db.create_all() #Vuelve a crear las tablas
    print("BD creada nuevamente con exito") 
