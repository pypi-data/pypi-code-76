import random
import typing
import urllib.parse
from datetime import datetime
from timeit import default_timer as timer

import sqlalchemy
from sqlalchemy import (
    Column,
    Table,
    MetaData,
    create_engine,
    DateTime,
    func,
    literal_column,
)
from bakplane.bakplane_pb2 import (
    ResolveResourcePathResponse,
    ResolveResourceIntentResponse,
    ComparisonType,
)
from bakplane.extensions.base import (
    WriteResponse,
    WriteRequest,
    ReadResponse,
    ReadAllRequest,
    ReadRequest,
    ReadRequestBuildingBlocks,
    DataStoreHelper,
    INFINITY_PROXY_DATE,
    DT_COLUMN_NAME,
    DEFAULT_SERIES,
)
from bakplane.extensions.spark.utils import (
    to_spark_save_mode,
    timestamp_to_date_string,
    datetime_to_date_string,
)
from bakplane.utils import to_execution_statistics


class JDBCStoreHelper(DataStoreHelper):
    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        port: int,
        database: str,
        schema_name: str,
        driver: str,
        table_prefixes: typing.List[str] = None,
        series_schema: str = "series",
    ):

        self.metadata = MetaData()
        self.engine = create_engine(
            f"{driver}://{user}:{password}@{host}:{port}/{database}",
            executemany_values_page_size=10000,
            executemany_batch_page_size=500,
            executemany_mode="batch",
        )
        self.schema_name = schema_name
        self.table_prefixes = table_prefixes
        self.series_schema = series_schema
        self.frequency_to_tbl = {}

        self.__preload_existing_series()

    def get_series_table(
        self, series: typing.Tuple[datetime, datetime, str], alias: str = None
    ) -> Table:
        freq = series[2].strip().lower()

        if freq not in self.frequency_to_tbl:
            raise RuntimeError(
                f"Frequency `{freq}` is not found within cache. Verify the series exist in `{self.series_schema} on `{self.engine.url}`."
            )

        if alias is None:
            alias = f"t_{freq}_{str(int(datetime.utcnow().timestamp()))}_{str(random.randint(1, 100000))}"

        return self.frequency_to_tbl[freq].alias(alias)

    def __preload_existing_series(self):
        for s in DEFAULT_SERIES:

            freq = s.lower().strip()
            tbl_name = f"s_{freq}"

            columns = [
                Column(
                    DT_COLUMN_NAME, DateTime, nullable=False, primary_key=True
                )
            ]

            tbl = Table(
                tbl_name, self.metadata, *columns, schema=self.series_schema
            )

            if self.engine.dialect.has_table(
                self.engine, table_name=tbl_name, schema=self.series_schema
            ):
                self.frequency_to_tbl[freq] = tbl

    def create_temporary_table(
        self,
        prefix: str,
        columns: typing.List[Column],
        rows: typing.List[typing.Dict[str, typing.Any]],
    ) -> Table:

        for c in columns:
            c.table = None

        tbl = Table(
            prefix
            + "_"
            + str(int(datetime.utcnow().timestamp()))
            + "_"
            + str(random.randint(1, 1000)),
            self.metadata,
            *columns,
            schema=self.schema_name,
        )

        tbl.create(bind=self.engine)
        self.engine.execute(tbl.insert(), rows)

        return tbl


def __build_read_all_query(
    r: ReadAllRequest, res: ResolveResourcePathResponse
) -> str:
    return f'select {", ".join(r.columns)} from {res.context["schema_name"]}.{res.context["table_name"]}'


def __get_range_semantics_ops(semantics: str) -> typing.Tuple[str, str]:
    if semantics == "[)":
        return ">=", "<"
    elif semantics == "[]":
        return ">=", "<="
    elif semantics == "(]":
        return ">", "<="
    elif semantics == "()":
        return ">", "<"
    else:
        raise RuntimeError(f"`{semantics}` is not a valid range semantics.")


def __add_effective_dating_constraint(
    blocks: ReadRequestBuildingBlocks,
    res: ResolveResourceIntentResponse,
    r: ReadRequest,
):
    a = blocks.asset_table

    if r.effective_dating is None:
        return

    op1, op2 = __get_range_semantics_ops(
        blocks.effective_dating_range_semantics
    )

    if blocks.effective_dating_table is not None:
        blocks.constraints.append(
            blocks.effective_dating_table.c.dt.op(op1)(a.c.effective_start_dt)
        )

        blocks.constraints.append(
            blocks.effective_dating_table.c.dt.op(op2)(a.c.effective_end_dt)
        )

        blocks.constraints.append(
            blocks.effective_dating_table.c.dt.op(op1)(
                datetime_to_date_string(blocks.effective_start_dt)
            )
        )

        blocks.constraints.append(
            blocks.effective_dating_table.c.dt.op(op2)(
                datetime_to_date_string(blocks.effective_end_dt)
            )
        )

        blocks.columns.append(
            blocks.effective_dating_table.c.dt.label("effective_dt")
        )

    else:
        blocks.constraints.append(
            a.c.effective_start_dt
            <= timestamp_to_date_string(res.effective_dating.end_dt.seconds)
        )
        blocks.constraints.append(
            a.c.effective_end_dt
            >= timestamp_to_date_string(res.effective_dating.start_dt.seconds)
        )


