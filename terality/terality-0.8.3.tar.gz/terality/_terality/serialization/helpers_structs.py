from typing import Any, List, Optional

import pandas as pd
from pydantic import BaseModel


######################################################################################################################
# Structures to help with serde of classes not JSON serializable


class UploadRequest(BaseModel):
    transfer_id: str
    aws_region: Optional[str]


class Upload(BaseModel):
    path: str


class ExportRequest(BaseModel):
    path: str
    aws_region: Optional[str]


class ExportResponse(BaseModel):
    path: str
    aws_region: Optional[str]
    is_folder: bool
    transfer_id: str


class StructRef(BaseModel):
    id: str


class DTypeWrapper(BaseModel):
    type_name: str


class PythonTypeWrapper(BaseModel):
    module_name: str
    type_name: str


class CallableWrapper(BaseModel):
    dill_payload: str


class IndexColNames(BaseModel):
    names: List[Any]   # Pydantic can't assert Hashable, so use Any here
    name: Any  # Pydantic can't assert Hashable, so use Any here

    @classmethod
    def from_index(cls, index: pd.Index):
        return IndexColNames(names=list(index.names), name=index.name)


class PandasIndexMetadata(BaseModel):
    transfer_id: str
    cols_json_encoded: List[bool]
    index_col_names: IndexColNames

    @classmethod
    def from_index(cls, index: pd.Index, transfer_id: str, cols_json_encoded: List[bool]):
        return PandasIndexMetadata(
            transfer_id=transfer_id,
            cols_json_encoded=cols_json_encoded,
            index_col_names=IndexColNames.from_index(index)
        )


class PandasSeriesMetadata(BaseModel):
    transfer_id: str
    cols_json_encoded: List[bool]
    index_col_names: IndexColNames
    series_name: Any  # Pydantic can't assert Hashable, so use Any here

    @classmethod
    def from_series(cls, series: pd.Series, transfer_id: str, cols_json_encoded: List[bool]):
        return PandasSeriesMetadata(
            transfer_id=transfer_id,
            cols_json_encoded=cols_json_encoded,
            index_col_names=IndexColNames.from_index(series.index),
            series_name=series.name
        )


class PandasDFMetadata(BaseModel):
    transfer_id: str
    cols_json_encoded: List[bool]
    index_col_names: IndexColNames
    col_names: List[Any]  # Pydantic can't assert Hashable, so use Any here

    @classmethod
    def from_df(cls, df: pd.DataFrame, transfer_id: str, cols_json_encoded: List[bool]):
        return PandasDFMetadata(
            transfer_id=transfer_id,
            cols_json_encoded=cols_json_encoded,
            index_col_names=IndexColNames.from_index(df.index),
            col_names=list(df.columns)
        )
