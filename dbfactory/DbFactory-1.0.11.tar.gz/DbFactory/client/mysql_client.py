#!/usr/bin/env python
# coding=utf-8
"""
mysql 基础类，封装pymysql

"""

import time
import pymysql
import traceback

try:
    from dbutils.pooled_db import PooledDB  # 2.0.0 版本    todo 确定区别在哪里去？
except ImportError:
    from DBUtils.PooledDB import PooledDB  # 1.0.2 版本

from .db_base import DbBase

"""
注意：如果使用事务，需要关闭自动提交。

todo 传入 cursor时，规定下返回结果。
"""


class MysqlClient(DbBase):
    """这个看成mysql 最小的客户端。类似redis, 这个里面，反射出去的任何方法，都会被 添加上 异常处理。"""

    def __init__(self, **kwargs):
        super(MysqlClient, self).__init__(**kwargs)
        self.log.info("mysql_kwargs_log:{}".format(kwargs))
        self.client_ = None
        self.__init_base_args()
        self.singleton_sign = ''
        self._last_use_time = time.time()
        self._reconnect()

    def __init_base_args(self):
        """"""
        self._host = self._kwargs.pop('host', '0.0.0.0')
        self._port = int(self._kwargs.pop('port', 3306))
        """
        # todo 暂时不支持线程池。有很多问题。（例如，数据库单例模式问题，数据库切换问题。）
        实际上，也不需要支持线程池，因为dbfactory 本身就是轻量化。 dbfactory为每个单例维持一个connection。（tornado 多线程怎么处理？）
        """
        self._use_connection_pool = self._kwargs.pop('use_connection_pool', True)  # 是否开启连接池
        """
        不开启连接池，每个mysql 实例使用一个 connection，每次调用时，获取cursor，调用结束释放cursor。程序会自动确保 connection 连接正常。
        开启连接池，连接池会自动维持一个连接池。连接池一般使用在多线程状态下。（限定连接池最大连接数）
        """

        self._new_kwargs = {
            "user": self._kwargs.pop('username', 'root'),
            "passwd": self._kwargs.pop('password', 'root'),
            "db": str(self._kwargs.pop('db_name', 'siterec_dashboard')),
            "charset": self._kwargs.pop('charset', 'utf8'),
            "connect_timeout": self._kwargs.pop('connect_timeout', 10),
            "sql_mode": self._kwargs.pop('sql_mode', None),
            "use_unicode": self._kwargs.pop('use_unicode', True)  # 默认使用Unicode字符,
        }

        time_zone = self._kwargs.pop('time_zone', None)  # time_zone = "+0:00"   如果不指定，则使用当地服务器时间
        if time_zone:
            self._new_kwargs["init_command"] = 'SET time_zone="{}"'.format(time_zone),  # 时区
        self._init_cursorclass()
        self._autocommit = self._kwargs.pop('autocommit', True)
        # We accept a path to a MySQL socket file or a host(:port) string
        if "/" in self._host:
            self._new_kwargs["unix_socket"] = self._host
        else:
            self.socket = None
            pair = self._host.split(":")
            if len(pair) == 2:
                self._new_kwargs["host"] = pair[0]
                self._new_kwargs["port"] = int(pair[1])
            else:
                self._new_kwargs["host"] = self._host
                self._new_kwargs["port"] = self._port

        self.client_args = {**self._kwargs, **self._new_kwargs}

    def _init_cursorclass(self):
        self._cursorclass = self._kwargs.pop('cursorclass', 'cursor')
        if isinstance(self._cursorclass, str):
            self._cursorclass = self._cursorclass.lower()
            if self._cursorclass == 'cursor':
                self._new_kwargs["cursorclass"] = pymysql.cursors.Cursor
            elif self._cursorclass == 'dictcursor':
                self._new_kwargs["cursorclass"] = pymysql.cursors.DictCursor
            elif self._cursorclass == 'sscursor':
                self._new_kwargs["cursorclass"] = pymysql.cursors.SSCursor
            elif self._cursorclass == 'ssdictcursor':
                self._new_kwargs["cursorclass"] = pymysql.cursors.SSDictCursor
            elif self._cursorclass == 'dictcursormixin':
                self._new_kwargs["cursorclass"] = pymysql.cursors.DictCursorMixin
            else:
                raise TypeError('not support cursorclass')
        elif isinstance(self._cursorclass, object):
            self._new_kwargs["cursorclass"] = self._cursorclass
            if self._cursorclass == pymysql.cursors.Cursor:
                self._cursorclass = 'cursor'
            elif self._cursorclass == pymysql.cursors.DictCursor:
                self._cursorclass = 'dictcursor'
            elif self._cursorclass == pymysql.cursors.SSCursor:
                self._cursorclass = 'sscursor'
            elif self._cursorclass == pymysql.cursors.SSDictCursor:
                self._cursorclass = 'ssdictcursor'
            elif self._cursorclass == pymysql.cursors.DictCursorMixin:
                self._cursorclass = 'dictcursormixin'
            else:
                raise TypeError('not support cursorclass')
        else:
            raise TypeError('cursorclass type error')

    def _get_connection_pool(self):
        """
        @summary: 类方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        # 默认 cursor_class, 字典类型  （todo 产品封装里面，使用 dict  ）
        if getattr(self, "_db", None) is None:  # 如果使用连接池，连接池本身会保证连接可用。所以不需要重新实例化。
            db = PooledDB(
                creator=pymysql,
                mincached=int(self._kwargs.pop('mincached', 1)),
                maxcached=int(self._kwargs.pop('maxcached', 20)),
                maxconnections=int(self._kwargs.pop('maxconnections', 30)),
                setsession=self._kwargs.pop('setsession', ['SET AUTOCOMMIT = 1']),
                ping=int(self._kwargs.pop('ping', 7)),  # 稳定性优先，7 = aways
                maxusage=int(self._kwargs.pop('maxusage', 3)),  # 每个链接，使用 3 次后废弃
                **self.client_args
            )
            self.client_ = db.connection()
            self.log.info("=== 连接池初始化成功 ===\n")
        else:
            self.log.info("=== 连接池已存在 ===\n")

    def _reconnect(self, count=0):
        """Closes the existing database connection and re-opens it."""
        try:
            self.close(info="when create connection")
            self.log.info("=== mysql kwargs is:{} ===".format(self.client_args))  # 部分日志不规范，无法打印
            if self._use_connection_pool:
                self._get_connection_pool()
            else:
                self.log.info("=== db connect try initialized ===\n")
                self.client_ = pymysql.connect(**self.client_args)
                self.log.info("=== db connect initialized success ===\n")
                if self._autocommit is True:
                    self.log.info("=== set autocommit is True ===\n")
                    self.client_.autocommit(self._autocommit)
            self.log.info("mysql connected success !")
        except pymysql.err.OperationalError:
            count += 1
            self.log.error("mysql OperationalError: \n retry connect {}\n {}".format(count, traceback.format_exc()))
            time.sleep(self._retry_sleep_time * 3)
            self._reconnect(count)
        except Exception as e:
            count += 1
            self.log.error("retry connect {}\n {}".format(count, traceback.format_exc()))
            time.sleep(self._retry_sleep_time)
            self._reconnect(count)

    def _execute(self, cursor, query, parameters, kwparameters):
        try:
            return cursor.execute(query, kwparameters or parameters)
        except Exception as e:
            self.log.error(e)
            raise

    def _cursor(self):
        """
        如果 写成静态方法，反射到外部时，表示为 functools.partial，不能直接使用。
        这里不写成静态方法，为了可读性，以及统一性，以及方便测试。
        """
        return self.client_.cursor()

    def rollback(self):
        self.client_.rollback()

    def _close_cursor(self):
        """这里需要使用try，否则会进入死循环"""
        try:
            if self._cursor() is not None:  # 释放游标
                self._cursor().close()
        except:
            self.log.error(traceback.format_exc())

    def close(self, info=''):
        """Closes this database connection."""
        self.log.info('{} {} do close'.format(info, self.singleton_sign))
        if getattr(self, "_db", None) is not None:  # 优点，不用在初始化时，定义 _db.同时会带来一个问题，会优先触发类中的getattr导致意外发生
            self._close_cursor()
            self.client_.close()  # 如果是连接池，则归还连接/ 非连接池则断开连接，下次执行需要再去连接池取
            self.client_ = None

    def iter(self, query, *parameters, **kwparameters):
        """Returns an iterator for the given query and parameters."""
        cursor = pymysql.cursors.SSCursor(self.client_)
        try:
            self._execute(cursor, query, parameters, kwparameters)
            column_names = [d[0] for d in cursor.description]
            for row in cursor:
                yield Row(list(zip(column_names, row)))
        finally:
            cursor.close()

    def query(self, query, *parameters, **kwparameters):
        """Returns a row list for the given query and parameters."""
        cursor = self._cursor()  # 每次动态获取，使用完成后释放
        try:
            self._execute(cursor, query, parameters, kwparameters)
            if self._use_connection_pool:
                return cursor.fetchall()
            else:
                if self._cursorclass in ['cursor', 'sscursor']:
                    column_names = [d[0] for d in cursor.description]
                    return [list(zip(column_names, row)) for row in cursor]
                else:
                    return cursor.fetchall()
        finally:
            cursor.close()  # 释放游标

    def get(self, query, *parameters, **kwparameters):
        """Returns the (singular) row returned by the given query.
        If the query has no results, returns None.  If it has
        more than one result, raises an exception.
        """
        rows = self.query(query, *parameters, **kwparameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise TypeError("Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    # rowcount is a more reasonable default return value than lastrowid,
    # but for historical compatibility execute() must return lastrowid.
    def execute(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""
        return self.execute_lastrowid(query, *parameters, **kwparameters)

    def execute_lastrowid(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def execute_rowcount(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the rowcount from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany(self, query, parameters):
        """Executes the given query against all the given param sequences.
        We return the lastrowid from the query.
        """
        return self.executemany_lastrowid(query, parameters)

    def executemany_lastrowid(self, query, parameters):
        """Executes the given query against all the given param sequences.
        We return the lastrowid from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def executemany_rowcount(self, query, parameters):
        """Executes the given query against all the given param sequences.
        We return the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    # -------------- 别名方法 --------------
    select = get
    selectmany = query

    update = delete = execute_rowcount
    updatemany = executemany_rowcount

    insert = execute_lastrowid
    insertmany = executemany_lastrowid


class Row(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


if pymysql is not None:
    # todo 这个后期处理
    # Alias some common MySQL exceptions
    IntegrityError = pymysql.IntegrityError
    OperationalError = pymysql.OperationalError
