class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "Z\xb6?.\xdf\x9f\xb7m\xf8\x8a%,\xe7\x24\x1a\x11"
    #USE_X_SENDFILE = True
    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    #SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    TESTING = True

    SESSION_COOKIE_SECURE = False