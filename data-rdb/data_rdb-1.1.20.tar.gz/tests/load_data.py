from rethinkdb import RethinkDB
from data_rdb import Rethink_DBS
from rethinkdb import r
import asyncio
from datetime import datetime
from tasktools.taskloop import TaskLoop
from networktools.time import get_datetime_di
import random
from pytz import timezone
import math
from networktools.colorprint import rprint
rdb = RethinkDB()
rdb.set_loop_type('asyncio')

key = "DT_GEN"


async def run(*args, **kwargs):
    try:
        rdb = args[0]
        first = args[1]
        counter = args[2]
        print("Running loop")
        di = kwargs['di']
        if first:
            conn = await rdb.async_connect()
            dbs = await rdb.list_dbs()
            dbname = "test"
            result = await rdb.create_db(dbname)
            result = await rdb.select_db(dbname)
            result = await rdb.list_tables()
            result = await rdb.create_table("STATION")
            result = await rdb.create_index("STATION", "DT_GEN")
            result = await rdb.create_index("STATION", "COUNTER")
            print(f"Databases...{dbs}")
            if dbs:
                first = False
            try:
                await rdb.list_tables()
                await asyncio.sleep(3)
            except Exception as e:
                print("Algo pasa...")
        data = {}
        dt_now = datetime.utcnow()
        zona_chile = timezone("UTC")
        fecha_chile = zona_chile.localize(dt_now)
        dt_gen = rdb.iso8601(fecha_chile.isoformat())
        data['DT_GEN'] = dt_gen
        data["COUNTER"] = counter
        data["VALOR"] = math.sin(random.randint(-10, 10))
        rprint(f"Guardando...{data}")
        cursor = await rdb.save_data("STATION", data)
        for c in cursor:
            print(f"New data ---> {c}")
        if not cursor:
            print("No data")
        await asyncio.sleep(.8)
        return [rdb, first, counter + 1], kwargs
    except Exception as e:
        print("Error connection %s" % e)
        await asyncio.sleep(10)
        return args, kwargs


if __name__ == "__main__":
    di = get_datetime_di(delta=-0)
    loop = asyncio.get_event_loop()
    kwargs = {
        'code': 'STATION',
        'host': 'localhost',
        'port': 28015,
        'dbname': 'test'
    }
    rdb = Rethink_DBS(**kwargs)
    task = TaskLoop(run, [rdb, True, 0], {'di': rdb.iso8601(di)},
                    **{"name": "run_test_rdb"})
    task.create()
    loop.run_forever()
