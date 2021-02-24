from sro_db.model.core.models import ApplicationReference
from sro_db.service.core.service import ApplicationReferenceService, ConfigurationService, ApplicationService, ApplicationTypeService
from sro_db.application.abstract_application import AbstractApplication


class ApplicationApplicationType(AbstractApplication):
    
    def __init__(self):
        super().__init__(ApplicationTypeService())

class ApplicationApplication(AbstractApplication):
    
    def __init__(self):
        super().__init__(ApplicationService())

class ApplicationConfiguration(AbstractApplication):
    
    def __init__(self):
        super().__init__(ConfigurationService())
    
    def retrive_by_organization_and_application(self, organization, application):
        return self.service.retrive_by_organization_and_application(organization, application)
    

class ApplicationApplicationReference(AbstractApplication):
    
    def __init__(self):
        super().__init__(ApplicationReferenceService())
        
    def get_by_external_uuid(self,external_id):
        return self.service.retrive_by_external_id(external_id)

    def get_by_external_uuid_and_seon_entity_name(self,external_id,seon_entity_name):
        return self.service.retrive_by_external_id_and_seon_entity_name(external_id, seon_entity_name)
                    
                    