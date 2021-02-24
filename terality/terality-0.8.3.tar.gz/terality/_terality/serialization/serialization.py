import base64
from io import BytesIO
import json
# from pathlib import Path
from uuid import uuid4
from typing import List, Tuple, Dict

from boto3.exceptions import Boto3Error
import dill
import numpy as np
import pandas as pd
from pandas.core.dtypes.base import ExtensionDtype

from terality import TeralityDataUploadError, TeralityTypeError
from .helpers_structs import StructRef, DTypeWrapper, ExportRequest
from .. import Connection
from . import (
    DataTransfer, upload_local_files, upload_s3_files,
    Upload, UploadRequest, PythonTypeWrapper, CallableWrapper, PandasIndexMetadata, PandasSeriesMetadata, PandasDFMetadata
)


def _serialize_upload_path(upload: Upload) -> str:
    transfer_id = str(uuid4())
    path = upload.path
    if path.startswith('s3://'):
        upload_s3_files(path, transfer_id)
    else:
        upload_local_files(path, transfer_id)
    return transfer_id


def _serialize_ndarray(array: np.ndarray) -> str:
    data_bytes = BytesIO()
    # noinspection PyTypeChecker
    np.save(data_bytes, array)
    import_id = DataTransfer.upload_bytes(Connection.session.upload_config, data_bytes)
    return import_id


def _check_if_col_needs_json_encoding(col: pd.Series) -> bool:
    if isinstance(col.dtype, np.dtype) and col.dtype.hasobject:
        # Collect the types of all values in the column.
        dtypes = set()
        for value in col:
            dtypes.add(type(value))
        # Ignore absent values: they are gracefully handled by the Parquet format.
        dtypes -= {type(None)}

        # Based on the combination of types, decide if we need to JSON-encode.
        need_json = len(dtypes) > 1 or any(dtype in dtypes for dtype in [list, dict])
        return need_json
    return False


def _prepare_for_parquet(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[bool]]:
    is_col_json = []
    for col_num in range(len(df.columns)):
        col_needs_json = _check_if_col_needs_json_encoding(df.iloc[:, col_num])
        if col_needs_json:
            df.iloc[:, col_num] = df.iloc[:, col_num].apply(json.dumps)
        is_col_json.append(col_needs_json)
    return df, is_col_json


def _upload_df(df: pd.DataFrame) -> Tuple[str, List[bool]]:
    """ Parquet only supports dataframes so we transmit all pandas structures as dataframes """
    # WARNING: Parquet only accepts string column names
    # => We replace non-string column names with placeholders and pass the columns "out of band" (in the metadata).
    df = df.rename(columns={df.columns[col_num]: str(col_num) for col_num in range(len(df.columns))}, copy=False)

    df, is_col_json = _prepare_for_parquet(df)

    data_bytes = BytesIO()
    df.to_parquet(data_bytes)
    import_id = DataTransfer.upload_bytes(Connection.session.upload_config, data_bytes)
    return import_id, is_col_json


def _serialize_index(index: pd.Index) -> Dict:
    transfer_id, is_col_json = _upload_df(index.to_frame(index=False))
    return PandasIndexMetadata.from_index(index, transfer_id, is_col_json).dict()


def _serialize_series(series: pd.Series) -> Dict:
    transfer_id, is_col_json = _upload_df(series.copy(deep=True).to_frame())
    return PandasSeriesMetadata.from_series(series, transfer_id, is_col_json).dict()


def _serialize_df(df: pd.DataFrame) -> Dict:
    transfer_id, is_col_json = _upload_df(df.copy(deep=True))
    return PandasDFMetadata.from_df(df, transfer_id, is_col_json).dict()


class _JSONEncoderClient(json.JSONEncoder):
    def default(self, o):
        from terality import Index, Series, DataFrame
        if isinstance(o, type):
            type_ = 'type'
            json_ = PythonTypeWrapper(module_name=o.__module__, type_name=o.__name__).dict()
        elif callable(o):
            type_ = 'callable'
            json_ = CallableWrapper(dill_payload=base64.b64encode(dill.dumps(o)).decode()).dict()
        elif isinstance(o, UploadRequest):
            type_ = 'upload'
            json_ = o.dict()
        elif isinstance(o, ExportRequest):
            type_ = 'download'
            json_ = o.dict()
        elif isinstance(o, (np.bool_, np.int_, np.float_)):
            type_ = f'numpy.{o.__class__.__name__}'
            json_ = {'value': o.item()}
        elif isinstance(o, np.ndarray):
            type_ = 'ndarray'
            # FIXME: Avoid "JSON-in-JSON" (same below)
            json_ = {'value': _serialize_ndarray(o)}
        elif isinstance(o, pd.Index):
            type_ = 'pd.Index'
            json_ = _serialize_index(o)
        elif isinstance(o, pd.Series):
            type_ = 'pd.Series'
            json_ = _serialize_series(o)
        elif isinstance(o, pd.DataFrame):
            type_ = 'pd.DataFrame'
            json_ = _serialize_df(o)
        elif isinstance(o, (Index, Series, DataFrame)):
            type_ = 'terality'
            # noinspection PyProtectedMember
            json_ = StructRef(id=o._id).dict()
        elif isinstance(o, ExtensionDtype):
            type_ = 'dtype'
            json_ = DTypeWrapper(type_name=o.name).dict()
        else:
            raise TeralityTypeError(f'Unsupported argument type {type(o)}')
        json_['!terality:type'] = type_
        return json_


def json_dumps(o):
    try:
        return json.dumps(o, cls=_JSONEncoderClient)
    except (Boto3Error, IOError) as e:
        raise TeralityDataUploadError('Failed to upload data') from e
