# Built-in Modules
import cProfile
import json
from pstats import Stats
from unittest import TestCase

# Third Party Modules
import pandas as pd
import pandas.api.types as ptypes

# Project Specific Modules
from mms import TimescaleClientNarrow, TimescaleClientJSON
from tests.helpers import get_db_client_kwargs

class TestDataReads(TestCase):
    def setUp(self):
        self.pr = cProfile.Profile()
        self.pr.enable()
        # print("\n<<<---")
        self.clientArgs = get_db_client_kwargs()

    def tearDown(self):
        # p = Stats(self.pr)
        # p.strip_dirs()
        # p.sort_stats('cumtime')
        # p.print_stats(20)
        # print("\n--->>")
        pass

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
        device_ids = [353, 398, 399]
        device_metrics = ['P', 'Q', 'S']

        c2 = TimescaleClientJSON('device_metrics_json',
                                 **get_db_client_kwargs())
        df2 = c2.get_latest_metrics(device_ids, device_metrics, 5)
        self.check_standard_df_format(df2)

        c1 = TimescaleClientNarrow('device_metrics',
                                   **get_db_client_kwargs())
        df1 = c1.get_latest_metrics(device_ids, device_metrics, 5)
        self.check_standard_df_format(df2)

    def test_df_narrow_format(self):
        # Sample Narrow Format result DF
        c = TimescaleClientNarrow('device_metrics',
                                  **get_db_client_kwargs())

        query_result_df = pd.DataFrame(
            {'measurement_date': ['2019-09-19 00:00:00.000000+00:00',
                                  '2019-09-19 00:01:00.000000+00:00',
                                  '2019-09-19 00:02:00.000000+00:00',
                                  '2019-09-19 00:00:00.000000+00:00',
                                  '2019-09-19 00:01:00.000000+00:00',
                                  '2019-09-19 00:00:00.000000+00:00',
                                  '2019-09-19 00:01:00.000000+00:00',
                                  '2019-09-19 00:02:00.000000+00:00',
                                  '2019-09-19 00:00:00.000000+00:00',
                                  '2019-09-19 00:01:00.000000+00:00'],
             'device_id': [353, 353, 353,
                           354, 354,
                           353, 353, 353,
                           354, 354],
             'device_metric_type_id': ['P_Supply', 'P_Supply', 'P_Supply',
                                       'P', 'P',
                                       'Q_Supply', 'Q_Supply', 'Q_Supply',
                                       'Q', 'Q'],
             'value': [0, 1100000, -1100000,
                       300, 978097,
                       0.0, 0.0, 0.0,
                       -200.1, -30.12],
             'received_date': ['2019-09-19 00:00:01.000000+00:00',
                               '2019-09-19 00:01:00.000000+00:00',
                               '2019-09-19 00:02:00.000000+00:00',
                               '2019-09-19 00:00:00.000000+00:00',
                               '2019-09-19 00:01:00.000000+00:00',
                               '2019-09-19 00:00:00.000000+00:00',
                               '2019-09-19 00:01:00.000000+00:00',
                               '2019-09-19 00:02:00.000000+00:00',
                               '2019-09-19 00:00:00.000000+00:00',
                               '2019-09-19 00:01:00.000000+00:00']})
        df = c.standardize_df(query_result_df)
        self.check_standard_df_format(df)

        # Accessing Device Metric Timeseries (Sorted in ascending order)
        self.assertEqual([0, 1100000, -1100000],
                         df.loc[(353, 'P_Supply'), 'value'].values.tolist())

        # Accessing Most Recent Device Metric
        self.assertEqual(300,
                         df.loc[(354, 'P'), 'value'].iloc[0])

    def test_df_json_format(self):
        # Sample JSON result DF
        c = TimescaleClientJSON('device_metrics_json',
                                **get_db_client_kwargs())

        query_result_df = pd.DataFrame(
            {'measurement_date': ['2018-09-19 00:00:00.000000+00:00',
                                  '2018-09-19 00:01:00.000000+00:00',
                                  '2018-09-19 00:02:00.000000+00:00',
                                  '2018-09-19 00:00:00.000000+00:00',
                                  '2018-09-19 00:01:00.000000+00:00'],
             'device_id': [353, 353, 353,
                           354, 354],
             'metrics': [{"P_Supply": 0, "Q_Supply": 0.0},
                         {"P_Supply": 1100000, "Q_Supply": 0.0},
                         {"P_Supply": -1100000, "Q_Supply": 0.0},
                         {"P": 300, "Q": -200.1},
                         {"P": 978097, "Q": -30.12}]})
        df = c.standardize_df(query_result_df, ['P_Supply', 'P'])
        self.check_standard_df_format(df)

        # Accessing Device Metric Timeseries
        self.assertEqual([0, 1100000, -1100000],
                         df.loc[(353, 'P_Supply'), 'value'].values.tolist())

        # Accessing Most Recent Device Metric
        self.assertEqual(300,
                         df.loc[(354, 'P'), 'value'].iloc[0])
