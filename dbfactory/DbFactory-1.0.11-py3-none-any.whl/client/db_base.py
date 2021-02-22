# coding:utf-8
# author caturbhuja
# date   2020/9/7 12:13 下午
# wechat chending2012
from abc import ABCMeta, abstractmethod
from DbFactory.util.decorator import cost_time, time_out, try_and_reconnect
from DbFactory.util.decorator_redis_cache import redis_cache


class DbBase(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self.config = dict()
        self.__init_common_args()
        self.__prune_kwargs()

    def __init_common_args(self):
        self.log = self._kwargs.pop('log')   # 这个必须有，因为 db_factory 已经处理
        self._use_redis_local_cache = self._kwargs.pop('use_redis_local_cache')
        self.config.update({
            "NO_DB_SWITCH_CLIENT": ["redis_cluster"],  # 不支持 切换db 的数据库
            "use_time_out_decorator": self._kwargs.pop('use_time_out_decorator', True),  # 超时监控 装饰器开关
            "action_time_out": int(self._kwargs.pop('action_time_out', 240)),  # 超时监控 装饰器开关
            "use_redis_local_cache": self._use_redis_local_cache,  # 开启redis本地缓存 装饰器开关
            "db_type": self._kwargs.pop('db_type'),  # 数据库类型
            "action_warning_time": int(self._kwargs.pop('action_warning_time', 10)),  # 单次命令超时时间提醒
            "only_read_from_mini_redis": self._kwargs.pop('only_read_from_mini_redis'),
        })
        # 添加 redis 本地缓存
        if self._use_redis_local_cache:
            self.config["mini_redis"] = self._kwargs.pop("mini_redis")

        self._retry_times = int(self._kwargs.pop('retry_times', 10))   # 错误尝试次数，目前没有用到。以后废弃。
        self._retry_sleep_time = int(self._kwargs.pop('retry_sleep_time', 1))  # db 连接失败，sleep 时间

    def __prune_kwargs(self):
        """清理字典中不需要的内容，防止干扰 db 新建"""
        pop_list = [
            'singleton_num', 'db_type', 'singleton_sign', 'singleton_switch', 'show_db_configure',
            'use_time_out_decorator', 'use_redis_local_cache'
        ]
        [self._kwargs.pop(each, None) for each in pop_list]

    @cost_time
    @time_out
    @redis_cache
    @try_and_reconnect
    def generation_func(self, method, *args, **kwargs):
        """建立反射， 重试机制位置，要求 client 内不要有 try cache"""
        def action():
            return getattr(self, method)(*args, **kwargs)
        return action()

    def __getattr__(self, item):
        """找不到的方法，直接反射"""
        print(f'do getattr, item: {item}')
        return getattr(self.client_, item)

    @abstractmethod
    def _reconnect(self):
        """建立连接/重新连接"""

    @property
    def origin_client(self):
        """
        可以直接给外部使用，这个不会享受 异常处理加成效果，需要被加成，则需要类似 mysql 一样，再封装一次
        """
        return self.client_
