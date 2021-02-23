from sro_db.config.base import Entity
from sro_db.config.config import Base
from sqlalchemy import Column, Boolean ,ForeignKey, Integer, DateTime, String, Table, Float
from sqlalchemy.orm import relationship
from sro_db.model.process.models import Sprint
from sro_db.model.stakeholder.models import TeamMember
from sro_db.model.artifact.models import SprintBacklog
from sro_db.model.relationship.model import association_sprint_backlog_scrum_development_activity_table,  association_sprint_scrum_development_table, association_development_task_team_member_table


class ScrumDevelopmentTask(Entity):
    
    is_instance_of = "spo.activity"
    __tablename__ = "scrum_development_task"

    created_date = Column(DateTime)
    created_by = Column(Integer, ForeignKey('team_member.id'))
    assigned_by = relationship("TeamMember", secondary=association_development_task_team_member_table)

    story_points = Column(Float(),nullable=True) 
    type = Column(String(50))

    sprints = relationship(Sprint, 
                            secondary=association_sprint_scrum_development_table, 
                            back_populates="scrum_development_tasks")

    sprint_backlogs = relationship(SprintBacklog, 
                        secondary=association_sprint_backlog_scrum_development_activity_table, 
                        back_populates="scrum_development_tasks")
    
    atomic_user_story = Column(Integer, ForeignKey('atomic_user_story.id'))
    
    __mapper_args__ = {
        'polymorphic_identity':'scrum_development_task',
        'polymorphic_on':type
    }
    
class DevelopmentTaskType(Entity):

    __tablename__ = "development_task_type"

    Analysis = "analysis"
    deployment = "deployment"
    design = "design"
    development = "development"
    documentation = "documentation"
    requirements = "requirements"
    testing = "testing"
    
class Priority(Entity):
    __tablename__ = "priority"
    normal = "normal"
    medium = "medium"
    high = "high"
    
class Risk(Entity):
    __tablename__ = "risk"

    high = "high"
    medium = "medium"
    normal = "normal"

class ScrumIntentedDevelopmentTask(ScrumDevelopmentTask):

    is_instance_of = "spo.intended.activity.x"
    __tablename__ = "scrum_intented_development_task"

    id = Column(Integer, ForeignKey('scrum_development_task.id'), primary_key=True)
    
    type_activity = Column(Integer, ForeignKey('development_task_type.id'))
    priority = Column(Integer, ForeignKey('priority.id'))
    risk = Column(Integer, ForeignKey('risk.id'))

    __mapper_args__ = {
        'polymorphic_identity':'scrum_intented_development_task',
    }
    
class ScrumPerformedDevelopmentTask(ScrumDevelopmentTask):
    is_instance_of = "spo.performed.activity.x"
    __tablename__ = "scrum_performed_development_task"

    id = Column(Integer, ForeignKey('scrum_development_task.id'), primary_key=True)
    
    closed_date = Column(DateTime)
    activated_date = Column(DateTime)
    resolved_date = Column(DateTime)

    activated_by = Column(Integer, ForeignKey('team_member.id'))
    closed_by = Column(Integer, ForeignKey('team_member.id'))
    resolved_by = Column(Integer, ForeignKey('team_member.id'))
    
    caused_by = Column(Integer, ForeignKey('scrum_intented_development_task.id'))

    __mapper_args__ = {
        'polymorphic_identity':'scrum_performed_development_task',
    }
