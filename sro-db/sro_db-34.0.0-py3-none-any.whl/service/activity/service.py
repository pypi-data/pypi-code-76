from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sro_db.model.activity.models import *
from sro_db.service.base_service import BaseService

class ScrumDevelopmentTaskService(BaseService):
    def __init__(self):
        super(ScrumDevelopmentTaskService,self).__init__(ScrumDevelopmentTask)

class ScrumIntentedDevelopmentTaskService(BaseService):
    def __init__(self):
        super(ScrumIntentedDevelopmentTaskService,self).__init__(ScrumIntentedDevelopmentTask)

class ScrumPerformedDevelopmentTaskService(BaseService):
    def __init__(self):
        super(ScrumPerformedDevelopmentTaskService,self).__init__(ScrumPerformedDevelopmentTask)

class DevelopmentTaskTypeService(BaseService):
    def __init__(self):
        super(DevelopmentTaskTypeService,self).__init__(DevelopmentTaskType)
    
    def retrive_by_name (self, name):
        return self.session.query(DevelopmentTaskType).filter(DevelopmentTaskType.name.like (name)).first()

class PriorityService(BaseService):
    
    def __init__(self):
        super(PriorityService,self).__init__(Priority)
    
    def retrive_by_name (self, name):
        return self.session.query(Priority).filter(Priority.name.like (name)).first()

class RiskService(BaseService):

    def __init__(self):
        super(RiskService,self).__init__(Risk)
    
    def retrive_by_name (self, name):
        return self.session.query(Risk).filter(Risk.name.like (name)).first()




