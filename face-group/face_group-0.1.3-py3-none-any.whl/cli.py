"""
Command line module
"""
import time

import click
from click import Path

from face_group.api import process_images


@click.command()
@click.option(
    "-i",
    "--input-dir",
    "input_dir",
    type=Path(exists=True),
    help="Path of directory with rgb and infra images.",
)
@click.option(
    "-o",
    "--output-dir",
    "output_dir",
    default="out",
    type=Path(),
    help="Path of output directory (default='out').",
)
@click.option(
    "-v", "--verbose", "verbose", default=True, type=bool, help="Show info or not."
)
def group_faces(input_dir: str, output_dir: str, verbose: bool) -> None:
    """It groups the faces of similar people"""

    start = time.time()
    process_images(input_dir, output_dir, verbose)
    click.echo(f"Done in {time.time() - start}s")
