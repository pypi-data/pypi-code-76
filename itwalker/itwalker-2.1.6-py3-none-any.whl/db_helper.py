import pymysql, psycopg2
from dbutils.pooled_db import PooledDB
import psycopg2.extras

Log = None


class Singleton(object):
    def __new__(cls, conf, log):
        db = conf.get("db", "")
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            obj = orig.__new__(cls)
            obj.POOL = PooledDB(pymysql, maxconnections=4, setsession=["SET GLOBAL time_zone = '+8:00'"], **conf)
            cls._instance = {db: obj}
        else:
            if db not in cls._instance:
                orig = super(Singleton, cls)
                obj = orig.__new__(cls)
                obj.POOL = PooledDB(pymysql, maxconnections=4, setsession=["SET GLOBAL time_zone = '+8:00'"], **conf)
                cls._instance[db] = obj
        return cls._instance[db]


class Singleton2(object):
    def __new__(cls, conf, log):
        db = conf.get("db", "")
        if not hasattr(cls, '_instance'):
            orig = super(Singleton2, cls)
            obj = orig.__new__(cls)
            obj.POOL = PooledDB(creator=psycopg2, maxconnections=4, **conf)
            cls._instance = {db: obj}
        else:
            if db not in cls._instance:
                orig = super(Singleton2, cls)
                obj = orig.__new__(cls)
                obj.POOL = PooledDB(creator=psycopg2, maxconnections=4, **conf)
                cls._instance[db] = obj
        return cls._instance[db]


class MysqlHelper(Singleton):
    def __new__(cls, conf, log):
        return super(MysqlHelper, cls).__new__(cls, conf, log)

    def __init__(self, conf, log):
        self.Log = log

    def createConn(self, *format):
        # 创建引擎
        conn = self.POOL.connection()
        if format:
            cursor = conn.cursor()
        else:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cursor

    def executeParam(self, cursor, sql, Param):
        if Param:
            Param = Param[0]
        else:
            Param = None
        if isinstance(Param, dict):
            self.Log.debug(sql % Param)
            return cursor.execute(sql, Param)
        elif isinstance(Param, tuple):
            self.Log.debug(sql % Param)
            return cursor.execute(sql % Param)
        else:
            self.Log.debug(sql)
            return cursor.execute(sql)

    def QueryT(self, sql, *Param):
        try:
            conn, cursor = self.createConn("tuple")
            self.executeParam(cursor, sql, Param)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            if not result:
                return []
            if len(result) > 0:
                flag = False
                for k, v in result[0].items():
                    if not v is None:
                        flag = True
                        break
                if flag:
                    return result
                else:
                    return []
            else:
                return []
        except Exception as e:
            self.Log.error(','.join(e.args[:]))
            raise Exception(','.join(e.args[:]))

    def Query(self, sql, *Param):
        try:
            conn, cursor = self.createConn()
            self.executeParam(cursor, sql, Param)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            if not result:
                return []
            if len(result) > 0:
                flag = False
                for k, v in result[0].items():
                    if not v is None:
                        flag = True
                        break
                if flag:
                    return result
                else:
                    return []
            else:
                return []
        except Exception as e:
            self.Log.error(','.join(e.args[:]))
            raise Exception(','.join(e.args[:]))

    def QuerySingle(self, sql, *Param):
        try:
            conn, cursor = self.createConn()
            self.executeParam(cursor, sql, Param)
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result:
                flag = False
                for k, v in result.items():
                    if not v is None:
                        flag = True
                        break
                if flag:
                    return result
                else:
                    return None
            else:
                return None
        except Exception as e:
            self.Log.error(','.join(e.args[:]))
            raise Exception(','.join(e.args[:]))

    def QuerySingleT(self, sql, *Param):
        try:
            conn, cursor = self.createConn('tuple')
            self.executeParam(cursor, sql, Param)
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result:
                flag = False
                for k, v in result.items():
                    if not v is None:
                        flag = True
                        break
                if flag:
                    return result
                else:
                    return None
            else:
                return None
        except Exception as e:
            self.Log.error(','.join(e.args[:]))
            raise Exception(','.join(e.args[:]))

    def ExcuteSql(self, sql, *Param):
        conn = None
        try:
            conn, cursor = self.createConn()
            self.executeParam(cursor, sql, Param)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            conn.rollback()
            self.Log.error(','.join(e.args[:]))
            raise Exception(','.join(e.args[:]))

    def ExecuteMany(self, sql, Param):
        conn = None
        try:
            if not isinstance(Param, list):
                raise Exception("Param must is list")
            else:
                conn, cursor = self.createConn()
                cursor.executemany(sql, Param)
                conn.commit()
                cursor.close()
                conn.close()
                return True
        except Exception as e:
            conn.rollback()
            self.Log.error(','.join(e.args[:]))
            raise Exception(','.join(e.args[:]))


