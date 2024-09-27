from os import environ
from dotenv import load_dotenv


class Config(object):
    """Configuracion de la BD"""
    TESTING= False
    SECRET_KEY="secret"
    SESSION_TYPE= "filesystem"
  

class ProductionConfig(Config):
    """Configuracion de la BD en produccion"""
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")


class DevelopmentConfig(Config):
    """Development configuration"""

    load_dotenv() # Carga variables de entorno

    DB_USER = environ.get("DEV_DB_USER")
    DB_PASSWORD = environ.get("DEV_DB_PASSWORD")
    DB_HOST = environ.get("DEV_DB_HOST")
    DB_PORT = "5432"
    DB_NAME = environ.get("DEV_DB_NAME")
    SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


class TestingConfig(Config):
    """Testing config"""
    TESTING= True

config = {
     "production": ProductionConfig,
     "development": DevelopmentConfig,
     "test" : TestingConfig,
    }
    