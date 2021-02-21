import json
import string
import tempfile
import time

import jsonpyth

from .. import procfile, procrec, procret, proctree, utility
from . import CommandError


__all__ = 'run',


def run(
    procfile_list,
    output_file,
    delimiter=None,
    indent=None,
    query=None,
    sql_query=None,
    environment=None,
):
    readers = {k: v for k, v in procfile.registry.items() if k in procfile_list}
    forest = proctree.Forest(readers)
    result = forest.get_roots()

    if environment:
        evaluated = utility.evaluate(environment)
        query = string.Template(query or '').safe_substitute(evaluated)
        sql_query = string.Template(sql_query or '').safe_substitute(evaluated)

    if query:
        try:
            result = jsonpyth.jsonpath(result, query, always_return_list=True)
        except jsonpyth.JsonPathSyntaxError as ex:
            raise CommandError(f'JSONPath error: {ex}') from ex

    if sql_query:
        with tempfile.NamedTemporaryFile() as f:
            with procrec.SqliteStorage(f.name, procfile_list, utility.get_meta()) as store:
                store.record(time.time(), proctree.flatten(result, procfile_list))
                try:
                    result = procret.query(f.name, procret.Query(sql_query, None))
                except procret.QueryError as ex:
                    raise CommandError(f'SQL error: {ex}') from ex

    if delimiter:
        result = delimiter.join(map(str, result))
    else:
        result = json.dumps(result, indent=indent, sort_keys=True, ensure_ascii=False)

    output_file.write(result)
    output_file.write('\n')
