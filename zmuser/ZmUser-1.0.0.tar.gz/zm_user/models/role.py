from sqlalchemy import Column, Boolean, String, Integer
from zm_user.models.base import Base


class Role(Base):
    # 角色表
    __tablename__ = 'role'

    # 名称
    name = Column(String(50), nullable=False, comment='角色名称')
    # 等级，数值越小，权限越大，root权限为0，默认为10
    level = Column(Integer, default=10, comment='管理员等级，0: 超级管理员, 10: 普通管理员')
    # 是否可以修改，默认可以修改
    is_variable = Column(Boolean, default=True, comment='是否可以修改，默认可以修改，0: 否，1: 是')
