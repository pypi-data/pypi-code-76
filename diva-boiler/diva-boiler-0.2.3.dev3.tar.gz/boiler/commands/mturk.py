import locale
from typing import NamedTuple, Tuple

import click
from requests import Session
from tabulate import tabulate

from boiler import cli

locale.setlocale(locale.LC_ALL, '')


class CostStatistics(NamedTuple):
    count: int  # type: ignore
    total: float
    p50: float
    p90: float
    p95: float
    p99: float
    average: float


def mturk_costs(session: Session) -> Tuple[CostStatistics, CostStatistics]:
    resp = session.get('mturk/cost')
    obj = resp.json()
    video = CostStatistics(**obj['video'])
    activity = CostStatistics(**obj['activity'])
    return video, activity


def mturk_balance(session: Session) -> float:
    resp = session.get('mturk/balance')
    if not resp.ok:
        click.secho('Could not get mechanical turk balance.', fg='red')
        return 0
    return resp.json()


@click.group(name='mturk', short_help='Get information about HITs on mechanical turk')
def mturk():
    pass


@mturk.command(help='Get the available balance in our account')
@click.pass_obj
def balance(ctx):
    b = mturk_balance(ctx['session'])
    click.echo(locale.format('%.2f', b, grouping=True))


@mturk.command(help='Get historical costs from previous HITs')
@click.pass_obj
def costs(ctx):
    v, a = mturk_costs(ctx['session'])
    click.echo(locale.format_string('Number of videos: %i', v.count))
    click.echo('\nCosts per video\n' + '-' * 15)
    table = [
        ('Average:', '$' + locale.format('%.2f', v.average, grouping=True)),
        ('Median:', '$' + locale.format('%.2f', v.p50, grouping=True)),
        ('95th percentile:', '$' + locale.format('%.2f', v.p95, grouping=True)),
        ('Total:', '$' + locale.format('%.2f', v.total, grouping=True)),
    ]
    click.echo(tabulate(table, tablefmt='plain', colalign=('left', 'right')))
    click.echo('')
    click.echo(locale.format_string('Number of activities: %i', a.count))
    click.echo('\nCosts per activity\n' + '-' * 18)
    table = [
        ('Average:', '$' + locale.format('%.2f', a.average, grouping=True)),
        ('Median:', '$' + locale.format('%.2f', a.p50, grouping=True)),
        ('95th percentile:', '$' + locale.format('%.2f', a.p95, grouping=True)),
        ('Total:', '$' + locale.format('%.2f', a.total, grouping=True)),
    ]
    click.echo(tabulate(table, tablefmt='plain', colalign=('left', 'right')))


cli.add_command(mturk)
