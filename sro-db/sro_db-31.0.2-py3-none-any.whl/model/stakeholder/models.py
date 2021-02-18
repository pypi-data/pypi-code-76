from sro_db.config.base import Entity
from sqlalchemy import Column ,ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

class Person (Entity):
    is_instance_of = "eo.person"    
    __tablename__ = "person"
    
    email = Column(EmailType, unique=True)
    
    organization_id = Column(Integer, ForeignKey('organization.id'))
    organization = relationship("Organization", back_populates="people")
    team_member = relationship("TeamMember", back_populates="person")
    
class TeamMember(Entity):
    is_instance_of = "eo.team_member"
    __tablename__ = "team_member"

    type = Column(String(50))
    
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship("Person",back_populates="team_member")
    
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship("Team",back_populates="team_members")
    
    team_role = Column(String(200), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity':'team_member',
        'polymorphic_on':type
    }

class Developer(TeamMember):
    is_instance_of = "eo.team_member"
    __tablename__ = "developer"

    id = Column(Integer, ForeignKey('team_member.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':'developer',
    }

class ScrumMaster(TeamMember):
    is_instance_of = "eo.team_member"
    __tablename__ = "scrum_master"

    id = Column(Integer, ForeignKey('team_member.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':'scrum_master',
    }

class ProductOwner(TeamMember):
    is_instance_of = "eo.team_member"
    __tablename__ = "product_owner"

    id = Column(Integer, ForeignKey('team_member.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':'product_owner',
    }

class Client(TeamMember):
    is_instance_of = "eo.team_member"
    __tablename__ = "client"

    id = Column(Integer, ForeignKey('team_member.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':'client',
    }