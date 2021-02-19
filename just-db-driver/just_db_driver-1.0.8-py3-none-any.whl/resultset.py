# -*- coding: utf-8 -*-


import json
import time

import pandas as pd

from just.justerror import JustError


class ResultSet:
    """
    @author: hujian9@jd.com
    @description: 结果集
    @date: 2019-09-03 16:18
    """

    def __init__(self, execute_json_result, sql_id, session, sql_web_url, headers={}):
        """
        初始化函数
        :param execute_json_result: 执行JSON结果
        :param sql_id: SQL ID
        :param session: HTTP Session
        :param sql_web_url: WEB APP地址
        """
        self.__sql_id = sql_id
        self.__sql_web_url = sql_web_url
        self.__session = session
        self.__has_next = False
        self.__next_part_dict = None
        self._headers = headers

        self.__next_part_dict = self.__parse_execute_result(execute_json_result)
        if self.__next_part_dict['data']:
            # 第一次
            self.__has_next = True

    def next_part_dataframe(self):
        """
        获取下一部分DataFrame,,每一部分最多1万条数据
        :return: DataFrame
        """
        tmp_next_part_df = pd.DataFrame()
        self.__has_next = False
        if self.__next_part_dict and self.__next_part_dict['data']:
            if 'hasNext' in self.__next_part_dict['data']:
                self.__has_next = self.__next_part_dict['data']['hasNext']

            tmp_next_part_df = self.__dict_to_dataframe(self.__next_part_dict)

        self.__next_part_dict = None

        if self.__has_next:
            # 下一次
            url = self.__sql_web_url + "/api/sdk/v1/next/" + self.__sql_id
            response = self.__session.get(url, headers=self._headers)
            response.encoding = 'utf-8'
            json_result = response.text
            self.__next_part_dict = self.__parse_execute_result(json_result)

        return tmp_next_part_df

    def __parse_execute_result(self, execute_json_result):
        """
        解析执行结果
        :param execute_json_result: 执行JSON结果
        :return: dict
        """
        dict_data = json.loads(execute_json_result)
        result_code = dict_data['resultCode']
        if result_code != 200:
            result_msg = dict_data['resultMsg'] or '未知错误'
            raise JustError(result_msg)
        return dict_data

    def __dict_to_dataframe(self, dict_data):
        """
        字典转DataFrame
        :param dict_data: 字典数据
        :return: DataFrame
        """
        # print("解析JSON为DataFrame...")
        start = time.time()
        # 不存在数据时返回空
        if 'values' not in dict_data['data']:
            return pd.DataFrame()
        values = dict_data['data']['values']
        schema = dict_data['data']['schema']
        columns = []
        for item in schema:
            columns.append(item['name'])
        # index = list(range(1, len(values) + 1))
        # result_dict = {'index': index, 'columns': columns, 'data': values}
        result_dict = {'columns': columns, 'data': values}
        result_str = json.dumps(result_dict)
        df = pd.read_json(result_str, orient='split', dtype={'tid': str, 'oid': str})
        end = time.time()
        # print("解析完成,解析用时：%s" % (str(end - start)))
        return df

    def has_next(self):
        """
        是否有下一次
        :return: bool
        """
        return self.__has_next
