"""CLI commands for bin/cmempy-cli."""

from shutil import get_terminal_size

import click

from cmem.cmemc.cli import completion
from cmem.cmemc.cli.commands import CmemcCommand, CmemcGroup
from cmem.cmempy.queries import (
    QUERY_CATALOG,
    get_query_status
)


def _get_queries_filtered_by_slower_than(time_ms):
    """Get queries filter by slower-than x ms filter.

    Args:
        time_ms (int):time in milliseconds

    Returns:
        filtered list of status reports

    Raises:
        ValueError
    """
    try:
        time_ms = int(time_ms)
    except ValueError as error:
        raise ValueError("This filter needs an integer as parameter.")\
            from error
    queries = get_query_status()
    filtered_queries = []
    for _ in queries:
        if _["executionTime"] is not None and _["executionTime"] > time_ms:
            filtered_queries.append(_)
    return filtered_queries


def _get_queries_filtered_by_status(status):
    """Get queries filter by a status.

    Args:
        status (str): one of failed, running, finished

    Returns:
        filtered list of status reports

    Raises:
        ValueError
    """
    valid_filter_values = ("running", "finished")
    if status not in valid_filter_values:
        raise ValueError(
            "This filter needs one of {} as parameter."
            .format(valid_filter_values)
        )
    queries = get_query_status()
    filtered_queries = []
    if status == "running":
        for _ in queries:
            if _["executionTime"] is None:
                filtered_queries.append(_)
    elif status == "finished":
        for _ in queries:
            if _["executionTime"] is not None:
                filtered_queries.append(_)
    return filtered_queries


def _get_queries_filtered_by_uuid(uuid):
    """Get query status by uuid.

    Args:
        uuid (str): query status uuid

    Returns:
        status dict
    """
    queries = get_query_status()
    filtered_queries = []
    for _ in queries:
        if _["id"] == uuid:
            filtered_queries.append(_)
    return filtered_queries


def _get_queries_filtered(filter_name, filter_value):
    """Get queries filtered according to filter name and value.

    Args:
        filter_name (str): one of "status" or "slower-than"
        filter_value (str): value according to filter

    Returns:
        list of filtered queries from the get_query_status API call

    Raises:
        ValueError
    """
    # filter by uuid
    if filter_name == "uuid":
        return _get_queries_filtered_by_uuid(filter_value)
    # filter by status
    if filter_name == "status":
        return _get_queries_filtered_by_status(filter_value)
    # filter by slower-than
    if filter_name == "slower-than":
        return _get_queries_filtered_by_slower_than(filter_value)
    # default is unfiltered
    return get_query_status()


def _output_query_status_details(app, status_dict):
    """Output key/value table as well as query string of a query.

    Args:
        status_dict (dict): The dict from the query status list.
    """
    table = []
    for key in status_dict.keys():
        if key != "queryString":
            row = [
                key,
                str(status_dict[key])
            ]
            table.append(row)
    app.echo_info_table(
        table,
        headers=["Key", "Value"]
    )
    app.echo_info("")
    app.echo_info_sparql(status_dict["queryString"])


@click.command(cls=CmemcCommand, name="list")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only query identifier and no labels or other meta data. "
         "This is useful for piping the ids into other cmemc commands."
)
@click.pass_obj
def list_command(app, id_only):
    """List available queries from the catalog.

    Outputs a list of query URIs which can be used as reference for
    the query execute command.
    """
    queries = QUERY_CATALOG.get_queries().items()
    if id_only:
        # sort dict by short_url - https://docs.python.org/3/howto/sorting.html
        for _, sparql_query in sorted(
                queries, key=lambda k: k[1].short_url.lower()
        ):
            app.echo_info(
                sparql_query.short_url
            )
    else:
        table = []
        for _, sparql_query in queries:
            row = [
                sparql_query.short_url,
                sparql_query.query_type,
                ','.join(sparql_query.get_placeholder_keys()),
                sparql_query.label
            ]
            table.append(row)
        # sort output by label - https://docs.python.org/3/howto/sorting.html
        table = sorted(table, key=lambda k: k[3].lower())
        app.echo_info_table(
            table,
            headers=["Query URI", "Type", "Placeholder", "Label"]
        )


