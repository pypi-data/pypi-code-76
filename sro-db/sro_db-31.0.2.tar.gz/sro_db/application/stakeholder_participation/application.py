from sro_db.application.abstract_application import AbstractApplication
from sro_db.service.stakeholder_participation.service import *

class ApplicationIntentedStakeholderParticipation(AbstractApplication):
    
    def __init__(self):
        super().__init__(IntentedStakeholderParticipationService())
    
class ApplicationPerformedStakeholderParticipation(AbstractApplication):
    
    def __init__(self):
        super().__init__(PerformedStakeholderParticipationService())

class ApplicationPerformedFragmentParticipation(AbstractApplication):
    
    def __init__(self):
        super().__init__(PerformedFragmentParticipationService())

