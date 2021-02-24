# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

RESOURCES = {}
CONF = {}

ALL = [
    "initMysql",
    "getMysqlClient"
]


class MysqlExcept(Exception):
    pass


def new_mysql(**kwargs):
    engine = create_engine(kwargs.get("uri"))
    DBSession = sessionmaker(bind=engine)
    return DBSession

def initMysql(**kwargs):
    name = kwargs.get("name")
    if not name:
        name = "base"
    CONF["conf"] = {"name": kwargs}
    mysql_client = new_mysql(**kwargs)
    
    RESOURCES[name] = mysql_client

def getMysqlClient(name="base"):
    """
    获取mysql客户端 name不同 数据库不同
    """
    client = RESOURCES.get(name)
    if not client:
        kwargs = CONF.get("conf")
        if not kwargs:
            raise MysqlExcept("mysql模块未初始化")
        conf = kwargs.get("name")
        if not conf:
            raise MysqlExcept("mysql没有对应的配置")
        mysql_client = new_mysql(**conf)
        RESOURCES[name] = mysql_client
        return mysql_client
    return client