#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : field_utils
# @Time         : 2020/12/2 11:32 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from typing import List


def gen_fields(str_names: List[str] = None, float_names: List[str] = None, datetime_names: List[str]=None):
    result = []
    if str_names:
        result += [f"{name}: str = None" for name in str_names]
    if float_names:
        result += [f"{name}: float = None" for name in float_names]
    # return name_str
    print('\n'.join(result))

