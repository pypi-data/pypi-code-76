# coding: utf-8
from sqlalchemy import *
from sqlalchemy.dialects.mysql import *
from sqlalchemy.ext.declarative import declarative_base
import datetime
from decimal import Decimal

DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata


class Base(DeclarativeBase):
    __abstract__ = True

    def to_dict(self):
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        for key, value in _dict.items():
            if isinstance(value, datetime.datetime):
                _dict[key] = str(value)
            elif isinstance(value, Decimal):
                _dict[key] = float(value)
        return _dict


class Example(Base):
    __tablename__ = 'asset_info'

    asset_id = Column(TINYINT(2), primary_key=True, comment='资产类型id')
    asset_type = Column(String(20), nullable=False, unique=True, comment='资产类型')
    alias = Column(String(20), nullable=False, unique=True, comment='类型别名')
    description = Column(String(50), comment='详细描述')
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')

