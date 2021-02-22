import os


class BaseConfig:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery configuration
    CELERY_BROKER_URL = f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT", 6379)}/0'
    CELERY_RESULT_BACKEND = f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT", 6379)}/0'
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_REDIS_MAX_CONNECTIONS = 5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        f"postgresql://{os.environ.get('PG_USER', 'postgres')}:{os.environ.get('PG_PASSWORD')}" \
        f"@{os.environ.get('PG_HOST', 'localhost')}:{os.environ.get('PG_PORT', 5432)}/{os.environ.get('PG_DB')}"


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        f"postgresql://{os.environ.get('PG_USER', 'postgres')}:{os.environ.get('PG_PASSWORD')}" \
        f"@{os.environ.get('PG_HOST', 'localhost')}:{os.environ.get('PG_PORT', 5432)}/" \
        f"{os.environ.get('TEST_DB') or os.environ.get('PG_DB')}"


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = \
        f"postgresql://{os.environ.get('PG_USER', 'postgres')}:{os.environ.get('PG_PASSWORD')}" \
        f"@{os.environ.get('PG_HOST', 'localhost')}:{os.environ.get('PG_PORT', 5432)}/{os.environ.get('PG_DB')}"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