# pylint: disable-msg=too-many-locals,too-many-arguments
@click.command(cls=CmemcCommand, name="execute")
@click.argument(
    "QUERIES",
    nargs=-1,
    required=True,
    autocompletion=completion.remote_queries_and_sparql_files
)
@click.option(
    "--accept",
    default="default",
    show_default=True,
    help="Accept header for the HTTP request(s). Setting this to 'default' "
         "means that cmemc uses an appropriate accept header for terminal "
         "output (text/csv for tables, text/turtle for graphs, * otherwise). "
         "Please refer to the Corporate Memory system manual for a list "
         "of accepted mime types."
)
@click.option(
    "--no-imports",
    is_flag=True,
    help="Graphs which include other graphs (using owl:imports) will be "
         "queried as merged overall-graph. This flag disables this "
         "default behaviour. The flag has no effect on update queries."
)
@click.option(
    "--base64",
    is_flag=True,
    help="Enables base64 encoding of the query parameter for the "
         "SPARQL requests (the response is not touched). "
         "This can be useful in case there is an aggressive firewall between "
         "cmemc and Corporate Memory."
)
@click.option(
    "--parameter", "-p",
    type=(str, str),
    autocompletion=completion.placeholder,
    multiple=True,
    help="In case of a parameterized query (placeholders with the '{{key}}' "
         "syntax), this option fills all placeholder with a given value "
         "before the query is executed."
         "Pairs of placeholder/value need to be given as a tuple 'KEY VALUE'. "
         "A key can be used only once."
)
@click.option(
    "--limit",
    type=int,
    help="Override or set the LIMIT in the executed SELECT query. Note that "
         "this option will never give you more results than the LIMIT given "
         "in the query itself."
)
@click.option(
    "--offset",
    type=int,
    help="Override or set the OFFSET in the executed SELECT query."
)
@click.option(
    "--distinct",
    is_flag=True,
    help="Override the SELECT query by make the result set DISTINCT."
)
@click.option(
    "--timeout",
    type=int,
    help="Set max execution time for query evaluation (in milliseconds)."
)
@click.pass_obj
def execute_command(
        app, queries, accept, no_imports, base64, parameter,
        limit, offset, distinct, timeout
):
    """Execute queries which are loaded from files or the query catalog.

    Queries are identified either by a file path, an URI from the query
    catalog, or a shortened URI (qname, using a default namespace).

    If multiple queries are executed one after the other, the first failing
    query stops the whole execution chain.

    Limitations: All optional parameters (e.g. accept, base64, ...) are
    provided for ALL queries in an execution chain. If you need different
    parameters for each query in a chain, run cmemc multiple times and use
    the logical operators && and || of your shell instead.
    """
    # pylint: disable=too-many-arguments
    placeholder = dict()
    for key, value in parameter:
        if key in placeholder:
            raise ValueError(
                "Parameter can be given only once, "
                "Value for '{}' was given twice.".format(key)
            )
        placeholder[key] = value
    app.echo_debug("Parameter: " + str(placeholder))
    for file_or_uri in queries:
        executed_query = QUERY_CATALOG.get_query(file_or_uri)
        if executed_query is None:
            raise ValueError(
                "{} is neither a (readable) file nor a query URI."
                .format(file_or_uri)
            )
        app.echo_debug("Execute ({}): {} < {}"
                       .format(executed_query.query_type,
                               executed_query.label,
                               executed_query.url)
                       )
        if accept == "default":
            submitted_accept = executed_query.get_default_accept_header()
            app.echo_debug(
                "Accept header set to default value: '{}'"
                .format(submitted_accept)
            )
        else:
            submitted_accept = accept

        results = executed_query.get_results(
            accept=submitted_accept,
            owl_imports_resolution=not no_imports,
            base64_encoded=base64,
            placeholder=placeholder,
            distinct=distinct,
            limit=limit,
            offset=offset,
            timeout=timeout
        )
        app.echo_result(results)


