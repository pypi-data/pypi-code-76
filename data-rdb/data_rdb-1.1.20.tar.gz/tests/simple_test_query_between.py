from pytz import timezone
from datetime import datetime, timedelta
import asyncio
from rethinkdb import r as rdb

loop = asyncio.get_event_loop()


async def query():
    host = 'localhost'
    port = 28015
    rdb.set_loop_type('asyncio')
    conn = await rdb.connect(db='test', host=host, port=port)
    first = datetime.utcnow() - timedelta(seconds=200)
    tz = timezone("UTC")
    firsttz = tz.localize(first)
    firstrdb = rdb.iso8601(firsttz.isoformat())
    post = datetime.utcnow()
    posttz = tz.localize(post)
    postrdb = rdb.iso8601(posttz.isoformat())
    table = "STATION"
    filter_opt = {
        'left_bound': 'open',
        "right_bound": "open",
        'index': "DT_GEN"
    }
    print(f"Desde {firstrdb}, hasta {postrdb}")
    query_q = rdb.db("test").table(table).between(firstrdb, postrdb,
                                                  **filter_opt).run(conn)
    result = await asyncio.wait_for(query_q, timeout=60)
    return result


result = loop.run_until_complete(query())
print(result)
