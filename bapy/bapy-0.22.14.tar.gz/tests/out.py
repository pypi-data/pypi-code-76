#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from bson.son import SON
from bson.codec_options import TypeCodec
from bson.codec_options import TypeDecoder

from bapy import *
from tests import *
from pymongo import MongoClient

ic.enabled = True
client = MongoClient()
client.drop_database('custom_type_example')
db = client.custom_type_example

class IPBaseCodec(TypeCodec):
    python_type = IPBase
    bson_type = SON

    def transform_python(self, value):


    def transform_bson(self, value):
        return value.to_dict()

#
# ic(ipmine())
# ic(asyncio.run(ipmine_aio()))
# loc = ic(iploc())
# ic(asyncio.run(iploc_aio()))
# addr = ic(ipaddr())
# ic(addr.public)
# addr = ic(ipaddr(loc=loc))
# ic(addr.public)
#
# addr_aio = ic(asyncio.run(ipaddr_aio()))
# ic(addr_aio.public)
#
# addr = ic(ipaddr('4.4.4.4'))
# ic(ipaddr('4.4.4.4').text)
#
# addr = ic(ipaddr('4.4.4.4', loc=True))
# ic(ipaddr('4.4.4.4').text)
# ic(addr.public)

if __name__ == '__main__':
    pass

