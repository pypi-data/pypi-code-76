# from pprint import pformat
from os.path import join
import typer
from typing import List
from pathlib import Path
from core import ensure_dirs, __version__
from cli.constants import filter_file_default_content
from cli.utils import new_definition_template, cli_run_definition
from core.errors import TemplateDoesNotExistError
from conf import config

app = typer.Typer()


@app.command()
def dump_config():
    print(f"|> path.templates:\t {config.path.templates}")
    print(f"|> path.snapshots:\t {config.path.snapshots}")
    print(f"|> path.definitions:\t {config.path.definitions}")
    print(f"|> path.filters:\t {config.path.filters}")


@app.command()
def init():
    """
    Creates the .init folder to keep stuff
    """
    print(":: sigla init")
    print(f":: - checking/creating folder {config.path.templates}")
    print(f":: - checking/creating folder {config.path.snapshots}")
    print(f":: - checking/creating folder {config.path.definitions}")
    ensure_dirs(
        config.path.templates,
        config.path.snapshots,
        config.path.definitions,
    )

    filter_file = config.path.filters
    print(f":: - checking/creating file {filter_file}")
    # create file if it does not exist
    if Path(filter_file).exists():
        return
    with open(filter_file, "w") as h:
        h.write(filter_file_default_content)


@app.command()
def new(name: str):
    """
    Generate a new definition for a generator.
    """
    print(f":: creating new definition: {name}")
    destination_folder = config.path.definitions
    destination = join(destination_folder, name + ".xml")
    p = Path(destination)
    if p.exists():
        raise typer.Exit("✋ This definition already exists")

    content = new_definition_template(name)
    p.write_text(content)


@app.command()
def run(references: List[str]):
    """
    Run a generator
    """
    for reference in references:
        glob = Path(config.path.definitions).glob(f"{reference}.xml")

        c = 0
        for p in glob:
            c += 1
            if not p.exists():
                raise typer.Exit(f"✋ The definition(s) do not exists {p}")

            if p.is_dir():
                continue

            try:
                cli_run_definition(p)
            except TemplateDoesNotExistError as e:
                print("|> e", e)
                raise Exception()
                raise typer.Exit(e)

        if c == 0:
            print(f"✋ No definition(s) found for {references}")


@app.command()
def version():
    """
    Print the version
    """
    print(f"Version: {__version__}")


if __name__ == "__main__":
    app()

# # @click.option("--debug/--no-debug", default=False)
# # click.echo('Debug mode is %s' % ('on' if debug else 'off'))
# @click.group()
# @pass_config
# def cli(conf: Config):
#     print("=== core ===")
#     conf.load()
#     print(f":: conf\n{pformat(conf, indent=1)}")
#     print("")
#     conf.save()


# @cli.command()
# @click.argument("files", nargs=-1, type=click.Path(exists=True))
# def snapshot(files):
#     """
#     Makes snapshots
#     """
#     for file in files:
#         cli_make_snapshots(cli_read_snapshot_definition(file))


# @cli.command()
# @click.argument("files", nargs=-1, type=click.Path(exists=True))
# def verify(files):
#     """
#     Verify snapshots
#     """
#     for file in files:
#         cli_verify_snapshots(cli_read_snapshot_definition(file))

