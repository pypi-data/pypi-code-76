import os
import sys
import platform
import argparse
import logging
import subprocess

from .settings import DPC_REPOS, DPC_ROOTS


OS_NAME = platform.system().lower()
DPC_DEFAULT_ROOT = DPC_ROOTS.get(OS_NAME)
DPC_CLIENT = os.environ.get("DPC_CLIENT")

if not DPC_CLIENT:
    logging.warning("Environment var `DPC_CLIENT` is not set? " \
    "Try to load form default location: %s", DPC_DEFAULT_ROOT)
    DPC_CLIENT = os.path.join(DPC_DEFAULT_ROOT, "stationscript")


def dpc_main():
    parser = argparse.ArgumentParser(prog="dpc")
    subparsers = parser.add_subparsers(title='sub commands', dest='command', metavar="")
    parser_a = subparsers.add_parser('init', help='install and init Dapeng Client')
    parser_a.add_argument("-path", default=None, help="The path of new client to install.")
    parser_a.add_argument("-f", "--force", default=None, help="Force to install and init new client.")
    args = parser.parse_args()
    if args.command == "init":
        install(args.path)


def clone_repo(url, cwd):
    clone_cmd = "git clone --depth 30 --branch master {}".format(url)
    try:
        subprocess.check_call(clone_cmd, cwd=cwd)
    except subprocess.CalledProcessError:
        pass


def install(root=None):
    if not root:
        root = DPC_DEFAULT_ROOT

    if not os.path.exists(root):
        os.makedirs(root)

    for name, url in DPC_REPOS.items():
        print("%s %s" % (name, url))
        clone_repo(url, root)

    os.environ["DPC_CLIENT"] = os.path.join(root, "stationscript")
    subprocess.check_call("dpc init")
    subprocess.check_call("dpc install staf")
    subprocess.check_call("dpc install armgcc")


main = dpc_main
try:
    sys.path.append(DPC_CLIENT)
    from core.__main__ import main
except ImportError:
    logging.debug("Use main from dpc")


if __name__ == '__main__':
    main()
