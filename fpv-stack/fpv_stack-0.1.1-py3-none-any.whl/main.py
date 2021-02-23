import argparse

from fpv_stack.create import ProjectCreator


def fpv_stack() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--create',
        nargs=1,
    )

    parsed_args = parser.parse_args()

    if parsed_args.create:
        ProjectCreator(parsed_args.create[0]).create()
