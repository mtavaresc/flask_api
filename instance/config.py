import os


class Config(object):
    """Parent configuration class"""
    DEBUG = True
    CSRF_ENABLED = True
    SECRET = 'a-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.getcwd(), "development.db")}'


class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database"""
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.getcwd(), "testing.db")}'
    TESTING = True
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging"""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production"""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
