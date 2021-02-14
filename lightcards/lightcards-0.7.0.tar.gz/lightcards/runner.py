# Markdown flashcard utility
# Armaan Bhojwani 2021

import argparse
import curses
import pkg_resources
from random import shuffle
import sys

from . import parse, progress, config
from .display import Display
from .deck import Status


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Terminal flashcards from Markdown"
    )
    parser.add_argument(
        "-c",
        "--config",
        metavar="config_file",
        type=str,
        default="/dev/null",
        help="specify custom config file",
    )
    parser.add_argument(
        "-V",
        "--view",
        metavar="1-3",
        type=int,
        choices=range(1, 4),
        help="specify which view to start in",
    )
    parser.add_argument("inp", metavar="input_files", type=str, nargs="+")
    parser.add_argument(
        "-l",
        "--lenient",
        action="store_true",
        help="don't raise exception if tables are malformed",
    )
    parser.add_argument(
        "-t",
        "--table",
        metavar="num_table",
        type=int,
        help="specify which table to use if multiple are given",
    )
    parser.add_argument(
        "-a",
        "--alphabetize",
        action="store_true",
        help="alphabetize card order",
    )
    parser.add_argument(
        "-p",
        "--purge",
        action="store_true",
        help="delete cache before starting",
    )
    parser.add_argument(
        "-r", "--reverse", action="store_true", help="reverse card order"
    )
    parser.add_argument(
        "-s", "--shuffle", action="store_true", help="shuffle card order"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"lightcards {pkg_resources.require('lightcards')[0].version}",
    )
    return parser.parse_args()


def show(args, stack, headers, conf):
    """
    Get objects from cache, manipulate deck according to passed arguments, and
    send it to the display functions
    """
    # Purge caches if asked
    if args.purge:
        progress.purge(get_orig()[1])

    # Check for caches
    idx = Status()
    cache = progress.dive(get_orig()[1])
    if cache and conf["cache"]:
        (stack) = cache

    # Manipulate deck
    if args.shuffle or conf["shuffle"]:
        shuffle(stack)
    if args.alphabetize or conf["alphabetize"]:
        stack.sort(key=lambda x: x.front)
    if args.reverse or conf["reverse"]:
        stack.reverse()

    # Set view
    if args.view:
        view = args.view
    else:
        view = conf["default_view"]

    # Send to display
    win = Display(stack, headers, idx, view, args, conf)
    try:
        curses.wrapper(win.run)
    except curses.error as e:
        raise e


def get_orig():
    """Return original header and stack"""
    return (headers, stack)


def main(args=sys.argv):
    args = parse_args()
    conf = config.read_file(args.config)

    if not conf["debug"]:
        sys.tracebacklimit = 0

    global headers, stack
    (headers, stack) = parse.parse_html(parse.md2html(args.inp), args, conf)

    show(args, stack, headers, conf)


if __name__ == "__main__":
    main()
