#!/usr/bin/env python3

import argparse
import json
import sys
from difflib import unified_diff
from pathlib import Path
from typing import List, Optional, Union

from more_itertools import always_iterable
from rich import print as rprint
from schema import Or, Schema

from apply_subs import __version__

SUBS_SCHEMA = Schema({str: Or(str, list)})


def print_err(message: str) -> None:
    rprint(f"[bold white on red]Error[/] {message}", file=sys.stderr)


def _sub(to_replace: Union[str, List[str]], new: str, content: str) -> str:
    for old in always_iterable(to_replace):
        content = content.replace(old, new)
    return content


def colored_diff(diff):
    # this is adapted from
    # https://chezsoi.org/lucas/blog/colored-diff-output-with-python.html

    for line in diff:
        if line.startswith("+"):
            yield f"[green]{line}[/green]"
        elif line.startswith("-"):
            yield f"[red]{line}[/red]"
        else:
            yield line


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="*", help="target text file(s)")
    parser.add_argument(
        "-s",
        "--subs",
        action="store",
        default=None,
        help="json file describing substitutions to apply (order matters).",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--inplace", action="store_true")
    group.add_argument("-d", "--diff", action="store_true", help="print a diff.")
    group.add_argument(
        "-cd",
        "--cd",
        "--cdiff",
        "--colored-diff",
        dest="colored_diff",
        action="store_true",
        help="print a colored diff.",
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="print apply-subs version."
    )

    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        return 0

    if not args.target:
        print_err("no target file provided.")
        parser.print_help(file=sys.stderr)
        return 1

    if args.subs is None:
        print_err("`--subs/-s` flag is mandatory.")
        parser.print_help(file=sys.stderr)
        return 1

    try:
        with open(args.subs, "r") as fh:
            subs = json.load(fh)
    except FileNotFoundError:
        print_err(f"{args.subs} not found.")
        return 1
    except json.decoder.JSONDecodeError:
        print_err(f"invalid json file `{args.subs}`")
        return 1

    if not SUBS_SCHEMA.is_valid(subs):
        print_err("unrecognized json schema.")
        return 1

    for target in args.target:
        if not Path(target).is_file():
            print_err(f"{target} not found.")
            return 1
        with open(target, "r") as fh:
            new_content = fh.read()

        for new, old in subs.items():
            new_content = _sub(old, new, new_content)

        if args.inplace:
            with open(target, "w") as fh:
                fh.write(new_content)
        elif args.diff or args.colored_diff:
            s1 = open(target).read().splitlines(keepends=True)
            s2 = new_content.splitlines(keepends=True)
            diff = unified_diff(s1, s2, fromfile=target, tofile=f"{target} (patched)")
            if args.colored_diff:
                diff = colored_diff(diff)
            toprint = "".join(list(diff))
            if toprint:
                rprint(toprint)
        else:
            rprint(new_content, end="")
    return 0
