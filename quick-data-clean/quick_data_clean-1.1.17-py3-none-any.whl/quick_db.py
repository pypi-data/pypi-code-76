# -*- coding: utf-8 -*-
import abc
import sqlite3
import pyodbc


class DBCommon(metaclass=abc.ABCMeta):

    username = ""
    password = ""
    conn_str = ""
    conn = None

    def query_recordset_count(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)

        result = cursor.fetchall()
        cursor.close()
        return len(result)

    def query(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)

        field_name_list = (self.get_query_field_name(cursor))

        for row in cursor.fetchall():
            field_dict = {}
            field_index = 0
            for field in row:
                field_dict[field_name_list[field_index]] = field
                field_index = field_index + 1
            yield field_dict

        cursor.close()

    def get_drive(self, tag):
        drive_list = [x for x in pyodbc.drivers() if x.startswith(tag)]

        if len(drive_list) == 1:
            return drive_list[0]
        else:
            maxlength = max(len(s) for s in drive_list)
            longest_str_list = [s for s in drive_list if len(s) == maxlength]
            return longest_str_list[0]

    def query_by_index(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)

        for row in cursor.fetchall():
            yield row
        cursor.close()

    def query_show_data(self, sql):

        cursor = self.conn.cursor()
        cursor.execute(sql)

        field_name_list = (self.get_query_field_name(cursor))
        yield field_name_list

        for row in cursor.fetchall():
            yield row

        cursor.close()

    def begin_trans(self):

        if self.is_begin_trains:
            raise Exception("Transaction operation has been started")

        if self.is_excel:
            raise Exception("Excel does not support "
                            "transaction operations")

        self.is_begin_trains = True

    def rollback_trans(self):

        if not self.is_begin_trains:
            raise Exception("The transaction operation is not started or the "
                            "transaction operation has been processed")

        self.is_begin_trains = False

        self.conn.rollback()

    def commit_trans(self):

        if not self.is_begin_trains:
            raise Exception("The transaction operation is not started or the "
                            "transaction operation has been processed")

        self.is_begin_trains = False

        if self.is_sqlite:
            self.conn.commit()
        else:
            cursor = self.conn.cursor()
            cursor.commit()

    def execute_sql(self, sql, is_sqlite=False):

        cursor = self.conn.cursor()
        effect_count = self.conn.execute(sql)
        if is_sqlite:
            if not self.is_begin_trains:
                self.conn.commit()
        else:
            if not self.is_begin_trains:
                cursor.commit()
                cursor.close()

        return effect_count

    @abc.abstractmethod
    def connect(self, is_excel=False, is_sqlite3=False):
        self.close()
        if is_excel:
            self.conn = pyodbc.connect(self.conn_str, autocommit=True)
            self.is_excel = True
        else:
            self.is_excel = False
            if is_sqlite3:
                self.conn = sqlite3.connect(self.conn_str)
                self.is_sqlite = True
            else:
                self.conn = pyodbc.connect(self.conn_str)
                self.is_sqlite = False

        self.is_begin_trains = False

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def get_query_field_name(self, cursor):
        name_list = []
        for tup in cursor.description:
            name_list.append(tup[0])

        return name_list

    def get_field_name(self, cursor, tablename):
        name_list = []
        for row in cursor.columns(table=tablename):
            name_list.append(row.column_name)

        return name_list


class Oracle(DBCommon):

    odbc_name = ""

    def __init__(self, odbc_name, username, password):
        self.odbc_name = odbc_name
        self.username = username
        self.password = password

    def connect(self):
        self.conn_str = "DSN={0};UID={1};pwd={2};".format(self.odbc_name,
                                                          self.username,
                                                          self.password)
        super().connect()


class SqlServer(DBCommon):

    serverinfo = ""
    db_name = ""

    def __init__(self, serverinfo, db_name, username, password):
        self.serverinfo = serverinfo
        self.username = username
        self.password = password
        self.db_name = db_name

    def connect(self):
        self.conn_str = "SERVER={0};DATABASE={1};UID={2};PWD={3}".format(
            self.serverinfo,
            self.db_name,
            self.username,
            self.password)
        drive_str = "DRIVER={SQL Server};"
        self.conn_str = drive_str + self.conn_str
        super().connect()


class Access(DBCommon):
    """docstring for ClassName"""

    db_path = ""

    def __init__(self, db_path, password, username):
        self.username = username
        self.password = password
        self.db_path = db_path

    def connect(self):
        self.conn_str = "DBQ={0};Uid={1};Pwd={2};".format(
            self.db_path,
            self.username,
            self.password)
        drive_str = "DRIVER={{{0}}};".format(super().get_drive("Microsoft Access Driver"))

        self.conn_str = drive_str + self.conn_str
        super().connect()


class Excel(DBCommon):
    """docstring for ClassName"""

    db_path = ""

    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        self.conn_str = "ReadOnly=0;DBQ={0};".format(self.db_path)
        drive_str = (
            "DRIVER={Microsoft Excel Driver (*.xls, *.xlsx, "
            "*.xlsm, *.xlsb)};")

        drive_str = "DRIVER={{{0}}};".format(super().get_drive("Microsoft Excel Driver"))
        self.conn_str = drive_str + self.conn_str
        super().connect(True)


