from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sro_db.model.organization.models import *
from sro_db.service.base_service import BaseService

class OrganizationService(BaseService):
    def __init__(self):
        super(OrganizationService,self).__init__(Organization)

class TeamService(BaseService):
    def __init__(self):
        super(TeamService,self).__init__(Team)

class ScrumTeamService(BaseService):
    def __init__(self):
        super(ScrumTeamService,self).__init__(ScrumTeam)
    
class DevelopmentTeamService(BaseService):
    def __init__(self):
        super(DevelopmentTeamService,self).__init__(DevelopmentTeam)
