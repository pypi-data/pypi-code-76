from sro_db.application.abstract_application import AbstractApplication
from sro_db.model.process.models import Sprint, ScrumAtomicProject, ScrumComplexProject, ScrumProcess, ProductBacklogDefinition
from sro_db.model.artifact.models import ProductBacklog
from sro_db.model.organization.models import ScrumTeam, DevelopmentTeam
from sro_db.application.core.application import ApplicationApplicationReference

from sro_db.service.process.service import SprintService, ScrumComplexProjectService, ScrumAtomicProjectService, ScrumProjectService, ScrumAtomicProjectService, ScrumProcessService, ProductBacklogDefinitionService
from sro_db.service.artifact.service import ProductBacklogService
from sro_db.service.organization.service import ScrumTeamService, DevelopmentTeamService


class ApplicationSprint(AbstractApplication):

    def __init__(self):
        super().__init__(SprintService())
        
    def retrive_by_name_and_project_name(self, sprint_name, project_name):
        return self.service.retrive_by_name_and_project_name(sprint_name, project_name)
    
    def retrive_limbo(self, project_uuid):
        return self.service.retrive_limbo(project_uuid)
    
class ApplicationScrumComplexProject(AbstractApplication):

    def __init__(self):
        super().__init__(ScrumComplexProjectService())
    
    def get_all(self, organization_uuid):
        return self.service.get_all(organization_uuid)

    
class ApplicationScrumAtomicProject(AbstractApplication):

    def __init__(self):
        super().__init__(ScrumAtomicProjectService())
    
    def get_all(self, organization_uuid):
        return self.service.get_all(organization_uuid)
    
class ApplicationScrumProject(AbstractApplication):

    def __init__(self):
        super().__init__(ScrumProjectService())
    
    
class ApplicationScrumProcess(AbstractApplication):
    
    def __init__(self):
        super().__init__(ScrumProcessService())

class ApplicationProductBacklogDefinition(AbstractApplication):
    
    def __init__(self):
        super().__init__(ProductBacklogDefinitionService())
    