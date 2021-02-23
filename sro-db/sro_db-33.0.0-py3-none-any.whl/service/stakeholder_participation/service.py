from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sro_db.model.stakeholder_participation.models import *
from sro_db.service.base_service import BaseService

class IntentedStakeholderParticipationService(BaseService):
    def __init__(self):
        super(IntentedStakeholderParticipationService,self).__init__(IntentedStakeholderParticipation)

class PerformedStakeholderParticipationService(BaseService):
    def __init__(self):
        super(PerformedStakeholderParticipationService,self).__init__(PerformedStakeholderParticipation)

class PerformedFragmentParticipationService(BaseService):
    def __init__(self):
        super(PerformedFragmentParticipationService,self).__init__(PerformedFragmentParticipation)
