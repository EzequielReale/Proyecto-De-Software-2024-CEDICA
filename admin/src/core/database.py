from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    """inicializa la bd con la app"""
    db.init_app(app)
    config(app)
    return app


def config(app):
    """
    confi de hooks para la bd
    """
    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()
    return app

def reset():
    """resetea la bd"""
    db.drop_all() #borra tdo
    db.create_app() #vuelve a crear
    print("se creo nuevamente") 

