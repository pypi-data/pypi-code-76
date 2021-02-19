# -*- coding: utf-8 -*-
import hashlib
import random
import string
import time
from abc import abstractmethod
from typing import Optional

from flask import request

from easi_py_common.core.error import ServiceException


def __is_int(s):
    try:
        int(s)
        return True
    except Exception:
        pass
    return False


def __to_str(s):
    if isinstance(s, str):
        return s
    return str(s or '')


def __generate_sign(app_key: str, app_secret: str, url: str, method: str, body_str: str, timestamp: str, nonce: str,
                    salt: str = '&') -> str:
    signs = [__to_str(app_key), __to_str(app_secret), __to_str(timestamp), __to_str(nonce), __to_str(method),
             __to_str(url), __to_str(body_str)]
    signs = sorted(signs)
    sg = salt.join(signs)

    h = hashlib.md5()
    h.update(sg.encode("utf8"))
    sign = h.hexdigest()
    return sign.upper()


def generate_sign(app_key: str, app_secret: str, url: str, method: str, body_str: str = '', salt: str = '&') -> (
        str, str, str):
    timestamp = str(int(time.time() * 1000))
    nonce = ''.join(random.sample(string.digits + string.ascii_letters, 32))
    sign = __generate_sign(app_key, app_secret, url, method, body_str, timestamp, nonce, salt)

    return timestamp, nonce, sign


def valid_sign(app_key: str, app_secret: str, url: str, method: str, body_str: str, timestamp: str, nonce: str,
               sign: str, salt: str = '&') -> bool:
    if not nonce or len(nonce) < 16:
        return False
    if not timestamp or not __is_int(timestamp):
        return False
    if not sign:
        return False

    valid_generate_sign = __generate_sign(app_key, app_secret, url, method, body_str, timestamp, nonce, salt)
    return valid_generate_sign == str(sign).upper()


class AppInfo:
    def __init__(self, app_key: str, app_secret: str, self_info: object = None):
        self.app_key = app_key
        self.app_secret = app_secret
        self.self_info = self_info


class AppInfoService:
    @abstractmethod
    def get_app_info(self, app_key: str) -> AppInfo: pass


class AppSignValidService:
    def __init__(self, app_info_service: AppInfoService, salt: str = '&',
                 header_app_key: str = 'app_key',
                 header_timestamp: str = 'timestamp',
                 header_nonce: str = 'nonce',
                 header_sign: str = 'sign'):

        self.app_info_service = app_info_service
        self.salt = salt
        self.header_app_key = header_app_key
        self.header_timestamp = header_timestamp
        self.header_nonce = header_nonce
        self.header_nonce = header_nonce
        self.header_sign = header_sign

    def __get_header_value(self, name):
        return request.headers[name] if name in request.headers else None

    def __get_url(self):
        url = request.full_path
        index = url.index("?")
        if index != -1:
            if len(url) - index == 1:
                url = url[0:index]
        return url

    def valid(self):
        app_key = self.__get_header_value(self.header_app_key)
        timestamp = self.__get_header_value(self.header_timestamp)
        nonce = self.__get_header_value(self.header_nonce)
        sign = self.__get_header_value(self.header_sign)
        request_data = request.get_data().decode('utf-8')
        url = self.__get_url()

        app_info = self.app_info_service.get_app_info(app_key)
        if not valid_sign(app_key=app_info.app_key, app_secret=app_info.app_secret, url=url,
                          method=request.method.upper(), body_str=request_data, timestamp=timestamp, nonce=nonce,
                          sign=sign, salt=self.salt):
            raise ServiceException(code=400, msg=u"invalid sign")

        return app_info.self_info
