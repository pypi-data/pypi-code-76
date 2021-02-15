import urllib3
import click
import os
from sys import argv

from cli.commands import product
from cli.commands import component
from cli.commands import releaseNote
from cli.commands import config
from cli.commands import changelog

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@click.group(help="Atlassian CLI")
@click.option('--skipssl/--no-skipssl', required=False, default=False, help="Skips ssl validation in case you have certificates issues (not recommended)")
@click.option('--bitbucket-url', required=True, default="", help="Bitbucket URL")
@click.option('--jira-url', required=True, default="", help="Jira URL")
@click.option('--confluence-url', required=True, default="", help="Confluence URL")
@click.option('--username', required=True, default="", help="Username to use for accessing Atlassian products")
@click.option('--password', required=True, default="", help="Password to use for accessing Atlassian products")
@click.pass_context
def cli(ctx, skipssl, bitbucket_url, jira_url, confluence_url, username, password):
    ctx.ensure_object(dict)
    ctx.obj['skipssl'] = not skipssl
    ctx.obj['bitbucket_url'] = bitbucket_url.strip()
    ctx.obj['jira_url'] = jira_url.strip()
    ctx.obj['confluence_url'] = confluence_url.strip()
    ctx.obj['username'] = username.strip()
    ctx.obj['password'] = password.strip()
    pass


@cli.command()
def version():
    """App version"""
    print("app version here")


cli.add_command(changelog)
cli.add_command(config)
cli.add_command(releaseNote)
cli.add_command(product)
cli.add_command(component)

if __name__ == '__main__':
    cli()
