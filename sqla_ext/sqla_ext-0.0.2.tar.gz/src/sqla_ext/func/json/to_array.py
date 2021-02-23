from typing import Any, Dict

from sqlalchemy import func as sqla_func
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import cast
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.sql.type_api import TypeEngine


class to_array(FunctionElement):
    """JSON object creation"""

    name = "to_array"


function = to_array


@compiles(function, "postgresql")
def pg(element: function, compiler: SQLCompiler, **kw: Dict[str, Any]) -> SQLCompiler:

    args = element.clauses

    if len(args) != 2:
        raise Exception("Invalid n arguments for to_array")

    json_field, type_bind_param = args

    type_ = type_bind_param.value

    assert isinstance(type_, TypeEngine)

    select_from = sqla_func.jsonb_array_elements(cast(json_field, JSONB())).alias()
    statement = (
        select([sqla_func.array_agg(cast(select_from.column, type_))])
        .select_from(select_from)
        .scalar_subquery()
    )

    return compiler.process(statement, **kw)
