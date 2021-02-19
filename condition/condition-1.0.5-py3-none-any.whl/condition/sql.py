from . import Condition
import os
from typing import Optional


def render_sql(
    sql_template: str, condition: Condition, dbmap: Optional[dict] = None
) -> str:
    """
    Renders a jinja2 sql template with ``dict`` from :meth:`condition.to_sql_dict`.
    Optionally overwrite field names with ``dbmap``.
    Please see also `usage examples <usage.html#sql-generation>`_.

    :param sql_template: a jinja2 sql template.
    :param condition: for generating the ``dict`` of conditions to be used in sql
    :param dbmap: optionally overwrite field names.
    :raise UndefinedError: if a variable in sql template is undefined
    """

    from jinja2 import Template, Environment, meta, StrictUndefined, UndefinedError

    kwargs = condition.to_sql_dict(dbmap)
    kwargs["env"] = os.environ

    try:
        template = Template(sql_template, undefined=StrictUndefined)
        rendered = template.render(**kwargs)
    except UndefinedError:
        reqd_vars = meta.find_undeclared_variables(
            Environment(autoescape=True).parse(sql_template)
        )
        missing_vars = set(reqd_vars).difference(kwargs.keys())
        msg = (
            "Could not render sql template. It is missing some variables. "
            f"\nPlease check this set: {missing_vars}."
        )
        # logging.exception(msg)
        raise UndefinedError(msg)
    return rendered
