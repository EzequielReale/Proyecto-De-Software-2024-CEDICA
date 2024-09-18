class Config(object):
    """configuracion de la bd."""
    TESTING= False
  

class ProductionConfig(Config):
     """Configuracion de la bd en produccion"""
     SQLALCHEMY_DATABASE_URI = None

class DevelopmentConfig(Config):
    """ development configuration"""
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "grupo04"
    SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

class TestingConfig(Config):
    """testing config"""

    TESTING= True

config = {
     "production": ProductionConfig,
     "development": DevelopmentConfig,
     "test" : TestingConfig,
    }
    