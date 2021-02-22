import os
from keyring import get_password
from keyrings.alt.file import PlaintextKeyring
from werkzeug.utils import import_string
import keyring.backend

DB = "calculator_service"
PORT = 27017
MONGO_IP = "134.122.79.43"
KAFKA_BROKERS = "192.168.1.57:9092"
TRANSACTIONS_TOPIC_NAME = "transactions_2"


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SERVERNAME = "localhost"
    PORT = PORT
    DATABASE = DB
    USERNAME = ""
    PASSWORD = ""
    LOGS_PATH = '../cryptodataaccess/logs/cryptodataaccess.log'
    KAFKA_BROKERS = KAFKA_BROKERS
    TRANSACTIONS_TOPIC_NAME = TRANSACTIONS_TOPIC_NAME


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SERVERNAME = "localhost"
    PORT = PORT
    DATABASE = DB
    USERNAME = "test"
    PASSWORD = "test"
    LOGS_PATH = '../cryptodataaccess/logs/cryptodataaccess.log'
    KAFKA_BROKERS = KAFKA_BROKERS
    TRANSACTIONS_TOPIC_NAME = TRANSACTIONS_TOPIC_NAME


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SERVERNAME = MONGO_IP
    PORT = PORT
    DATABASE = DB
    USERNAME = ""
    PASSWORD = ""
    LOGS_PATH = '../cryptodataaccess/logs/cryptodataaccess.log'
    KAFKA_BROKERS = KAFKA_BROKERS
    TRANSACTIONS_TOPIC_NAME = TRANSACTIONS_TOPIC_NAME


config = {
    "development": "cryptodataaccess.config.DevelopmentConfig",
    "production": "cryptodataaccess.config.ProductionConfig",
    "default": "cryptodataaccess.config.DevelopmentConfig",
}


def configure_app():
    keyring.set_keyring(PlaintextKeyring())
    config_name = os.getenv('FLASK_ENV', "cryptodataaccess.config.DevelopmentConfig")
    cfg = import_string(config_name)()
    cfg.USERNAME = get_password('cryptodataaccess', 'USERNAME')
    cfg.PASSWORD = get_password('cryptodataaccess', cfg.USERNAME)
    return cfg
