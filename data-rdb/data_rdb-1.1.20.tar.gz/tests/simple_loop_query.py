"""
Python 3.8
"""

from pytz import timezone
from datetime import datetime, timedelta
import asyncio
from rethinkdb import r as rdb
from tasktools.taskloop import TaskLoop

host = 'localhost'
port = 28015
loop = asyncio.get_event_loop()
rdb.set_loop_type('asyncio')
filter_opt = {'left_bound': 'open', 'index': "DT_GEN"}
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
    conn = args[2]
    if not connected:
        conn = await rdb.connect(db='test', host=host, port=port)
        connected = True
    if connected:
        await asyncio.sleep(5)
        postrdb = date_rdb()
        print(f"Desde {firstrdb}, hasta {postrdb}")
        query = rdb.db("test").table(table).between(firstrdb,
                                                    postrdb,
                                                    left_bound='closed',
                                                    right_bound='closed',
                                                    index='DT_GEN').run(conn)
        result = await query
        print(result)
        if result:
            firstrdb = postrdb
    return [connected, firstrdb, conn], kwargs


connected = False
now = date_rdb(-100)
conn = None
args = [connected, now, conn]
kwargs: dict = {}

task = TaskLoop(run, args, kwargs)
task.create()

loop.run_forever()
