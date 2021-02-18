from mjango import db
from revdb import db_settings


class MongoBase(db.MongoBase):
    def __init__(self, collection, settings=None):
        self.settings = settings or db_settings
        self.collection = collection
