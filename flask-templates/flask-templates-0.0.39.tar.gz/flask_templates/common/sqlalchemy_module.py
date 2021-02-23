# -*- coding: utf-8 -*-
"""
----------------------------------------------------
    File Name:              __init__.py
    Description
    Author:                 develop
    date:                   4/3/2019
----------------------------------------------------
"""
__author__ = 'develop'

import random
from hashlib import md5
from threading import Lock
from copy import deepcopy
from contextlib import closing
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_templates.configs.template import DB_CONFIG, MYSQL_CONFIG
from flask_templates.common.utils import decrypt

Base = declarative_base()

_MANAGER_LOCKS = Lock()

common_config = {
    'pool_recycle': 30,  # 数据库连接超时回收时间
    'echo': MYSQL_CONFIG.get("echo",False),
}


class MySQL(object):
    """数据库连接类"""
    INSTANCE = {}

    def __new__(cls, master_name=None, charset='utf8'):
        """
        构造方法
        :param master_name: 主库名
        :param charset: 数据库字符集
        :return:
        """
        e_type = 'special' if DB_CONFIG.get('encryption') else None
        slave_config = []
        master_config = MYSQL_CONFIG.get("master",{})
        use_slave = MYSQL_CONFIG.get('use_slave',False)
        if use_slave:
            slave_config = MYSQL_CONFIG.get('slaves',[])

        config_hash = md5(("".join(map(lambda i: "{}{}".format(i[0], i[1]), sorted(master_config.items()))) +
                           str(use_slave)).encode()).hexdigest()
        if config_hash in cls.INSTANCE:
            return cls.INSTANCE[config_hash]

        with _MANAGER_LOCKS:
            if config_hash not in cls.INSTANCE:
                instance = object.__new__(cls)
                instance.engine = cls.get_engine(master_config, charset, e_type)
                slave_session_class_dict = {}
                cls.INSTANCE[config_hash] = instance
                if use_slave:
                    for index, one_slave in enumerate(slave_config):
                        name = one_slave.get('name', str(index))
                        cur_engine = cls.get_engine(one_slave, charset, e_type)
                        slave_session_class_dict[name] = cls.get_session_class(cur_engine)
                instance.slave_session_class_dict = slave_session_class_dict
        return cls.INSTANCE[config_hash]

    @staticmethod
    def get_engine(config, charset, e_type):
        """
        创建sqlalchemy数据库引擎
        :param config: 数据库配置字典
        :param charset: 数据库字符集
        :param e_type: 是否加密密码
        :return:
        """
        common_db_config = deepcopy(common_config)
        config = deepcopy(config)
        config.update({
                    'password': decrypt(config["password"], e_type),
                    'charset': charset
                })
        if 'name' in config:
            config.pop('name')
        common_db_config.update(config)
        order = ['user', 'password', 'host', 'port', 'database', 'charset']
        return create_engine(
            "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(*[common_db_config.pop(i) for i in order]),
            echo_pool=MYSQL_CONFIG.get("echo",False), **common_db_config
        )

    @staticmethod
    def get_session_class(cur_engine):
        return sessionmaker(bind=cur_engine, autoflush=False, autocommit=False, expire_on_commit=False)

    def sql_session(self, session_class_name=None, random_slave=False):
        db_session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False)
        if random_slave:
            if len(self.slave_session_class_dict) == 0:
                session_class = db_session
            else:
                session_class = self.slave_session_class_dict[random.choice(list(self.slave_session_class_dict.keys()))]
        elif session_class_name:
            if session_class_name in self.slave_session_class_dict:
                session_class = self.slave_session_class_dict[session_class_name]
            else:
                raise Exception("salve name {} don't exist".format(session_class_name))
        else:
            session_class = db_session
        return session_class()


# 初始化SQLalchemy引擎,其中strategy='threadlocal' 是使用本地线程模式。
engine = MySQL().engine
DB_Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def commit_connection(func):
    """Single Mysql commit Connection Manager"""

    def args_wraps(*args, **kwargs):
        with closing(engine.raw_connection()) as con:
            ret = func(cursor=con.cursor(), *args, **kwargs)
            con.commit()
            return ret
    return args_wraps

if __name__ == "__main__":
    print(DB_Session().execute("select now()").fetchall())
