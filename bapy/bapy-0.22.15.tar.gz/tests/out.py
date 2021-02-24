#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from bson import CodecOptions
from bson.codec_options import TypeRegistry

from test_IPBase import addr_loc_name
from bson.son import SON
from bson.codec_options import TypeCodec
from bson.codec_options import TypeDecoder

from bapy import *
from pymongo import MongoClient

ic.enabled = True
red('Custom Type Example', e=False)

client = MongoClient()
client.drop_database('test')
db = client.test

magenta('The TypeCodec Class')


class IPBaseCodec(TypeCodec):
    python_type = IPBase
    bson_type = SON

    def transform_python(self, value):
        return value.asdict

    def transform_bson(self, value):
        return IPBase(value.to_dict())


ipbase_coded = IPBaseCodec()
magenta('The TypeRegistry Class¶')

type_registry = TypeRegistry([ipbase_coded])
magenta('Putting It Together')

codec_options = CodecOptions(type_registry=type_registry)
collection = db.get_collection('test', codec_options=codec_options)

collection.insert_one({'ipbase': addr_loc_name})

mydoc = collection.find_one()

vanilla_collection = db.get_collection('test')
ic(vanilla_collection.find_one())
collection.drop()
client.drop_database('test')

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

