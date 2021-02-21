import pymysql
from easysql.setting import *


class databaseSQL:
    """
    数据库类
    """

    def __init__(self, database: str, user="root", passwd="123456", host="127.0.0.1"):
        self.database = database
        self.user = user
        self.passwd = passwd
        self.host = host

    def connect(self):
        database = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.database)
        return database


class tableSQL:
    """
    数据表类
    """

    def __init__(self, tableName: str, engine="InnoDB", charset="utf8mb4"):
        self.tableName = tableName
        self.engine = engine
        self.charset = charset
        self.index_i = 0
        self.attributeDic = {}
        self.primaryKeys = []

    def reset(self, tableSQL_table):
        """
        将值替换为目标数据表（方便等于操作）
        """
        if type(tableSQL_table) == tableSQL:
            self.tableName = tableSQL_table.tableName
            self.engine = tableSQL_table.engine
            self.charset = tableSQL_table.charset
            self.index_i = tableSQL_table.index_i
            self.attributeDic = tableSQL_table.attributeDic
            self.primaryKeys = tableSQL_table.primaryKeys
        else:
            print("%s无法替换为%s" % (self.tableName, tableSQL_table))

    def addAttribute(
            self, aName: str,
            aType: str,
            aLong=255,
            default=None,
            isNotNull=False,
            isPrimaryKey=False,
            isAuto=False,
            isUnique=False, isUnsigned=False
    ):
        """
        添加字段
        :param aName: 字段名
        :param aType: 字段类型
        :param aLong: 字段长度
        :param default: 字段默认值
        :param isNotNull: 字段非空设置
        :param isPrimaryKey: 字段主键设置
        :param isAuto: 字段自增设置
        :param isUnique: 字段非空设置
        :param isUnsigned: 字段无符号设置
        :return: 无
        """
        if aType.lower() in CHARLIST:
            if default is not None:
                default = '"%s"' % default
        self.attributeDic[self.index_i] = {
            "name": aName,
            "type": aType,
            "long": aLong,
            "notnull": isNotNull,
            "primarykey": isPrimaryKey,
            "auto": isAuto,
            "unique": isUnique,
            "unsigned": isUnsigned,
            "default": default
        }
        if isPrimaryKey:
            self.primaryKeys += [aName]
        self.index_i += 1

    def creatLanguage(self):
        """
        生成创建表语句
        :return: SQL语句（str）
        """
        sql = ""
        for attribute in self.attributeDic.values():
            if attribute["type"].lower() in TYPEUSEDLONG:
                sql += "`%s` %s(%s)" % (attribute["name"], attribute["type"], attribute["long"])
            elif attribute["type"].lower in INTLIST:
                sql += "`%s` %s" % (attribute["name"], attribute["type"])
                if attribute["unsigned"]:
                    sql += " UNSIGNED"
                if attribute["auto"]:
                    sql += " AUTO_INCREMENT"
            else:
                sql += "`%s` %s" % (attribute["name"], attribute["type"])

            if attribute["notnull"] and not attribute["primarykey"]:
                sql += " NOT NULL"

            if attribute["unique"]:
                sql += " UNIQUE"

            if attribute["default"] is not None:
                sql += " DEFAULT %s" % attribute["default"]
            sql += ","
        if self.primaryKeys:
            sql += "PRIMARY KEY("
            for primary_key in self.primaryKeys:
                sql += "`%s`," % primary_key
        if sql != "":
            sql = sql[:-1] + ")"
            sql0 = """CREATE TABLE %s (%s)ENGINE=%s DEFAULT CHARSET=%s""" % (
                self.tableName, sql, self.engine, self.charset)
        else:
            sql0 = """CREATE TABLE %s ENGINE=%s DEFAULT CHARSET=%s""" % (
                self.tableName, self.engine, self.charset)
        return sql0

    def __str__(self):
        return self.creatLanguage()

    def belong(self, tableSQL_table):
        """
        判断数据表类型归属
        用于创建数据表时判断重复问题
        所有非主键的字段全属于另一个表
        :param tableSQL_table:
        :return:
        """
        if type(tableSQL_table) == tableSQL:
            for attribute in self.attributeDic.values():
                if not attribute["primarykey"]:
                    if attribute not in tableSQL_table.attributeDic.values():
                        return False
            return True
        else:
            return False

    def belongList(self, *tableSQLList):
        for table in tableSQLList:
            if self.belong(table):
                return True
        return False

    def addSameTableList(self, *tableSQLList):
        if self.belongList(*tableSQLList):
            return tableSQLList
        else:
            for i in range(0, len(tableSQLList)):
                if tableSQLList[i].belong(self):
                    tableSQLList[i].reset(self)
                    return tableSQLList
            tableSQLList += (self,)
            return tableSQLList


