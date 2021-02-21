#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created By Murray(m18527) on 2019/12/13 13:57
"""
from __future__ import absolute_import, unicode_literals

SUCCESS = 0

GONE_AWAY = -1
UNKNOWN_ERROR = 10000
BAD_REQUEST = 10001
ERROR_PARAMS = 10002

MSG = {
    SUCCESS: '正常。',
    GONE_AWAY: '服务器开小差了，请稍后再试。',
    UNKNOWN_ERROR: '未知错误。',
    BAD_REQUEST: '错误请求。',
    ERROR_PARAMS: '参数错误。',
}
