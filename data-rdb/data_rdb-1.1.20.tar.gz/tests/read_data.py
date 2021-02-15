import math
from pytz import timezone
from rethinkdb import RethinkDB
from data_rdb import Rethink_DBS
from rethinkdb import r
import asyncio
from datetime import datetime
from tasktools.taskloop import TaskLoop
from networktools.time import get_datetime_di
from networktools.colorprint import rprint, bprint, gprint
from asyncio import wait_for, shield
import random
rdb = RethinkDB()
rdb.set_loop_type('asyncio')

key = "DT_GEN"
filter_opt = {'left_bound': 'open', 'index': key}


async def run(*args, **kwargs):
    try:
        rdb = args[0]
        first = args[1]
        last = args[2]
        print("Running loop")
        di = kwargs['di']
        dbname = "test"
        if first:
            conn = await rdb.async_connect()
            print(f"Result {conn}")
            dbs = await rdb.list_dbs()
            result = await rdb.select_db(dbname)
            result = await rdb.list_tables()
            print(f"Databases...{dbs}")
            if dbs:
                first = False
            try:
                await rdb.list_tables()
                await asyncio.sleep(3)
            except Exception as e:
                print("Algo pasa...")
        df = rdb.iso8601(datetime.now().isoformat())
        final = 50
        gprint("-" * 30)
        bprint(f"Consultando di {di}, df {df}")
        gprint("-" * 30)
        try:
            cursor = await rdb.get_data_filter('STATION', [di, df], filter_opt,
                                               key)
            for c in cursor:
                print(f"New data ---> {c}")
            if not cursor:
                print("No data, {cursor}")
        except Exception as e:
            print("Error", e)
        await asyncio.sleep(5)
        kwargs['di'] = df
        return [rdb, first, last + final], kwargs
    except Exception as e:
        print("Error connection %s" % e)
        return args, kwargs


if __name__ == "__main__":
    di = datetime.now().isoformat()
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
