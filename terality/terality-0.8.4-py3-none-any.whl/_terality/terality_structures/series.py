from io import TextIOBase
from pathlib import Path
from typing import Any, Optional, Union, Type

import numpy as np
import pandas as pd
from pandas.core.dtypes.base import ExtensionDtype

from . import ClassMethod, Struct, call_pandas_function
from .structure import Property, StructIterator
from .index import Index, MultiIndex
from ..utils import write_output


class ClassMethodSeries(ClassMethod):
    _class_name: str = 'series'
    _pandas_class = pd.Series
    _additional_class_methods = ClassMethod._additional_class_methods | {'random', 'random_integers'}


class Series(Struct, metaclass=ClassMethodSeries):
    _class_name: str = 'series'
    _pandas_class_instance = pd.Series(dtype='float64')
    _acessors = {'str', 'dt'}
    _additional_methods = Struct._additional_methods | {'get_range_auto'}

    index = Property('index')

    def __init__(self, data: Any = None, index: Any = None, dtype: Optional[Union[str, Type, ExtensionDtype]] = None,
                 name: Optional[str] = None, copy: bool = True):
        # NOTE: Compared to vanilla Pandas, Terality's default for the `copy` argument is True.
        # The reason is that shallow copies (`copy=False`) are not supported. If it were the default, the client
        # would need to pass `copy=True` every time when calling this constructor, which is terrible UX.

        # If the data is not already a Terality series, convert it.
        if data is not None:
            if not isinstance(data, Series):
                if not isinstance(data, pd.Series):
                    data = pd.Series(data, dtype=dtype)
                data = Series.from_pandas(data)

        # If the index is not already a Terality index, convert it.
        if index is not None:
            if isinstance(index, (MultiIndex, pd.MultiIndex)):
                raise TypeError('Index must have a single level')
            if not isinstance(index, Index):
                if not isinstance(index, pd.Index):
                    index = pd.Index(index)
                index = Index.from_pandas(index)

        # Create a new Terality Series from the data (and, optionally, index).
        # NOTE: `copy` is completely ignored, as we do not support it.
        # The reason we do not raise an exception is that Pandas' default is false.
        new_series = call_pandas_function('series', None, '__init__', data=data, index=index, name=name, dtype=dtype,
                                          copy=copy)
        self._assign(new_series)

    def __iter__(self):
        return StructIterator(self)

    def to_list(self):
        series_pd = self._call(None, 'to_list')
        return series_pd.to_list()

    def tolist(self):
        series_pd = self._call(None, 'tolist')
        return series_pd.tolist()

    def to_dict(self):
        series_pd = self._call(None, 'to_dict')
        return series_pd.to_dict()

    def to_string(
            self, buf: Optional[Union[TextIOBase, str, Path]] = None, na_rep: str = 'NaN', float_format: Any = None,
            header: bool = True, index: bool = True, length: bool = False, dtype: bool = False, name: bool = False,
            max_rows: Optional[int] = None, min_rows: Optional[int] = None, encoding: Optional[str] = None
    ) -> Optional[str]:
        result = self._call(None, 'to_string', na_rep=na_rep, float_format=float_format, header=header, index=index,
                            length=length, dtype=dtype, name=name, max_rows=max_rows, min_rows=min_rows)
        if buf is None:
            return result
        else:
            write_output(result, buf, encoding)

    def unique(self) -> 'np.ndarray':
        result: Series = self._call(None, 'unique')
        return result.to_pandas().values
