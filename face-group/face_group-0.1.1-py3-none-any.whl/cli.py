"""
Command line module
"""
import time

import click
from click import BOOL
from click import Path

from face_group.api import process_images


@click.command()
@click.option("-i", "--input-dir", "input_dir", type=Path(exists=True))
@click.option("-o", "--output-dir", "output_dir", default="out", type=Path())
@click.option("-v", "--verbose", "verbose", default=True, type=bool)
def group_faces(input_dir: str, output_dir: str, verbose: bool) -> None:
    """Группирует лица одинаковых людей"""
    print(verbose)
    st = time.time()
    process_images(input_dir, output_dir, verbose)
    click.echo(f"Done in {time.time() - st}s")
