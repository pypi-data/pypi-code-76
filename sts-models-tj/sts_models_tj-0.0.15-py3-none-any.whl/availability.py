import datetime

from . import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

class Availability(Base):
    """ Availability Model for storing when users are available to tutor """
    __tablename__ = "availability"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subjects = Column(String(511), nullable=False)
    startTime = Column(DateTime, nullable=False)
    endTime = Column(DateTime, nullable=False)
    tutor = Column(Integer, ForeignKey('users.cognitoId'))

    def __init__(self, subjects, startTime, endTime, tutor):
        self.subjects = subjects
        self.startTime = startTime
        self.endTime = endTime
        self.tutor = tutor
