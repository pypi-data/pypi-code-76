"""
Index: COUNTER
Python 3.6
Python 3.8
"""

from pytz import timezone
from datetime import datetime, timedelta
import asyncio
from rethinkdb import r as rdb
from tasktools.taskloop import TaskLoop
from networktools.colorprint import bprint, rprint, gprint

host = 'localhost'
port = 28015
loop = asyncio.get_event_loop()
rdb.set_loop_type('asyncio')
filter_opt = {'left_bound': 'open', 'index': "COUNTER"}
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
        gprint("MMMMMMMMMMM")
        bprint(f"Desde {firstrdb}, hasta {postrdb}")
        gprint("WWWWWWWWWWW")
        query = rdb.db("test").table(table).between(
            firstrdb,
            postrdb,
            index="DT_GEN",
            left_bound="closed",
            right_bound="open").coerce_to("array").order_by("DT_GEN").run(conn)
        result = await query
        if result:
            element = None
            for q in result:
                element = q
            if element:
                firstrdb = element["DT_GEN"]
            print("Las data", postrdb)
        else:
            print(f"No data...{result}")
    return [connected, firstrdb, conn], kwargs


connected = False
now = date_rdb()
conn = None
args = [connected, now, conn]
kwargs: dict = {}

task = TaskLoop(run, args, kwargs, **{"name": "test_query_dt_gen"})
task.create()
loop.run_forever()