def __add_valid_dating_constraint(
    blocks: ReadRequestBuildingBlocks, res: ResolveResourceIntentResponse
):
    a = blocks.asset_table

    op1, op2 = __get_range_semantics_ops(blocks.valid_dating_range_semantics)

    if blocks.valid_dating_table is not None:
        blocks.constraints.append(
            blocks.valid_dating_table.c.dt.op(op1)(a.c.valid_start_dt)
        )

        blocks.constraints.append(
            blocks.valid_dating_table.c.dt.op(op2)(a.c.valid_end_dt)
        )

        blocks.constraints.append(
            blocks.valid_dating_table.c.dt.op(op1)(
                datetime_to_date_string(blocks.valid_start_dt)
            )
        )

        blocks.constraints.append(
            blocks.valid_dating_table.c.dt.op(op2)(
                datetime_to_date_string(blocks.valid_end_dt)
            )
        )

        blocks.columns.append(blocks.valid_dating_table.c.dt.label("valid_dt"))


def __populate_building_blocks_dating(
    request_field: str,
    start_field: str,
    end_field: str,
    dating_tbl_field: str,
    semantics_field: str,
    helper: DataStoreHelper,
    blocks: ReadRequestBuildingBlocks,
    r: ReadRequest,
):
    if not hasattr(r, request_field):
        raise RuntimeError("Invalid field name.")

    dating = getattr(r, request_field)

    if dating is None:
        return

    if isinstance(dating, tuple):
        if len(dating) == 2:
            start, end = dating

            setattr(blocks, start_field, start)
            setattr(blocks, end_field, end)

        elif len(dating) == 3:
            setattr(
                blocks,
                dating_tbl_field,
                helper.get_series_table(dating, alias=request_field),
            )
            setattr(blocks, start_field, dating[0])
            setattr(blocks, end_field, dating[1])
        elif len(dating) == 4:
            setattr(
                blocks,
                dating_tbl_field,
                helper.get_series_table(dating, alias=request_field),
            )
            setattr(blocks, start_field, dating[0])
            setattr(blocks, end_field, dating[1])
            setattr(blocks, semantics_field, dating[3])

        else:
            raise RuntimeError("Invalid dating constraint.")

    elif isinstance(dating, datetime):
        setattr(blocks, start_field, dating)
        setattr(blocks, end_field, INFINITY_PROXY_DATE)
    else:
        raise ValueError("Effective dating has unknown type.")


