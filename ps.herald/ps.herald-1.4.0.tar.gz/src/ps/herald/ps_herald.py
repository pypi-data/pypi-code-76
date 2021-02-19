import click
import shutil
import sys
from ps.basic import DEV_STAGES, Config
from ps.herald import create_app

import os


@click.command()
@click.option(
    "--extra",
    "-x",
    is_flag=True,
    type=bool,
    default=False,
    help="internal tests only",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    type=bool,
    default=False,
    help="set verbose mode",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    type=bool,
    default=False,
    help="set debug mode",
)
@click.option("--use", "-u", type=str, help="set database file to use")
def main(extra, verbose, debug, use):
    global VERBOSE, DEBUG
    VERBOSE = verbose
    DEBUG = debug
    click.echo("ps_herald. Debug mode is %s" % ("on" if debug else "off"))
    if extra:
        return 0
    if use:
        suffix = DEV_STAGES[os.environ["DEV_STAGE"]]["suffix"]
        herald_sqlite_filename = os.path.join(
            os.getcwd(), f"herald.sqlite{suffix}"
        )
        shutil.copy(f"{use}", f"{herald_sqlite_filename}")
        print(f"Copied {use} To {herald_sqlite_filename} ")
    app = create_app("ps.herald")
    app.run(host="0.0.0.0", port=Config.webserver_port)


if __name__ == "__main__":
    # execute only if run as a script
    sys.exit(main())
