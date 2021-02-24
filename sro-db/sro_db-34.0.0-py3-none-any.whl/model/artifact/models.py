from sro_db.config.base import Entity
from sro_db.config.config import Base
from sqlalchemy import Column, Boolean ,ForeignKey, Float, Integer, DateTime, String, Table
from sqlalchemy.orm import relationship
from sro_db.model.relationship.model import association_user_story_sprint_team_member_table, association_sprint_backlog_scrum_development_activity_table,  association_atomic_user_story_sprint_backlog_table

class ProductBacklog(Entity):
    is_instance_of = "spo.document"
    __tablename__ = "product_backlog"

    product_backlog_definition = Column(Integer, ForeignKey('product_backlog_definition.id')) 


class UserStory(Entity):
    is_instance_of = "rsro.requirements.artifact"
    __tablename__ = "user_story"

    product_backlog =  Column(Integer, ForeignKey('product_backlog.id'))
    
    created_by = Column(Integer, ForeignKey('team_member.id')) 
    activated_by = Column(Integer, ForeignKey('team_member.id'))
    closed_by = Column(Integer, ForeignKey('team_member.id'))
    assigned_by = relationship("TeamMember", secondary=association_user_story_sprint_team_member_table)
    
    story_points = Column(Float(),nullable=True) 

    created_date = Column(DateTime)
    activated_date = Column(DateTime)
    closed_date = Column(DateTime)
    resolved_date = Column(DateTime)
    
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity':'user_story',
        'polymorphic_on':type
    }
    
class Epic(UserStory):

    __tablename__ = "epic"
    id = Column(Integer, ForeignKey('user_story.id'), primary_key=True)

    epic = Column(Integer, ForeignKey('epic.id'))

    __mapper_args__ = {
        'polymorphic_identity':'epic',
    }

class AtomicUserStory(UserStory):

    __tablename__ = "atomic_user_story"
    
    id = Column(Integer, ForeignKey('user_story.id'), primary_key=True)
    epic = Column(Integer, ForeignKey('epic.id'))
    sprint_backlogs = relationship("SprintBacklog", secondary=association_atomic_user_story_sprint_backlog_table, back_populates="atomic_user_stories")

    __mapper_args__ = {
        'polymorphic_identity':'atomic_user_story',
    }

class SprintBacklog(Entity):
    is_instance_of = "spo.document"
    __tablename__ = "sprint_backlog"

    sprint = Column(Integer, ForeignKey('sprint.id'))
    planning_meeting = Column(Integer, ForeignKey('planning_meeting.id'))
    
    scrum_development_tasks = relationship("ScrumDevelopmentTask", secondary=association_sprint_backlog_scrum_development_activity_table, back_populates="sprint_backlogs")
    atomic_user_stories = relationship("AtomicUserStory", secondary=association_atomic_user_story_sprint_backlog_table, back_populates="sprint_backlogs")


class AcceptanceCriterion(Entity):
    is_instance_of = "rsro.requirements"
    __tablename__ = "acceptance_criterion"

    user_story =  Column(Integer, ForeignKey('user_story.id'))

    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity':'acceptance_criterion',
        'polymorphic_on':type
    }
    

class NonFunctionalAcceptanceCriterion(AcceptanceCriterion):
    is_instance_of = "rsro.non_functional_requirements"
    __tablename__ = "non_functional_acceptance_criterion"
    
    id = Column(Integer, ForeignKey('acceptance_criterion.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'non_functional_acceptance_criterion',
    }

class FunctionalAcceptanceCriterion(AcceptanceCriterion):
    is_instance_of = "rsro.functional_requirements"
    __tablename__ = "functional_acceptance_criterion"
    
    id = Column(Integer, ForeignKey('acceptance_criterion.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'functional_acceptance_criterion',
    }
