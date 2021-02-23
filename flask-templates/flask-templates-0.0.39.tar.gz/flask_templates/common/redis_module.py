# -*- coding: utf-8 -*-
"""
----------------------------------------------------
    File Name:              redis_module
    Description             
    Author:                 develop
    date:                   2019/4/8
----------------------------------------------------
"""
__author__ = 'develop'

from hashlib import md5
from threading import Lock
from redis import Redis, ConnectionPool, sentinel
from copy import deepcopy
from functools import wraps
from flask_templates.common.utils import decrypt
from flask_templates.configs.template import REDIS_CONFIG
from flask_templates.common.logger import logger

_MANAGER_LOCKS = Lock()


def cache_decorator(redis_name=None,master=True):
    def wrapper(func):
        @wraps(func)
        def dec(*args, **kwargs):
            if "redis_client" not in kwargs and all([not isinstance(x,Redis) for x in args]):
                if "redis_name" in kwargs and not redis_name:
                    my_redis_name = kwargs['redis_name']
                else:
                    my_redis_name = redis_name
                kwargs['redis_client'] = MyRedis(redis_name=my_redis_name).get_redis_client(master=master)
            try:
                res = func(*args, **kwargs)
                return res
            except Exception as e:
                # import traceback
                # traceback.print_exc()
                logger.warning(str(e))

        return dec
    return wrapper

class MyRedis(object):
    """Redis连接类"""

    INSTANCE = {}

    def __new__(cls, redis_name=None):
        """
        singleton redis constructor
        :param redis_name: redis_name string in application.yaml
        :return:
        """
        e_type = 'special' if REDIS_CONFIG.get('encryption') else None
        if not redis_name:
            redis_config = deepcopy(REDIS_CONFIG.get('default'))
        else:
            redis_config = deepcopy(REDIS_CONFIG.get(redis_name))
            if not redis_config:
                raise Exception("no such redis configs named `{}`".format(redis_name))
        config_hash = md5("".join(map(
            lambda i: "{}{}".format(i[0], i[1]), sorted(redis_config.items())
        )).encode()).hexdigest()
        if config_hash in cls.INSTANCE:
            return cls.INSTANCE[config_hash]
        with _MANAGER_LOCKS:
            if config_hash not in cls.INSTANCE:
                instance = object.__new__(cls)
                redis_config['host'] = [x.strip() for x in redis_config['host'].split(',')]
                redis_config['port'] = [int(x.strip()) for x in str(redis_config['port']).split(',')]
                redis_config['password'] = decrypt(redis_config['password'], e_type)
                instance.redis_name = redis_name
                instance.use_sentinel = redis_config.pop('use_sentinel') if 'use_sentinel' in redis_config else False
                if not instance.use_sentinel:
                    redis_config['host'] = redis_config['host'][0]
                    redis_config['port'] = redis_config['port'][0]
                instance.redis_config = redis_config
                MyRedis.construct(instance)
                cls.INSTANCE[config_hash] = instance
        return cls.INSTANCE[config_hash]

    @staticmethod
    def construct(instance):
        redis_config = instance.redis_config
        redis_name = instance.redis_name
        use_sentinel = instance.use_sentinel
        if use_sentinel:
            st = sentinel.Sentinel(list(zip(redis_config.pop('host'), redis_config.pop('port'))))
            instance.master = st.master_for(redis_name, **redis_config)
            instance.slave = st.slave_for(redis_name, **redis_config)
        else:

            pool = ConnectionPool(**redis_config)  # decode_responses=True保证解析出来的不是bytes类型
            instance.master = instance.slave = Redis(connection_pool=pool)

    def refresh(self):
        MyRedis.construct(self)

    def get_redis_client(self, master=True):
        """返回一个Redis对象的实例"""
        if master:
            return self.master
        return self.slave


if __name__ == '__main__':
    myredis = MyRedis('default')
    print(id(myredis.get_redis_client()))
    myredis.refresh()
    print(id(myredis.get_redis_client()))
    print(id(myredis.get_redis_client()))
