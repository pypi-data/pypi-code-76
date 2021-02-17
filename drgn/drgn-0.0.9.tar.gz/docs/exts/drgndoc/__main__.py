# Copyright (c) Facebook, Inc. and its affiliates.
# SPDX-License-Identifier: GPL-3.0+

if __name__ == "__main__":
    import argparse
    import sys

    from drgndoc.format import Formatter
    from drgndoc.namespace import Namespace, ResolvedNode
    from drgndoc.parse import parse_paths

    parser = argparse.ArgumentParser(description="TODO")
    parser.add_argument(
        "--rst", action="store_true", default=True, help="format as reStructuredText"
    )
    parser.add_argument(
        "--plain", dest="rst", action="store_false", help="format as plain text"
    )
    parser.add_argument("names", metavar="NAME", nargs="+", help="name to format")
    args = parser.parse_args()

    # TODO
    args.paths = ["drgn", "_drgn.pyi"]

    namespace = Namespace(parse_paths(args.paths))
    formatter = Formatter(namespace)
    for name in args.names:
        resolved = namespace.resolve_global_name(name)
        if isinstance(resolved, ResolvedNode):
            print("\n".join(formatter.format(resolved, name, rst=args.rst)))
        else:
            sys.exit(f"name {name} not found")