class MySql(DBCommon):
    """docstring for ClassName"""

    serverinfo = ""
    db_name = ""
    port = ""
    odbc_name = ""
    drive_info = ""
    conn_type = 0

    def __init__(self, *args):
        if len(args) == 5:
            self.serverinfo = args[0]
            self.port = args[1]
            self.db_name = args[2]
            self.username = args[3]
            self.password = args[4]
            self.drive_info = "MySQL ODBC 8.0 Unicode Driver"
            self.conn_type = 2
        elif len(args) == 6:
            self.serverinfo = args[0]
            self.port = args[1]
            self.db_name = args[2]
            self.username = args[3]
            self.password = args[4]
            self.drive_info = args[5]
            self.conn_type = 2
        elif len(args) == 1:
            self.odbc_name = args[0]
            self.conn_type = 1
        else:
            raise Exception("MySql init need 1 or 5 parameters")

    def connect(self):
        if self.conn_type == 1:
            self.conn_str = "DSN=" + self.odbc_name
        else:
            self.conn_str = ("SERVER={0};Port={1};DATABASE={2};User={3};"
                             "Password={4};Option=3;").format(
                self.serverinfo,
                self.port,
                self.db_name,
                self.username,
                self.password)
            drive_str = "DRIVER={{{0}}};".format(super().get_drive("MySQL ODBC"))
            self.conn_str = drive_str + self.conn_str

        super().connect()


class Sqlite3(DBCommon):
    """docstring for ClassName"""

    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):

        self.conn_str = self.db_path
        super().connect(False, True)

    def execute_sql(self, sql):
        super().execute_sql(sql, True)


class DataBaseSingleton(object):
    """docstring for ClassName"""

    db_obj = None

    def __init__(self, arg):
        self.arg = arg

    @classmethod
    def connect_oracle(cls, odbc_name, username, password):
        cls.db_obj = Oracle(odbc_name, username, password)
        cls.db_obj.connect()

    @classmethod
    def connect_sqlserver(cls, serverinfo, db_name, username, password):
        cls.db_obj = SqlServer(serverinfo, db_name, username, password)
        cls.db_obj.connect()

    @classmethod
    def connect_access(cls, db_path, password="", username="admin"):
        cls.db_obj = Access(db_path, password, username)
        cls.db_obj.connect()

    @classmethod
    def connect_excel(cls, db_path):
        cls.db_obj = Excel(db_path)
        cls.db_obj.connect()

    @classmethod
    def connect_mysql(cls, serverinfo, port, db_name, username, password):
        cls.db_obj = MySql(serverinfo, port, db_name, username, password)
        cls.db_obj.connect()

    @classmethod
    def connect_mysql_by_odbc(cls, odbc_name):
        cls.db_obj = MySql(odbc_name)
        cls.db_obj.connect()

    @classmethod
    def query(cls, sql):
        for row in cls.db_obj.query(sql):
            yield row

    @classmethod
    def execute_sql(cls, sql):
        return cls.db_obj.execute_sql(sql)

    @classmethod
    def close(cls):
        cls.db_obj.close()


class DataBase(object):
    """docstring for ClassName"""

    db_obj = None

    def __init__(self):
        pass

    def connect_oracle(self, odbc_name, username, password):
        self.db_obj = Oracle(odbc_name, username, password)
        self.db_obj.connect()

    def connect_sqlserver(self, serverinfo, db_name, username, password):
        self.db_obj = SqlServer(serverinfo, db_name, username, password)
        self.db_obj.connect()

    def connect_access(self, db_path, password="", username="admin"):
        self.db_obj = Access(db_path, password, username)
        self.db_obj.connect()

    def connect_excel(self, db_path):
        self.db_obj = Excel(db_path)
        self.db_obj.connect()

    def connect_mysql(self, *args):
        self.db_obj = MySql(*args)
        self.db_obj.connect()

    def connect_sqlite(self, db_path=":memory:"):
        self.db_obj = Sqlite3(db_path)
        self.db_obj.connect()

    def query(self, sql):
        for row in self.db_obj.query(sql):
            yield row

    def query_by_index(self, sql):
        for row in self.db_obj.query_by_index(sql):
            yield row

    def query_show_data(self, sql):
        query_result = self.db_obj.query_show_data(sql)

        columns_name = next(query_result)

        from quick_data_clean.quick_gui import DataViewWidget
        tv = DataViewWidget()
        tv.show_treeview(sql, columns_name, query_result)

    def execute_sql(self, sql):
        return self.db_obj.execute_sql(sql)

    def begin_trans(self):
        self.db_obj.begin_trans()

    def commit_trans(self):
        self.db_obj.commit_trans()

    def rollback_trans(self):
        self.db_obj.rollback_trans()

    def close(self):
        self.db_obj.close()

    def query_recordset_count(self, sql):
        return self.db_obj.query_recordset_count(sql)
