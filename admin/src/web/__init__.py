from flask import Flask

from src.core import database
from src.core.config import config
from src.web import routes
from src.web import blueprints
from src.web import commands

def create_app(env="development", static_folder="../../static"):

    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    database.init_app(app)

    # Rutas
    routes.register(app)
    
    # Blueprints
    blueprints.register(app)
    
    # Comandos
    commands.register(app)

    return app
