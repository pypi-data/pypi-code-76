from rethinkdb import r as rdb
import asyncio
from typing import Callable, Dict
from datetime import datetime, timezone
from pathlib import Path
import os
import time
import socket
from networktools.colorprint import bprint, gprint, rprint
from datadbs.general import GeneralData
from asyncio import shield, wait_for
from rethinkdb.errors import RqlDriverError, RqlError


class Rethink_DBS(GeneralData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.station = self.code
        self.default_db = kwargs.get('dbname')
        self.loop = kwargs.get('io_loop')
        if self.loop:
            asyncio.set_event_loop(self.loop)
        self.env = kwargs.get('env', 'natural')
        self.dblist = []
        self.tables = {}
        self.index = {}
        self.set_defaultdb(self.dbname)
        r = rdb
        r.set_loop_type('asyncio')
        self.r = r

    async def msg_log(self, msg, level):
        if self:
            self.save_log(msg, level)

    async def async_connect(self, loop=None, *args, **kwargs):
        self.session = None
        try:
            if self.default_db:
                kwargs = {}
                if not loop:
                    kwargs = {'io_loop': loop}
                else:
                    kwargs = {'io_loop': self.loop}
                dbname = self.dbname
                dbhost = self.address[0]
                dbport = self.address[1]
                gprint("=" * 30)
                bprint(
                    f"Conectando {dbname}, {dbhost}, {dbport}, for station {self.station}"
                )
                gprint("=" * 30)
                self.session = await self.r.connect(db_name=dbname,
                                                    host=dbhost,
                                                    port=dbport,
                                                    **kwargs)
                self.logger.info(
                    f"Connected to RethinkDB with database {self.default_db}")
            else:
                self.session = await self.r.connect(host=self.host,
                                                    port=self.port)
                self.logger.info(
                    "Connected to RethinkDB without database selected")
        except (RqlDriverError, RqlError) as r_error:
            kwargs["origin_exception"] = RqlError
            msg = f'''PD_CONN, ConnectionClosed {r_error} connection....'''
            self.logger.exception(kwargs.get("origin_exception"))
            raise r_error
        except (socket.error, ConnectionResetError,
                ConnectionAbortedError) as conn_error:
            msg = f'''PD_TOA_-1 + {conn_error}, ConnectionClosed rc_enu
        connection....{{socket.error}}'''
            kwargs["origin_exception"] = msg
            self.logger.exception(kwargs.get("origin_exception"))
            raise conn_error
        except Exception as ex:
            self.logger.exception("Excepcion al conectar a Rethinkdb %s" % ex)
            raise ex
        return self.session

    async def close(self):
        if self.session:
            await self.session.close(noreply_wait=True)
        super().close()

    async def reconnect(self, wait=False):
        await self.session.reconnect(noreply_wait=wait)

    # database manage
    def set_defaultdb(self, dbname: str, first_time=False):
        if dbname:
            self.default_db = dbname
            print("Station %s, db %s" % (self.station, self.default_db))
            if first_time:
                self.logger.info("Database set on %s by default" % dbname)

    @property
    def defaultdb(self):
        return self.default_db

    async def server_info(self):
        self.logger.info("Info from server obtained")
        return await self.session.server()

    async def select_db(self, dbname: str = None):
        list_dbs = await self.list_dbs()
        if dbname not in list_dbs:
            await self.create_db(dbname)
        if not dbname:
            result = self.session.use(self.defaultdb)
            self.set_defaultdb(self.defaultdb, first_time=True)
            self.logger.info("Set default db to use on session %s" % dbname)
            return result
        else:
            result = await self.list_dbs()
            if dbname in self.dblist:
                result = self.session.use(dbname)
                self.set_defaultdb(dbname, first_time=True)
                self.logger.info("Set db to use on session %s" % dbname)
                return "Usando %s" % dbname
            else:
                self.logger.error(
                    "Set default db to use on session, and database doesn\'t exists %s"
                    % dbname)
                result = await self.create_db(dbname)
                return result

    async def create_db(self, dbname: str = None):
        try:
            if not dbname and self.defaultdb:
                dbname = self.defaultdb
            await self.list_dbs()
            result = None
            if dbname and dbname not in self.dblist:
                self.set_defaultdb(dbname)
                result = await self.r.db_create(dbname).run(self.session)
                self.logger.info("Database %s creada" % dbname)
            else:
                result = "Database exists"
            return result
        except Exception as e:
            print("An exception happen when try to create a database: %s" % e)
            self.logger.exception("Error al intentar crear Database %s" % e)

    async def delete_db(self, dbname: str):
        self.logger.info("Delete database %s" % dbname)
        return await self.r.db_drop(dbname).run(self.session)

    async def list_dbs(self):
        self.logger.info("Lists databases on %s" % self.hostname)

        self.dblist = await self.r.db_list().run(self.session)
        # print("Lista de databasesx")
        return self.dblist

    # table manager

    async def create_table(self, table_name: str, dbname: str = None):
        self.logger.info("Creating table %s" % table_name)
        if not dbname:
            dbname = self.default_db
        try:
            await self.list_tables(self.defaultdb)
            # print("Tables by database: %s" %self.tables)
            if dbname in self.tables.keys():
                # print("Inside create tables")
                if table_name not in self.tables[dbname]:
                    self.logger.info("Creating table named %s" % table_name)
                    result = await self.r.db(dbname).table_create(
                        table_name).run(self.session)
                    await self.list_tables()
                    return {"result":result,"created":True}
                else:
                    self.logger.error("Table exists %s" % table_name)
                    msg = "Table Name %s exists" % table_name
                    # print(msg)
                    return {'msg': msg}
        except Exception as e:
            self.logger.exception(
                "Error crítico al crear tabla %s, exception" % (e))
            raise e

    async def get_indexes(self, table_name: str, dbname: str = None):
        if not dbname:
            dbname = self.default_db
        await self.list_tables()
        if table_name in self.tables.get(dbname, {}):
            indexes = await self.r.db(dbname).table(
                table_name).index_list().run(self.session)
            self.index.update({table_name: indexes})
            self.logger.info("Obtaining list of indexes %s" % indexes)
            return indexes
        else:
            return []

    async def create_index(self,
                           table_name: str,
                           index: str = None,
                           dbname: str = None):
        self.logger.info("Creating index %s on table %s" % (index, table_name))
        if not dbname:
            dbname = self.default_db
        try:
            indexes = []
            if table_name in self.tables.get(dbname, {}):
                indexes = await self.get_indexes(table_name, dbname)
                if not table_name in self.index.keys():
                    self.index.update({table_name: []})

                if not index in indexes:
                    result_a = await self.r.db(dbname).table(
                        table_name).index_create(index).run(self.session)
                    result_b = await self.r.db(dbname).table(
                        table_name).index_wait().run(self.session)
                    self.index[table_name].append(index)
                    return result_a, result_b
                else:
                    return index, True
            else:
                return await self.create_table(table_name, dbname)

        except Exception as e:
            self.logger.exception(
                f"Index {index} can't be created {table_name}, exception {e}")
            raise e

    async def delete_table(self, table_name: str, dbname: str):
        if dbname in self.dblist:
            if table_name in self.tables[dbname]:
                self.logger.info("Table deleted %s on database %s" %
                                 (table_name, dbname))
                return await self.r.db(dbname).table_drop(table_name).run(
                    self.session)

    async def list_tables(self, dbname: str = None):
        tlist = []
        if not dbname:
            dbname = self.default_db

        await self.list_dbs()
        # print("DB %s in list %s" %(dbname, await self.list_dbs()))
        if dbname in self.dblist:
            tlist = await self.r.db(dbname).table_list().run(self.session)
            # print("Tables on database %s are %s" %(dbname, tlist))
            self.tables.update({dbname: tlist})
            # print(self.tables)
        self.logger.info("Tables listed on database %s" % dbname)
        return tlist

    async def set_change_handler(self, table_name: str):
        changes = await self.r.table(table_name).changes().run(self.session)
        return changes

    async def save_data(self, table_name, data, options=None):
        task = asyncio.current_task()
        task.set_name(f"save_data_{table_name}")
        try:
            if table_name in self.tables[self.defaultdb]:
                task_coro = self.r.db(self.defaultdb).table(table_name).insert(
                    data, durability='soft').run(self.session)
                return await task_coro
            else:
                return {"result": False}
        except asyncio.InvalidStateError as invalid_e:
            raise invalid_e
        except asyncio.CancelledError as ce:
            task = asyncio.current_task()
            self.logger.exception(
                "Error de cancelación de tarea {result},{table_name}")
            raise ce
        except Exception as error:
            self.logger.critical(
                "Error in saving data on %s with data %s, error %s" %
                (table_name, data, error))
            print("Error when send data %s" % error)
            raise error

    @property
    def dbname(self):
        return self.default_db

    async def update_data(self, table_name, id, conditional_data):
        dbname = self.defaultdb
        self.logger.info("Updating data in %s" % table_name)
        if table_name in self.tables[self.default_db]:
            await self.r.db(dbname).table(table_name).get(id).update(
                conditional_data).run(self.session)

    async def replace_data(self, table_name, id, conditional_data):
        dbname = self.defaultdb
        self.logger.info("Replacing data in %s" % table_name)
        if table_name in self.tables[dbname]:
            await self.r.db(dbname).table(table_name).get(id).replace(
                conditional_data).run(self.session)

    async def delete_data(self, table_name, id):
        dbname = self.defaultdb
        self.logger.info("Deleting data in %s" % table_name)
        if table_name in self.tables[dbname]:
            if isinstance(id, dict):
                await self.r.db(dbname).table(table_name).filter(
                    id).delete().run(self.session)
            else:
                await self.r.db(dbname).table(table_name).get(id).delete().run(
                    self.session)

    async def get_infoserver(self):
        self.logger.info("Get info server")
        return await self.session.server()

    async def get_data_between(self, table_name, lower, upper):
        dbname = self.dbname
        msg = "Extracting data between %s and %s from %s" % (lower, upper,
                                                             table_name)
        self.logger.info(msg)
        if table_name in self.tables[self.default_db]:
            return await self.r.db(dbname).table(table_name).between(
                lower, upper).run(self.session)
        else:
            print("No hay datos entre esos valores")

    async def get_data(self, table_name, index_name, value):
        return await self.r.db(self.dbname).table(table_name).get_all(
            value, index=index_name).run(self.session)

    async def get_data_filter(self,
                              table_name,
                              filter_exp,
                              filter_opt: dict,
                              order_by: str,
                              options={}):
        """
        filter expression could ve a json like:
        {'age':30} or an expression:
        r.row['age']=30 or a lambda function:
        lambda user: user['age]==30
        """
        task = asyncio.current_task()
        if task:
            task.set_name(f"get_data_filter_{table_name}")
        dbname = self.dbname
        index = filter_opt.get('index')
        if table_name in self.tables.get(self.default_db, {}):
            options = {'read_mode': 'single'}

        try:
            if table_name in self.tables.get(self.default_db, {}):
                if index:
                    lower = None
                    upper = None
                    if not type(filter_exp) == list:
                        lower = filter_exp
                        upper = self.r.maxval
                    else:
                        lower = filter_exp[0]
                        upper = filter_exp[1]
                    query = rdb.db(dbname).table(table_name).between(
                        lower,
                        upper,
                        index=index,
                        left_bound="open",
                        right_bound="open").coerce_to("array").order_by(
                            index).run(self.session)
                    result = await query
                    return result
                else:
                    self.logger.info(
                        "Obtaining data with filters %s using table %s" %
                        (filter_opt, table_name))

                    return await self.r.db(dbname).table(table_name).filter(
                        filter_exp).order_by(order_by).coerce_to("array").run(
                            self.session, **options)
            else:
                return []
        except asyncio.InvalidStateError as ie:
            rprint(f"Invalida state task {task}")
            task = asyncio.current_task()
            if task:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError as can_error:
                    raise can_error
            self.logger.exception("Error de cancelación de tarea {result}")
            bprint(
                f"Se cancela tarea para {table_name}, {filter_opt}, {result}")
            raise ie
        except asyncio.CancelledError as ce:
            task = asyncio.current_task()
            if task:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError as can_error:
                    raise can_error
            self.logger.exception("Error de cancelación de tarea {result}")
            bprint(
                f"Se cancela tarea para {table_name}, {filter_opt}, {result}")
            raise ce
        except Exception as ec:
            task = asyncio.current_task()
            if task:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError as can_error:
                    raise can_error
            bprint(
                f"Se cancela tarea para {table_name}, {filter_opt}, result {result}"
            )
            self.logger.exception(
                f"Error on the data extraction, error {ec}, result {result}")
            await asyncio.sleep(5)
            await self.reconnect(wait=True)
            raise ec

    def iso8601(self, date):
        return self.r.iso8601(date)

    def loginfo(self, msg):
        self.logger.info(msg)

    def logdebug(self, msg):
        self.logger.debug(msg)

    def logerror(self, msg):
        self.logger.error(msg)

    # DEFINE JOINS....
    # https://www.rethinkdb.com/api/python/#index_create
