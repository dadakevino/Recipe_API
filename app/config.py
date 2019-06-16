class Config(object):
    """Parent configuration class."""
    DEBUG = False
    DEVELOPMENT = False
    ITEMS_PER_PAGE = 10


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    DEVELOPMENT = True
    ITEMS_PER_PAGE = 2

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    DEVELOPMENT = False
    ITEMS_PER_PAGE = 10

class TestingConfig(Config):
    """Configurations for Production."""
    Testing = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
    }
