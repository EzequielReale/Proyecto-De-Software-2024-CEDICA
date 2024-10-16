from src.core import database
from src.core import seeds


def register(app):
    
    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    
    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()