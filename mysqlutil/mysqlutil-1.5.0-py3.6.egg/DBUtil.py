# -*- coding:utf-8 -*-
import sys
import pymysql.cursors
from pymysql.constants import CLIENT
import queue
import time
import threading
import logging
import logging.handlers
import traceback


def init_log(log_name='mysqlutil'):
    """
    init module log
    :param log_name:
    :return:
    """
    logger = logging.getLogger(name=log_name)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s')
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger


def escape_name(s):
    return f"`{s.replace('`', '``')}`"


def query(func):
    def wrapper(self, *args, **kwargs):
        conn = self.get_conn()
        kwargs['conn'] = conn

        try:
            ret = func(self, *args, **kwargs)
        except GeneratorExit:
            if conn:
                conn.commit()
            return
        except:
            self.log.error(traceback.format_exc())
            return False
        finally:
            self.recycle(conn)
        return ret

    return wrapper


class DB:

    def __init__(self, conn_info=None, max_cached=5, idle_time=300, log=None):
        """
        init mysql util
        :param conn_info:
            {
                "host": "localhost",
                "port": 3306,
                "user": "",
                "password": "",
                "db": "",
                "charset": "utf8"
            }
        :param max_cached:
        :param idle_time:
        :param log:
        """
        if not log:
            self.log = init_log()
        else:
            self.log = log

        self._conn_info = conn_info
        if not self._conn_info:
            self.log.error('Pls provide connection information')
            sys.exit(1)
        for k in ['host', 'user', 'password', 'db']:
            if k not in self._conn_info:
                self.log.error(f'need {k} configuration')
                sys.exit(1)

        #
        self._max_cached = min(max_cached, 20)
        self._max_cached = max(self._max_cached, 1)
        self._idle_time = max(idle_time, 300)
        self._idle_time = min(self._idle_time, 1800)
        self.pool = queue.Queue(maxsize=self._max_cached)

        # check pool
        t = threading.Thread(target=self._check_pool)
        t.setDaemon(True)
        t.start()

    def _create_conn(self):
        conn = pymysql.connect(
            host=self._conn_info['host'],
            port=self._conn_info['port'],
            user=self._conn_info['user'],
            password=self._conn_info['password'],
            db=self._conn_info['db'],
            charset=self._conn_info['charset'],
            cursorclass=pymysql.cursors.DictCursor,
            client_flag=CLIENT.MULTI_STATEMENTS
        )

        return conn

    def get_conn(self):
        try:
            return self.pool.get_nowait()[0]
        except queue.Empty:
            return self._create_conn()

    def recycle(self, conn):
        """
        recycle connection
        :param conn:
        :return:
        """
        if not conn:
            return
        try:
            self.pool.put_nowait((conn, time.time()))
        except queue.Full:
            conn.close()

    def _check_pool(self):
        while True:
            time.sleep(10)
            self._check_alive()

    def _check_alive(self):
        try:
            conn, last_time = self.pool.get_nowait()
        except queue.Empty:
            return

        try:
            conn.ping(reconnect=False)
            if time.time() - last_time > self._idle_time:
                conn.close()
            else:
                try:
                    self.pool.put_nowait((conn, last_time))
                except queue.Full:
                    conn.close()
        except pymysql.err.Error:
            self.log.error(traceback.format_exc())
        except:
            self.log.error(traceback.format_exc())

    @query
    def fetchall(self, sql, data=(), **kwargs):
        """
        Fetch all the rows
        :param sql:
        :param data:
        :return: False - DB Error | () - No result | [{field1: value1, field2: value2}, ...]
        """

        conn = kwargs['conn']
        with conn.cursor() as cur:
            if not data:
                cur.execute(sql)
            else:
                cur.execute(sql, data)
            result = cur.fetchall()
        conn.commit()

        return result

    @query
    def fetchfirst(self, sql, data=(), **kwargs):
        """
        Fetch the first row
        :param sql:
        :param data:
        :return: False - DB Error | None - No Result | {field1: value1, field2: value2}
        """

        conn = kwargs['conn']
        with conn.cursor() as cur:
            if not data:
                cur.execute(sql)
            else:
                cur.execute(sql, data)
            result = cur.fetchone()
        conn.commit()

        return result

    @query
    def fetchone(self, sql, data=(), **kwargs):
        """
        Fetch the next row
        :param sql:
        :param data:
        :return: iterable, False - DB Error | {field1: value1, field2: value2}
        """

        conn = kwargs['conn']
        with conn.cursor() as cur:
            if not data:
                cur.execute(sql)
            else:
                cur.execute(sql, data)
        for _ in range(cur.rowcount):
            yield cur.fetchone()
        conn.commit()

    @query
    def fetchmany(self, sql, num, data=(), **kwargs):
        """
        Fetch several rows
        :param sql:
        :param num:
        :param data:
        :return: iterable, False - DB Error | [{field1: value1, field2: value2}, ...]
        """

        conn = kwargs['conn']
        with conn.cursor() as cur:
            if not data:
                cur.execute(sql)
            else:
                cur.execute(sql, data)
        # Python 3.8 syntax walrus
        # while result := cur.fetchmany(num):
        #     yield result
        while True:
            result = cur.fetchmany(num)
            if not result:
                break
            yield result
        conn.commit()

    @query
    def execute(self, sql, data=(), **kwargs):
        """
        Execute a query
        :param sql: Query to execute.
        :param data:
        :return: False - DB Error | True - execute successfully
        """

        conn = kwargs['conn']
        with conn.cursor() as cur:
            if not data:
                cur.execute(sql)
            else:
                cur.execute(sql, data)
        conn.commit()

        return True

    @query
    def executemany(self, sql, data_list, **kwargs):
        """
        Run several data against one query
        :param sql: query to execute on server
        :param data_list: Sequence of sequences.  It is used as parameter.
        :return: False - DB Error | True - execute successfully
        """

        if not isinstance(data_list, list):
            return False

        conn = kwargs['conn']
        with conn.cursor() as cur:
            cur.executemany(sql, data_list)
        conn.commit()

        return True

    @query
    def insert(self, tbl, data, **kwargs):
        """
        Insert one row into table
        :param tbl:
        :param data:
        :return: False - DB Error | True - insert successfully
        """

        if not isinstance(data, dict):
            return False

        names = list(data)
        cols = ', '.join(map(escape_name, names))
        placeholders = ', '.join([f'%({name})s' for name in names])
        query = f'INSERT INTO `{tbl}` ({cols}) VALUES ({placeholders})'

        conn = kwargs['conn']
        with conn.cursor() as cur:
            cur.execute(query, data)
        conn.commit()
        return True

    @query
    def insertmany(self, tbl, data, **kwargs):
        """
        Insert one row into table
        :param tbl:
        :param data:
        :return: False - DB Error | True - insert successfully
        """

        result_list = []

        if not isinstance(data, list):
            return False

        for row in data:
            result_list.append(self.insert(tbl, row))

        return all(result_list)
