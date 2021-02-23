from typing import Any, Dict

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import JSON


class build_object(FunctionElement):
    """JSON object creation"""

    type = JSON()
    name = "jsonb_build_object"


@compiles(build_object, "postgresql")
def pg_build_object(
    element: build_object, compiler: SQLCompiler, **kw: Dict[str, Any]
) -> SQLCompiler:
    return "jsonb_build_object(%s)" % compiler.process(element.clauses, **kw)


@compiles(build_object, "sqlite")
@compiles(build_object, "mysql")
def other_build_object(
    element: build_object, compiler: SQLCompiler, **kw: Dict[str, Any]
) -> SQLCompiler:
    return "json_object(%s)" % compiler.process(element.clauses, **kw)
