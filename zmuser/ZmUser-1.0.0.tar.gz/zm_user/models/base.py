import datetime
from types import MethodType, FunctionType

from flask_sqlalchemy import BaseQuery
from sqlalchemy import Column, Integer, TIMESTAMP, Boolean, MetaData
from zm_user.conf import Config
import json

db = Config.zm_user_db


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, comment="自增ID")
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now, comment="该数据创建时间")
    is_delete = Column(Boolean, default=False, comment='是否是管理员，0: 否，1: 是')
    update_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now, comment="该数据最后更新时间")

    @classmethod
    def _q_all(cls, *args):
        # 查询多个
        return cls.query.filter(cls.is_delete != True, *args).all()

    @classmethod
    def _q(cls, *args):
        # 查询单个
        return cls.query.filter(cls.is_delete != True, *args).first()

    @classmethod
    def _q_count(cls, *args):
        # 查询数量
        return cls.query.filter(cls.is_delete != True, *args).count()

    def to_save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        res = {}
        attr_list = dir(Base)
        for attr in attr_list:
            if not attr.startswith("_") and hasattr(self, attr) and attr not in ["query_class"]:
                value = getattr(self, attr)
                if isinstance(value, BaseQuery) \
                        or isinstance(value, MetaData) \
                        or isinstance(value, MethodType) \
                        or isinstance(value, FunctionType):
                    continue
                res[attr] = getattr(self, attr)
        return str(res)
