#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : client
# @Time         : 2020/12/4 3:33 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import thriftpy2
thrift = thriftpy2.load("ping.thrift", module_name="ping__thrift")

from thriftpy2.rpc import make_client

client = make_client(thrift.Test)
print(client.ping())
