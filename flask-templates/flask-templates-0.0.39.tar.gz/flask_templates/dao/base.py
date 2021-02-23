# -*- coding: utf-8 -*-
"""
----------------------------------------------------
    File Name:              __init__.py
    Description
    Author:                 develop
    date:                   2019/4/4
----------------------------------------------------
"""
__author__ = 'develop'

import traceback
from sqlalchemy import or_, and_
from functools import wraps
from sqlalchemy.orm import Query
from flask_templates.common.sqlalchemy_module import MySQL
from flask_templates.model import *


def transaction(master_name=None, session_class_name=None, random_slave=False):
    def wrap(func):
        """
        不与dao里的start_transaction，end_transaction联用
        Parameters
        ----------
        func

        Returns
        -------

        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            if kwargs.get('tr'):
                return func(*args, **kwargs)
            b = TransactionAction(master_name, session_class_name, random_slave)
            b.start_transaction()
            kwargs['tr'] = b
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                try:
                    b.session.rollback()
                    b.session.close()
                except:
                    pass
                raise e
            else:
                b.end_transaction()
            return res

        return wrapper

    return wrap


master_transaction = simple_transaction = transaction(session_class_name=None)
random_slave_transaction = transaction(random_slave=True)
slave_transaction = lambda slave_name: transaction(session_class_name=slave_name)


class BaseDaoError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.__str__()


class TransactionAction(object):

    def __init__(self, master_name=None, session_class_name=None, random_slave=False):
        self.session_class_name = session_class_name
        self.random_slave = random_slave
        self.session = None
        self.transaction = False
        self.master_name = master_name

    def start_transaction(self):
        if self.transaction:
            raise BaseDaoError('end error!!!transaction has not begun')
        self.start()
        self.transaction = True

    def start(self):
        if self.session:
            return self.session
        self.session = MySQL(master_name=self.master_name).sql_session(self.session_class_name, self.random_slave)
        return self.session

    def end_transaction(self):
        if not self.transaction:
            raise BaseDaoError('end error!!!transaction has not begun')
        self.transaction = False
        self.end()

    def end(self):
        if self.transaction:
            return
        if self.session:
            self.session.commit()
            self.session.close()
            self.session = None


def sql_wrapper(result_func):
    def addition_type(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            temp = func(self, *args, **kwargs)
            if "order_by" in kwargs and kwargs['order_by']:
                temp = temp.order_by(kwargs['order_by'])
            if "desc" in kwargs and kwargs['desc']:
                temp = temp.desc()
            if "limit" in kwargs and kwargs['limit']:
                temp = temp.limit(kwargs['limit'])
            if "offset" in kwargs and kwargs['offset']:
                temp = temp.limit(kwargs['offset'])
            result = result_func(temp)
            self.tr.end()
            return result

        return wrapper

    return addition_type


class BaseDao(object):

    def __init__(self, entry_class, master_name=None, session_class_name=None, rs=False, tr=None):
        self.entry = entry_class
        if tr:
            self.tr = tr
        else:
            random_slave = rs
            self.tr = TransactionAction(master_name, session_class_name, random_slave)

    @sql_wrapper(Query.all)
    def get_all(self, where_dict=None, **kwargs):
        session = self.tr.start()
        if where_dict:
            return session.query(self.entry).filter_by(**where_dict)
        return session.query(self.entry)

    def filter_fetch(self,query,limit=None, offset=None, page=None, per_page=None,order_by=None,count=None,**kwargs):
        """
        :param query:
        :param limit:
        :param offset:
        :param page:
        :param per_page:
        :param order_by: 排序，示例[{"XX":"asc"},{"YY":"desc"}] 或者 {"XX":"asc"}
        :return:
        """
        if order_by:
            orders = []
            if type(order_by) == dict:
                for k, v in order_by.items():
                    if getattr(self.entry, k, None) is not None:
                        orders.append(getattr(getattr(self.entry, k), v)())
            elif type(order_by) == list:
                for item in order_by:
                    for k, v in item.items():
                        if getattr(self.entry, k, None) is not None:
                            orders.append(getattr(getattr(self.entry, k), v)())
            if orders:
                query = query.order_by(*orders)
        total = 0
        if page:
            total = query.count()
            query = query.offset((int(page) - 1) * int(per_page))
            query = query.limit(int(per_page))

        else:
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
        if count:
            if page:
                res = total
            else:
                res = query.count()
        else:
            res = query.all()
        if page:
            return res, total
        return res

    def simple_get_all_filter(self, params, condition_type='and', **kwargs):
        session = self.tr.start()
        if params:
            if type(params) == list:
                arg_list = []
                for one in params:
                    if isinstance(one[2], str) and not one[2].startswith("'") and not one[2].startswith("\""):
                        one[2] = "'{}'".format(one[2])
                    # print("self.entry.{}{}{}".format(one[0], one[1], one[2]))
                    arg_list.append(eval("self.entry.{}{}{}".format(one[0], one[1], one[2])))
                if condition_type == 'and':
                    condition_func = and_
                else:
                    condition_func = or_
                q = session.query(self.entry).filter(condition_func(*arg_list))
            elif type(params) == dict:
                filters = []
                for k, v in params.items():
                    if type(v) is list:
                        filters.append(getattr(self.entry, k).in_(v))
                    else:
                        filters.append(getattr(self.entry, k) == v)
                q = session.query(self.entry).filter(*filters)
            else:
                q = session.query(self.entry)
        else:
            q = session.query(self.entry)
        res = self.filter_fetch(q,**kwargs)
        self.tr.end()
        return res

    def simple_get_join(self, join_entry, on_dict, *args, order_by=None, **kwargs):
        session = self.tr.start()
        eval_str = 'and'.join(['{}.{}=={}.{}'.format(self.entry.__name__, x, join_entry.__name__, on_dict[x]) for x in
                               on_dict])
        temp = res = session.query(self.entry, join_entry).outerjoin(join_entry, eval(
            eval_str))
        if args:
            temp = temp.filter(*args)
        if order_by:
            orders = []
            for k, v in order_by.items():
                if getattr(self.entry, k, None) is not None:
                    orders.append(getattr(getattr(self.entry, k), v)())
                else:
                    orders.append(getattr(getattr(join_entry, k), v)())
            temp = temp.order_by(*orders)
        res = self.filter_fetch(temp,**kwargs)
        self.tr.end()
        return res

    def get_join_new(self, join_entry, on_dict, *args,
                     order_by=None, in_filter=None, equal_filter=None, range_filter=None,**kwargs):
        session = self.tr.start()
        eval_str = 'and'.join(['{}.{}=={}.{}'.format(self.entry.__name__, x, join_entry.__name__, on_dict[x]) for x in
                               on_dict])
        temp = res = session.query(self.entry, join_entry).outerjoin(join_entry, eval(eval_str))
        filters = []
        if equal_filter:
            for k, v in equal_filter.items():
                if v is not None:
                    if getattr(self.entry, k, None) is not None:
                        key = getattr(self.entry, k)
                    else:
                        key = getattr(join_entry, k)
                    filters.append(key == v)
        if in_filter:
            for k, v in in_filter.items():
                if v is not None:
                    if getattr(self.entry, k, None) is not None:
                        key = getattr(self.entry, k)
                    else:
                        key = getattr(join_entry, k)
                    filters.append(key.in_(v))
        if range_filter:
            for k, v in range_filter.items():
                if v:
                    if getattr(self.entry, k, None) is not None:
                        key = getattr(self.entry, k)
                    else:
                        key = getattr(join_entry, k)
                    if v[0] is not None:
                        filters.append(key >= v[0])
                    if v[1] is not None:
                        filters.append(key <= v[1])
        temp = temp.filter(*filters)
        if args:
            temp = temp.filter(*args)
        if order_by:
            orders = []
            for k, v in order_by.items():
                if getattr(self.entry, k, None) is not None:
                    orders.append(getattr(getattr(self.entry, k), v)())
                else:
                    orders.append(getattr(getattr(join_entry, k), v)())
            temp = temp.order_by(*orders)
        res = self.filter_fetch(temp, **kwargs)
        self.tr.end()
        return res

    def simple_get_all(self, extra_dict=None,**kwargs):
        """
        简单查询，
        :param extra_dict:
        :param kwargs:查询条件 都是逻辑与的关系
        :return: 
        """
        if not extra_dict:
            extra_dict = dict()
        or_list = kwargs.pop("or_list", None)
        session = self.tr.start()
        try:
            if kwargs:
                filters = []
                for k, v in kwargs.items():
                    if type(v) is list:
                        filters.append(getattr(self.entry, k).in_(v))
                    else:
                        filters.append(getattr(self.entry, k) == v)
                q = session.query(self.entry).filter(*filters)
            elif or_list:
                arg_list = []
                for one in or_list:
                    arg_list.append(eval("{}.{}=={}".format(self.entry.__name__, one[0], one[-1])))
                q = session.query(self.entry).filter(or_(*arg_list))
            else:
                q = session.query(self.entry)
            res = self.filter_fetch(q, **extra_dict)
            self.tr.end()
        except:
            traceback.print_exc()
            session.rollback()
            session.close()
            return
        return res

    def simple_get_one(self, first=False, **kwargs):
        """
        简单查询，
        :param first:是否取一个
        :param kwargs:查询条件 都是逻辑与的关系
        :return: 
        """
        session = self.tr.start()
        if kwargs:
            res = session.query(self.entry).filter_by(**kwargs).limit(1)
        else:
            res = session.query(self.entry).limit(1)
        if first:
            res = res.first()
        else:
            res = res.all()
        self.tr.end()
        return res

    def insert(self, **kwargs):
        session = self.tr.start()
        # print(id(session))
        try:
            obj = self.entry(**kwargs)
            session.add(obj)
            session.flush()
            # session.commit()
            self.tr.end()
            return obj
        except Exception as e:
            session.rollback()
            session.close()
            raise (e)

    def simple_delete_one(self, **kwargs):
        """
        简单查询删除，
        :param kwargs:查询条件 都是逻辑与的关系
        :return:
        """
        session = self.tr.start()
        if kwargs:
            res = session.query(self.entry).filter_by(**kwargs).first()
        else:
            res = session.query(self.entry).first()
        session.delete(res)
        self.tr.end()
        return res

    def simple_delete_all(self, **kwargs):
        """
        简单查询删除，
        :param kwargs:查询条件 都是逻辑与的关系
        :return:
        """
        session = self.tr.start()
        filters = []
        if kwargs:
            for k, v in kwargs.items():
                if type(v) is list:
                    filters.append(getattr(self.entry, k).in_(v))
                else:
                    filters.append(getattr(self.entry, k) == v)
            # res = self.entry.__table__.delete().where(*filters)
            res = session.query(self.entry).filter(*filters).delete(synchronize_session=False)
        else:
            res = session.query(self.entry).delete()
        self.tr.end()
        return res

    def batch_insert(self, data_list):
        session = self.tr.start()
        try:
            objs = [self.entry(**kwargs) for kwargs in data_list]
            session.add_all(objs)
            session.flush()
            res = objs
            self.tr.end()
            return res
        except Exception as e:
            session.rollback()
            session.close()
            raise (e)

    def batch_insert_ignore(self, data_list):  # 这个不支持transaction的装饰器事务
        session = self.tr.start()
        try:
            return_list = []
            for kwargs in data_list:
                obj = self.entry(**kwargs)
                try:
                    session.add(obj)
                    session.commit()
                    return_list.append(obj)
                except Exception as e:
                    if 'Duplicate entry' in str(e):
                        session.rollback()

                    else:
                        raise e
            # session.flush()
            self.tr.end()
            return return_list
        except Exception as e:
            session.rollback()
            session.close()
            raise (e)

    def batch_insert_update(self, data_list):
        if len(data_list) == 0:
            return False
        insert_keys = data_list[0].keys()
        sql = "INSERT INTO `" + self.entry.__tablename__ + "`("
        sql += ','.join(["`" + x + "`" for x in insert_keys])
        sql += ')VALUES'
        temp_list = []
        for x in data_list:
            temp_str = '('
            tt_list = []
            for k in insert_keys:
                if x[k] is None:
                    tt_list.append("null")
                elif type(x[k]) == str:
                    tt_list.append("'" + x[k] + "'")
                else:
                    tt_list.append(str(x[k]))
            temp_str += ','.join(tt_list)
            temp_str += ')'
            temp_list.append(temp_str)
        sql += ",".join(temp_list)
        sql += " ON DUPLICATE KEY UPDATE "
        temp_list = ["`" + x + "`=values(`" + x + "`)" for x in insert_keys]
        sql += ','.join(temp_list)
        self.execute(sql,_is_direct=True)
        return True

    def simple_update(self, update_query_condition={}, **kwargs):
        session = self.tr.start()
        try:
            res = session.query(self.entry).filter_by(**update_query_condition).update(kwargs)
            # session.flush()
            self.tr.end()
            return res > 0
        except Exception as e:
            session.rollback()
            session.close()
            raise (e)

    def simple_filter_update(self, filters=None, **kwargs):
        session = self.tr.start()
        try:
            res = session.query(self.entry).filter(*filters).update(kwargs, synchronize_session=False)
            # session.flush()
            self.tr.end()
            return res > 0
        except Exception as e:
            session.rollback()
            session.close()
            raise (e)

    def execute(self, sql, *args, _is_direct=False,**kwargs):
        session = self.tr.start()
        # session.begin_nested()
        res = session.execute(sql, *args, **kwargs)
        self.tr.end()
        return res

    def select_execute(self, sql, num=0, *args,  _is_direct=False,**kwargs):
        session = self.tr.start()
        res = session.execute(sql, *args, **kwargs).fetchall()
        if type(num) == int and num > 0:
            res = res[:num]
        elif type(num) == int and num == 0:
            pass
        else:
            res = None
        self.tr.end()
        return res

    @staticmethod
    def select(sql):
        def dec(func):
            def wrapper(self, *args, **kwargs):
                orm_keys = [x for x in self.entry.__dict__.keys() if not x.startswith('_')]
                f_sql = "select " + ','.join(orm_keys) + " from " + self.entry.__name__ + " where " + sql.format(
                    **kwargs)
                result = self.select_execute(f_sql)
                sql_result = []
                for one in result:
                    entry_dict = dict(zip(orm_keys, list(one)))
                    sql_result.append(self.entry(**entry_dict))
                return sql_result

            return wrapper

        return dec


class ObjectCovertToDictDao(BaseDao):

    def __deal_res(self, res):
        if type(res) == tuple:
            temp = [one.to_dict() for one in res[0]]
            res[0].clear()
            res[0].extend(temp)
            return res
        elif type(res) == list:
            return [one.to_dict() for one in res]
        return res

    def simple_get_all(self, **kwargs):
        res = super().simple_get_all(**kwargs)
        return self.__deal_res(res)

    def simple_get_all_filter(self, params, condition_type='and',  **kwargs):
        res = super().simple_get_all_filter(params, condition_type=condition_type, **kwargs)
        return self.__deal_res(res)

    def simple_get_one(self, **kwargs):
        res = super().simple_get_all(**kwargs)
        return self.__deal_res(res)

    def simple_get_join(self, join_entry, on_dict, *args,order_by=None, **kwargs):
        res = super().simple_get_join(join_entry, on_dict, *args, order_by=order_by, **kwargs)
        return self.__deal_res(res)


if __name__ == "__main__":
    print(BaseDao.simple_get_all.__doc__)
    from pprint import pprint

    pprint({"code": 0, "msg": "success", "data": [
        {"a": 1, "b": "\u4e2d\u56fd\u94f6\u884c", "c": "1", "d": 0, "e": 1},
        {"a": 1, "b": "\u4e0a\u6d77\u94f6\u884c", "c": "1", "d": 0, "e": 2},
        {"a": 1, "b": "\u4e2d\u4fe1\u94f6\u884c", "c": "1", "d": 0, "e": 3}]})
    pass
