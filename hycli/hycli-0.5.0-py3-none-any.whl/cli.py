import click

from hycli import extract, compare, evaluate
from hycli.commands.callbacks import print_version


@click.group()
@click.option(
    "-v",
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Print out hycli version",
)
@click.pass_context
def main(ctx):
    """
    Hypatos cli tool to batch extract documents through the API and to compare the results.
    """
    ctx.obj = {}


main.add_command(extract.extract)
main.add_command(compare.compare)
main.add_command(evaluate.evaluate)

if __name__ == "__main__":
    main()
