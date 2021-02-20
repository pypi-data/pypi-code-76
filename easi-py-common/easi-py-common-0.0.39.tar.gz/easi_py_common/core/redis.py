import time
import uuid
import random

from flask_redis import FlaskRedis

# lua脚本，用来释放分布式锁, Redis执行lua脚本是原子性
# 保证 check and del 是原子性
LOCK_PREFIX = 'RLOCK_'
LUA_SCRIPT = "if redis.call('get', KEYS[1]) == KEYS[2] then return redis.call('del',KEYS[1]) else return 0 end"


class RedisRO(object):
    def __init__(self):
        self.clients = []

    def init_app(self, app):
        if app is not None:
            ro_count = app.config.get('REDIS_RO_COUNT', 0)
            if ro_count > 0:
                for i in range(0, ro_count):
                    c = FlaskRedis(app=app, config_prefix='REDIS_RO{}'.format(i + 1), decode_responses=True)
                    self.clients.append(c)

    @property
    def client(self):
        if len(self.clients) > 0:
            # 30%机会，让主节点承担查询操作
            # if random.randint(1, 10) in [6, 7, 8]:
            #     return redis_store
            return self.clients[random.randint(0, len(self.clients) - 1)]
        return redis_store


def get_lock(key, val='1', expire=10):
    return redis_store.set(LOCK_PREFIX + key, val, ex=expire, nx=True)


class RedisLock:
    """
    仅限需要进行原子操作的业务使用
    lock_name代表锁的范围， 比如lock_name=order_123
    代表对123这个订单加锁
    """

    def __init__(self, lock_name, interval_ms=10, timeout_ms=3000, expire=8, timeout=None):
        # timeout_ms 等待锁的超时时间(毫秒)
        # expire 锁的存活时间(秒), (在redis突然挂掉的时候,用于防止死锁现象)
        # 如果业务代码在锁的存活时间内还没执行完，就不能保证原子性了
        if timeout:
            timeout_ms = 1000 * timeout
        self.lock_name = lock_name
        self.timeout_ms = timeout_ms
        self.expire = expire
        if interval_ms > 200:
            interval_ms = 200
        if interval_ms < 0:
            interval_ms = 0
        self.interval_ms = interval_ms / 1000.0
        self.val = '{0}_{1}'.format(lock_name, str(uuid.uuid4()).replace('-', ''))

    def __enter__(self):
        return self.get()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get(self):
        # 获取锁, 阻塞
        end = self.get_utc_timestamp() + self.timeout_ms
        while True:
            if get_lock(self.lock_name, val=self.val, expire=self.expire):
                return True
            if self.get_utc_timestamp() > end:
                break
            if self.interval_ms > 0:
                time.sleep(self.interval_ms)
        return False

    def close(self):
        # 释放锁时，根据value判断，是不是我的锁，不能释放别人的锁
        redis_store.eval(LUA_SCRIPT, 2, LOCK_PREFIX + self.lock_name, self.val)

    @staticmethod
    def get_utc_timestamp():
        timestamp = time.time()
        return int(timestamp * 1000)


redis_store = FlaskRedis(decode_responses=True)
redis_ro_store = RedisRO()
