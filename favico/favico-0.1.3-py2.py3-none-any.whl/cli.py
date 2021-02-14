# -*- coding: utf-8 -*-

"""Console script for favico."""
import sys
import typing

import click

from favico import generate


@click.command()
@click.argument("image", type=click.Path(exists=True))
@click.argument("output", type=click.Path(exists=False))
@click.option("-b", "--base-url", type=str)
def main(image: str, output: str, base_url: typing.Optional[str]) -> int:
    """Console script for favico."""
    generate(image, output, base=base_url or "/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
