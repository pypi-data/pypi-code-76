#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : date_utils
# @Time         : 2020/11/12 11:41 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from meutils.common import *

"""
pd.to_datetime(time.time(), unit='s')
>>> f'{now:%Y-%m-%d %H:%M:%S}'

"""


def date_difference(format='%Y-%m-%d %H:%M:%S', **kwargs) -> str:
    """
    days: float = ...,
    seconds: float = ...,
    microseconds: float = ...,
    milliseconds: float = ...,
    minutes: float = ...,
    hours: float = ...,
    weeks
    """
    now = datetime.datetime.now()  # datetime.datetime.today()
    date = now - datetime.timedelta(**kwargs)
    return date.strftime(format)


if __name__ == '__main__':
    print(date_difference(days=1))
