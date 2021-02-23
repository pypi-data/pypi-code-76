import click
import yaml
import json

from client.constants import *


class ConfigHelp(click.Command):
    def format_help(self, ctx, formatter):
        click.echo("Usage: covid-cloud config [OPTIONS] KEY VALUE")
        click.echo("Options:")
        click.echo(" --help  Show this message and exit.")
        click.echo("Accepted Keys: ")
        click.echo("\tsearch-url")
        click.echo("\tdrs-url")


@click.command(cls=ConfigHelp)
@click.pass_context
@click.argument("key")
@click.argument("value", required=False, default=None)
def config(ctx, key, value):
    if key == 'list' and not value:
        click.echo(json.dumps(ctx.obj, indent=4))
        return

    ctx.obj[key] = value

    with open(config_file_path, 'w') as config_file:
        yaml.dump(ctx.obj, config_file)

    click.echo(json.dumps(ctx.obj, indent=4))
