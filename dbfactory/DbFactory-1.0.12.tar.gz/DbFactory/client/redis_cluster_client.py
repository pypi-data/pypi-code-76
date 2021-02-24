# -*- coding: utf-8 -*-
# wechat: chending2012

# python pack
import traceback
import time

# third part pack
from rediscluster import RedisCluster  # todo  redis-3.0.1 redis-py-cluster-2.0.0 如果以前安装了redis，这个可能会导致redis 用法上有些差异

# self pack
from DbFactory.client.redis_client import RedisClient


class RedisClusterClient(RedisClient):
    def __init__(self, **kwargs):
        """
        _startup_nodes = [
            {"host": "10.100.16.170", "port": 6381},
            {"host": "10.100.16.170", "port": 6382},
            {"host": "10.100.16.170", "port": 6383}
        ]
        :param kwargs:
        """
        super(RedisClusterClient, self).__init__(**kwargs)
        self.__init_db_base_args()
        self.client_ = None
        self._reconnect()

    def __init_db_base_args(self):
        """ 这里 填写一些默认的参数 """
        self._new_kwargs = {
            "startup_nodes": self._kwargs.pop('startup_nodes', None),
            "password": self._kwargs.pop('password', None),
            "decode_responses": self._kwargs.pop('decode_responses', True),
            "skip_full_coverage_check": self._kwargs.pop('skip_full_coverage_check', True),
            "socket_timeout": self._kwargs.pop('socket_timeout', 10),
        }
        self._new_kwargs = {**self._kwargs, **self._new_kwargs}

    def _reconnect(self, count=0):
        try:
            self.log.info('=== redis cluster kwargs is:{} ==='.format(self._new_kwargs))
            if self.client_:
                self.client_.close()
            self.client_ = RedisCluster(**self._new_kwargs)
            self.log.info("redis_cluster connected success")
        except Exception as e:
            count += 1
            self.log.error(
                "redis cluster connecting error. retry times is {}, err_msg: {}\t{}".format(
                    count, str(e), traceback.format_exc()))
            time.sleep(self._retry_sleep_time)
            self._reconnect(count)
