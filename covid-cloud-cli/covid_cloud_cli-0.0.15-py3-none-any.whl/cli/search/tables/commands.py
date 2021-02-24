from covid_cloud.client import *


@click.group()
@click.pass_context
def tables(ctx):
    pass


@tables.command(name="list")
@click.pass_context
def list_tables(ctx):
    click.echo(search_client.get_tables(ctx.obj['search-url'], ctx.obj.get('oauth_token', None)))


@tables.command()
@click.pass_context
@click.argument('table_name')
def get(ctx, table_name):
    click.echo(search_client.get_table(ctx.obj['search-url'], table_name, ctx.obj.get('oauth_token', None)))