@click.command(cls=CmemcCommand, name="open")
@click.argument(
    "QUERIES",
    nargs=-1,
    required=True,
    autocompletion=completion.remote_queries_and_sparql_files
)
@click.pass_obj
def open_command(app, queries):
    """Open queries in the editor of the query catalog in your browser.

    With this command, you can open (remote) queries from the query catalog in
    the query editor in your browser (e.g. in order to change them).
    You can also load local query files into the query editor, in order to
    import them into the query catalog.

    The command accepts multiple query URIs or files which results in
    opening multiple browser tabs.
    """
    for file_or_uri in queries:
        opened_query = QUERY_CATALOG.get_query(file_or_uri)
        if opened_query is None:
            raise ValueError(
                "{} is neither a (readable) file nor a query URI."
                .format(file_or_uri)
            )
        open_query_uri = opened_query.get_editor_url()
        app.echo_debug("Open {}: {}".format(file_or_uri, open_query_uri))
        click.launch(open_query_uri)


@click.command(cls=CmemcCommand, name="status")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only query identifier and no labels or other meta data. "
         "This is useful for piping the ids into other cmemc commands."
)
@click.option(
    "--raw",
    is_flag=True,
    help="Outputs raw JSON response of the query status API."
)
@click.option(
    "--filter", "filter_",
    type=click.Tuple([
        click.Choice(["status", "slower-than"]),
        str
    ]),
    autocompletion=completion.query_status_filter,
    default=[None] * 2,
    help="Filter queries based on execution status and time. "
         "First parameter CHOICE can be 'status' or 'slower-than'. "
         "The second parameter has to be a status  in case "
         "of 'status' or a time in miliseconds in case "
         "of 'slower-than' filter."
)
@click.argument(
    "query_uuid",
    required=False,
    type=click.STRING
)
@click.pass_obj
def status_command(app, id_only, raw, filter_, query_uuid):
    """Get status information of executed and running queries.

    With this command, you can access the latest executed SPARQL queries
    on the DataPlatform. These queries are identified by UUIDs and listed
    ordered by starting timestamp.

    You can filter queries based on status and runtime in order to investigate
    slow queries. In addition to that, you can get the details of a specific
    query by using the UUID as a parameter.

    Known Issue: Timeouted queries are currently shown as running queries
    (means: they have no runtime and no ending timestamp).
    This will be fixed in a future release.
    """
    width, height = get_terminal_size((120, 20))
    max_query_string_width = width - 46 - 1
    app.echo_debug("Terminal size = {} x {}".format(width, height))

    if query_uuid:
        queries = _get_queries_filtered("uuid", query_uuid)
    else:
        filter_name, filter_value = filter_
        queries = _get_queries_filtered(filter_name, filter_value)
    if raw:
        app.echo_info_json(queries)
        return
    if id_only:
        for _ in queries:
            app.echo_info(_["id"])
        return
    if len(queries) == 1 and query_uuid:
        _output_query_status_details(app, queries[0])
        return
    table = []
    for _ in queries:
        query_string = " ".join(_["queryString"].splitlines())
        if len(query_string) > max_query_string_width:
            query_string = query_string[0:max_query_string_width] + "…"
        row = [
            _["id"],
            _["executionTime"],
            query_string
        ]
        table.append(row)
    app.echo_info_table(
        table,
        headers=["Query ID", "Time", "Query String"]
    )


@click.group(cls=CmemcGroup)
def query():
    """List, execute or open local and remote SPARQL queries.

    Queries are identified either by a file path, an URI from the query
    catalog or a shortened URI (qname, using a default namespace).

    In order to get a list of queries from the query catalog, use the list
    command. One or more queries can be executed one after the other with the
    execute command. With open command you can jump to the query editor in your
    browser.

    Queries can use a mustache like syntax to specify placeholder for
    parameter values (e.g. {{resourceUri}}). These parameter values need to
    be given as well, before the query can be executed (use the -p option).
    """


query.add_command(execute_command)
query.add_command(list_command)
query.add_command(open_command)
query.add_command(status_command)