class PgHelper(Singleton2):
    def __new__(cls, conf, log):
        return super(PgHelper, cls).__new__(cls, conf, log)

    def __init__(self, conf, log):
        self.Log = log

    def createConn(self, *format):
        # 创建引擎
        conn = self.POOL.connection()
        if format:
            cursor = conn.cursor()
        else:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return conn, cursor

    def executeParam(self, cursor, sql, Param):
        if Param:
            return cursor.execute(sql, Param[0])
        else:
            return cursor.execute(sql)

    def QueryT(self, sql, *Param):
        try:
            conn, cursor = self.createConn("tuple")
            self.executeParam(cursor, sql, Param)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            if not result:
                return []
            if len(result) > 0:
                flag = False
                for k, v in result[0].items():
                    if not v is None:
                        flag = True
                        break
                if flag:
                    return result
                else:
                    return []
            else:
                return []
        except Exception as e:
            self.Log.error(','.join(e.args[:]))
            raise Exception(','.join(e.args[:]))

    def Query(self, sql, *Param):
        try:
            conn, cursor = self.createConn()
            self.executeParam(cursor, sql, Param)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            if not result:
                return []
            if len(result) > 0:
                flag = False
                for k, v in result[0].items():
                    if not v is None:
                        flag = True
                        break
                if flag:
                    result = [dict(v) for v in result]
                    return result
                else:
                    return []
            else:
                return []
        except Exception as e:
            self.Log.error(','.join(e.args[:]))
            raise Exception(','.join(e.args[:]))

    def QuerySingle(self, sql, *Param):
        try:
            conn, cursor = self.createConn()
            self.executeParam(cursor, sql, Param)
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result:
                flag = False
                for k, v in result.items():
                    if not v is None:
                        flag = True
                        break
                if flag:
                    result = dict(result)
                    return result
                else:
                    return None
            else:
                return None
        except Exception as e:
            self.Log.error(','.join(e.args[:]))
            raise Exception(','.join(e.args[:]))

    def QuerySingleT(self, sql, *Param):
        try:
            conn, cursor = self.createConn('tuple')
            self.executeParam(cursor, sql, Param)
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result:
                flag = False
                for k, v in result.items():
                    if not v is None:
                        flag = True
                        break
                if flag:
                    return result
                else:
                    return None
            else:
                return None
        except Exception as e:
            self.Log.error(','.join(e.args[:]))
            raise Exception(','.join(e.args[:]))

    def ExcuteSql(self, sql, *Param):
        conn = None
        try:
            conn, cursor = self.createConn()
            self.executeParam(cursor, sql, Param)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            conn.rollback()
            self.Log.error(','.join(e.args[:]))
            raise Exception(','.join(e.args[:]))

    def ExecuteMany(self, sql, Param):
        conn = None
        try:
            if not isinstance(Param, list):
                raise Exception("Param must is list")
            else:
                conn, cursor = self.createConn()
                cursor.executemany(sql, Param)
                conn.commit()
                cursor.close()
                conn.close()
                return True
        except Exception as e:
            conn.rollback()
            self.Log.error(','.join(e.args[:]))
            raise Exception(','.join(e.args[:]))
