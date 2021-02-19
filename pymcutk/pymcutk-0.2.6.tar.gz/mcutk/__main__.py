import sys
import logging
import click
from mcutk import __version__


class ComplexCLI(click.MultiCommand):

    COMMANDS = [
        'build',
        'scan',
        'config',
        # 'gdbserver',
        'flash'
    ]

    def list_commands(self, ctx):
        return self.COMMANDS

    def get_command(self, ctx, name):
        if sys.version_info[0] == 2:
            name = name.encode('ascii', 'replace')
        mod = __import__('mcutk.commands.' + name, None, None, ['cli'])
        return mod.cli



@click.command(cls=ComplexCLI, invoke_without_command=True, help="mcutk command line tool")
@click.option('-v', '--verbose', is_flag=True, help='show more console message')
@click.option('--version', is_flag=True, help="show mcutk version")
def main(version=False, verbose=False, debug=False):
    if verbose:
        logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.DEBUG)
    else:
        logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.WARNING)

    if version:
        click.echo(__version__)


if __name__ == '__main__':
    main()
