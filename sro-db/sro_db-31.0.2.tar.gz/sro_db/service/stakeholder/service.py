from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sro_db.model.stakeholder.models import *
from sro_db.model.organization.models import ScrumTeam, DevelopmentTeam
from sro_db.model.process.models import ScrumProject
from sro_db.model.organization.models import Organization
from sro_db.service.core.service import ApplicationReferenceService
from sro_db.service.base_service import BaseService

class PersonService(BaseService):

    def __init__(self):
        super(PersonService,self).__init__(Person)
    
    def get_all(self, organization_uuid):
        return self.session.query(self.object).join(Organization).filter(Organization.uuid == organization_uuid).order_by(self.object.id)
    
    def get_by_email(self, email):
        return self.session.query(self.object).filter(Person.email == email).first()

class TeamMemberService(BaseService):
    def __init__(self):
        super(TeamMemberService,self).__init__(TeamMember)
        
    def retrive_by_external_id_and_project_name (self, person, project_name):
        
        scrum_team = self.session.query(ScrumTeam).join(ScrumProject).filter(ScrumProject.name.like (project_name)).first()
        team_member = self.session.query(TeamMember).filter(TeamMember.person == person, TeamMember.team == scrum_team).first()
        
        if team_member is None and scrum_team is not None: 
            developmen_team = self.session.query(DevelopmentTeam).filter(DevelopmentTeam.scrum_team_id == scrum_team.id).first()
            team_member = self.session.query(TeamMember).join(DevelopmentTeam).filter(TeamMember.team_id == developmen_team.id, TeamMember.person == person, DevelopmentTeam.scrum_team_id == scrum_team.id).first()
        
        return team_member

class DeveloperService(BaseService):
    def __init__(self):
        super(DeveloperService,self).__init__(Developer)
    
    def create_with_project_name(self, person, project_name):
        
        scrum_team = self.session.query(ScrumTeam).join(ScrumProject).filter(ScrumProject.name.like (project_name)).first()
        developmen_team = self.session.query(DevelopmentTeam).filter(DevelopmentTeam.scrum_team_id == scrum_team.id).first()

        developer = Developer()
        developer.name = person.name
        developer.description = person.description
        developer.person = person
        developer.team_role = ""
        developer.team = developmen_team
        return developer

    
class ScrumMasterService(BaseService):
    def __init__(self):
        super(ScrumMasterService,self).__init__(ScrumMaster)

class ProductOwnerService(BaseService):
    def __init__(self):
        super(ProductOwnerService,self).__init__(ProductOwner)

class ClientService(BaseService):
    def __init__(self):
        super(ClientService,self).__init__(Client)