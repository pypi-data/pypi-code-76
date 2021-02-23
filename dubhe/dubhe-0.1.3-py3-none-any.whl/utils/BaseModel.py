import peewee
from dubhe.utils import config

db = peewee.SqliteDatabase(config.DB_FILE)


def init_table(table):
    db.create_tables(table)


def clear_table(table):
    db.drop_tables(table)


class BaseModel(peewee.Model):
    class Meta:
        database = db
