import json

from typing import Dict
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import click

from hycli.commons.request import extract_invoice
from hycli.commons.jobs import read_pdf


def convert_to_json(
    files: Dict[Path, str],
    url: str,
    header: Dict,
    params: Dict,
    token: str,
    workers: int = 1,
    output_path: Path = Path.cwd(),
):
    """Sends requests to defined Hypatos services for every document found in given
    directory and saves response as a JSON structure.

    Args:
        files (dict): Dictionary of processed files containing PosixPath as a key and MIME type as a value
        url (str): URL endpoint of exposed Hypatos Invoice Extractor
        header (dict): Optional. Extractor endpoint header(s) can be multiple.
        params (dict): Optional. Extractor endpoint param(s) can be multiple.
        token (str): API token. (default: {None})
        workers (int): Amount of multithread. (default: {1})
        output_path (PosixPath): output directory for CSV file

    """

    skipped_files = []

    with ThreadPoolExecutor(max_workers=workers) as exe:
        jobs = {
            exe.submit(
                extract_invoice,
                read_pdf(file_path),
                url,
                content_type,
                token,
                header,
                params,
            ): file_path
            for file_path, content_type in files.items()
        }
        label = f"Extracting {len(jobs)} documents"
        with click.progressbar(jobs, label=label) as bar:
            for idx, future in enumerate(as_completed(jobs)):
                file_name = jobs[future].stem
                try:
                    response = future.result(timeout=300)

                except Exception as e:
                    skipped_files.append((file_name, e))
                    continue

                save_loc = output_path.joinpath(str(file_name) + ".json")

                with open(save_loc, "w") as f:
                    json.dump(response, f)

                bar.update(1)

    return skipped_files
