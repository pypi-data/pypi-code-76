# -*- coding: utf-8 -*-

import json
import uuid

import pandas as pd

from just.baseclient import BaseClient
from just.justerror import JustError
from just.resultset import ResultSet
from just.stable import keep_connection


class JustClient(BaseClient):
    """
     JUST客户端
    pydocmd simple just+ just.justclient.JustClient+ > docs.md
    :date 2019-08-14 16:00
    """

    # 最大重试次数
    max_retry = 3

    def __init__(self, public_key, secret_key, sql_web_app_url=None, stand_alone=False, max_retry=3):
        """
        初始化函数
        :param public_key: 公钥
        :param secret_key: 秘钥
        :param sql_web_app_url: WEB APP地址
        :param stand_alone 是否使用单机版
        """
        super(JustClient, self).__init__(public_key, secret_key, sql_web_app_url, stand_alone)

        JustClient.max_retry = max_retry
        self.__page_size = 0
        self.__do_page = True
        # k：dbName   v: dbId
        self.__db_dict = {}
        # 1.初始化 __db_dict
        self.list_db()

    def __set_token(self):
        """
        设置token
        :returns: void
        """
        url = self._default_sql_web_app_url + "/api/sdk/v1/setToken"
        response = self._session.post(url, headers=self._headers)
        self.__parse_response_result(response)

    def get_current_db(self):
        """
        获取当前正在使用的DB
        :return: 当前的DB名称
        """
        return self._current_db

    def list_db(self):
        """
        查看所有的DB
        :return: DataFrame
        """
        url = self._default_sql_web_app_url + "/api/sdk/v1/dbs"
        response = self._session.get(url, headers=self._headers)
        response.encoding = 'utf-8'
        json_result = response.text
        dict_data = json.loads(json_result)
        result_code = dict_data['resultCode']
        if result_code == 200:
            data_list = []
            data = dict_data['data']
            for item in data:
                data_list.append({
                    'db_name': item['name']
                })
                self.__db_dict[item['name']] = item['id']
            json_list = json.dumps(data_list)
            df = pd.read_json(json_list, orient='values')
            return df
        else:
            result_msg = dict_data['resultMsg']
            raise JustError(result_msg)

    def delete_db(self, db_name):
        """
        删除DB
        :param db_name: DB名称
        :return: bool 是否删除成功
        """
        # 判断是否有该库
        if db_name == self._default_db:
            raise JustError("default库不可删除")
        db_id = self.__db_dict.get(db_name, None)
        if db_id:
            url = self._default_sql_web_app_url + "/api/sdk/v1/db/" + str(db_id)
            response = self._session.delete(url, headers=self._headers)
            try:
                self.__parse_response_result(response)
                # 移除__db_dict中对应的kv
                self.__db_dict.pop(db_name)
                # 如果删除的db是当前正在使用的db, 切换当前db为default
                if db_name == self._current_db:
                    self._current_db = self._default_db
                return True
            except JustError as e:
                return False
        else:
            raise JustError("删除的" + db_name + "库不存在")

    def create_db(self, db_name):
        """
        创建DB
        :param db_name: DB名称
        :return: bool
        """
        url = self._default_sql_web_app_url + "/api/sdk/v1/db"
        json_str = {'dbName': db_name}
        response = self._session.post(url, json=json_str, headers=self._headers)
        try:
            self.__parse_response_result(response)
            # 刷新__db_dict
            self.list_db()
            return True
        except JustError as e:
            return False

    def use_db(self, db_name):
        """
        切换DB
        :param db_name: DB名称
        """
        # 判断是否有该库
        db_id = self.__db_dict.get(db_name, None)
        if db_id:
            url = self._default_sql_web_app_url + "/api/sdk/v1/useDb"
            json_str = {'dbName': db_name}
            response = self._session.post(url, json=json_str, headers=self._headers)
            self.__parse_response_result(response)
            self._current_db = db_name
            self._headers['dbName'] = self._current_db
        else:
            raise JustError("您选择的" + db_name + "库不存在,切换失败")

    @keep_connection
    def execute_query(self, sql):
        """
        执行DQL、DAL语句(SELECT、SHOW TABLES等语句)
        :param sql: SQL语句
        :return: 结果集DataFrame
        """
        sql_id = self.__generate_sql_id()
        json_result = self.__execute_http(sql, sql_id)
        return ResultSet(json_result, sql_id, self._session, self._default_sql_web_app_url, self._headers)

    @keep_connection
    def execute_update(self, sql):
        """
        执行DDL、DML语句(CREATE TABLE、DROP TABLE等语句)
        失败会抛异常
        :param sql: SQL语句
        :raise JustError
        """
        sql_id = self.__generate_sql_id()
        json_result = self.__execute_http(sql, sql_id)
        dict_data = json.loads(json_result)
        result_code = dict_data['resultCode']
        if result_code != 200:
            result_msg = dict_data['resultMsg']
            raise JustError(result_msg)

    def __generate_sql_id(self):
        """
        生成SQL ID
        :return 只含有下划线和字母数字的token
        """
        return str(uuid.uuid1()).replace("-", "")

    def __execute_http(self, sql, sql_id):
        """
        发送网络请求执行SQL语句
        :param sql: SQL语句
        :return JSON字符串
        """
        json_str = {'sql': sql, 'dbId': self.__db_dict[self._current_db], 'sqlId': sql_id, 'pageSize': self.__page_size,
                    'doPage': self.__do_page}
        sql_execute_url = self._default_sql_web_app_url + "/api/sdk/v1/execute"
        response = self._session.post(sql_execute_url, json=json_str, headers=self._headers)
        response.encoding = 'utf-8'
        return response.text

    def __parse_response_result(self, response):
        """
        解析响应结果
        :param response
        """
        response.encoding = 'utf-8'
        json_result = response.text
        dict_data = json.loads(json_result)
        result_code = dict_data['resultCode']
        if result_code != 200:
            result_msg = dict_data['resultMsg']
            raise JustError(result_msg)

    def set_page_size(self, page_size):
        """
        只有当查询语句的结果集条数大于10000才有效
        :param page_size 每页数据大小
        """
        self.__page_size = page_size

    def set_do_page(self, do_page):
        """
        设置是否分页，默认true
        :param do_page 是否分页
        """
        self.__do_page = do_page


if __name__ == "__main__":
    pass
