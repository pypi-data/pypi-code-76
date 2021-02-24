from io import StringIO, TextIOBase
from pathlib import Path
import sys
from typing import Any, Dict, Hashable, List, Literal, Optional, Sequence, Union, Type, Mapping, Iterable

import pandas as pd
from pandas.core.dtypes.base import ExtensionDtype

from .. import ExportRequest
from . import ClassMethod, Struct, call_pandas_function
from .structure import Property, StructIterator
from .index import Index, MultiIndex
from .series import Series
from ..serialization.data_transfers import _S3
from ..utils import write_output

LengthUnit = Union[int, str]


class ClassMethodDF(ClassMethod):
    _class_name: str = 'dataframe'
    _pandas_class = pd.DataFrame


class DataFrame(Struct, metaclass=ClassMethodDF):
    _class_name: str = 'dataframe'
    _pandas_class_instance = pd.DataFrame()
    _additional_methods = Struct._additional_methods | {'to_csv_folder', 'to_parquet_folder'}

    axes = Property('axes')
    columns = Property('columns')
    index = Property('index')

    def __init__(self, data: Any = None, index: Any = None, columns: Optional[Iterable] = None,
                 dtype: Optional[Union[str, Type, ExtensionDtype]] = None, copy: bool = True):
        # NOTE: Compared to vanilla Pandas, Terality's default for the `copy` argument is True.
        # The reason is that shallow copies (`copy=False`) are not supported. If it were the default, the client
        # would need to pass `copy=True` every time when calling this constructor, which is terrible UX.

        # If the index is not already a Terality index, convert it.
        if index is not None:
            if isinstance(index, (MultiIndex, pd.MultiIndex)):
                raise TypeError('Index must have a single level')
            if not isinstance(index, (Index, MultiIndex)):
                if not isinstance(index, (pd.Index, pd.MultiIndex)):
                    # TODO: Support creating multi-indices?
                    index = pd.Index(index)
                if isinstance(index, pd.Index):
                    index = Index.from_pandas(index)
                else:
                    index = MultiIndex.from_pandas(index)

        # If columns are not already a list, convert them.
        if columns is not None:
            if not isinstance(columns, list):
                columns = list(columns)

        if data is not None:
            if not isinstance(data, DataFrame):
                # We have many options to construct a data frames, but they basically fall down into two families:
                # 1. As a dictionary-like of list-like values, which are interpreted as columns
                # 2. As a list-like of list-like values, which are interpreted as rows
                #
                # We handle specially the case of a dictionary of Terality series, because it allows to stitch themn
                # together very cheaply.
                if isinstance(data, dict) and all(isinstance(value, Series) for value in data.values()):
                    pass
                # Otherwise, we let Pandas figuring it out.
                else:
                    if not isinstance(data, pd.DataFrame):
                        data = pd.DataFrame(data, columns=columns)
                    data = DataFrame.from_pandas(data)

        # At this stage, data is either None, a `te.DataFrame`, or a dict of `te.Series`.
        new_df = call_pandas_function('dataframe', None, '__init__', data=data, index=index, columns=columns,
                                      dtype=dtype, copy=copy)
        self._assign(new_df)

    def __iter__(self):
        # Iterating on a `DataFrame` is the same as iterating on its columns.
        return StructIterator(self.columns)

    def info(self, verbose: Optional[bool] = None, buf: Optional[StringIO] = None, max_cols: Optional[int] = None,
             memory_usage: Optional[Union[bool, Literal['deep']]] = None, null_counts: Optional[bool] = None):
        result = self._call(None, 'info', verbose=verbose, max_cols=max_cols, memory_usage=memory_usage,
                            null_counts=null_counts)
        # NOTE: `info` works by side effect. The return value is always `None`.
        out = buf or sys.stdout
        out.write(result)

    def _truc(self, path: str) -> ExportRequest:
        if path.startswith('s3://'):
            bucket = path[5:].split('/', maxsplit=1)[0]
            aws_region = _S3.client().get_bucket_location(Bucket=bucket)['LocationConstraint']
        else:
            aws_region = None
        return ExportRequest(path=path, aws_region=aws_region)

    def to_csv(self, path: str):
        return self._call(None, 'to_csv', self._truc(path))

    def to_csv_folder(self, path: str, num_files: int):
        return self._call(None, 'to_csv_folder', self._truc(path), num_files)

    def to_parquet(self, path: str):
        return self._call(None, 'to_parquet', self._truc(path))

    def to_parquet_folder(self, path: str, num_files: int):
        return self._call(None, 'to_parquet_folder', self._truc(path), num_files)

    def to_dict(self, orient: Literal['dict', 'list', 'series', 'split', 'records', 'index'] = 'dict',
                into: Union[Type[Mapping], Mapping] = dict):
        df_pd = self._call(None, 'to_dict')
        return df_pd.to_dict(orient=orient, into=into)

    def to_string(
            self, buf: Optional[Union[TextIOBase, str, Path]] = None, columns: Optional[Sequence[Hashable]] = None,
            col_space: Optional[Union[int, List[int], Dict[Hashable, int]]] = None,
            header: Union[bool, Sequence[str]] = True, index: bool = True, na_rep: str = 'NaN', formatters: Any = None,
            float_format: Any = None, sparsify: bool = True, index_names: bool = True, justify: Optional[str] = None,
            max_rows: Optional[int] = None, min_rows: Optional[int] = None, max_cols: Optional[int] = None,
            show_dimensions: bool = False, decimal: str = '.', line_width: Optional[int] = None,
            max_colwidth: Optional[int] = None, encoding: Optional[str] = None
    ) -> Optional[str]:
        result = self._call(None, 'to_string', columns=columns, col_space=col_space, header=header, index=index,
                            na_rep=na_rep, formatters=formatters, float_format=float_format, sparsify=sparsify,
                            index_names=index_names, justify=justify, max_rows=max_rows, min_rows=min_rows,
                            max_cols=max_cols, show_dimensions=show_dimensions, decimal=decimal, line_width=line_width,
                            max_colwidth=max_colwidth)
        if buf is None:
            return result
        else:
            write_output(result, buf, encoding)

    def to_html(
            self, buf: Optional[Union[TextIOBase, str, Path]] = None, columns: Optional[Sequence[Hashable]] = None,
            col_space: Optional[Union[LengthUnit, List[LengthUnit], Dict[Hashable, LengthUnit]]] = None,
            header: Union[bool, Sequence[str]] = True, index: bool = True, na_rep: str = 'NaN',
            formatters: Any = None, float_format: Any = None, sparsify: bool = True,
            index_names: bool = True, justify: Optional[str] = None, max_rows: Optional[int] = None,
            max_cols: Optional[int] = None, show_dimensions: bool = False,
            decimal: str = '.', bold_rows: bool = True, classes: Optional[Union[str, List[str]]] = None,
            escape: bool = True, notebook: bool = False, border: Optional[int] = None, encoding: Optional[str] = None,
            table_id: Optional[str] = None, render_links: bool = False
    ) -> Optional[str]:
        result = self._call(None, 'to_html', columns=columns, col_space=col_space, header=header, index=index,
                            na_rep=na_rep, formatters=formatters, float_format=float_format, sparsify=sparsify,
                            index_names=index_names, justify=justify, max_rows=max_rows, max_cols=max_cols,
                            show_dimensions=show_dimensions, decimal=decimal, bold_rows=bold_rows, classes=classes,
                            escape=escape, notebook=notebook, border=border, table_id=table_id,
                            render_links=render_links)
        if buf is None:
            return result
        else:
            write_output(result, buf, encoding)
