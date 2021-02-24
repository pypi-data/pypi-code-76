import base64
from io import BytesIO
import json
from typing import List, Dict

from boto3.exceptions import Boto3Error
import numpy as np
import pandas as pd

from terality import TeralityDataDownloadError
from .. import Connection
from . import (
    DataTransfer, download_to_s3_files,
    ExportResponse, IndexColNames, PandasIndexMetadata, PandasSeriesMetadata, PandasDFMetadata
)


def _deserialize_tuple(obj: Dict):
    return tuple(obj['value'])


def _deserialize_display(value):
    # No need to force it in package dependencies, if it gets called it means we are in a Jupyter Notebook
    # and and this dependency is present
    # noinspection PyUnresolvedReferences
    from IPython.display import display, HTML
    display(HTML(value))
    return None


def _deserialize_export(value: dict) -> None:
    export = ExportResponse.parse_obj(value)
    path = export.path
    transfer_id = export.transfer_id
    if path.startswith('s3://'):
        download_to_s3_files(transfer_id, export.aws_region, path)
    else:
        DataTransfer.download_to_local_files(Connection.session.download_config, transfer_id, path, export.is_folder)


def _deserialize_np_scalar(value):
    bytes_io = BytesIO(base64.b64decode(value.encode()))
    # noinspection PyTypeChecker
    result = np.load(bytes_io).flatten()[0]
    return result


def _deserialize_np_array(value):
    # noinspection PyTypeChecker
    return np.load(DataTransfer.download_to_bytes(Connection.session.download_config, value))


def _download_df(transfer_id: str, is_col_json: List[bool]):
    df = pd.read_parquet(DataTransfer.download_to_bytes(Connection.session.download_config, transfer_id))
    # Some data types require post-processing.
    for col_num in range(len(is_col_json)):
        if is_col_json[col_num]:
            df.iloc[:, col_num] = df.iloc[:, col_num].apply(json.loads)
    return df


def _rename_index(index: pd.Index, index_col_names: IndexColNames):
    if isinstance(index, pd.MultiIndex):
        index.names = index_col_names.names
    index.name = index_col_names.name


def _deserialize_index(obj: Dict) -> pd.Index:
    index_metadata = PandasIndexMetadata.parse_obj(obj)
    df = _download_df(index_metadata.transfer_id, index_metadata.cols_json_encoded)
    if len(df.columns) == 1:
        index = pd.Index(data=df.iloc[:, 0])
    else:
        index = pd.MultiIndex.from_arrays([df.iloc[:, i] for i in range(len(df.columns))])
    _rename_index(index, index_metadata.index_col_names)
    return index


def _deserialize_series(obj: Dict) -> pd.Series:
    series_metadata = PandasSeriesMetadata.parse_obj(obj)
    df = _download_df(series_metadata.transfer_id, series_metadata.cols_json_encoded)
    series = df.iloc[:, 0]
    series.name = series_metadata.series_name
    _rename_index(series.index, series_metadata.index_col_names)
    return series


def _deserialize_df(obj: Dict) -> pd.DataFrame:
    df_metadata = PandasDFMetadata.parse_obj(obj)
    df = _download_df(df_metadata.transfer_id, df_metadata.cols_json_encoded)
    df.columns = df_metadata.col_names
    _rename_index(df.index, df_metadata.index_col_names)
    return df


class _JSONDecoderClient(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.object_hook)

    @classmethod
    def object_hook(cls, obj: dict):
        # Imports not top level to protect against circular dependencies
        from terality import Index, Series, DataFrame
        if '!terality:type' in obj:
            type_ = obj.pop('!terality:type')
            if type_ == 'tuple':
                return _deserialize_tuple(obj)
            elif type_ == 'display':
                return _deserialize_display(obj['value'])
            elif type_ == 'ExportResponse':
                return _deserialize_export(obj)
            elif type_ == 'np.scalar':
                return _deserialize_np_scalar(obj['value'])
            elif type_ == 'np.ndarray':
                return _deserialize_np_array(obj['value'])
            elif type_ == 'pd.Index':
                return _deserialize_index(obj)
            elif type_ == 'pd.Series':
                return _deserialize_series(obj)
            elif type_ == 'pd.DataFrame':
                return _deserialize_df(obj)
            elif type_ == 'index':
                # noinspection PyProtectedMember
                return Index._deser(**obj)
            elif type_ == 'series':
                # noinspection PyProtectedMember
                return Series._deser(**obj)
            elif type_ == 'dataframe':
                # noinspection PyProtectedMember
                return DataFrame._deser(**obj)
            else:
                raise ValueError(f'Cannot deserialize unknown type {type_}')
        return obj


def json_loads(s: str):
    try:
        if s is None:
            return None
        return json.loads(s, cls=_JSONDecoderClient)
    except (Boto3Error, IOError) as e:
        raise TeralityDataDownloadError() from e
