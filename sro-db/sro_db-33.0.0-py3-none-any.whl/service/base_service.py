from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sro_db.config.config import session
from sro_db.model.core.models import ApplicationReference

class BaseService():
    
    def __init__(self, object):
        self.session = session
        self.object = object
        self.type = self.object.__tablename__
    
    def get_all(self):
        return self.session.query(self.object).order_by(self.object.id).all()
    
    def get_by_uuid(self, uuid):
        return self.session.query(self.object).filter(self.object.uuid == uuid).first()
        
    def create(self, object):
        self.session.add(object)
        self.session.commit()

    def update (self, object):
        
        self.session.query(self.object).filter(self.object.id == object.id).update({column: getattr(object, column) for column in self.object.__table__.columns.keys()})
        self.session.commit()

    def delete(self, object):
        self.session.delete(object)
        self.session.commit()
