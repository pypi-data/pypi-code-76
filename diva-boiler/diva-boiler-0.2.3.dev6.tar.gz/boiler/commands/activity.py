import click

from boiler import cli
from boiler.commands.utils import exit_with, handle_request_error
from boiler.definitions import all_activity_codes


@click.group(name='activity', short_help='get information about activities')
@click.pass_obj
def activity(ctx):
    pass


@activity.command(name='list-types', help='list known activities')
@click.option('--count', '-c', is_flag=True, help='print the number of activity types')
def list_activities(count):
    if count:
        click.echo(len(all_activity_codes.values()))
    else:
        for activity_type in sorted(str(t.value) for t in all_activity_codes.values()):
            click.echo(activity_type)


@activity.command(name='list', help='list activities for video')
@click.option('--video-id', required=True)
@click.pass_obj
def list_video_activities(ctx, video_id):
    r = ctx['session'].get(f'video/{video_id}/activities')
    exit_with(handle_request_error(r))


@activity.command(name='count', short_help='get the number of activities by type')
@click.argument('output', type=click.File('wb'), default='-')
@click.pass_obj
def get_activity_count(ctx, output):
    """
    Get a summary of annotated activities grouped by phase.  By default,
    this will print to the terminal.  Add a path argument to write to
    a file.
    """
    r = ctx['session'].get('activity/summary')
    output.write(r.content)


cli.add_command(activity)
