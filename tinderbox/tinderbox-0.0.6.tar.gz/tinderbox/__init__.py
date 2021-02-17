import inspect
from dataclasses import fields
from typing import List
from typing import Type, TypeVar, Generic

from pyspark.sql import DataFrame

from tinderbox.smoke import _Empty
from tinderbox.tinder import col, AddColumn, DataFrameOperation

t_Source = TypeVar('t_Source')


class TinderBox(Generic[t_Source]):

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    @property
    def df(self) -> t_Source:
        return self._columns

    def __init__(self, df_model: Type[t_Source]):
        self._df_model = df_model
        self._mode = "config"
        self._pipeline: List[DataFrameOperation] = []
        self._columns = singe(df_model, self)
        self._current_data_frame: DataFrame = _Empty.of(DataFrame)

    def ignite(self, data_frame):
        self._current_data_frame = data_frame
        for dfo in self._pipeline:
            print("sparkline", dfo._name)
            dfo.propagate_context(self)
            self._current_data_frame = dfo.eval()
        return self._current_data_frame

    def transform(self, *steps, **named_steps):
        for step in steps:
            self._pipeline.append(step)
        self._pipeline.extend(named_steps.items())
        return self

    def add_column(self, name, expr) -> 'TinderBox':
        return self.transform(AddColumn(name, expr))

    def get_df(self) -> DataFrame:
        return self._current_data_frame


def singe(dtcls: Type[t_Source], tinder_context=None) -> Type[t_Source]:
    dt_fields = fields(dtcls)
    props = dict((k, col(k, tinder_context)) for k, v in inspect.getmembers(dtcls, lambda a: isinstance(a, property)))
    props.update((dtf.name, col(dtf, tinder_context)) for dtf in dt_fields)
    atype = type(dtcls.__name__, (object,), props)
    return atype


def make(df_model: Type[t_Source] = None) -> TinderBox[t_Source]:
    return TinderBox(df_model)
