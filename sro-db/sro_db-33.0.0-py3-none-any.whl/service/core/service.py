from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sro_db.model.core.models import *
from sro_db.service.base_service import BaseService

class ApplicationTypeService(BaseService):
    def __init__(self):
        super(ApplicationTypeService,self).__init__(ApplicationType)

class ConfigurationService(BaseService):
    def __init__(self):
        super(ConfigurationService,self).__init__(Configuration)
    
    def retrive_by_organization_and_application(self, organization, application):
        return self.session.query(Configuration).filter(Configuration.organization_id == organization.id, Configuration.application_id == application.id).all()

class ApplicationReferenceService(BaseService):
    def __init__(self):
        super(ApplicationReferenceService,self).__init__(ApplicationReference)

    def retrive_by_external_id (self, external_id):
        
        if isinstance(external_id, int):
            external_id = str(external_id)
        
        return self.session.query(ApplicationReference).filter(ApplicationReference.external_id == external_id).first()
    
    def retrive_by_external_id_and_seon_entity_name (self, external_id, seon_entity_name):
        
        if isinstance(external_id, int):
            external_id = str(external_id)

        return self.session.query(ApplicationReference).filter(ApplicationReference.external_id == external_id, 
                                                               ApplicationReference.entity_name == seon_entity_name).first()

class ApplicationService(BaseService):
    def __init__(self):
        super(ApplicationService,self).__init__(Application)
    
    def retrive_by_name(self, name):
        return self.session.query(Application).filter(Application.name == name).first()
        
