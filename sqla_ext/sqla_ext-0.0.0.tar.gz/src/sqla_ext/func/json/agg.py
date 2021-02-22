from typing import Any, Dict

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import JSON


class agg(FunctionElement):
    type = JSON()
    name = "agg"


@compiles(agg, "postgresql")
def pg(element: agg, compiler: SQLCompiler, **kw: Dict[str, Any]) -> SQLCompiler:
    return "jsonb_agg(%s)" % compiler.process(element.clauses, **kw)


@compiles(agg, "sqlite")
def sqlite(element: agg, compiler: SQLCompiler, **kw: Dict[str, Any]) -> SQLCompiler:
    return "json_group_array(%s)" % compiler.process(element.clauses, **kw)


@compiles(agg, "mysql")
def mysql(element: agg, compiler: SQLCompiler, **kw: Dict[str, Any]) -> SQLCompiler:
    return "json_arrayagg(%s)" % compiler.process(element.clauses, **kw)
