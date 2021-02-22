import csv

from typing import Dict
from pathlib import Path
from copy import deepcopy

from hycli.commons.structure import structure_sheets, structure_sheet
from hycli.commons.jobs import run_requests


def convert_to_csv(
    files: Dict[Path, str],
    url: str,
    headers: Dict,
    params: Dict,
    token: str,
    workers: int = 1,
    file_name: str = "hycli",
    output_path: Path = Path.cwd(),
):
    """Converts all documents (\*.pdf, \*.png etc) and JSON OCR files found in the directory and saves them in CSV structure.
    Sends requests to defined Hypatos service for every document found in given
    directory. Merges results off all services into multiple CSV files and writes to
    project directory.

    Args:
        files (dict): Dictionary of processed files containing PosixPath as a key and MIME type as a value
        url (str): URL endpoint of exposed Hypatos Invoice Extractor
        headers (dict): Optional. Extractor endpoint header(s) can be multiple.
        params (dict): Optional. Extractor endpoint param(s) can be multiple.
        token (str): API token. (default: {None})
        workers (int): amount of workers (default: {1})
        file_name (str): filename of the result
        output_path (PosixPath): output directory for CSV file

    """  # NOQA
    # Get requests result
    extracted_files = run_requests(files, url, workers, headers, params, token)

    # Structure result
    sheets = structure_sheets(extracted_files)

    for sheet in sheets:
        write_csv(
            output_path.joinpath(f"{file_name}_{sheet}.csv"),
            structure_sheet(sheets[sheet]),
        )


def write_csv(file_name, records):
    set_values(records)
    with open(file_name, mode="w") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=records[0].keys(),
            extrasaction="ignore",
            delimiter=";",
        )
        writer.writeheader()
        for row in records:
            writer.writerow(row)


def set_values(records):
    for idx, row_items in enumerate(deepcopy(records)):
        for field, value in row_items.items():
            records[idx][field] = value[0]