def addTableList(tableSQLList_1: list or tuple, tableSQLList_2: list):
    """
    :param tableSQLList_1:
    :param tableSQLList_2: 添加之前确保该列表符合唯一
    :return:
    """
    for tableSQL_table in tableSQLList_1:
        tableSQLList_2 = tableSQL_table.addSameTableList(*tableSQLList_2)
    return tableSQLList_2


class dataSQL:
    """
    数据类
    """
    def __init__(self, database, table, cursor, findInfo=None):
        self.findInfo = findInfo
        self.database = database
        self.table = table
        self.find = ""
        self.dataList = []
        self.attribute = []
        self.values = []
        sql = """SELECT column_name from information_schema.columns where table_schema ='%s'  and table_name = '%s'"""
        cursor.execute(sql % (database, table))
        results = cursor.fetchall()
        self.setAttribute(results)

    def setData(self, results):
        """
        设置数据
        :param results:
        :return:
        """
        if not self.attribute:
            return
        for result in results:
            dic = {}
            for i in range(0, len(self.attribute)):
                dic[self.attribute[i]] = result[i]
            self.dataList += [dic]

    def setAttribute(self, results):
        """
        设置字段
        :param results:
        :return:
        """
        for result in results:
            self.attribute += [result[0]]

    def setValues(self, results=None, *args):
        """
        设置数据（无字段列表型）
        :param results:
        :param args:
        :return:
        """
        if results is not None:
            self.values = list(results)
        else:
            for arg in args:
                if type(arg) not in [tuple, list]:
                    return
                else:
                    self.values += arg

    def __str__(self):
        return str(self.dataList) if self.dataList else "没有数据"

    def show(self):
        """
        展示数据
        :return:
        """
        if not self.dataList:
            print("没有数据")
            return
        for dataSQL_data in self.dataList:
            print(dataSQL_data)

    def add(self, data_from_dataSQL):
        """
        数据集加，只支持相同字段的数据集
        :param data_from_dataSQL:
        :return:
        """
        if self.attribute == data_from_dataSQL.attribute:
            self.dataList += data_from_dataSQL.dataList
            self.findInfo += " OR" + data_from_dataSQL.findInfo[6:]
            self.values += data_from_dataSQL.values

    def get(self, *args):
        """
        获取对应字段的数据集
        :param args:
        :return:
        """
        if len(args) == 0:
            return self.values
        elif len(args) == 1:
            get_dataList = []
            for dataSQL_data in self.dataList:
                get_dataList += [dataSQL_data.get(args[0], None)]
            return get_dataList
        else:
            get_dataList = []
            for dataSQL_data in self.dataList:
                get_data = ()
                for arg in args:
                    get_data += (dataSQL_data.get(arg, None),)
                get_dataList += [get_data]
            return get_dataList

    # 仅限于单一key唯一
    def getDic(self, *args, key=None):
        """
        获取以key为dict.key的字段集
        :param args: 字段
        :param key: key
        :return:
        """
        i = 0

        def uniqueId():
            """
            获取唯一名
            :return:
            """
            nonlocal i
            i += 1
            return "noKey_%s" % i

        if key is None:
            if len(args) == 0:
                return self.dataList
            else:
                get_dataList = []
                for dataSQL_data in self.dataList:
                    get_data = {}
                    for arg in args:
                        get_data[arg] = dataSQL_data.get(arg, None)
                    get_dataList += get_data
                return get_dataList
        else:
            if len(args) == 0:
                get_dataDic = {}
                for dataSQL_data in self.dataList:
                    get_data = {}
                    for arg in self.attribute:
                        if arg != key:
                            get_data[arg] = dataSQL_data.get(arg, None)
                    get_dataDic[dataSQL_data.get(key, uniqueId())] = get_data
                return get_dataDic
            elif len(args) == 1:
                get_dataDic = {}
                for dataSQL_data in self.dataList:
                    get_dataDic[dataSQL_data.get(key, uniqueId())] = dataSQL_data.get(args[0], None)
                return get_dataDic
            else:
                get_dataDic = {}
                for dataSQL_data in self.dataList:
                    get_data = {}
                    for arg in args:
                        get_data[arg] = dataSQL_data.get(arg, None)
                    get_dataDic[dataSQL_data.get(key, uniqueId())] = get_data
                return get_dataDic


