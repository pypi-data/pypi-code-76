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
    postrdb = firstrdb
    conn = args[2]
    if not connected:
        conn = await rdb.connect(db='test', host=host, port=port)
        connected = True
    if connected:
        await asyncio.sleep(5)
        val2 = val + 20
        print(f"Desde {firstrdb}, hasta {postrdb}")
        query = rdb.db("test").table(table).filter(
            lambda data: data["DT_GEN"] >= firstrdb).coerce_to(
                "array").order_by("DT_GEN").run(conn)
        result = await query
        if result:
            lista = []
            for q in result:
                print(q)
                lista.append(q)
            postrdb = lista[-1]["DT_GEN"]
            print("Las data", postrdb)
    return [connected, postrdb, conn], kwargs


connected = False
now = date_rdb()
conn = None
val = 0
args = [connected, now, conn]
kwargs: dict = {}

task = TaskLoop(run, args, kwargs, **{"name": "test_query_dt_gen"})
task.create()
loop.run_forever()
