# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------
    File Name:              base
    Description:            
    Author:                 hzy
    date:                   2019/8/24
------------------------------------------------------------------
    Change Activity:
                            2019/8/24
------------------------------------------------------------------
"""

__author__ = 'hzy'

import time
from flask_templates.common.utils import BaseError, construct_result
from flask_templates.var import ErrorCode, USER_ID, TOKEN_PARAM_NAME, CHARACTER_PARAM_NAME, VISITOR_ID
from flask_templates.common.class_holder import ClassHolder
import functools


class ServiceError(BaseError):
    base_msg = 'service error'


class ServiceForViewError(ServiceError):
    message = ''
    code = 0

    def __init__(self):
        super().__init__(msg=self.message)

    @property
    def resp(self):
        return construct_result(self.code, self.message)


class TokenLostError(ServiceForViewError):
    code = ErrorCode.TOKEN_LOST_ERROR
    message = TOKEN_PARAM_NAME + ' lost!'

    def __init__(self, **kwargs):
        self.message = self.message.format(**kwargs)
        super().__init__()


class AuthError(ServiceForViewError):
    code = ErrorCode.AUTH_ERROR
    message = 'auth error!info:{info}'

    def __init__(self, **kwargs):
        self.message = self.message.format(**kwargs)
        super().__init__()


class RangeError(ServiceForViewError):
    code = ErrorCode.RANGE_ERROR
    message = '{param} not in range {range_list}!'

    def __init__(self, **kwargs):
        self.message = self.message.format(**kwargs)
        super().__init__()


class ExceedLimitError(ServiceForViewError):
    code = ErrorCode.EXCEED_LIMIT_ERROR
    message = '{param}超过限制'

    def __init__(self, **kwargs):
        self.message = self.message.format(**kwargs)
        super().__init__()


class PermissionForbiddenError(ServiceForViewError):
    code = ErrorCode.PERMISSION_FORBIDDEN_ERROR
    message = '行内资产无法修改和删除'


class NotFoundError(ServiceForViewError):
    code = ErrorCode.NOT_FOUND_ERROR
    message = '{param}不存在'

    def __init__(self, **kwargs):
        self.message = self.message.format(**kwargs)
        super().__init__()


class DuplicateError(ServiceForViewError):
    code = ErrorCode.DUPLICATE_ERROR
    message = '{param}重复'

    def __init__(self, **kwargs):
        self.message = self.message.format(**kwargs)
        super().__init__()


class AccountError(ServiceForViewError):
    code = ErrorCode.ACCOUNT_ERROR
    message = '{msg}'

    def __init__(self, **kwargs):
        self.message = self.message.format(**kwargs)
        super().__init__()


class DBError(ServiceForViewError):
    code = ErrorCode.DB_ERROR
    message = '存储数据异常'

    def __init__(self, **kwargs):
        self.message = self.message.format(**kwargs)
        super().__init__()


class CountiFeignError(ServiceError):
    code = ErrorCode.COUNTI_FEIGN_ERROR
    message = 'counti request error info :{info}'

    def __init__(self, **kwargs):
        self.message = self.message.format(**kwargs)
        super().__init__(self.message)


class BankFeignError(ServiceError):
    code = ErrorCode.BANK_FEIGN_ERROR
    message = 'bank request error info :{info}'

    def __init__(self, **kwargs):
        self.message = self.message.format(**kwargs)
        super().__init__(self.message)


class CountiValidationError(ServiceError):
    code = ErrorCode.COUNTI_VALIDATION_ERROR
    def __init__(self, msg, data):
        self.message = msg
        self.messages =msg
        self.valid_data = data
        super().__init__(msg=self.message)


class BaseChecker:

    def check_access(self,*args,**kwargs):
        pass

def check_auth(character=None):
    """
    检验调用权限函数
    :param character:
    :return:
    """

    def auth(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if TOKEN_PARAM_NAME not in kwargs:
                raise TokenLostError()
            character_name = kwargs.setdefault(CHARACTER_PARAM_NAME, None)
            result = ClassHolder().get(BaseChecker).check_access(kwargs[TOKEN_PARAM_NAME], character_name)
            # kwargs.pop(TOKEN_PARAM_NAME)
            if character_name is None:
                kwargs[USER_ID] = result
            kwargs[VISITOR_ID] = result
            return func(*args, **kwargs)

        return wrapper

    return auth


def get_user_id(kwargs):
    token = kwargs[USER_ID]

    return token['user_id']


def catch_feign(service_error):
    def do(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # res = func(*args, **kwargs)
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                raise service_error(info=str(e))
            return res

        return wrapper

    return do

