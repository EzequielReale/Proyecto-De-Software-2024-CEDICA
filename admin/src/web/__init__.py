from flask import Flask
from flask import render_template
from src.web.controllers.issues import bp as issues_bp
from src.web.handlers import error
from src.core import database
from src.core import seeds
from src.core.config import config


def create_app(env="development", static_folder="../../static"):

    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    database.init_app(app)

    @app.route("/")
    def home(): 
        return render_template("home.html")
    

    app.register_blueprint(issues_bp)

    app.register_error_handler(404, error.not_found)
    
    @app.cli.command(name="reset-db") #refistro comando
    def reset_db():
       database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()

    return app