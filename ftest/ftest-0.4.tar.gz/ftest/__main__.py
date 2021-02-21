"""Main."""
# pylint: disable=no-value-for-parameter

import atexit
import os
import sys
from result import Ok, Err

import click
import toml
import inspect

import signal

from .processes import ProcessMonitor
from .lang import global_env, parse, rep, printer, Procedure
from .register import register_functions
from .supervisor import Supervisor
from .version import VERSION
from .logger import logger, Level

def is_ftest_file(file):
    """Check that file path exists and has correct extension."""
    if not os.path.isfile(file):
        return Err(f"Error: {file} doesn't exist")

    if ".ftest" not in os.path.splitext(file)[1]:
        return Err(f"Error: {file} doesn't have a .ftest extensionn")

    return Ok()


def cleanup(supervisor, monitor):
    """Cleanup."""
    if supervisor is not None:
        supervisor.stop()
    if monitor is not None:
        monitor.kill()
    os.system("rm -f *.log")


def init(config, verbose, repl_mode):
    supervisor = None
    monitor = None

    def clean(*args):
        cleanup(supervisor, monitor)
        sys.exit(0)

    signal.signal(signal.SIGINT, clean)


    """Initialize repl and run file modes."""
    with open(config) as file:
        config = toml.loads(file.read())

    config["verbose"] = verbose
    config["repl"] = repl_mode

    monitor = ProcessMonitor(config)
    monitor.launch()

    supervisor = Supervisor(config)
    global_env["supervisor"] = supervisor

    register_functions(global_env, config, monitor, supervisor)

    #atexit.register(clean)

    return config, monitor, supervisor


@click.command("run")
@click.argument("config")
@click.argument("ftest_file")
@click.option("--verbose/--noverbose", default=False, help="hides debug output")
@click.option("--debug/--nodebug", default=False, help="hides debug output")
def run(config, ftest_file, verbose, debug=False):
    """Run ftest file."""
    logger.start()
    config, monitor, supervisor = init(config, verbose, False)

    if debug:
        logger.set_level(Level.DEBUG)
    else:
        logger.set_level(Level.ERROR)

    if (result := is_ftest_file(ftest_file)).is_err():
        cleanup(supervisor, monitor)
        print(result.err())
        sys.exit(1)

    count = parse(ftest_file, config)

    cleanup(supervisor, monitor)
    sys.exit(count)


@click.command("repl")
@click.argument("config")
@click.option("--verbose/--noverbose", default=False, help="hides debug output")
def repl(config, verbose):
    """Ftest REPL mode."""
    logger.set_repl()
    config, monitor, supervisor = init(config, verbose, True)

    count = 0
    while True:
        line = input(">> ")
        result = rep(config, line)
        if result == "exit":
            print("Quiting!")
            break

        printer(config, result)
        if result is False:
            count += 1

    cleanup(supervisor, monitor)
    sys.exit(count)

@click.command("docs")
@click.argument("config")
@click.option("--verbose/--noverbose", default=False, help="hides debug output")
def docs(config, verbose=False):
    """Generate documentation for ftest function"""

    logger.stop()

    config, monitor, supervisor = init(config, verbose, True)

    keys = [key for key in global_env.keys() if not key.startswith("_")]

    print("FTest Function")
    print("====================")

    for key in keys:
        if key.startswith("builtin"):
            continue
        if isinstance(global_env[key], Procedure) or callable(global_env[key]):
            print("\\"+key)
            print("-----------------")
        if isinstance(global_env[key], Procedure):
            print(global_env[key].doc())
        elif callable(global_env[key]):
            print(inspect.getdoc(global_env[key]))

        print("")

        #print(key, type(global_env[key]))

    cleanup(supervisor, monitor)



@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, default=False)
def main(version):
    """FTest."""
    if len(sys.argv) == 1:
        print("ftest cli util.\nVersion:", VERSION, "\nFor usage see fcp --help")
    if version:
        click.echo(VERSION)


main.add_command(run)
main.add_command(repl)
main.add_command(docs)


if __name__ == "__main__":
    main()
