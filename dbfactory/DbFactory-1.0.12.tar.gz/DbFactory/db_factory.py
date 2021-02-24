#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:    db_factory.py
   Description:  DB工厂类
   Author:       Caturbhuja
   date:         2020/8/31
   WeChat:       chending2012
-------------------------------------------------
   Change Activity:
       2020/8/31:   DB工厂类创建
       2020/9/1:    redis_client 方法使用反射
       2020/9/2:    DB工厂类增加自动反射
       2020/9/27：  统一重试装饰函数
       2020/10/9:   添加kafka封装
-------------------------------------------------
目前已知dlog进程安全，遇到单例模式时，会出现无法获取锁。虽然有报错，但是，不影响使用。

"""
__author__ = 'Caturbhuja'

# python pack
import os
from functools import partial
from importlib import import_module

# self pack
from .util.six import with_metaclass
from .util.singleton import Singleton
from .mixin import MysqlMixin, RedisMixin, KafkaMixin

dir_path = os.path.dirname(os.path.abspath(__file__))


# sys.path.append(dir_path)


class IdleTips(MysqlMixin, RedisMixin, KafkaMixin):
    """此类中均为伪方法，仅仅为了提供IDE的提示功能"""


class DbFactory(with_metaclass(Singleton), IdleTips):
    """
    DbFactory DB工厂类
    利用 Singleton 控制生成db为单例模式 ，默认 每种数据库一个单例。
    通过 singleton_switch 控制是否为单例模式。

    抽象方法定义：
        假  详见 每一个 client 的 参数处理部分

    所有方法需要相应类去具体实现：（新增数据库命名规则）
        mysql:          mysql_client.py
        mysql_pool:     mysql_pool_client.py
        redis:          redis_client.py
        redis_async:    redis_async_client.py
        redis_cluster:  redis_cluster_client.py

    数据格式例子：
        startup_nodes = [{"host": "10.100.16.170", "port": 6381},
                 {"host": "10.100.16.170", "port": 6382},
                 {"host": "10.100.16.170", "port": 6383}]

        host = '0.0.0.0'

    """

    def __init__(
            self,
            # 说明: 除了dbfactory设置外，其他所有默认值在 client base内 有设置。这里写出参数，仅仅为了提示。
            # ------------------ common ------------------
            db_type=None,  # 必需 mysql(默认)/redis/redis_cluster/kafka 初始化数据库类型
            host=None,  # 必须 redis 集群时，可能不需要
            port=None,  # 必须 redis 集群时，可能不需要
            db_name=None,  # 必须 'string'/int  redis 集群时，可能不需要

            # ------------------ 可选参数 ------------------
            username=None,  # 非必须
            password=None,  # 非必须
            connect_timeout=None,  # 非必须 int mysql/redis 有这个参数

            # ----------------- dbfactory -----------------
            singleton_switch=False,  # 非必需 True/False(默认) 单例模式开关
            singleton_num='0',  # 非必需 'any string' 单例编号，如果开启单例模式，可以使用编号开启多个单例
            show_db_configure=False,  # 非必需 显示数据库配置
            retry_sleep_time=5,  # 非必需 db 连接失败，sleep 时间
            debug=False,  # 非必需 控制日志级别
            log=None,  # 非必需 内置日志
            use_redis_local_cache=False,  # 非必需 True/False(默认) redis 启用本地缓存
            only_read_from_mini_redis=True,  # 非必需 True/False(默认) redis 读取时，仅仅使用本地缓存。 优点，防止缓存击穿
            use_time_out_decorator=True,  # 非必需 执行命令超时监控 用户在命令执行超时时，强制结束，防止程序卡死。多线程时，不能用在子线程中，建议使用多进程。
            action_time_out=None,  # 非必需 240 (默认) 单次命令超时断开时间。
            action_warning_time=None,  # 非必需 10 (默认) 单次命令超时提醒日志。

            # ------------------ mysql ------------------
            autocommit=None,  # 非必需 True(默认)/False
            charset=None,  # 非必需 'utf-8'(默认)
            use_unicode=None,  # 非必需 True(默认)/False
            sql_mode=None,  # 非必需 None
            cursorclass=None,  # 非必需 cursor/dictcursor/sscursor/ssdictcursor/dictcursormixin

            # ------------------ mysql_connection_pool 如果开启连接池，则需要下面参数 ------------------
            use_connection_pool=None,  # 非必需 True(默认)/False 是否使用线程池
            mincached=None,
            maxcached=None,

            # ------------------ redis ------------------

            # ------------------ redis_cluster ------------------
            startup_nodes=None,  # 非必需 集群节点列表(类型参考开头注释) 使用这个，连接所有集群，不使用的话，可以使用host，port参数，连接单点

            # ------------------ kafka_common ------------------
            init_type=None,  # 非必需 kafka 初始化种类，consumer(默认)/producer
            partition=None,  # 非必需 某些情况下需要
            group_id=None,  # 非必需 string 默认没有 group_id 多个consumer会重复消费
            bootstrap_servers=None,  # 必须 'ip:port' or ['ip:port', 'ip:port' ...]
            hide_detail=None,  # 非必需 True(默认)/False 是否返回详细结果，dbfactory 自己封装功能

            # ------------------ kafka_consumer ------------------
            enable_auto_commit=None,  # 非必需 True(默认)/False 是否自动提交
            max_partition_fetch_bytes=None,  # 非必需 6291456(默认)
            auto_offset_reset=None,  # 非必需 "earliest"/""

            # ------------------ kafka_producer ------------------
            auto_flush=None,  # 非必需 True(默认)/False 是否自动推送，dbfactory 自己封装功能
            max_block_ms=None,  # 非必需 2000(默认)
            batch_size=None,  # 非必需 64384(默认)
            buffer_memory=None,  # 非必需 640554432(默认)
            compression_type=None,  # 非必需 'gzip'(默认)
            linger_ms=None,  # 非必需 2000(默认)
            api_version=None,  # 非必需 (0, 10)(非默认)

            # ------------------ others ------------------
            **kwargs  # 其他参数 上述没有写出，但是数据库本身支持的，可以通过此传入
    ):
        """
        暂时只支持 kwargs 传参方式，传入错误参数，可能导致数据库创建失败。
        """
        self._kwargs = kwargs

        # db_factory
        self.singleton_sign = kwargs.get("singleton_sign")  # 单例标记
        self._show_db_configure = show_db_configure  # 显示数据库初始化参数信息
        self._debug = debug  # 显示数据库初始化参数信息
        self.__init_arg("log", log)
        self.__init_arg("db_type", db_type)
        self._db_type = self._kwargs.get("db_type", 'mysql').upper().strip()
        self.__init_arg("retry_sleep_time", retry_sleep_time)
        self.__init_arg("use_time_out_decorator", use_time_out_decorator)
        self.__init_arg("action_time_out", action_time_out)
        self.__init_arg("action_warning_time", action_warning_time)  # 操作超时告警时间
        self.__init_arg("use_redis_local_cache", use_redis_local_cache)  # redis启用本地缓存
        self.__init_arg("only_read_from_mini_redis", only_read_from_mini_redis)  # redis启用本地缓存

        # common
        host = host or '0.0.0.0'
        self.__init_arg("host", host)
        self.__init_arg("port", port)
        self.__init_arg("username", username)
        self.__init_arg("password", password)
        self.__init_arg("db_name", db_name)
        self.__init_arg("connect_timeout", connect_timeout)

        # mysql
        self.__init_arg("autocommit", autocommit)
        self.__init_arg("charset", charset)
        self.__init_arg("use_unicode", use_unicode)
        self.__init_arg("sql_mode", sql_mode)
        self.__init_arg("cursorclass", cursorclass)

        # mysql_pool
        self.__init_arg("use_connection_pool", use_connection_pool)
        self.__init_arg("mincached", mincached)
        self.__init_arg("maxcached", maxcached)

        # kafka
        self.__init_arg("init_type", init_type)
        self.__init_arg("partition", partition)
        self.__init_arg("group_id", group_id)
        self.__init_arg("bootstrap_servers", bootstrap_servers)
        self.__init_arg("hide_detail", hide_detail)

        # kafka_consumer
        self.__init_arg("enable_auto_commit", enable_auto_commit)
        self.__init_arg("max_partition_fetch_bytes", max_partition_fetch_bytes)
        self.__init_arg("auto_offset_reset", auto_offset_reset)

        # kafka_producer
        self.__init_arg("auto_flush", auto_flush)
        self.__init_arg("max_block_ms", max_block_ms)
        self.__init_arg("batch_size", batch_size)
        self.__init_arg("buffer_memory", buffer_memory)
        self.__init_arg("compression_type", compression_type)
        self.__init_arg("linger_ms", linger_ms)
        self.__init_arg("api_version", api_version)

        # redis_cluster
        self.__init_arg("startup_nodes", startup_nodes)

        # process
        self.__init_log()
        self.__init_redis_local_cache()
        self.__init_sub()

    def __init_redis_local_cache(self):
        # redis # todo 本功能暂时不支持集群模式
        if self._kwargs["use_redis_local_cache"]:
            from DbFactory.util.mini_redis import MiniRedis
            self._kwargs["mini_redis"] = MiniRedis(
                cache_size=1000000, sync_period=100, log=self.log,
                db_type='redis', host=self._kwargs['host'], port=self._kwargs['port'],
                password=self._kwargs['password'], db_name=self._kwargs.get('db_name', 0)
            )

    def __init_arg(self, arg_name, arg_value):
        """将参数写入到 _kwargs，统一管理"""
        if arg_value is not None:  # 0 False 会被过滤。导致没有参数,
            self._kwargs[arg_name] = arg_value

    def __init_log(self):
        self.log = self._kwargs.get("log")
        if not self.log:
            # from dlog import DLog
            # self.log = self._kwargs["log"] = DLog(debug=self._debug, only_console=True).get_log
            import logging
            if self._debug:
                logging.basicConfig(level=logging.DEBUG)
            self.log = self._kwargs["log"] = logging

    def __init_sub(self):
        """初始化数据库基本流程"""
        self.__print_config()
        self.__init_db_client()

    def __check_client_file(self, __type):
        """
        检查数据库是否有支持文件
        """
        status = False
        for each in os.walk(dir_path):
            for name in each[2]:
                if name.endswith("py"):
                    if name.split('.')[0] == __type:
                        status = True
        if not status:
            __type = None
        assert __type, 'type error, Not support DB type: {}'.format(self._db_type)

    def __init_db_client(self):
        """
        init DB Client
        """
        __path = "DbFactory.client.{}_client".format(self._db_type.lower())
        self.__check_client_file(__path.split('.')[-1])
        self.client = getattr(import_module(__path), self.__make_class_name())(**self._kwargs)

    def __make_class_name(self):
        class_name = "{}Client".format(''.join([each.title() for each in self._db_type.split('_')]))
        return class_name

    def __print_config(self):
        self.log.info('singleton_sign:{}'.format(self.singleton_sign))
        if self._show_db_configure:
            self.log.info("============ DATABASE CONFIGURE =========================")
            self.log.info("DB_TYPE: %s" % self._db_type)
            self.log.info("DB_HOST: %s" % self._kwargs.get("host", "default or none"))
            self.log.info("DB_PORT: %s" % self._kwargs.get("port", "default or none"))
            self.log.info("DB_NAME: %s" % self._kwargs.get("db_name", "default or none"))
            self.log.info("DB_USER: %s" % self._kwargs.get("username", "default or none"))
            self.log.info("=========================================================")

    def __check_switch_db(self):
        if self._db_type in ["redis_cluster"]:
            raise TypeError("this db：{}，not support switch db action".format(self._db_type))
        if self._kwargs.get("use_connection_pool"):
            raise TypeError("db pool：{}，not support switch db action".format(self._db_type))

    # --------------------------- 自动反射 ---------------------------------
    def __getattr__(self, item):
        """如果没有遇到没有封装的命令，会自动反射"""
        return partial(self.client.generation_func, item)

    # --------------------------- base func -------------------------------
    def __del__(self):
        """整条链路中，只需要有一个析构函数，client 只需要提供close方法。如果client 提供析构，会导致数据库被关闭2次，报错"""
        # todo 定位到问题了，是下面的close函数，直接调用的是 原本的 client，（这个版本修复）
        # todo 暂时关闭析构函数。确保稳定性
        # self.close()
        # if self._kwargs.get("mini_redis"):
        #     self._kwargs["mini_redis"].close()

    def close(self):
        """切换 db 会调用 close，小心close 里面的方法"""
        try:
            self.log.info('close {}'.format(self.singleton_sign))
            if self._db_type in ['KAFKA']:
                self.client.client__.close(timeout=1, info='when __del__')
            elif self._db_type in ['MYSQL']:
                self.client.client__.close(info='when __del__')
            else:
                self.client.client__.close()
        except AttributeError:
            pass

    @property
    def origin_client(self):
        """测试功能，直接动态反射出db， """
        self.log.warning('use origin_client 直接反射出 db 暂时没有 异常处理加成')
        if self._db_type in {"MYSQL", "KAFKA"}:
            return self.client.client__.origin_client(self.singleton_sign)
        else:
            return self.client.client__

    # --------------------------- 命令封装 ---------------------------------
    def switch_db(self, db_name):
        """切换db"""
        self.__check_switch_db()
        self.log.info("switch db to: {}".format(db_name))
        self._kwargs["db_name"] = db_name
        self.close()
        self.__init_sub()
