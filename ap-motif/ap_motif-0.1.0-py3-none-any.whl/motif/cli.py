import click

# Pylint native python 3.3+ namespace hackery
#pylint: disable=import-error
from ap.motif import utils
#pylint: enable=import-error


@click.group()
def cli(): pass

@cli.command()
@click.argument('config_file', type=click.File('r'))
def validate(config_file):
    config = utils.load_config(config_file)
    print(config)


@cli.command()
@click.argument('config_file', type=click.File('r'))
def create(config_file): pass


if __name__ == '__main__':
    cli()
