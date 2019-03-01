"""
This contains msomi app configurations
"""
import os

class Config:
    """
    This is the default configuration class
    Set Debug to False
    """
    DEBUG = False


class Development(Config):
    """
    Our development configuration class
    Set Debug to True
    """
    DEBUG = True


class Testing(Config):
    """
    Our testing configuration class
    Set Debug to True
    """
    DEBUG = True
class Production(Config):
    """
    Our testing configuration class
    Set Debug to True
    """
    DEBUG = True
    DATABASE_URL="dbname='msomidb' host='127.0.0.1' port='5432' user='postgres' password='root'"
class Staging(Config):
    """
    Our testing configuration class
    Set Debug to True
    """
    DEBUG = True


"""
Declaring our application configuration
for development and testing
"""
app_config = {
    "development": Development,
    "testing": Testing,
    "staging":Staging,
    "production": Production,
    "DB_URL": os.getenv('DATABASE_URL'),
    "TEST_DB_URL": os.getenv('DATABASE_TEST_URL')
}