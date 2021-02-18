#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : result
# @Time         : 2021/2/18 6:16 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.zk_utils import zk_cfg
from meutils.http_utils import request


def get_ac(docid):
    return request(f"{zk_cfg.ac_url}/{docid}").json().get('item', {})


def get_acs(docids, max_workers=10):
    return docids | xThreadPoolExecutor(get_ac, max_workers) | xlist
