# Built-in Modules
import cProfile
from datetime import datetime
from pstats import Stats
import collections
from unittest import TestCase

# Third Party Modules
import numpy as np
from psycopg2 import DatabaseError, IntegrityError

# Project Specific Modules
from mms.helpers import generate_sample_df
from tests.helpers import get_db_client_kwargs
from mms import TimescaleClientNarrow


device_metrics = {353: ['P_Supply', 'Q_Supply'], 398: ['P', 'Q']}
dates1 = ['2018-09-18 00:00:00.000000+00:00',
          '2018-09-18 00:01:00.000000+00:00',
          '2018-09-18 00:02:00.000000+00:00']
dates2 = ['2018-09-18 00:00:00.000000+00:00',
          '2018-09-18 00:01:30.000000+00:00',
          '2018-09-18 00:02:00.000000+00:00']

narrow_df_ignore_keys = [(datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f%z"),
                          dev_id, m)
                         for dt in np.setdiff1d(dates2, dates1)
                         for dev_id, metrics in device_metrics.items()
                         for m in metrics]

narrow_df_update_keys = [(datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f%z"),
                          dev_id, m)
                         for dt in dates2
                         for dev_id, metrics in device_metrics.items()
                         for m in metrics]


class TestNarrowWrites(TestCase):
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

    def test_copy_narrow(self):
        c1 = TimescaleClientNarrow('device_metrics', **self.clientArgs)
        df1_narrow = generate_sample_df(dates1, device_metrics)
        num_rows = c1.copy_df_from_stringio(df1_narrow)
        self.assertEqual(num_rows, len(df1_narrow.index))
        standard_df = c1.standardize_df(df1_narrow)
        db_df = c1.get_all_metrics([353, 398],
                                   ['P_Supply', 'P', 'Q_Supply', 'Q'],
                                   '2018-09-18 00:00:00.000000+00:00',
                                   '2018-09-18 00:02:00.000000+00:00')
        self.assertTrue(db_df.equals(standard_df))
        c1.rollback()
        return

    def test_insert_update_narrow(self):
        c1 = TimescaleClientNarrow('device_metrics', **self.clientArgs)
        df1_narrow = generate_sample_df(dates1, device_metrics)
        df2_narrow = generate_sample_df(dates2, device_metrics)
        c1.execute_values(df1_narrow)
        keys = c1.execute_values(df2_narrow, method='update')
        self.assertEqual(collections.Counter(keys),
                         collections.Counter(narrow_df_update_keys))
        c1.rollback()

    def test_insert_ignore_narrow(self):
        c1 = TimescaleClientNarrow('device_metrics', **self.clientArgs)
        df1_narrow = generate_sample_df(dates1, device_metrics)
        df2_narrow = generate_sample_df(dates2, device_metrics)
        c1.execute_values(df1_narrow)
        keys = c1.execute_values(df2_narrow, method='ignore')
        self.assertEqual(collections.Counter(keys),
                         collections.Counter(narrow_df_ignore_keys))
        c1.rollback()

    def test_insert_fail_narrow(self):
        c1 = TimescaleClientNarrow('device_metrics', **self.clientArgs)
        df1_narrow = generate_sample_df(dates1, device_metrics)
        df2_narrow = generate_sample_df(dates2, device_metrics)
        c1.execute_values(df1_narrow)
        with self.assertRaises(IntegrityError):
            c1.execute_values(df2_narrow, method='fail')

        c1.rollback()
