import os
from dotenv import load_dotenv

# Load environment variables of file .env
load_dotenv()


class Config(object):
    """
    Base configuration class.

    Attributes:
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): If set to False,
        it disables the modification tracking system in SQLAlchemy
                                               to save memory.
        SQLALCHEMY_DATABASE_URI (str): The database URI that should be used
        for the connection. It reads from the environment
                                       variable 'DATABASE_URL' or defaults to
                                       'sqlite:///development.db'.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'sqlite:///development.db')


class DevelopmentConfig(Config):
    """
    Development configuration class that inherits from the base Config class.

    Attributes:
        DEBUG (bool): If set to True, enables debug mode for the Flask
        application.
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    Production configuration class that inherits from the base Config class.

    Attributes:
        DEBUG (bool): If set to False, disables debug mode for the Flask
        application.
    """

    DEBUG = False


def get_config():
    """
    Determines the configuration class to use based on the 'ENV' environment
    variable.

    Returns:
        Config: The appropriate configuration class (DevelopmentConfig or
        ProductionConfig).

    Notes:
        - If 'ENV' is set to 'production', it returns the ProductionConfig
        class.
        - If 'ENV' is set to any other value or is not set, it returns the
        DevelopmentConfig class.
    """
    env = os.environ.get('ENV', 'development')
    if env == 'production':
        return ProductionConfig
    else:
        return DevelopmentConfig