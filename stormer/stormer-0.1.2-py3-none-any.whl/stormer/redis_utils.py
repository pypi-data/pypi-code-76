#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created By Murray(Murray) on 2021/1/12 22:08
--------------------------------------------------
pip install redis-py-cluster==2.1.0
"""
import logging

import redis
from rediscluster import RedisCluster

logger = logging.getLogger(__name__)


def spilt_cluster_nodes(nodes):
    """构建redis cluster node"""
    if not nodes:
        return []
    nodes = nodes.split(",")
    _nodes = []
    for node in nodes:
        if not node:
            continue
        _ip_port = node.split(":")
        if len(_ip_port) != 2:
            raise Exception("redis cluster nodes param error, you need setting nodes like ip:7000,ip:7002")
        _nodes.append({
            'host': _ip_port[0],
            'port': _ip_port[1],
            'db': 0
        })
    return _nodes


def redis_cluster(nodes, password=''):
    _cache = None
    try:
        _cache = RedisCluster(
            startup_nodes=nodes,
            password=password,
            decode_responses=True,
            skip_full_coverage_check=True
        )
    except (Exception,) as e:
        logger.error('Init RedisCluster error {}'.format(e))
    return _cache


class RedisClusterCache(object):
    def __init__(self, nodes, password=''):
        self.nodes = nodes
        if not isinstance(self.nodes, list):
            self.spilt_cluster_nodes()
        self.connect = redis_cluster(
            nodes=self.nodes,
            password=password
        )

    def spilt_cluster_nodes(self):
        """构建redis cluster node"""
        if isinstance(self.nodes, list):
            return
        self.nodes = spilt_cluster_nodes(nodes=self.nodes)

    def get_info(self):
        """获取redis集群info信息"""
        # 查看info信息, 返回dict
        dic = self.connect.cluster_info()
        return dic or {}

    def get_has_aof(self):
        """查看aof是否打开"""
        _config = self.connect.config_get('appendonly')
        return _config

    def set(self, key, value, timeout=None, **kwargs):
        """设置缓存"""
        return self.connect.set(key, value, ex=timeout, **kwargs)

    def get(self, key):
        """获取缓存"""
        _val = self.connect.get(key)
        if isinstance(_val, bytes):
            _val = _val.decode(encoding='utf8')
        return _val

    def delete(self, key):
        """删除缓存"""
        return self.connect.delete(key)

    def expire(self, key, timeout):
        """设置过期时间"""
        return self.connect.expire(key, timeout)

    def persist(self, key):
        """取消过期时间"""
        return self.connect.persist(key)

    def ttl(self, key):
        """获取过期时间"""
        return self.connect.ttl(key)


def get_redis_cache(redis_url, redis_nodes, password=''):
    _cache = None
    if redis_url:
        try:
            _cache = redis.Redis(connection_pool=redis.ConnectionPool.from_url(redis_url))
        except ConnectionError:
            logger.warning("Redis connection pool is max number of clients reached, now disconnect.")
            if _cache:
                _cache.connection_pool.disconnect()
    elif redis_nodes:
        _cache = RedisClusterCache(nodes=redis_nodes, password=password)
    if not _cache:
        raise Exception("Init redis cache fail.")
    return _cache


if __name__ == '__main__':
    import time

    _redis_nodes = "103.131.169.104:8000,103.131.169.104:8001,103.131.169.104:8002," \
                   "103.131.169.104:8003,103.131.169.104:8004,103.131.169.104:8005"
    _password = "SXsE3jHZPtYhcYMO"
    cache = RedisClusterCache(nodes=_redis_nodes, password=_password)
    print(cache.get_info())
    print(cache.get_has_aof())
    cache.set("key1", "value1", timeout=2)
    time.sleep(1)
    print("1 ==> ", cache.get("key1"))
    cache.expire("key1", 3)
    time.sleep(2)
    print("2 ==> ", cache.get("key1"))
    print("3 ==> ", cache.ttl("key1"))
    cache.persist("key1")
    print("4 ==> ", cache.ttl("key1"))
    cache.delete("key1")
    print("5 ==> ", cache.get("key1"))
