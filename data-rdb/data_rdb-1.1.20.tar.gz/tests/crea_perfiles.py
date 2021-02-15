"""
Este test se trata de:

- pedir un nombre de database
- listar database
- listar tablas
- crear/seleeccionar la database
- crear tabla
- crear DT_GEN

- pedir nombres, edad, mascota
- crear un dic con llave DT_GEN
"""
import asyncio
from functools import partial
from datetime import datetime
from networktools.colorprint import gprint, bprint, rprint
from networktools.library import choice_input
from tasktools.taskloop import coromask, renew, simple_fargs_out
from data_rdb.rdb import Rethink_DBS
from pytz import timezone
off_actions = {
    "conectar":"conectar"
}
on_actions = {
    "listar_db":"listar_db",
    "crear_db":"crear_db",
    "select_db":"select_db",
    "listar_tablas":"listar_tablas",
    "crear_tabla":"crear_tabla",
    'set_tabla': 'set_tabla',
    "crear_index":"crear_index",
    "add_data":"add_data"
}

async def ciclo(*args, **kwargs):
    await asyncio.sleep(1)
    connected = kwargs.get('connected')
    gprint("esperar %s" %connected)
    if not connected:
        print("RDB no conectada")
        command, option, msg_type = choice_input(off_actions, xprint=rprint)
        if command == "conectar":
            creds =  kwargs.get('credentials')
            rdb = Rethink_DBS(**creds)
            await rdb.async_connect()
            kwargs["connected"] = True
            kwargs["rdb"] = rdb
    else:
        rdb = kwargs.get('rdb')
        print("RDB", rdb)
        command, option, msg_type = choice_input(on_actions, xprint=rprint)
        if command == "listar_db":
            dbs = await rdb.list_dbs()
            print("Lista de databases")
            print(dbs)
            kwargs["dbs"] = dbs
        elif command == "crear_db":
            name = input("Nombre de database ")
            result = await rdb.create_db(name)
            print("Resultado de creard db", result)
        elif command == "select_db":
            dbs =  kwargs.get("dbs")
            print("de kwargs", dbs)
            print("de rdb", rdb.dblist)
            name =  input("Seleccionar db: ")
            if name in rdb.dblist:
                result = await rdb.select_db(name)
                print("seleccionar db", result)
                kwargs['db']=name
            else:
                print("No existe db")
        elif command == "listar_tablas":
            result = await rdb.list_tables()
            print("Lista de tablas:", result)
        elif command=="crear_tabla":
            name = input("nombre de tabla: ")
            result = await rdb.create_table(name)
            print("Resultado de crear tabla", result)
        elif command == 'set_tabla':
            name = input("nombre de tabla: ")
            if name in rdb.tables.get(kwargs["db"]):
                kwargs['tabla'] = name
            else:
                print("No existe esa tabla")
        elif command=="crear_index":
            print("Tablas disponiles", rdb.tables)
            print("Tablas disponiles", rdb.tables.get(kwargs["db"]))
            name = input("nombre de tabla: ")
            if name in rdb.tables.get(kwargs["db"]):
                indexes = await rdb.get_indexes(name)
                print("Indices en tabla:", indexes, "default db", rdb.default_db)
                index = input("nombre de index: ")
                result = await rdb.create_index(name, index)
                print("Creación de index", result)
            else:
                print("No existe esa tabla")
        elif command=='add_data':
            data = {}
            dt_now = datetime.utcnow()
            zona_chile = timezone("America/Santiago")
            fecha_chile = zona_chile.localize(dt_now)
            dt_gen = rdb.iso8601(fecha_chile.isoformat())
            data['DT_GEN'] = dt_gen
            data["NOMBRE"] = input("nombre? ")
            data["APELLIDO"] = input("apellido? ")
            data["EDAD"] = float(input("edad? "))
            data["EMAIL"] = input("email? ")
            resultado = await rdb.save_data(kwargs["tabla"], data)
            print("Resultado de guardar datos")
            bprint(resultado)
    return args, kwargs


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    iteracion = 0
    args = [iteracion]
    credentials = {"host":"localhost", "port":28015}
    kwargs = {"connected":False, "credentials": credentials}
    task = loop.create_task(coromask(ciclo, args, kwargs, simple_fargs_out))
    task.add_done_callback(partial(renew, task, ciclo, simple_fargs_out))
    loop.run_until_complete(task)
    if not loop.is_running():
        loop.run_forever()

