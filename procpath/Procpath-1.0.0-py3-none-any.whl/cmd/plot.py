import itertools
from datetime import datetime

from .. import plotting, procret
from . import CommandError


__all__ = 'run',


def _get_file_queries(filenames: list):
    for filename in filenames:
        with open(filename, 'r') as f:
            yield procret.Query(f.read(), 'Custom query')


def _get_expr_queries(exprs: list):
    for expr in exprs:
        yield procret.create_query(expr, 'Custom expression')


def _get_named_queries(names: list):
    for query_name in names:
        try:
            query = procret.registry[query_name]
        except KeyError:
            raise CommandError(f'Unknown query {query_name}')
        else:
            yield query


def _get_pid_series_points(
    timeseries: list,
    epsilon: float = None,
    moving_average_window: int = None,
) -> dict:
    pid_series = {}
    for pid, series in itertools.groupby(timeseries, lambda r: r['pid']):
        pid_series[pid] = [(r['ts'], r['value']) for r in series]
        if epsilon:
            pid_series[pid] = plotting.decimate(pid_series[pid], epsilon)
        if moving_average_window:
            x, y = zip(*pid_series[pid])
            pid_series[pid] = list(zip(
                plotting.moving_average(x, moving_average_window),
                plotting.moving_average(y, moving_average_window),
            ))

    return pid_series


def run(
    database_file: str,
    plot_file: str,
    query_name_list: list = None,
    after: datetime = None,
    before: datetime = None,
    pid_list: list = None,
    epsilon: float = None,
    moving_average_window: int = None,
    logarithmic: bool = False,
    style: str = None,
    formatter: str = None,
    title: str = None,
    custom_query_file_list: list = None,
    custom_value_expr_list: list = None,
):
    queries = []
    if query_name_list:
        queries.extend(_get_named_queries(query_name_list))
    if custom_value_expr_list:
        queries.extend(_get_expr_queries(custom_value_expr_list))
    if custom_query_file_list:
        queries.extend(_get_file_queries(custom_query_file_list))

    if not (0 < len(queries) <= 2):
        raise CommandError('No or more than 2 queries to plot')

    for i, query in enumerate(queries):
        if title:
            queries[i] = query._replace(title=title)
        elif len(queries) > 1:
            queries[i] = query._replace(title=f'{queries[0].title} vs {queries[1].title}')

    pid_series_list = []
    for query in queries:
        timeseries = procret.query(database_file, query, after, before, pid_list)
        pid_series_list.append(_get_pid_series_points(timeseries, epsilon, moving_average_window))

    plotting.plot(
        plot_file=plot_file,
        title=queries[0].title,
        pid_series1=pid_series_list[0],
        pid_series2=pid_series_list[1] if len(pid_series_list) > 1 else None,
        logarithmic=logarithmic,
        style=style,
        formatter=formatter,
    )
