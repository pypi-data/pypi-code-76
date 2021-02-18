# -*- coding:UTF-8 -*-
# 作者: l0n0l
# 时间: 2020/06/30 周二
# 点: 17:46:04

# 描述:对数据库的操作


import pymysql
import logging
import time


class dbmysql:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.conn_timestamp = time.time()
        self.conn = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.tables = {}
        self.timer = 0
        self.privileges = {}
        self.allow_operators = ["=",  "<>", ">",
                                "<", ">=", "<=",
                                "like", "in", "not in"]
        self.allow_values_func = ["from_unixtime", "unix_timestamp"]
        self.functions = []
        self.need_commit = False
        self.connect()

    def __make_where(self, col_names: list, where: dict, inject: str = None):
        where_str = ""
        args = []

        if where is not None:
            for k, v in where.items():
                k = k.split('#')
                key_len = len(k)
                if key_len > 2 or key_len <= 0:
                    continue
                if k[0] not in col_names:
                    continue
                if key_len == 2 and k[1] not in self.allow_operators:
                    continue
                if key_len == 1:
                    k.append(isinstance(v, list) and "in" or "=")
                where_str += f"`{k[0]}` {k[1]} %s and "
                args.append(v)

        if len(args) <= 0:
            if inject and len(inject) > 0:
                where_str = f"where 1 = 1 {inject}"
            else:
                where_str = ""
        else:
            inject = inject or ""
            where_str = f" where {where_str[:-4]} {inject} "

        return where_str, args

    def __make_column(self, col_names, cols, need_index_list=False):
        # 筛选列名
        columns = []
        if need_index_list:
            index_list = []
        ret_str = ""
        for i in range(len(cols)):
            if cols[i] in col_names:
                ret_str += f"`{cols[i]}`,"
                columns.append(cols[i])
                if need_index_list:
                    index_list.append(i)
            elif cols[i] in self.functions:
                ret_str += f"{cols[i]},"
                columns.append(cols[i])
                if need_index_list:
                    index_list.append(i)
        if len(columns) <= 0:
            return

        ret_str = ret_str[:-1]

        if need_index_list:
            return ret_str, columns, index_list

        return ret_str, columns

    def flush_tables_cache(self):
        """
        更新表格名，列名缓存
        """
        tables = self.get_table_names()
        for tn in tables:
            self.tables[tn] = self.get_table_columns(tn)

    def add_col_func(self, funcname):
        self.functions.append(funcname)


    def update_info(self, elapse: float):
        """
        帧更新函数
            @elapse:float:上一帧执行耗时
        """
        if self.need_commit:
            self.commit()
            self.need_commit = False

        self.timer += elapse
        if self.timer >= 1:
            self.update_privilege()
            # self.flush_tables_cache()
            self.timer = 0

    def get_table_names(self):
        """
        获取所有的表格名称
        @return:list:表格名称列表
        """
        tables = self.get("SELECT `TABLE_NAME` FROM `information_schema`.`TABLES`"
                          " WHERE `information_schema`.`TABLES`.TABLE_SCHEMA=%s",
                          [self.database])
        ret = []
        if tables is not None:
            for table in tables:
                ret.append(table["TABLE_NAME"])
        return ret

    def get_table_columns(self, table: str):
        """
        获取表头
            @return:list:表头字段列表
        """
        columns = self.get("SELECT `COLUMN_NAME` FROM `information_schema`.`COLUMNS`"
                           "WHERE `information_schema`.`COLUMNS`.TABLE_NAME = %s"
                           "AND `information_schema`.`COLUMNS`.TABLE_SCHEMA = %s",
                           [table, self.database])
        if not columns:
            return
        ret = []
        for column in columns:
            ret.append(column["COLUMN_NAME"])
        return ret

    def connect(self):
        """
        从新链接数据库
        """
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            charset='utf8'
        )
        self.flush_tables_cache()

    def commit(self):
        self.conn.ping()
        self.conn.commit()

    def get(self, sql: str, params: any = {}) -> tuple:
        """
        从数据库获取数据
            @sql:要执行的sql语句，%(key)s 或 %s 表示占位符
            @params:dict:表示占位符的值。
            @return:tuple:返回的结果
        例如:
            1.
            sql = 'select * from `users` where `id` = %(id)s
            params = {'id': 123}
            2.
            sql = 'select * from `users` where `id` = %s
            params = (123)
        """
        try:
            self.conn.ping()
            cursor: pymysql.cursors.Cursor = self.conn.cursor(
                cursor=pymysql.cursors.SSDictCursor)
            ret = cursor.execute(sql, params)
            self.need_commit = True
            if ret <= 0:
                ret = None
            else:
                ret = cursor.fetchall()
                if len(ret) <= 0:
                    ret = None
            cursor.close()
            return ret
        except Exception as e:
            logging.error(f"db get error {e.with_traceback(None)}")
            logging.error(f"get sql error:{sql},params = {str(params)}")

    def select(self, table: str, cols: list, where: dict, order_by: str = "",  limit: int = None, offset: int = None, order_direction: str = "asc", inject: str = ""):
        """
        从数据库获取数据
            @table:str:要查询的表格
            @cols:list:要返回的数据列
            @where:dict:{
                "xxx#=": 123
            }帅选条件
            @order_by:str:排序 (xxx asc | xxx desc)
            @limit:int:要返回的数据条数
            @offset:int:从offset条数据后面返回limit条数据
        """
        # 获取表格名称
        col_names = self.tables.get(table)
        if not col_names:
            return

        # 构建列名
        col_str, _ = self.__make_column(col_names, cols)

        # 构建sql
        sql = f"select {col_str} from `{table}`"

        # 构建where筛选语句
        where_str, args = self.__make_where(col_names, where, inject)
        sql += where_str

        # 构建排序
        if order_by in col_names:
            if order_direction not in ["asc", "desc"]:
                order_direction = "asc"
            sql += f"order by `{order_by}` {order_direction}"

        # 构建Limit offset
        if limit:
            sql += f" limit {limit}"
        if offset:
            sql += f" offset {offset}"

        return self.get(sql, args)

    def post(self, sql: str, params: any = {}) -> bool:
        """
        修改数据库数据
            @sql:字符串:要执行的sql语句，%(key)s 或 %s 表示占位符
            @params:表示占位符的值。
        例如：
            1.
            sql = 'update `users` set `name` = %(name)s where `id` = %(id)s
            params = {'id': 123,'name':'hahaha'}
            2.
            sql = 'update `users` set `name` = %s where `id` = %s
            params = [123, 'hahaha']
        """
        try:
            self.conn.ping()
            cursor: pymysql.cursors.Cursor = self.conn.cursor()
            cursor.execute(sql, params)
            cursor.close()
            self.need_commit = True
        except Exception as e:
            self.conn.rollback()
            cursor.close()
            logging.error(e.with_traceback(None))
            logging.error(f"post sql error:{sql},params = {str(params)}")
            return False
        return True

    def exec_proc(self, name: str, args: tuple = (), ret_count: tuple = ()) -> tuple:
        """
        执行存储过程
            @name:str: 存储过程名None
            @args:tuple: 存储过程参数
            @ret_count:tuple:需要返回结果的索引
        例如:
            有存储过程create_folder需要三个参数(
                foldername：varchar:in,
                ownerid:varchar:in,
                folderid:int:out)
            我们需要执行create_folder并返回folderid
            folderid = exec_proc(
                'create_folder', ['folder_name','owner_id', 0], [2])
            结果为folderid = (60,)
        """
        try:
            self.conn.ping()
            cursor: pymysql.cursors.Cursor = self.conn.cursor()
            cursor.callproc(name, args)
            params = ",".join(f"@_{name}_{i}" for i in ret_count)
            s_result_sql = f"select {params}"
            cursor.execute(s_result_sql)
            result = cursor.fetchone()
            cursor.close()
            self.need_commit = True
            return result
        except Exception as e:
            logging.error(e.with_traceback(None))
            logging.error(f"excute procedure error:{name},args = {str(args)}")

    def update(self, table: str, values: dict, where: dict, values_func: dict = None, inject: str = ""):
        """
        更新数据库某个表的某个值
            @table:str:表名
            @id_name:str:主键名称
            @id_value:str:主键值
            @kwargs:dict:目标值的键值对
        """
        col_names = self.tables.get(table)
        if col_names is None:
            return
        sql = f"update `{table}` set "
        set_string = ""
        args = []
        for k, v in values.items():
            if k in col_names:
                if values_func is not None:
                    f = values_func.get(k)
                    if f is not None:
                        if f not in self.allow_values_func:
                            logging.error(
                                f"{f} not in {self.allow_values_func}")
                            return
                        set_string += f"`{k}` = {f}(%s) "
                    else:
                        set_string += f"`{k}` = %s "
                else:
                    set_string += f"`{k}` = %s "
                args.append(v)

        sql += set_string

        # 构建where筛选语句
        where_str, where_args = self.__make_where(col_names, where)
        sql += where_str

        # 合并参数
        args += where_args

        # 执行sql
        self.post(sql, args)

    def delete(self, table: str, where: dict, inject: str = ""):
        """
        从表中删除数据
            @table:str:表名
            @where:dict:{
                "xxx =": 123
            }帅选条件
        """
        col_names = self.tables.get(table)
        if not col_names:
            return
        sql = f"delete from `{table}` "
        where_str, args = self.__make_where(col_names, where)
        sql += where_str
        self.post(sql, args)

    def insert(self, table: str, cols: list, values: list, values_func: dict = None, cols_str: str = None, index_list: list = None):
        """
        向表中插入数据
            @table:str:表名
            @cols:list:要插入的列名
            @values:list:值列表
        """
        # 获取列
        col_names = self.tables.get(table)
        if not col_names:
            return

        # 构建列名
        if cols_str is None:
            cols_str, cols, index_list = self.__make_column(
                col_names, cols, True)
        if not cols_str:
            return
        values_str = ""
        for col in cols:
            if values_func is not None:
                f = values_func.get(col)
                if f is not None:
                    if f not in self.allow_values_func:
                        logging.error(
                            f"{f} not in {self.allow_values_func}")
                        return
                    values_str += f"{f}(%s),"
                else:
                    values_str += " %s,"
            else:
                values_str += " %s,"
        values_str = values_str[:-1]

        # 筛选value
        args = []
        for i in index_list:
            args.append(values[i])

        sql = f"insert into `{table}` ({cols_str}) values ({values_str})"

        self.post(sql, args)

        return True

    def set_privilege(self, id: str, privilege: dict, espire_in: int):
        """
        生成权限ID
            @id:权限ID
            @privilege:dict:{
                "table":{
                    "insert":[col1, col2, ...],
                    "select":[col1, col2, ...],
                    "update":[col1, col2, ...],
                    "delete":true|false,
                    "where_inject":{
                        "select":str,
                        "update":str,
                        "delete":str
                    }
                }
            }
            @espire_in:int:id生效时常
        """
        self.privileges[id] = {
            "timestamp": time.time() + espire_in,
            "privilege": privilege
        }

    def update_privilege(self):
        """
        帧更新权限
        """
        remove_list = []
        cur_time = time.time()
        for id, privilege_data in self.privileges.items():
            if cur_time >= privilege_data["timestamp"]:
                remove_list.append(id)

        for id in remove_list:
            del self.privileges[id]

    def execute(self, args: dict):
        """
        根据参数执行相关函数
            args:dict:{
                "id":权限ID
                "table":"表格名称",
                "func":"insert|delete|update|select",对表格的操作,
                "cols":[col1,col2]要操作的列,insert,select有效
                "where":dict:{"id =":1...}数据筛选条件。
                        可用的运算符右["=",  "<>", ">", "<", ">=", "<=", "like", "in", "not in"]
                        select, delete, update 有效
                "values":dict:{"col":值} 数据的值。 update,insert有效
                "order_by":str:"列名" 按照哪一列排序, select 有效
                "limit":int:需要select 多少条数据
                "offset":int:select数据的偏移量，从offset调后select数据
                "order_direction":asc|desc select出来的数据排序 asc升序 ，desc降序
                "values_func":{"列名":"from_unixtime"}:某个值的更新时要执行的函数
            }
        """
        # 获取权限数据
        id = args.get("id")
        if id is None:
            return {"errMsg": "No id not supported!"}

        privilege: dict = self.privileges.get(args['id'])
        if privilege is None:
            return {"errMsg": "Permmison deny!"}
        privilege = privilege['privilege']

        # 获取表格权限
        table = args.get("table")
        if table is None:
            return {"errMsg": "Table id not supported!"}

        privilege = privilege.get(table)
        if privilege is None:
            return {"errMsg": "Permmison deny!"}

        where_inject = privilege.get("where_inject") or {}

        # 获取方法权限
        func = args.get("func")
        if func is None:
            return {"errMsg": "func id not supported!"}

        privilege = privilege.get(func)
        if privilege is None:
            return {"errMsg": "Permmison deny!"}

        ret = None

        # 增
        if func == "insert":
            cols = args.get("cols")
            if cols is None:
                return {"errMsg": "cols id not supported!"}

            # 过滤列
            cols_str, cols, index_list = self.__make_column(
                privilege, cols, True)
            if cols_str is None:
                return {"errMsg": "columns error!"}

            values = args.get("values")
            if values is None:
                return {"errMsg": "values id not supported!"}

            self.insert(table, cols, values, args.get(
                "values_func"), cols_str, index_list)
        # 删除
        elif func == "delete":
            where = args.get("where")
            self.delete(table, where, where_inject.get("delete") or "")
        # 改
        elif func == "update":
            values = args.get("values")
            if values is None:
                return {"errMsg": "values id not supported!"}
            where = args.get("where")
            self.update(table, values, where, args.get(
                "values_func"), where_inject.get("update") or "")
        # 查
        elif func == "select":
            cols = args.get("cols")
            if cols is None:
                return {"errMsg": "cols id not supported!"}

            # 过滤列
            cols_str, cols, index_list = self.__make_column(
                privilege, cols, True)
            if cols_str is None:
                return {"errMsg": "columns error!"}

            page = args.get("page")
            limit = args.get("limit")
            if page is not None and limit is not None:
                args['offset'] = (page - 1) * limit

            ret = self.select(table, cols, args.get("where"),
                              args.get("order_by") or "",
                              limit,
                              args.get("offset"),
                              args.get("order_direction"),
                              where_inject.get("select"))

        return {"errMsg": "OK", "data": ret}