class easySQL:
    """
    主功能类，利用前面结构类进行简化
    """
    def __init__(
            self, databaseName: str = "", user="root", passwd="123456", host="127.0.0.1",
            database: databaseSQL = None
    ):
        """
        初始化连接数据库
        :param databaseName:
        :param user:
        :param passwd:
        :param host:
        :param database: 输入databaseSQL类，无需额外定义对应值，引用时其他参数失效
        """
        if database is not None:
            self.database = database.database
            self.user = database.user
            self.host = database.host
            self.passwd = database.passwd
            self.db = pymysql.connect(
                host=database.host, user=database.user, passwd=database.passwd, db=database.database
            )
            self.cursor = self.db.cursor()
        else:
            if databaseName == "":
                databaseName = "test"
            self.user = user
            self.host = host
            self.passwd = passwd
            self.database = databaseName
            self.db = pymysql.connect(host=host, user=user, passwd=passwd, db=databaseName)
            self.cursor = self.db.cursor()

    def start(self):
        """
        连接数据库，定义时默认启动，一般用于close后再次启用
        :return:
        """
        self.db = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.database)
        self.cursor = self.db.cursor()

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        self.db.close()

    def creat(self, tableName="", childDeep=0, **kwargs):
        """
        根据字典创建数据表（匹配JSON使用）（逻辑异常，需修改）
        :param tableName:
        :param childDeep: childDeep = x(>1) :进行x-1次分层; childDeep = 1 :不进行分层; childDeep = x(<1) :直到无法分层
        :param kwargs:
        :return:
        """
        tableSQLList = []
        tableSQL_table = tableSQL(tableName)
        tableSQL_table.addAttribute("%s_Id" % tableName, "INT", isPrimaryKey=True)
        for key in kwargs:
            if childDeep != 1:
                if type(kwargs[key]) not in [list, tuple, dict]:
                    if kwargs[key] is None:
                        kwargs[key] = "NULL"
                    tableSQL_table.addAttribute(key, typeTo[type(kwargs[key])])
                elif type(kwargs[key]) == dict:
                    tableSQLList = addTableList(
                        self.creat("%s_%s" % (tableName, key), childDeep - 1, **kwargs[key]),
                        tableSQLList
                    )
                elif len(kwargs[key]) != 0:
                    tempDic = {
                        "%s_Id" % tableName: 0,
                        key: kwargs[key][0],
                    }
                    if type(kwargs[key][0]) not in [dict]:
                        tableSQLList = addTableList(
                            self.creat("%s_%s" % (tableName, key), childDeep - 1, **tempDic),
                            tableSQLList
                        )
                    else:
                        kwargs[key][0]["%s_Id" % tableName] = 0
                        tableSQLList = addTableList(
                            self.creat("%s_%s" % (tableName, key), childDeep - 1, **kwargs[key][0]),
                            tableSQLList
                        )
            else:
                tableSQL_table.addAttribute(key, typeTo[type(kwargs[key])])
        tableSQLList = tableSQL_table.addSameTableList(*tableSQLList)
        return tableSQLList

    def add(self, tableName, data_from_dataSQL: dataSQL = None, **kwargs):
        """
        添加数据
        :param tableName:
        :param data_from_dataSQL:
        :param kwargs:
        :return:
        """
        if data_from_dataSQL is not None:
            sql = """INSERT INTO %s""" % tableName
            sql0 = """("""
            for attribute in data_from_dataSQL.attribute:
                sql0 += """`%s`,""" % attribute
            sql0 = sql0[:-1] + """) VALUE ("""
            for values in data_from_dataSQL.values:
                # print(values)
                sql1 = """"""
                for value in values:
                    if type(value) == str:
                        value = value.replace('"', "'")
                        sql1 += """"%s",""" % value
                    else:
                        sql1 += """%s,""" % value
                sql1 = sql1[:-1] + """)"""
                self.commit(sql + sql0 + sql1)
        else:
            sql = """INSERT INTO %s""" % tableName
            sql0 = """("""
            sql1 = """("""
            for attribute in kwargs.keys():
                sql0 += """`%s`,""" % attribute
                if type(kwargs[attribute]) == str:
                    kwargs[attribute] = kwargs[attribute].replace('"', "'")
                    sql1 += """"%s",""" % kwargs[attribute]
                else:
                    sql1 += """%s,""" % kwargs[attribute]
            sql0 = sql0[:-1] + """) VALUE """
            sql1 = sql1[:-1] + """)"""
            # print(sql + sql0 + sql1)
            self.commit(sql + sql0 + sql1)

    def addList(self, tableName, **kwargs):
        """
        添加数据列
        :param tableName:
        :param kwargs:
        :return:
        """
        temp = 0
        for key in kwargs:
            if type(kwargs[key]) not in [list, tuple]:
                if kwargs[key] == "":
                    return
            else:
                if len(kwargs[key]) == 0:
                    return
                if type(kwargs[key]) == tuple:
                    kwargs[key] = list(kwargs[key])
                if temp != 0:
                    if len(kwargs[key]) != temp:
                        return
                else:
                    temp = len(kwargs[key])
        tKwargs = {}
        for key in kwargs:
            if type(kwargs[key]) not in [list, tuple]:
                kwargs[key] = [kwargs[key]] * temp
        for i in range(0, temp):
            for key in kwargs.keys():
                tKwargs[key] = kwargs[key][i]
            self.add(tableName, **tKwargs)

    def delete(self, tableName, data_from_dataSQL: dataSQL = None, **kwargs):
        """
        删除数据
        :param tableName:
        :param data_from_dataSQL:
        :param kwargs:
        :return:
        """
        if data_from_dataSQL is not None:
            sql = """DELETE FROM %s%s""" % (data_from_dataSQL.table, data_from_dataSQL.findInfo)
            self.commit(sql)
        else:
            findInfo = self.__findInfo(**kwargs)
            sql = """DELETE FROM %s%s""" % (tableName, findInfo)
            self.commit(sql)

    def find(self, tableName, **kwargs):
        """
        查找数据
        :param tableName:
        :param kwargs:
        :return:
        """
        findInfo = self.__findInfo(**kwargs)
        sql = """SELECT * FROM %s%s""" % (tableName, findInfo)
        results = self.getData(sql)
        data_from_easySQL_find = dataSQL(self.database, tableName, self.cursor, findInfo=findInfo)
        data_from_easySQL_find.setData(results)
        data_from_easySQL_find.setValues(results)
        return data_from_easySQL_find

    def update(self, data_from_dataSQL: dataSQL, **kwargs):
        """
        更新数据
        :param data_from_dataSQL:
        :param kwargs:
        :return:
        """
        if not kwargs:
            return
        sql = """UPDATE %s SET """ % data_from_dataSQL.table
        for key in kwargs.keys():
            if type(kwargs[key]) == str:
                kwargs[key] = kwargs[key].replace('"', "'")
                sql += '`%s`="%s",' % (key, kwargs[key])
            else:
                sql += "`%s`=%s," % (key, kwargs[key])
        sql = sql[:-1] + data_from_dataSQL.findInfo
        print(sql)
        self.commit(sql)

    def execute(self, sql: str):
        """
        执行事务
        :param sql:
        :return:
        """
        self.commit(sql)

    def commit(self, sql: str):
        """
        提交事务
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print("事务执行异常！", e)
            print(sql)

    def getData(self, sql: str):
        """
        查找事务
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.db.rollback()
            print("数据查找异常！", e)
            print(sql)
        else:
            return self.cursor.fetchall()

    def __findInfo(self, **kwargs):
        """
        合成条件语句
        :param kwargs:
        :return:
        """
        if kwargs:
            findInfo = " WHERE ("
            for key in kwargs.keys():
                if type(kwargs[key]) == str:
                    kwargs[key] = kwargs[key].replace('"', "'")
                    kwargs[key] = '"%s"' % kwargs[key]
                findInfo += " `%s`=%s AND" % (key, kwargs[key])
            findInfo = findInfo[:-4] + " )"
        else:
            findInfo = ""
        return findInfo


if __name__ == "__main__":
    a = tableSQL("asdf")
    b = tableSQL("asd")
    a.reset(b)
    print(a)

