from pytz import timezone
from datetime import datetime, timedelta
import asyncio
from rethinkdb import r as rdb

host = 'localhost'
port = 28015
loop = asyncio.get_event_loop()
rdb.set_loop_type('asyncio')
conn = loop.run_until_complete(rdb.connect(db='test', host=host, port=port))
table = "STATION"
di = "11284c5c-458a-45a1-ac78-faa0bdd9facd"
query = rdb.db("test").table(table).get(di).run(conn)
result = loop.run_until_complete(query)
print(result)
if result:
    for q, v in result.items():
        print(q, v)
"""
Para valores entre -.5 y .5
"""

query = rdb.db("test").table(table).between(
    10, 500, **{
        "right_bound": "closed",
        'left_bound': "closed",
        "index": "COUNTER"
    }).run(conn)
result = loop.run_until_complete(query)
print(result)
