import typing
from functools import lru_cache

from bakplane.bakplane_pb2 import (
    ResolveResourcePathResponse,
    ResolveResourceIntentResponse,
)
from bakplane.extensions.base import (
    WriteRequest,
    ConnectionStringContext,
    ReadResponse,
    ReadAllRequest,
    ReadRequest,
)
from bakplane.extensions.spark import PluginEntry, WriteResponse
from bakplane.extensions.spark.stores.jdbc import JDBCStoreHelper
from cachetools import cached
from cachetools.keys import hashkey

DRIVER_NAME = "com.amazon.redshift.jdbc42.Driver"


def get_registration():
    return PluginEntry(
        name="Redshift",
        code="redshift",
        description="Redshift store",
        author="Isaac Elbaz",
        read_fn=__read_fn,
        read_all_fn=__read_all_fn,
        write_fn=__write_fn,
        connection_string_url_fn=__connection_string_url,
        driver_name=DRIVER_NAME,
    )


@cached(
    cache={},
    key=lambda user, password, host, port, database, schema_name: hashkey(
        host, database
    ),
)
def get_helper(
    user: str,
    password: str,
    host: str,
    port: int,
    database: str,
    schema_name: str,
):
    return JDBCStoreHelper(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
        schema_name=schema_name,
        driver="redshift+psycopg2",
        series_schema="series",
    )


def __connection_string_url(c: ConnectionStringContext) -> str:
    return f'jdbc:redshift://{c.context["host"]}:{c.context["port"]}/{c.context["database"]}'


def __write_fn(
    r: WriteRequest, res: ResolveResourcePathResponse
) -> WriteResponse:
    from bakplane.extensions.spark.stores.jdbc import write_fn

    return write_fn(
        r=r,
        res=res,
        driver=DRIVER_NAME,
        url=__connection_string_url(ConnectionStringContext(res.context)),
    )


def __read_all_fn(
    ctx: typing.Any, r: ReadAllRequest, res: ResolveResourcePathResponse
) -> ReadResponse:
    from bakplane.extensions.spark.stores.jdbc import read_all_fn

    return read_all_fn(
        ctx=ctx,
        r=r,
        res=res,
        url=__connection_string_url(ConnectionStringContext(res.context)),
        driver=DRIVER_NAME,
    )


def __read_fn(
    ctx: typing.Any, r: ReadRequest, res: ResolveResourceIntentResponse
) -> ReadResponse:
    from bakplane.extensions.spark.stores.jdbc import read_fn
    from sqlalchemy.dialects import postgresql

    return read_fn(
        ctx=ctx,
        r=r,
        res=res,
        dialect=postgresql.dialect(),
        url=__connection_string_url(ConnectionStringContext(res.context)),
        driver=DRIVER_NAME,
        store_helper=get_helper(
            user=res.context["username"],
            password=res.context["password"],
            host=res.context["host"],
            port=res.context["port"],
            database=res.context["database"],
            schema_name="temp_data",
        ),
    )
