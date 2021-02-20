from sqlalchemy import Column, Boolean, String, Integer
from zm_user.models.base import Base


class Permission(Base):
    # 角色表
    __tablename__ = 'permission'
    abbr = Column(String(50), nullable=False, unique=True, comment="权限简称，建议英文")
    # 名称
    name = Column(String(50), nullable=False, comment='角色名称')
