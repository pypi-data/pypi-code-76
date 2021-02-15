"""
Index: COUNTER
Python 3.6
Python 3.8

The query is correct with the value.
"""

from pytz import timezone
from datetime import datetime, timedelta
import asyncio
from rethinkdb import r as rdb
from tasktools.taskloop import coromask, renew, simple_fargs_out
from functools import partial

host = 'localhost'
port = 28015
loop = asyncio.get_event_loop()
rdb.set_loop_type('asyncio')
filter_opt = {
    'left_bound': 'open',
    "right_bound": "closed",
    'index': "COUNTER"
}
table = "STATION"


def date_rdb(td=0):
    first = datetime.utcnow() + timedelta(seconds=td)
    tz = timezone("UTC")
    firsttz = tz.localize(first)
    firstrdb = rdb.iso8601(firsttz.isoformat())
    return firstrdb


async def run(*args, **kwargs):
    connected = args[0]
    firstrdb = args[1]
    val = args[1]
    conn = args[2]
    if not connected:
        conn = await rdb.connect(db='test', host=host, port=port)
        connected = True
    if connected:
        await asyncio.sleep(5)
        val2 = val + 20
        postrdb = date_rdb()
        print(f"Desde {firstrdb}, hasta {postrdb}")
        query = rdb.db("test").table(table).between(val, val2,
                                                    **filter_opt).run(conn)
        result = await query
        print(result)
    return [connected, val2, conn], kwargs


connected = False
now = date_rdb()
conn = None
val = 0
#args = [connected, now, conn]
args = [connected, val, conn]
kwargs: dict = {}

task = loop.create_task(coromask(run, args, kwargs, simple_fargs_out))
task.add_done_callback(partial(renew, task, run, simple_fargs_out))

loop.run_forever()
