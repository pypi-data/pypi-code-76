from sro_db.config.base import Entity
from sro_db.config.config import Base
from sqlalchemy import Column ,ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

class IntentedStakeholderParticipation(Entity):
    is_instance_of = "spo.stakeholder.person.intented.participation"
    __tablename__ = "intented_stakeholder_participation"

    team_member = Column(Integer, ForeignKey('team_member.id'))
    intented_activity = Column(Integer, ForeignKey('scrum_intented_development_task.id'))
    
    
class PerformedStakeholderParticipation(Entity):
    is_instance_of = "spo.stakeholder.person.performed.participation"
    __tablename__ = "performed_stakeholder_participation"

    performed_activity = Column(Integer, ForeignKey('scrum_performed_development_task.id'))
    caused_by = Column(Integer, ForeignKey('intented_stakeholder_participation.id'))


class PerformedFragmentParticipation(Entity):
    is_instance_of = "spo.stakeholder.person.performed.participation.fragment"
    __tablename__ = "performed_fragment_participation"

    startDate = Column(DateTime)
    endDate = Column(DateTime)
    #cost = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)
    performedStakeholderParticipation = Column(Integer, ForeignKey('performed_stakeholder_participation.id'))

    