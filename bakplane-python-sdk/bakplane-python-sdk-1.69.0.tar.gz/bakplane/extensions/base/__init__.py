import datetime
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

import pandas as pd
from sqlalchemy import Table, Column
from sqlalchemy.sql import FromClause
from sqlalchemy.sql.elements import BooleanClauseList

from bakplane.bakplane_pb2 import (
    Universe,
    ResolveResourceIntentResponse,
    ResolveResourcePathResponse,
)

date_constraint_t = typing.Union[
    typing.Tuple[datetime.datetime, datetime.datetime],
    typing.Tuple[datetime.datetime, datetime.datetime, str],
    typing.Tuple[datetime.datetime, datetime.datetime, str, str],
    datetime.datetime,
]

DT_COLUMN_NAME = "dt"
DEFAULT_SERIES = [
    "B",
    "D",
    "W",
    "M",
    "SM",
    "BM",
    "MS",
    "SMS",
    "BMS",
    "Q",
    "BQ",
    "QS",
    "Y",
    "BY",
    "YS",
    "BYS",
]
INFINITY_PROXY_DATE = datetime.datetime(year=3000, month=12, day=31)


def flatten_date_constraints(
    c: date_constraint_t,
) -> typing.List[datetime.datetime]:
    if isinstance(c, datetime.datetime):
        return [c, INFINITY_PROXY_DATE]
    elif isinstance(c, tuple):
        if len(c) == 2:
            return [c[0], c[1]]
        elif len(c) == 3 or len(c) == 4:
            results = set()

            ranges = pd.bdate_range(start=c[0], end=c[1], freq=c[2])
            for r in ranges:
                results.add(r.to_pydatetime())
            return list(results)
        else:
            raise RuntimeError(
                f"Invalid dating definition: `{c}` is not valid."
            )


class WriteMode(Enum):
    ERROR_IF_EXISTS = 1
    APPEND = 2
    OVERWRITE = 3
    IGNORE = 4


@dataclass
class ExecutionStatistics:
    elapsed_ms: float


@dataclass
class ConnectionStringContext:
    context: typing.Dict[str, str]


@dataclass
class WriteRequest:
    path: str
    warehouse: str
    df: typing.Any
    mode: WriteMode


@dataclass
class ReadAllRequest:
    path: str
    warehouse: str
    columns: typing.List[str]

    partition_column_name: str = "knowledge_hash"
    partition_num: int = None


@dataclass
class ReadRequestBuildingBlocks:
    asset_table: Table
    mapping_table: Table
    selectable: FromClause
    constraints: typing.List[typing.Any]

    effective_dating_range_semantics: str
    valid_dating_range_semantics: str

    effective_dating_table: Table = None
    valid_dating_table: Table = None

    effective_start_dt: datetime = None
    effective_end_dt: datetime = None

    valid_start_dt: datetime = None
    valid_end_dt: datetime = None

    knowledge_dt: datetime.datetime = None
    query: typing.Any = None
    columns: typing.List[Column] = None
    modifier_context: typing.Dict[str, typing.Any] = None


class DataStoreHelper(ABC):
    @abstractmethod
    def create_temporary_table(
        self,
        prefix: str,
        columns: typing.List[Column],
        rows: typing.List[typing.Any],
    ) -> Table:
        pass

    @abstractmethod
    def get_series_table(
        self,
        frequency: typing.Tuple[datetime.datetime, datetime.datetime, str],
        alias: str = None,
    ) -> Table:
        pass


class Modifier:
    @abstractmethod
    def execute(
        self, r: ReadRequestBuildingBlocks, h: DataStoreHelper
    ) -> ReadRequestBuildingBlocks:
        pass


@dataclass
class ReadRequest:
    path: str
    warehouse: str
    universe: Universe

    pointers: typing.Dict[str, str]

    effective_dating: date_constraint_t = None
    valid_dating: date_constraint_t = None

    columns: typing.List[str] = None
    knowledge_dt: datetime.datetime = None

    query_builder: typing.Callable[
        [ReadRequestBuildingBlocks], typing.Any
    ] = None

    additional_constraints: typing.Callable[
        [ReadRequestBuildingBlocks], BooleanClauseList
    ] = None

    effective_dating_hint: typing.Union[
        str, typing.Tuple[datetime.datetime, datetime.datetime]
    ] = None

    modifiers: typing.List[Modifier] = None

    partition_column_name: str = "knowledge_hash"
    partition_num: int = None

    def get_derived_effective_start_dt(self) -> datetime.datetime:
        if self.effective_dating is not None:
            return self.get_min_effective_dt()
        return self.get_min_valid_dt()

    def get_derived_effective_end_dt(self) -> datetime.datetime:
        if self.effective_dating is not None:
            return self.get_max_effective_dt()
        return self.get_max_valid_dt()

    def get_resolved_effective_dating(self) -> typing.List[datetime.datetime]:
        return flatten_date_constraints(self.effective_dating)

    def get_resolved_valid_dating(self) -> typing.List[datetime.datetime]:
        return flatten_date_constraints(self.valid_dating)

    def get_min_effective_dt(self) -> datetime.datetime:
        return min(self.get_resolved_effective_dating())

    def get_max_effective_dt(self) -> datetime.datetime:
        return max(self.get_resolved_effective_dating())

    def get_min_valid_dt(self) -> datetime.datetime:
        return min(self.get_resolved_valid_dating())

    def get_max_valid_dt(self) -> datetime.datetime:
        return max(self.get_resolved_valid_dating())


@dataclass
class ReadUniverseRequest:
    universe: Universe
    effective_start_dt: datetime.datetime
    effective_end_dt: datetime.datetime
    knowledge_dt: datetime.datetime = None


@dataclass
class ReadResponse:
    df: typing.Any
    execution_statistics: ExecutionStatistics
    context: typing.Dict[str, str]


@dataclass
class WriteResponse:
    execution_statistics: ExecutionStatistics


@dataclass
class ReadUniverseResponse:
    df: typing.Any
    execution_statistics: ExecutionStatistics


@dataclass
class PluginEntry:
    name: str
    code: str
    description: str
    author: str
    write_fn: typing.Callable[
        [WriteRequest, ResolveResourcePathResponse], WriteResponse
    ]
    read_fn: typing.Callable[
        [typing.Any, ReadRequest, ResolveResourceIntentResponse], ReadResponse
    ]
    read_all_fn: typing.Callable[
        [typing.Any, ReadAllRequest, ResolveResourcePathResponse], ReadResponse
    ]
    connection_string_url_fn: typing.Callable[[ConnectionStringContext], str]
    driver_name: str


class BaseExtension(ABC):
    @abstractmethod
    def read(self, r: ReadRequest) -> ReadResponse:
        pass

    @abstractmethod
    def read_all(self, r: ReadAllRequest) -> ReadResponse:
        pass

    @abstractmethod
    def write(self, r: WriteRequest) -> WriteResponse:
        pass

    @abstractmethod
    def read_universe(self, r: ReadUniverseRequest) -> ReadUniverseResponse:
        pass
