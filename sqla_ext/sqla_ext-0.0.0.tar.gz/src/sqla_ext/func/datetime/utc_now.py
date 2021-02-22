from typing import Any, Dict

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import DateTime


class utc_now(FunctionElement):
    type = DateTime()


@compiles(utc_now, "postgresql")
def pg(element: utc_now, compiler: SQLCompiler, **kw: Dict[str, Any]) -> SQLCompiler:
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@compiles(utc_now, "sqlite")
def sqlite(
    element: utc_now, compiler: SQLCompiler, **kw: Dict[str, Any]
) -> SQLCompiler:
    return "datetime('now')"


@compiles(utc_now, "mysql")
def mysql(element: utc_now, compiler: SQLCompiler, **kw: Dict[str, Any]) -> SQLCompiler:
    return "utc_timestamp()"
