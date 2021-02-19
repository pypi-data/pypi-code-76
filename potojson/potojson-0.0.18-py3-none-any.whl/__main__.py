#!/usr/bin/env python

"""potojson command line interface."""

import argparse
import sys

from potojson import __description__, __version__, pofile_to_json


def build_parser():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s " + __version__,
        help="Show program version number and exit.",
    )
    parser.add_argument(
        "po_filepath_or_content",
        nargs="*",
        metavar="PO_FILEPATH_OR_CONTENT",
        help="Path to pofile or pofile content as string."
        " If not provided, will be read from STDIN.",
    )
    parser.add_argument(
        "-m",
        "--fallback-to-msgid",
        dest="fallback_to_msgid",
        action="store_true",
        help="Use msgid if translation is missing.",
    )
    parser.add_argument(
        "-f",
        "--fuzzy",
        dest="fuzzy",
        action="store_true",
        help="Include fuzzy messages.",
    )
    parser.add_argument(
        "-p",
        "--pretty",
        dest="pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )
    parser.add_argument(
        "-i",
        "--indent",
        dest="indent",
        help="Number of spaces for indentation used pretty-printing JSON"
        ' output. Only takes effect passing the "--pretty" option.',
        metavar="N",
        type=int,
    )
    parser.add_argument(
        "-l",
        "--language",
        dest="language",
        default=None,
        help="Language for the translations. Will be inserted in the empty key"
        " of the JSON output. If not provided and the passed pofile includes"
        ' the "Language" header, will be extracted from it.',
    )
    parser.add_argument(
        "-s",
        "--plural-forms",
        dest="plural_forms",
        default=None,
        help="Plural forms for the language of the translations. Will be"
        " inserted in the empty key of the JSON output. If not provided and"
        ' the passed pofile includes the "Plural-Forms" header, will be'
        " extracted from it.",
    )
    parser.add_argument(
        "-k",
        "--sort-keys",
        dest="sort_keys",
        action="store_true",
        help="Sort JSON output by keys.",
    )
    return parser


def parse_options(args=[]):
    parser = build_parser()
    if "-h" in args or "--help" in args:
        parser.print_help()
        sys.exit(0)
    opts = parser.parse_args(args)

    if not sys.stdin.isatty():
        opts.po_filepath_or_content = sys.stdin.read().strip("\n")
    elif isinstance(opts.po_filepath_or_content, list):
        opts.po_filepath_or_content = opts.po_filepath_or_content[0]

    return opts


def run(args=[]):
    opts = parse_options(args)

    kwargs = dict(
        fallback_to_msgid=opts.fallback_to_msgid,
        fuzzy=opts.fuzzy,
        pretty=opts.pretty,
        language=opts.language,
        plural_forms=opts.plural_forms,
        sort_keys=opts.sort_keys,
    )
    if isinstance(opts.indent, int):
        kwargs["indent"] = opts.indent

    output = "%s\n" % pofile_to_json(opts.po_filepath_or_content, **kwargs)
    sys.stdout.write(output)

    return (output, 0)


def main():
    sys.exit(run(args=sys.argv[1:])[1])


if __name__ == "__main__":
    main()
