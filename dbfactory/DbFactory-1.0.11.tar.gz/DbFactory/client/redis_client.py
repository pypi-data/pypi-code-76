#!/usr/bin/env python
# -*- coding: utf-8 -*-
# wechat: chending2012

# python pack
import traceback
import time

# third part pack
import redis
# import leveldb

# self pack
from DbFactory.util.decorator import cost_time, time_out, try_and_reconnect
from .db_base import DbBase

"""
http://redisdoc.com/
redis 方法参考

todo 使用 leveldb 或者其他 生成本地缓存
"""


class RedisClient(DbBase):
    def __init__(self, **kwargs):
        super(RedisClient, self).__init__(**kwargs)
        self.client_ = None  # 统一规定 数据库实例使用这个名字
        if self.__class__.__name__ == "RedisClient":
            self.__init_db_base_args()
            self._reconnect()

    def __init_db_base_args(self):
        """ 这里 填写一些默认的参数 """
        self._redis_ip = self._kwargs.pop('host', '0.0.0.0')
        self._redis_port = int(self._kwargs.pop('port', 6379))
        self._redis_db_name = int(self._kwargs.pop('db_name', 0))
        self._new_kwargs = {
            "host": self._redis_ip,
            "port": self._redis_port,
            "db": self._redis_db_name,
            "password": self._kwargs.pop('password', ''),
            "decode_responses": self._kwargs.pop('decode_responses', True),
            "socket_timeout": self._kwargs.pop('socket_timeout', 10),
        }
        self._new_kwargs = {**self._kwargs, **self._new_kwargs}

    def _reconnect(self, count=0):
        try:
            self.log.info('=== redis kwargs is:{} ==='.format(self._new_kwargs))
            if self.client_:
                self.client_.close()
            self.client_ = redis.StrictRedis(**self._new_kwargs)
            self.log.info("redis connected success !")
        except Exception as e:
            count += 1
            self.log.error(
                "redis connecting error. retry times is {}, host: {}, port: {}, db: {}, err_msg: {}\t{}".format(
                    count, self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
            time.sleep(self._retry_sleep_time)
            self._reconnect(count)
