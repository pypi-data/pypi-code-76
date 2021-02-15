from data_rdb import Rethink_DBS
from rethinkdb import r
import asyncio

kwargs = {
    'code': 'ATJN',
    'host': 'localhost',
    'port': 28015,
    'dbname': 'enu_data'
}


async def run(**kwargs):
    try:
        rdb = Rethink_DBS(**kwargs)
        conn = await rdb.async_connect()
        await r.table_create('marvel').run(conn)
        marvel_heroes = r.table('marvel')
        await marvel_heroes.insert({
            'id': 1,
            'name': 'Iron Man',
            'first_appearance': 'Tales of Suspense #39'
        }).run(conn)
        cursor = await marvel_heroes.run(conn)
        async for hero in cursor:
            print(hero['name'])

    except Exception as e:
        print("Error connection %s" % e)
        raise e


asyncio.get_event_loop().run_until_complete(run(**kwargs))
