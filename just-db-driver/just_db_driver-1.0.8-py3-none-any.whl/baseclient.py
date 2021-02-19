# -*- coding: utf-8 -*-

import json
import uuid

import requests

from just.justerror import JustError


class BaseClient:
    """
    @author: hujian9@jd.com
    @description: Client 基类
    @date: 2019-08-15 11:57
    """

    # WEB APP 地址
    _default_sql_web_app_url = 'http://portal-just.jd.com'
    # 客户端是否关闭
    __is_closed = False

    def __init__(self, public_key, secret_key, sql_web_app_url=None, stand_alone=False):
        """
        初始化函数
        :param public_key: 公钥
        :param secret_key: 秘钥
        :param sql_web_app_url: WEB APP地址
        """
        self._public_key = public_key
        self._secret_key = secret_key
        self._stand_alone = stand_alone
        if sql_web_app_url:
            self._default_sql_web_app_url = sql_web_app_url
        # 默认DB
        self._default_db = "default"
        # 当前正在使用的DB
        self._current_db = self._default_db
        self.__page_token = str(uuid.uuid1()).replace('-', '')
        self._headers = {}
        self._session = None
        self.connect()

    def connect(self):
        # page token
        self.__page_token = str(uuid.uuid1()).replace('-', '')
        # 请求头
        self._headers = {
            'User-agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
            'Content-Type': 'application/json',
            'publicKey': self._public_key,
            'secretKey': self._secret_key,
            'dbName': self._current_db,
            'pageToken': self.__page_token,
            'standAlone': 'true' if self._stand_alone else 'false'
        }
        self._session = self._link_session()

    def _link_session(self):
        """
        创建一个有效的session对象
        :return: http session对象
        """
        # 构造Session
        session = requests.Session()
        # 进行ping-pong
        auth_url = self._default_sql_web_app_url + "/api/sdk/v1/pong"
        response = session.get(auth_url, headers=self._headers)
        response.encoding = 'utf-8'
        json_result = response.text
        dict_data = json.loads(json_result)
        result_code = dict_data['resultCode']
        if result_code == 200:
            return session
        else:
            result_msg = dict_data['resultMsg']
            raise JustError(result_msg)

    def close(self):
        """
        关闭客户端
        :return: None
        """
        if not self.__is_closed:
            url = self._default_sql_web_app_url + "/api/sdk/v1/clear"
            response = self._session.post(url, headers=self._headers)
            response.encoding = 'utf-8'
            json_result = response.text
            dict_data = json.loads(json_result)
            result_code = dict_data['resultCode']
            if result_code == 200:
                self.__is_closed = True

    def __enter__(self):
        """
        紧跟with后面的语句被执行后,该函数自动被调用,返回值将被赋值给as后面的变量
        :return: self
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        当with后面的代码块全部被执行完之后, 该函数自动被调用
        :return: None
        """
        self.close()
