from .importer import main_importer, inner_importer

import argparse
from .core import JobManager
import logging as lg
import os
import shutil
from colorama import Fore
from .pogmake_execeptions import NoJobError

orig_dir = os.path.abspath(os.path.dirname(__file__))

def print_hidden_debug():
    pass


parser = argparse.ArgumentParser(description=("Registers and executes jobs"))

parser.add_argument("--print-hidden-debug", action="store_true", help=argparse.SUPPRESS)

parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Overrides logging level to DEBUG",
)

parser.add_argument(
    "--explain-depth",
    default=None,
    help="Show detailed debug information regarding a specific job",
)

parser.add_argument(
    "-e",
    "--explain",
    default=None,
    help="Show detailed debug information regarding a specific job",
)

parser.add_argument(
    "--init",
    action="store_true",
    help="Creates a default pogfile in the starting location.",
)

parser.add_argument(
    "-s",
    "--start_dir",
    default="./",
    help="This flag will cause pogmake to run in an alternate start location. As if that directory was the root directory.",
)

loglevels = {
    "DEBUG": lg.DEBUG,
    "INFO": lg.INFO,
    "WARNING": lg.WARNING,
}

parser.add_argument(
    "--log-level",
    default="INFO",
    choices=loglevels.keys(),
    help="Sets the logging level for the program's run. (gets overriden by --verbose)",
)

parser.add_argument(
    "jobs",
    nargs="*",
    default=["__ALL_JOBS__"],
    type=str,
    help="Jobs to run, defaults to all",
)

parser.add_argument(
    "-l", "--list-jobs", action="store_true", help="List all jobs available"
)

def log_setup(args):
    lg.basicConfig(level=loglevels[args.log_level])
    lg.info(f"Logging level set to: {args.log_level}")

def create_manager(args):

    args.start_dir = os.path.abspath(args.start_dir)
    dirpath = args.start_dir

    if not os.path.isdir(dirpath):
        dirpath = os.path.dirname(args.start_dir)

    lg.debug(f"Starting at path: {dirpath}.")

    gjobs = main_importer(dirpath, args)
    if len(gjobs.keys()) == 0:
        lg.error(f"{Fore.RED}: No jobs found in the root folder or any subfolders")
        raise NoJobError
    manager = JobManager(gjobs)
    
    return manager

def main():

    args = parser.parse_args()

    manager = create_manager(args)

    if args.explain:
        manager.show_detailed_info(args.explain)
        return

    if args.print_hidden_debug:
        print_debug()

    if args.list_jobs:
        manager.show_jobs()
        return

    manager.queue_jobs(args.jobs)
    manager.run_jobs()


def gmain():
    """
    This is the gui version of the pogmake frontend

    Not available yet.
    """
    pass
