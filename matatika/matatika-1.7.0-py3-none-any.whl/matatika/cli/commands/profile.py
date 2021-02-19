"""CLI 'profile' command"""

import click
from matatika.cli.utility import create_table, Resolver
from .root import matatika


@matatika.command('profile', short_help='Return the authenticated user profile')
@click.pass_context
def profile(ctx):
    """Returns the authenticated user profile"""

    client = Resolver(ctx).client(workspace_id=None)
    profile_ = client.profile()

    table = create_table(
        ['ID', 'NAME'], [profile_['id'], profile_['name']],
        separator="\t-->\t")
    click.secho(table)
