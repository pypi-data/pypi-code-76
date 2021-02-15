#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The following client is used to read data to and write data from the postgres
Meter Management System which includes TimescaleDB for meter metric data.
"""

# Built-in Modules

# Third Party Modules
import pandas as pd
import psycopg2
from psycopg2 import sql
from mms.helpers import get_db_client_kwargs


class MMSClient:
    def __init__(self, **kwargs):
        if kwargs.get('dbname') is None:
            self.kwargs = get_db_client_kwargs()
        else:
            self.kwargs = kwargs
        self.conn = psycopg2.connect(**kwargs, connect_timeout=5)
        if kwargs.get('port') == "5000":
            read_only = False
        else:
            read_only = True
        self.conn.set_session(isolation_level="read uncommitted",
                              readonly=read_only,
                              autocommit=False)

    def rollback(self, keep_alive=False):
        self.conn.rollback()
        if not keep_alive:
            self.conn.close()

    def commit(self):
        self.conn.commit()
        self.conn.close()

    def get_device_codes_for_service(self, service):
        """
        :param service: A device_service from the MMS (string).
        :return: A list of (device code) of type 'service'
        """
        query = sql.SQL(
            " SELECT code FROM devices "
            "JOIN device_models dm on devices.device_model_id = dm.id "
            "JOIN device_services ds on dm.device_service_id = ds.id "
            "WHERE device_service_id = %s") \
            .format(sql.SQL(', ').join(sql.Placeholder() * len(service)))
        with self.conn.cursor() as cur:
            cur.execute(query, (service,))
            if cur.fetchone:
                return [r[0] for r in cur.fetchall()]
            else:
                # No codes matching device service
                raise LookupError("No devices found with service {0}"
                                  .format(service))

    def get_device_ids_for_codes(self, codes):
        """
        :param codes: A list of device codes (strings) to return the
        device id's for.
        :return: A 1 to 1 dictionary with key (device code)
        and value (device id) (All strings)
        """
        query = sql.SQL("SELECT code, id FROM devices WHERE code IN ({})")\
            .format(sql.SQL(', ').join(sql.Placeholder() * len(codes)))
        df = pd.read_sql(query,
                         con=self.conn,
                         index_col='code',
                         params=codes)
        df['id'] = df['id'].apply(str)
        return dict(zip(list(df.index.values), list(df['id'].values)))

    def device_inverted(self, device_id):
        """
            :param device_id: A device codes (string) to return the
            device id for.
            :return: A single integer (device id)
            """
        if device_id is None:
            return 0

        query = "SELECT is_inverted " \
                "FROM meters " \
                "WHERE device_id = %s"
        with self.conn.cursor() as cur:
            cur.execute(query, (device_id,))
            if cur.fetchone:
                return int(cur.fetchone()[0])
            else:
                # No device record returned
                raise LookupError("No meter found for device {0}"
                                  .format(device_id))

    def add_simulation(self, sim_name):
        """
        :param string sim_name: Name of simulation (Unique in DB)
        :return: ID of newly inserted simulation
        """
        query = sql.SQL(
            "INSERT INTO simulations(name) "
            "VALUES(%s) "
            "RETURNING id")
        with self.conn.cursor() as cur:
            try:
                cur.execute(query, (sim_name,))
                id = cur.fetchone()[0]
                return id
            except psycopg2.Error as e:
                if int(e.pgcode) == 23505:
                    return None
                else:
                    raise e

    def update_simulation_stats(self, stats):
        """
        :param stats: Python Dict With:
            id, name, start_time, end_time, resolution_mins, run_time_sec
        :return:
        """
        cols = "id, name, start_time, end_time, resolution_mins, run_time_sec"

        query = sql.SQL(
            "UPDATE simulations "
            "SET ({}) = (%(id)s, %(name)s, %(start_time)s, %(end_time)s, "
            "%(resolution_mins)s, %(run_time_sec)s) "
            "WHERE id = %(id)s "
            "RETURNING *").format(sql.SQL(cols))

        with self.conn.cursor() as cur:
            cur.execute(query, stats)
            row = cur.fetchone()
            if row:
                if int(row[0]) == stats['id']:
                    return True
                else:
                    self.rollback()
            else:
                # No simulation_id found
                raise LookupError("No simulation found for id {0}"
                                  .format(stats['id']))

    def get_simulation_id(self, sim_name):
        """
            :param sim_name: Name of the simulation.
            :return: An integer (simulation id)
            """
        if sim_name is None:
            return None

        query = "SELECT id " \
                "FROM simulations " \
                "WHERE name = %s"
        with self.conn.cursor() as cur:
            cur.execute(query, (sim_name,))
            if cur.fetchone:
                return int(cur.fetchone()[0])
            else:
                # No device record returned
                raise LookupError("No simulation found for name {0}"
                                  .format(sim_name))