def __build_read_query(
    r: ReadRequest,
    res: ResolveResourceIntentResponse,
    dialect,
    store_helper: DataStoreHelper,
) -> str:
    from sqlalchemy import (
        Table,
        MetaData,
        Column,
        select,
        and_,
    )

    if (r.columns is None or len(r.columns) <= 0) and r.query_builder is None:
        raise RuntimeError("You must provide a set of columns.")

    metadata: MetaData = MetaData()

    src_tbl: Table = Table(
        res.table_name,
        metadata,
        *[Column(x.name) for x in res.columns],
        schema=res.schema_name,
    )

    mapping_tbl: Table = Table(
        res.mapping.table_name,
        metadata,
        *[Column(x.name) for x in res.mapping.columns],
        schema=res.mapping.schema_name,
    )

    a = src_tbl.alias("a")

    mapping_columns = []
    for column in res.mapping.columns:
        if not column.is_effective_dating:
            mapping_columns.append(
                mapping_tbl.c.get(column.name).label(column.name)
            )

    m = mapping_tbl.alias("m")
    clauses = []
    for clause in res.mapping.clauses:
        if clause.comparison == ComparisonType.EQ:
            clauses.append(
                m.c.get(clause.mapping_field_name)
                == a.c.get(clause.resource_field_name)
            )

    blocks = ReadRequestBuildingBlocks(
        mapping_table=m,
        asset_table=a,
        selectable=m.join(a, and_(*clauses)),
        knowledge_dt=r.knowledge_dt,
        constraints=[
            and_(
                *[
                    datetime_to_date_string(r.knowledge_dt)
                    >= a.c.knowledge_start_dt,
                    datetime_to_date_string(r.knowledge_dt)
                    < a.c.knowledge_end_dt,
                ]
            )
        ],
        valid_dating_range_semantics="[)",
        effective_dating_range_semantics="[)",
    )

    __populate_building_blocks_dating(
        "effective_dating",
        "effective_start_dt",
        "effective_end_dt",
        "effective_dating_table",
        "effective_dating_range_semantics",
        store_helper,
        blocks,
        r,
    )

    __populate_building_blocks_dating(
        "valid_dating",
        "valid_start_dt",
        "valid_end_dt",
        "valid_dating_table",
        "valid_dating_range_semantics",
        store_helper,
        blocks,
        r,
    )

    if r.query_builder:
        res = r.query_builder(blocks)
    else:
        blocks.columns = [a.c.get(x) for x in r.columns if x in a.c]

        if r.partition_num is not None:
            if r.partition_column_name not in a.c:
                raise RuntimeError("Could not identify partition column.")

            index_expression = func.abs(a.c.knowledge_hash % r.partition_num)
            blocks.columns.append(index_expression.label("partition"))

        if r.additional_constraints is not None:
            blocks.constraints.append(r.additional_constraints(blocks))

        if r.effective_dating is not None:
            if r.effective_dating_hint is None:
                blocks.constraints.append(
                    a.c.effective_start_dt
                    <= blocks.mapping_table.c.effective_end_dt
                )

                blocks.constraints.append(
                    a.c.effective_end_dt
                    >= blocks.mapping_table.c.effective_start_dt
                )
        else:
            blocks.constraints.append(
                a.c.valid_start_dt <= blocks.mapping_table.c.effective_end_dt
            )

            blocks.constraints.append(
                a.c.valid_end_dt >= blocks.mapping_table.c.effective_start_dt
            )

        __add_valid_dating_constraint(blocks, res)

        if r.effective_dating_hint is None:
            __add_effective_dating_constraint(blocks, res, r)

        else:
            if isinstance(r.effective_dating_hint, tuple):
                s = datetime_to_date_string(
                    typing.cast(datetime, r.effective_dating_hint[0])
                )
                e = datetime_to_date_string(
                    typing.cast(datetime, r.effective_dating_hint[1])
                )

                blocks.constraints.append(a.c.effective_start_dt <= e)
                blocks.constraints.append(a.c.effective_end_dt >= s)
            elif isinstance(r.effective_dating_hint, str):
                col = typing.cast(str, r.effective_dating_hint)

                s = col + "_start_dt"
                e = col + "_end_dt"

                blocks.constraints.append(a.c.effective_start_dt <= m.c.get(e))
                blocks.constraints.append(a.c.effective_end_dt >= m.c.get(s))
            else:
                raise RuntimeError("Invalid type for effective_dating_hint.")

        if r.modifiers:
            for m in r.modifiers:
                blocks = m.execute(blocks, store_helper)

        res = (
            select(blocks.columns)
            .select_from(blocks.selectable)
            .where(and_(*blocks.constraints))
        )

    query = str(
        res.compile(dialect=dialect, compile_kwargs={"literal_binds": True},)
    )

    return query.replace("%%", "%")


def write_fn(
    r: WriteRequest, res: ResolveResourcePathResponse, driver: str, url: str
) -> WriteResponse:
    start = timer()

    r.df.write.format("jdbc").mode(to_spark_save_mode(r.mode)).option(
        "driver", driver
    ).option("url", url).option(
        "dbtable", f"{res.context['schema_name']}.{res.context['table_name']}"
    ).option(
        "user", res.context["username"]
    ).option(
        "password", urllib.parse.unquote(res.context["password"])
    ).save()

    end = timer()

    return WriteResponse(
        execution_statistics=to_execution_statistics(start, end)
    )


def __read_query(
    spark,
    url: str,
    driver: str,
    query: str,
    user: str,
    password: str,
    partition_num: int,
):
    start = timer()

    if partition_num is None:
        df = (
            spark.read.format("jdbc")
            .option("url", url)
            .option("query", query)
            .option("user", user)
            .option("password", urllib.parse.unquote(password))
            .option("driver", driver)
            .load()
        )
    else:
        df = (
            spark.read.format("jdbc")
            .option("url", url)
            .option("dbtable", f"({query}) s")
            .option("user", user)
            .option("password", urllib.parse.unquote(password))
            .option("driver", driver)
            .option("partitionColumn", "partition")
            .option("lowerBound", 0)
            .option("upperBound", partition_num - 1)
            .option("numPartitions", partition_num)
            .load()
        )

    end = timer()

    return ReadResponse(
        df=df,
        execution_statistics=to_execution_statistics(start, end),
        context={"query": query,},
    )


def read_all_fn(
    ctx: typing.Any,
    r: ReadAllRequest,
    res: ResolveResourcePathResponse,
    url: str,
    driver: str,
) -> ReadResponse:
    return __read_query(
        spark=ctx,
        url=url,
        driver=driver,
        query=__build_read_all_query(r, res),
        user=res.context["username"],
        password=res.context["password"],
        partition_num=r.partition_num,
    )


def read_fn(
    ctx: typing.Any,
    r: ReadRequest,
    res: ResolveResourceIntentResponse,
    dialect,
    url: str,
    driver: str,
    store_helper: DataStoreHelper,
) -> ReadResponse:
    return __read_query(
        spark=ctx,
        url=url,
        driver=driver,
        query=__build_read_query(r, res, dialect, store_helper),
        user=res.context["username"],
        password=res.context["password"],
        partition_num=r.partition_num,
    )
