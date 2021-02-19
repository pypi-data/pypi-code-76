import logging
import typing
import traceback


from datetime import datetime, timedelta
from timeit import default_timer as timer

from bakplane.bakplane_pb2 import *
from bakplane.bakplane_pb2_grpc import BakplaneStub
from bakplane.errors import BakplaneException
from bakplane.extensions.base import (
    BaseExtension,
    PluginEntry,
    ReadRequest,
    ReadResponse,
    WriteRequest,
    WriteResponse,
    ReadUniverseRequest,
    ReadUniverseResponse,
    ReadAllRequest,
    ExecutionStatistics,
)
from bakplane.extensions.spark.stores import redshift, postgres
from bakplane.utils import to_proto_timestamp_range, parse_value_by_type

__plugins = {}


def register_plugin(entry):
    if entry.code not in __plugins:
        __plugins[entry.code] = entry


def get_plugin_or_die(code: str) -> PluginEntry:
    if code not in __plugins:
        raise RuntimeError(f"Failed to obtain plugin `{code}`.")

    return __plugins[code]


class SparkExtension(BaseExtension):
    def __init__(self, stub: BakplaneStub, spark):
        self.stub = stub
        self.spark = spark

    def read(self, r: ReadRequest) -> ReadResponse:
        try:
            intent = self.stub.ResolveResourceIntent(
                ResolveResourceRequest(
                    universe=r.universe,
                    effective_dating=to_proto_timestamp_range(
                        r.get_derived_effective_start_dt(),
                        r.get_derived_effective_end_dt(),
                    ),
                    path=r.path,
                    warehouse=r.warehouse,
                    pointers=r.pointers,
                )
            )

            if not intent:
                raise RuntimeError("Failed to resolve intent.")

            if r.knowledge_dt is None:
                tomorrow_dt = datetime.utcnow() + timedelta(days=1)
                r.knowledge_dt = datetime(
                    year=tomorrow_dt.year,
                    month=tomorrow_dt.month,
                    day=tomorrow_dt.day,
                )

            if r.effective_dating is None and r.valid_dating is None:
                raise RuntimeError(
                    "You must provide at least effective_dating or valid_dating."
                )

            p = get_plugin_or_die(intent.warehouse_kind)

            return p.read_fn(self.spark, r, intent)
        except Exception as ex:
            raise BakplaneException(
                "Failed to execute read request due to: "
                + traceback.format_exc(),
                ex,
            )

    def write(self, r: WriteRequest) -> WriteResponse:
        try:
            logging.info(f"Writing to resource path `{r.path}`.")

            internals = self.stub.ResolveResourcePath(
                ResolveResourcePathRequest(path=r.path, warehouse=r.warehouse)
            )

            if not internals:
                raise RuntimeError("Failed to resolve resource path.")

            p = get_plugin_or_die(internals.warehouse_kind)
            return p.write_fn(r, internals)
        except Exception as ex:
            raise BakplaneException("Failed to execute write request.", ex)

    def read_universe(self, r: ReadUniverseRequest) -> ReadUniverseResponse:
        try:
            logging.info(f"Resolving universe `{r}`.")

            res = self.stub.ResolveUniverse(
                ResolveUniverseRequest(
                    universe=r.universe,
                    effective_dating=to_proto_timestamp_range(
                        r.effective_start_dt, r.effective_end_dt
                    ),
                )
            )

            if not res:
                raise RuntimeError("Failed to resolve universe.")
            return self.__build_read_universe_response(res)

        except Exception as ex:
            raise BakplaneException("Failed to read universe.", ex)

    def read_all(self, r: ReadAllRequest) -> ReadResponse:
        try:
            logging.info(f"Resolving resource path `{r.path}`.")

            res = self.stub.ResolveResourcePath(
                ResolveResourcePathRequest(path=r.path, warehouse=r.warehouse)
            )

            if not res:
                raise RuntimeError("Failed to resolve resource path.")

            p = get_plugin_or_die(res.warehouse_kind)
            return p.read_all_fn(self.spark, r, res)
        except Exception as ex:
            raise BakplaneException("Failed to execute read all request.", ex)

    def __build_read_universe_response(
        self, res: typing.Iterable[ResolveUniverseGroupEntry]
    ) -> ReadUniverseResponse:
        start = timer()

        rows = []
        schema = []
        ix = 0

        for g in res:
            row = []
            for e in g.entries:
                if ix == 0:
                    schema.append(e.attribute)
                row.append(parse_value_by_type(e.value, e.data_type))

            ix += 1
            rows.append(row)

        end = timer()

        return ReadUniverseResponse(
            df=self.spark.createDataFrame(data=rows, schema=schema),
            execution_statistics=ExecutionStatistics(elapsed_ms=(end - start)),
        )


register_plugin(redshift.get_registration())
register_plugin(postgres.get_registration())
