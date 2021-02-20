import datetime

from sqlalchemy import Column, Boolean, ForeignKey, String, Integer
from sqlalchemy.orm import relationship, backref

from zm_user.models.base import Base


class User(Base):
    # 用户表
    __tablename__ = 'user'
    # 名称
    name = Column(String(50), nullable=False, comment='角色名称')
    # 所属角色
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False, comment='关联角色id')
    role = relationship('Role', backref=backref('extend', uselist=False))
