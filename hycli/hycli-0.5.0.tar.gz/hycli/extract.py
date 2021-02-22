from pathlib import Path
from mimetypes import guess_type

import click

from hycli.commands import to_csv, to_xlsx, to_json
from hycli.commands.callbacks import find_skippable_files
from hycli.commands.context_default import CONTEXT_SETTINGS


def get_input_files(input_path, skip_files=[]):
    file_types = ("*.pdf", "*.tif", "*.tiff", "*.png", "*.jpg", "*.json")
    files = []

    for file_type in file_types:
        files.extend(input_path.rglob(file_type))
        files.extend(input_path.rglob(file_type.upper()))

    skip_stems = [skip_f.stem for skip_f in skip_files]
    return {f: guess_type(f)[0] for f in files if f.stem not in skip_stems}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.argument("input_path", type=click.Path(exists=True, readable=True))
@click.option(
    "-o",
    "--output",
    type=click.Path(exists=False, file_okay=True, dir_okay=True, writable=True),
    default=Path.cwd(),
    callback=find_skippable_files,
    help="output directory for file(s) or output filename (e.g. hycli_batch_05.xlsx)",
)
@click.option(
    "-s",
    "--skip",
    is_flag=True,
    default=False,
    is_eager=True,
    help="Skip converting documents which are found to have been already extracted/converted in output path/file.",
)
@click.pass_context
def extract(ctx: object, input_path: str, output: str, skip: bool):
    """Can extract information from a directory of documents (invoices, receipts) to csv/xlsx using the Hypatos Extraction service."""
    input_path = Path(input_path).resolve()

    ctx.obj = {
        **ctx.obj,
        "input_files": get_input_files(input_path, ctx.obj.get("skip_files")),
        "input_path": input_path,
        "output_path": output,
    }


extract.add_command(to_csv.to_csv)
extract.add_command(to_xlsx.to_xlsx)
extract.add_command(to_json.to_json)
