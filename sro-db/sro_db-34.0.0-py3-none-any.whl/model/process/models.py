from sro_db.config.base import Entity
from sro_db.config.config import Base
from sqlalchemy import Column, Boolean ,ForeignKey, Integer, DateTime, String, Table, Text
from sqlalchemy.orm import relationship
from sro_db.model.relationship.model import association_sprint_scrum_development_table

class ScrumProject(Entity):
    is_instance_of = "spo.software_project"
    __tablename__ = "scrum_project"

    root = Column(Boolean, unique=False, default=True)
    organization_id = Column(Integer, ForeignKey('organization.id'))
    type = Column(String(50))

    start_date = Column(DateTime)
    end_date = Column(DateTime)    

    scope = Column(Text(), nullable=True)

    index = Column(String(200), nullable=False)
    
    organization = relationship("Organization", back_populates="scrum_project")
    scrum_process = relationship("ScrumProcess", back_populates="scrum_project", uselist=False)

    #scrum_complex_project_id = Column(Integer, ForeignKey('scrum_project.id'))
    #scrum_complex_project = relationship("ScrumComplexProject",back_populates="scrum_projects", foreign_keys=[scrum_complex_project_id])

    __mapper_args__ = {
        'polymorphic_identity':'scrum_project',
        'polymorphic_on':type
    }
    
class ScrumComplexProject(ScrumProject):
    is_instance_of = "spo.software_project.complex"  
    __tablename__ = "scrum_complex_project"

    id = Column(Integer, ForeignKey('scrum_project.id'), primary_key=True)

    #scrum_projects = relationship("ScrumProject", back_populates="scrum_complex_project")

    __mapper_args__ = {
        'polymorphic_identity':'scrum_complex_project',
    }


class ScrumAtomicProject(ScrumProject):
    is_instance_of = "spo.software_project.atomic"
    __tablename__ = "scrum_atomic_project"

    id = Column(Integer, ForeignKey('scrum_project.id'), primary_key=True)
    
    scrum_complex_project_id = Column(Integer, ForeignKey('scrum_complex_project.id'))
    
    __mapper_args__ = {
        'polymorphic_identity':'scrum_atomic_project',
    }

class ScrumProcess(Entity):
    is_instance_of = "spo.performed.process.general.project"
    __tablename__ = "scrum_process"
    
    scrum_project_id = Column(Integer, ForeignKey('scrum_project.id'))
    scrum_project= relationship("ScrumProject", back_populates="scrum_process")

    product_backlog_definition = relationship("ProductBacklogDefinition", back_populates="scrum_process")
    sprint = relationship("Sprint", back_populates="scrum_process")

class ProductBacklogDefinition(Entity):
    is_instance_of = "spo.performed.process.specific.project"
    __tablename__ = "product_backlog_definition"

    scrum_process_id = Column(Integer, ForeignKey('scrum_process.id'))
    scrum_process= relationship("ScrumProcess", back_populates="product_backlog_definition")

class Sprint(Entity):

    is_instance_of = "spo.performed.process.specific.project"
    __tablename__ = "sprint"
    
    startDate  = Column(DateTime)
    endDate = Column(DateTime)
    
    scrum_process_id = Column(Integer, ForeignKey('scrum_process.id'))
    scrum_process = relationship("ScrumProcess", back_populates="sprint")
    
    scrum_development_tasks = relationship("ScrumDevelopmentTask", secondary=association_sprint_scrum_development_table, back_populates="sprints")
    cerimony = relationship("Cerimony", back_populates="sprint")
    
class Cerimony(Entity):
    is_instance_of = "spo.performed.activity.project"
    __tablename__ = "cerimony"

    startDate  = Column(DateTime)
    endDate = Column(DateTime)

    sprint_id = Column(Integer, ForeignKey('sprint.id'))
    sprint = relationship("Sprint", back_populates="cerimony")
    
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity':'cerimony',
        'polymorphic_on':type
    }

   
class PlanningMeeting(Cerimony):
    __tablename__ = "planning_meeting"
    
    id = Column(Integer, ForeignKey('cerimony.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'planning_meeting',
    }

   
class DailyStandupMeeting(Cerimony):
    __tablename__ = "daily_standup_meeting"
    
    id = Column(Integer, ForeignKey('cerimony.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':'daily_standup_meeting',
    }


class ReviewMeeting(Cerimony):
    __tablename__ = "review_meeting"

    id = Column(Integer, ForeignKey('cerimony.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'review_meeting',
    }


class RetrospectiveMeeting(Cerimony):
    __tablename__ = "retrospective_meeting"

    id = Column(Integer, ForeignKey('cerimony.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':'retrospective_meeting',
    }
