# coding:utf-8
# author caturbhuja
# date   2020/12/18 5:59 下午
# wechat chending2012
"""
开源工具？

"""
import cacheout
import re
import time
from threading import Thread
from dlog import DLog
from DbFactory.util.sync_redis_handler import SyncHandler


class MiniRedis:
    """
    本地版本redis实现
    cache_size = 256  # 储存key的个数
    todo mini_redis 添加数据库数量管理，目前hand同步，可能出现，不同db内部，key相同时，数据重复现象。
    """

    def __init__(
            self, cache_size=1000000, sync_period=100, log=None,
            db_type='redis', host='0.0.0.0', port='6379', password='f66sU9iP', db_name='0'
    ):
        self._cache = cacheout.Cache(maxsize=cache_size)
        self.log = log or DLog().get_log
        self._sync = SyncHandler(
            self._cache, sync_period=sync_period * 2, log=self.log,
            db_type=db_type, host=host, port=port, password=password, db_name=db_name
        )
        self._stop = False
        self._ttl = 3600 * 24
        self._sync_period = sync_period
        t = Thread(target=self._sync_cache)
        t.start()
        self.log.info("MiniRedis setup success!")

    # ---------------------------------------- sync redis method ----------------------------------
    def _sync_cache(self):
        while not self._stop:
            if self._sync.sync_lock:
                self.log.info(f'SyncHandler is working ... please wait ...')
                time.sleep(10)
            else:
                self._cache.set_many(self._sync.all_value_dict, ttl=self._ttl)
                self.log.info(f'MiniRedis sync success, sync data len:{len(self._sync.all_value_dict)}')
                time.sleep(self._sync_period)

    def close(self):
        self._stop = True
        self._sync.close()

    # ---------------------------------------- read method ----------------------------------------
    # 这里参数，和redis取交集
    def get(self, name):    # todo 模糊匹配
        if '*' in name:
            name = name.split('*')[0]
            pattern = re.compile(name)
            return self._cache.get_many(pattern)
        else:
            return self._cache.get(name)

    def mget(self, keys: iter, *args):
        return self._cache.get_many(keys)

    def smembers(self, name):
        """返回 set 中所有 members 在设置时，已经做了set类型检查？"""
        return self._cache.get(name, set())

    def keys(self, key):
        return self.scan(key)

    def scan(self, key=None):
        """这里的scan 和 redis 的不同。这里本身就是字典"""
        res = self._cache.keys()
        if key:
            if '*' in key:
                res = list(self.get(key))
        else:
            res = list(res)
        return res

    @staticmethod
    def ping():
        return 'hello ,man/women! i am mini redis'

    def __getattr__(self, item):
        return 'wtf ,man/women! mini redis is developing, method maybe not support, please 找陈鼎！！！！！ to yang too simple!'

    # ---------------------------------------- modify method ----------------------------------------
    def set(self, key, value, ex=None, px=None, nx=False, xx=False, keepttl=False):
        return self._cache.set(key, value, ex)

    def mset(self, mapping):
        """这里只支持健值对的设置"""
        return self._cache.set_many(mapping)

    def sadd(self, name, *values):
        if self._cache.has(name):
            res = self._cache.get(name)
            [res.add(each) for each in values]  # todo 测试set 是否有更快的方法
        else:
            res = set(values)
        self._cache.set(name, res)

    def srem(self, name, *values):
        try:
            res_origin = self._cache.get(name)
            [res_origin.discard(each) for each in values]
            self._cache.set(name, res_origin)
        except Exception as e:
            print(e)

    def delete(self, *names):
        return self._cache.delete_many(names)

    def expire(self, name, time):
        return self._cache.set(name, value=self._cache.get(name), ttl=time)

    def items(self):
        return self._cache.items()


if __name__ == '__main__':
    try:
        sy = MiniRedis()
        n = 0
        count = 6
        while n < count:
            print(sy.items())
            time.sleep(3)
            n += 1
    except KeyboardInterrupt:
        sy.close()
