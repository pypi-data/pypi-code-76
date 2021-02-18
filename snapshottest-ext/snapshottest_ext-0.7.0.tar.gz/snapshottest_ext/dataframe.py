import pandas as pd
import pyarrow as pa
from snapshottest.formatter import Formatter
from snapshottest.formatters import BaseFormatter


def pandas_to_bytes(df: pd.DataFrame) -> str:
    df_bytestring = pa.serialize(df).to_buffer().to_pybytes()
    return df_bytestring


def bytes_to_pandas(raw_bytes) -> pd.DataFrame:
    original_df = pa.deserialize(raw_bytes)
    return original_df


class PandasSnapshot(object):
    def __init__(self, value):
        self.value = value


class PandasFormatter(BaseFormatter):
    def can_format(self, value):
        """
        dispatcher, decide which format to use
        https://github.com/syrusakbary/snapshottest/blob/master/snapshottest/formatter.py
        @staticmethod
        def get_formatter(value):
            for formatter in Formatter.formatters:
                if formatter.can_format(value):
                    return formatter
        :param value:
        :return:
        """
        return isinstance(value, PandasSnapshot)

    def store(self, formatter, pandas_snap: PandasSnapshot):
        """ store pd.DataFrame as bytes in snapshot file"""
        return pandas_to_bytes(pandas_snap.value)

    #def get_imports(self):
    #    """not useful in this one, because we do not deserialize from the bytes directly"""
    #    return ('pandasFormatter', 'PandasSnapshot'),

    def assert_value_matches_snapshot(self, test, test_value: PandasSnapshot, snapshot_value, formatter):
        """
        :param test:
        :param test_value: the value in snapshot.assert_mach(value)
        :param snapshot_value: the value of format.store (after load)
        """
        prev_df = bytes_to_pandas(snapshot_value)  # deserialize from bytes to pd.DataFrame
        pd.testing.assert_frame_equal(test_value.value, prev_df)


Formatter.register_formatter(PandasFormatter())
