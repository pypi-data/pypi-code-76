from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sro_db.model.artifact.models import *
from sro_db.model.process.models import ScrumProject, ScrumProcess, ProductBacklogDefinition, Sprint
from sro_db.service.base_service import BaseService

class ProductBacklogService(BaseService):
    def __init__(self):
        super(ProductBacklogService,self).__init__(ProductBacklog)
    
    def retrive_by_project_name(self, project_name):
        return self.session.query(ProductBacklog).join(ProductBacklogDefinition).join(ScrumProcess).join(ScrumProject).filter(ScrumProject.name.like(project_name)).first()

class UserStoryService(BaseService):
    def __init__(self):
        super(UserStoryService,self).__init__(UserStory)

class EpicService(BaseService):
    def __init__(self):
        super(EpicService,self).__init__(Epic)

class AtomicUserStoryService(BaseService):
    def __init__(self):
        super(AtomicUserStoryService,self).__init__(AtomicUserStory)

class SprintBacklogService(BaseService):
    def __init__(self):
        super(SprintBacklogService,self).__init__(SprintBacklog)

    def retrive_by_name_and_project_name(self, sprint_name, project_name):
        return self.session.query(SprintBacklog).join(Sprint).join(ScrumProcess).join(ScrumProject).filter(ScrumProject.name.like(project_name), Sprint.name.like(sprint_name)).first()

class AcceptanceCriterionService(BaseService):
    def __init__(self):
        super(AcceptanceCriterionService,self).__init__(AcceptanceCriterion)

class NonFunctionalAcceptanceCriterionService(BaseService):
    def __init__(self):
        super(NonFunctionalAcceptanceCriterionService,self).__init__(NonFunctionalAcceptanceCriterion)

class FunctionalAcceptanceCriterionService(BaseService):
    def __init__(self):
        super(FunctionalAcceptanceCriterionService,self).__init__(FunctionalAcceptanceCriterion)