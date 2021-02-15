# Built-in Modules
from datetime import datetime, timedelta
from unittest import TestCase

# Third Party Modules
import pandas as pd
import pandas.api.types as ptypes

# Project Specific Modules
from mms import TimescaleClientNarrow
from tests.helpers import get_db_client_kwargs

class TestDataReads(TestCase):
    def setUp(self):
        # self.pr = cProfile.Profile()
        # self.pr.enable()
        # print("\n<<<---")
        self.clientArgs = get_db_client_kwargs()

    def tearDown(self):
        # p = Stats(self.pr)
        # p.strip_dirs()
        # p.sort_stats('cumtime')
        # p.print_stats(20)
        # print("\n--->>")
        return

    def check_standard_df_format(self, df):
        idx = ['device_id', 'device_metric_type_id', 'measurement_date']
        # The DataFrame should have a MultiIndex
        self.assertIsInstance(df.index, pd.MultiIndex)
        # The DataFrame must have the following index names
        self.assertEqual(df.index.names, idx)
        # The device_id index column should be a int64
        self.assertTrue(ptypes.is_int64_dtype(df.index.get_level_values(0)))
        # The device_metric_type_id index column should be a string
        self.assertTrue(ptypes.is_string_dtype(df.index.get_level_values(1)))
        # The device_id index column should be a int64
        self.assertTrue(
            ptypes.is_datetime64_ns_dtype(df.index.get_level_values(2)))
        # Check that the dataframe is not empty
        self.assertFalse(df.empty)

    def test_latest_metrics(self):
        device_ids = [398]
        device_metrics = ['P', 'Q', 'S']

        c = TimescaleClientNarrow('device_metrics',
                                  **get_db_client_kwargs())
        df = c.get_latest_metrics(device_ids, device_metrics, 5)
        # This should pass assuming all the mock meters being pointed to are
        # being polled correctly.
        self.assertEquals(len(device_ids)*len(device_metrics), len(df.index))
        self.check_standard_df_format(df)

    def test_all_metrics(self):
        device_ids = [398]
        device_metrics = ['P', 'Q', 'S']

        c = TimescaleClientNarrow('device_metrics',
                                  **get_db_client_kwargs())
        df = c.get_all_metrics(device_ids, device_metrics,
                               (datetime.now() - timedelta(minutes=5))
                               .isoformat(),
                               datetime.now().isoformat())
        self.check_standard_df_format(df)

    def test_aggregated_metrics(self):
        device_ids = [398]
        device_metrics = ['P']

        c = TimescaleClientNarrow('device_metrics',
                                  **get_db_client_kwargs())
        # First
        self.check_standard_df_format(c.get_aggregated_metrics(
            '5 minutes', device_ids, device_metrics,
            (datetime.now() - timedelta(minutes=15)).isoformat(),
            datetime.now().isoformat(), 'first'))

        # Last
        self.check_standard_df_format(c.get_aggregated_metrics(
            '5 minutes', device_ids, device_metrics,
            (datetime.now() - timedelta(minutes=15)).isoformat(),
            datetime.now().isoformat(), 'last'))

        # Average
        self.check_standard_df_format(c.get_aggregated_metrics(
            '5 minutes', device_ids, device_metrics,
            (datetime.now() - timedelta(minutes=15)).isoformat(),
            datetime.now().isoformat(), 'avg'))

        # Last Observation Carried Forward (10 minutes into future)
        self.check_standard_df_format(c.get_aggregated_metrics(
            '5 minutes', device_ids, device_metrics,
            (datetime.now() - timedelta(minutes=15)).isoformat(),
            (datetime.now() + timedelta(minutes=10)).isoformat(),
            'avg', 'interpolate'))

        # Interpolate (10 minutes into future)
        self.check_standard_df_format(c.get_aggregated_metrics(
            '5 minutes', device_ids, device_metrics,
            (datetime.now() - timedelta(minutes=15)).isoformat(),
            (datetime.now() + timedelta(minutes=10)).isoformat(),
            'avg', 'locf'))

        # Average Interpolated
        df = c.get_aggregated_metrics(
            '10 seconds', device_ids, device_metrics,
            (datetime.now() - timedelta(minutes=2)).isoformat(),
            datetime.now().isoformat(), 'avg', 'interpolate')
        df = df.dropna()
        print(df)
        # If interpolation is wrong then there will only be 2 rows in the
        # last minute
        self.assertGreater(len(df.index), 6)
        self.check_standard_df_format(df)
