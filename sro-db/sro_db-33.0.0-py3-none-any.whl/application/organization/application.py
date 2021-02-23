from sro_db.application.abstract_application import AbstractApplication
from sro_db.service.organization.service import OrganizationService, TeamService, DevelopmentTeamService, ScrumTeamService

class ApplicationOrganization(AbstractApplication):

    def __init__(self):
        super().__init__(OrganizationService())

class ApplicationTeam(AbstractApplication):

    def __init__(self):
        super().__init__(TeamService())

class ApplicationDevelopmentTeam(AbstractApplication):

    def __init__(self):
        super().__init__(DevelopmentTeamService())

class ApplicationScrumTeam(AbstractApplication):

    def __init__(self):
        super().__init__(ScrumTeamService())