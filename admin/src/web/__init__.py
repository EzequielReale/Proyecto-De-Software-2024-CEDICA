from flask import Flask
from flask_session import Session
from src.core.bcrypt import bcrypt
from src.core import database
from src.core.config import config
from src.web.handlers.autenticacion import check_permission,autenticacion
from src.web import blueprints
from src.web import commands
from src.web import routes
from src.web.storage import storage


session = Session()


def create_app(env="development", static_folder="../../static"):
    

    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    database.init_app(app)
    session.init_app(app)
    bcrypt.init_app(app)
  
    #registro funcion en jinja para restringir el front
    app.jinja_env.globals.update(is_authenticated = autenticacion)
    app.jinja_env.globals.update(check_permission = check_permission)

    # Rutas
    routes.register(app)
    
    # Blueprints
    blueprints.register(app)
    
    # Comandos
    commands.register(app)

    # Storage
   # storage.init_app(app)

    return app
