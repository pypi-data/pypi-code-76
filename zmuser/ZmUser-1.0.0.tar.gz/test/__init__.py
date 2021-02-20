import datetime
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


class Config(object):
    DEBUG = False
    TESTING = False
    JSON_AS_ASCII = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=7)
    DB_URI = 'postgresql+psycopg2://postgres:mark@127.0.0.1:5432/big'
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", DB_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
# 如果数据库不存在就创建
engine = create_engine(Config.DB_URI)
if not database_exists(engine.url):
    create_database(engine.url)
