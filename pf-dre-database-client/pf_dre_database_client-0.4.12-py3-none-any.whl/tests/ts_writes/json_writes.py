# Built-in Modules
import cProfile
import json
from datetime import datetime
from pytz import timezone, utc
from pstats import Stats
import collections
from unittest import TestCase

# Third Party Modules
import pandas as pd
import numpy as np
from psycopg2 import DatabaseError, IntegrityError

# Project Specific Modules
from mms.helpers import generate_sample_df
from tests.helpers import get_db_client_kwargs
from mms import TimescaleClientJSON


device_metrics = {353: ['P_Supply', 'Q_Supply'], 398: ['P', 'Q']}
dates1 = ['2018-09-18 00:00:00.000000+00:00',
          '2018-09-18 00:01:00.000000+00:00',
          '2018-09-18 00:02:00.000000+00:00']
dates2 = ['2018-09-18 00:00:00.000000+00:00',
          '2018-09-18 00:01:30.000000+00:00',
          '2018-09-18 00:02:00.000000+00:00']

json_df_ignore_keys = [(datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f%z"), dev_id)
                       for dt in np.setdiff1d(dates2, dates1)
                       for dev_id in device_metrics.keys()]
json_df_update_keys = [(datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f%z"), dev_id)
                       for dt in dates2 for dev_id in device_metrics.keys()]


class TestJsonWrites(TestCase):
    def setUp(self):
        #self.pr = cProfile.Profile()
        #self.pr.enable()
        #print("\n<<<---")
        self.clientArgs = get_db_client_kwargs()

    def tearDown(self):
        #p = Stats(self.pr)
        #p.strip_dirs()
        #p.sort_stats('cumtime')
        #p.print_stats(20)
        #print("\n--->>")
        return

    def test_copy_json(self):
        c1 = TimescaleClientJSON('device_metrics_json', **self.clientArgs)
        df1_json = generate_sample_df(dates1, device_metrics, schema = 'json')
        json_df_stringified = df1_json.copy()
        json_df_stringified['metrics'] = \
            json_df_stringified['metrics'].apply(json.dumps)
        num_rows = c1.copy_df_from_stringio(json_df_stringified)
        self.assertEqual(num_rows, len(df1_json.index))
        standard_df = c1.standardize_df(df1_json, ['P', 'Q_Supply'])
        db_df = c1.get_all_metrics([353, 398],
                                   ['P', 'Q_Supply'],
                                   '2018-09-18 00:00:00.000000+00:00',
                                   '2018-09-18 00:02:00.000000+00:00')
        self.assertTrue(db_df.equals(standard_df))
        c1.rollback()
        return

    @staticmethod
    def write_json_df(c, df):
        json_df_stringified = df.copy()
        json_df_stringified['metrics'] = \
            json_df_stringified['metrics'].apply(json.dumps)
        c.execute_values(json_df_stringified)

    def test_insert_update_json(self):
        c1 = TimescaleClientJSON('device_metrics_json', **self.clientArgs)
        df1_json = generate_sample_df(dates1, device_metrics, schema = 'json')
        df2_json = generate_sample_df(dates2, device_metrics, schema = 'json')
        self.write_json_df(c1, df1_json)
        json_df_stringified = df2_json.copy()
        json_df_stringified['metrics'] = \
            json_df_stringified['metrics'].apply(json.dumps)
        keys = c1.execute_values(json_df_stringified, method='update')
        self.assertEqual(collections.Counter(keys),
                         collections.Counter(json_df_update_keys))
        c1.rollback()

    def test_insert_ignore_json(self):
        c1 = TimescaleClientJSON('device_metrics_json', **self.clientArgs)
        df1_json = generate_sample_df(dates1, device_metrics, schema = 'json')
        df2_json = generate_sample_df(dates2, device_metrics, schema = 'json')
        self.write_json_df(c1, df1_json)
        json_df_stringified = df2_json.copy()
        json_df_stringified['metrics'] = \
            json_df_stringified['metrics'].apply(json.dumps)
        keys = c1.execute_values(json_df_stringified, method = 'ignore')
        self.assertEqual(collections.Counter(keys),
                         collections.Counter(json_df_ignore_keys))
        c1.rollback()

    def test_insert_fail_json(self):
        c1 = TimescaleClientJSON('device_metrics_json', **self.clientArgs)
        df1_json = generate_sample_df(dates1, device_metrics, schema = 'json')
        df2_json = generate_sample_df(dates2, device_metrics, schema = 'json')
        self.write_json_df(c1, df1_json)
        with self.assertRaises(IntegrityError):
            json_df_stringified = df2_json.copy()
            json_df_stringified['metrics'] = \
                json_df_stringified['metrics'].apply(json.dumps)
            c1.execute_values(json_df_stringified, method = 'fail')

        c1.rollback()
