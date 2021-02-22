import datetime

from . import Base
from sqlalchemy import Column, DateTime, Boolean, Integer, String
from sqlalchemy.orm import relationship

# Availability class is used, so we must define it here or else it has to be definied by clients of the User class,
# and they don't necessarily know that they need to do this
from .availability import Availability


class User(Base):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    cognitoId = Column(String(255), nullable=False, unique=True)
    registeredOn = Column(DateTime, nullable=False)
    firstName = Column(String(65))
    lastName = Column(String(65))
    # TODO list of courses
    school = Column(String(127))
    grade = Column(String(15))
    bio = Column(String(511)) # TODO variable length string(s)
    admin = Column(Boolean, nullable=False, default=False)

    availabilities = relationship("Availability", cascade="all, delete, delete-orphan")

    def __init__(self, email, cognitoId, firstName="", lastName="", school="", grade="", bio=""):

        self.email = email
        self.cognitoId = cognitoId
        self.firstName = firstName
        self.lastName = lastName
        self.school = school,
        self.grade = grade,
        self.bio = bio
        self.registeredOn = datetime.datetime.now()

