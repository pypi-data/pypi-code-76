import logging

import click
import click_log

from .packs import install as pack_install

logger = logging.getLogger("njinn")
click_log.basic_config(logger)


@click.group()
def cli():
    pass


@cli.group()
def pack():
    pass


@pack.command()
@click.argument("repository_url")
@click_log.simple_verbosity_option(logger)
@click.option(
    "--branch",
    default="master",
    show_default=True,
    help="A branch from which the repository should be cloned.",
)
@click.option(
    "-u", "--username", "username", help="Username (Email Address) in Njinn API."
)
@click.option("-p", "--password", "password", help="Password for user in Njinn API.")
@click.option("-a", "--api", "api", help="Njinn API url.")
@click.option("-n", "--namespace", "namespace", help="Namespace for pack installation.")
def install(repository_url, branch, username, password, api, namespace):
    logger.info("Installing pack from %s" % repository_url)
    pack_install(repository_url, branch, username, password, api, namespace)


if __name__ == "__main__":
    cli()
