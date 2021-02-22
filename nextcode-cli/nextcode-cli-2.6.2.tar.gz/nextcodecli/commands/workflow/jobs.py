#!/usr/bin/env python

import click
from click import command, option, pass_context
from tabulate import tabulate

from nextcode.exceptions import ServerError

from nextcodecli.commands.workflow import status_to_color
from nextcodecli.utils import get_logger, abort, dumps

log = get_logger()


@command(help="List jobs")
@option('--mine', 'is_mine', is_flag=True, help='List jobs from me')
@option('-u', '--user', 'user_name', help='User to filter for')
@option('-s', '--status', 'status', default=None, help='Filter status')
@option('-p', '--project', 'project', default=None, help='Filter by project name')
@option('--pipeline', 'pipeline', default=None, help='Filter by pipeline name')
@option('--page', 'is_page', is_flag=True, help='Page results')
@option('--running', 'is_running', is_flag=True, help='Only show jobs in pending/running state')
@option('--context', help='Filter by context')
@option(
    '--completed',
    'is_completed',
    is_flag=True,
    help='Only show jobs in failed/cancelled/completed state',
)
@option('-n', '--num', default=20, help='Maximum number of jobs to return')
@option(
    '-o',
    '--output',
    type=click.Choice(['normal', 'wide', 'json']),
    default='normal',
    help='Format output',
)
@option('--raw', 'is_raw', is_flag=True, help='Dump raw json for further processing')
@pass_context
def jobs(
    ctx,
    is_mine,
    user_name,
    status,
    project,
    pipeline,
    is_page,
    is_running,
    context,
    is_completed,
    num,
    output,
    is_raw,
):
    svc = ctx.obj.service
    if is_mine:
        try:
            user_name = svc.current_user['email']
        except KeyError:
            abort("You appear not to be logged in")

    state = None
    if is_running:
        state = "running"
    elif is_completed:
        state = "completed"
    try:
        jobs = svc.get_jobs(
            user_name,
            status,
            project=project,
            pipeline=pipeline,
            limit=num,
            state=state,
            context=context,
        )
    except ServerError as e:
        abort(str(e))
    is_wide = output == 'wide'
    if is_raw or (output == 'json'):
        click.echo(dumps(jobs))
        return

    fields = [
        'job_id',
        'pipeline_name',
        'user_name',
        'project_name',
        'submit_date',
        'duration',
        'status',
    ]
    if is_wide:
        fields.extend(['desc', 'context', 'complete_date', 'pod', '#proc'])
    jobs_list = []
    for job in jobs:
        job_list = []
        for f in fields:
            v = None
            if hasattr(job, f):
                v = getattr(job, f) or 'N/A'
            if f in ('submit_date', 'complete_date'):
                try:
                    v = v.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    v = ''
            elif f == 'status':
                col = status_to_color.get(v)
                v = click.style(v, fg=col, bold=True)
            elif f == 'pod':
                v = job.details.get('pod_name', v)
            elif f == '#proc':
                v = sum(job.details.get('process_stats', {}).values())
            elif f == 'desc':
                v = job.description or ""
                if len(v) > 50:
                    v = v[:47] + "..."
            job_list.append(v)

        jobs_list.append(job_list)
    tbl = tabulate(jobs_list, headers=fields)
    if len(jobs_list) > 30 and is_page:
        click.echo_via_pager(tbl)
    else:
        click.echo(tbl)
