from pathlib import Path
from typing import Dict, List

import xlsxwriter
import pandas as pd
import numpy as np

from hycli.commons.jobs import run_requests
from hycli.commons.structure import structure_sheets, structure_sheet
from hycli.commons.consts import RED_TO_GREEN_GRADIENT


def convert_to_xlsx(
    files: Dict[Path, str],
    url: str,
    headers: Dict,
    params: Dict,
    token: str,
    workers: int = 1,
    normalize: bool = False,
    output_path: Path = Path("hycli.xlsx"),
):
    """Converts all documents (\*.pdf, \*.png etc) and JSON OCR files found in the directory and saves them in XLSX structure.
    Sends requests to defined Hypatos service for every document found in given
    directory. Merges results off all services into one Excel file and writes to
    project directory. Every key, value pair from Invoice Extractor will flattened
    into the following tuple:

        key = (value, probability)

    Args:
        files (dict): Dictionary of processed files containing PosixPath as a key and MIME type as a value
        url (str): URL endpoint of exposed Hypatos Invoice Extractor
        headers (dict): Optional. Extractor endpoint header(s) can be multiple.
        params (dict): Optional. Extractor endpoint param(s) can be multiple.
        token (str): API token. (default: {None})
        workers (int): Amount of multithread. (default: {1})
        normalize (bool): Normalize probability of every individual column from [min, max] to [0,1]. (default: {False})
        output_path (PosixPath): output directory for CSV file

    """  # NOQA
    # Get requests result
    extracted_files = run_requests(files, url, workers, headers, params, token)

    # Structure response into sheets (dict) containing records [{...}, {...}]
    sheets = structure_sheets(extracted_files)

    # Normalize probability
    if normalize and (headers.get("probabilities") == "true"):
        for sheet in sheets.copy():
            sheets[sheet] = normalize_probability(sheets[sheet])

    # Write sheets into workbook
    write_workbook(output_path, sheets)


def write_workbook(output_path: str, sheets: List[dict]):
    """Writes a list of sheets into a Excel workbook, every sheet is a dict with a records structure.

    Args:
        output_path (PosixPath): output path of written workbook.
        sheets (dict): dictionary containing key-value pairs of sheet names and flattened extraction.

    """
    # Init workbook/sheets
    workbook = xlsxwriter.Workbook(output_path)

    # Styling
    header_format = workbook.add_format({"bold": True})
    number_format = workbook.add_format({"num_format": "0.00"})
    probability_formats = [
        workbook.add_format({"bold": True, "bg_color": color})
        for color in RED_TO_GREEN_GRADIENT
    ]

    for sheet in sheets:
        workbook.add_worksheet(sheet)
        write_sheet(
            workbook.get_worksheet_by_name(sheet),
            structure_sheet(sheets[sheet]),
            header_format,
            number_format,
            probability_formats,
        )

    workbook.close()


def write_sheet(
    worksheet, records: list, header_format, number_format, probability_formats: list
):
    """Write items to workbook sheet.

    Arguments:
        worksheet {[type]} -- [description]
        records {[type]} -- [description]
        bold_header {[type]} -- [description]
        red_to_green_formats {[type]} -- [description]
    """
    for idx, row in enumerate(records):
        count = 0
        for key, value in row.copy().items():
            worksheet.write(0, count, key, header_format)
            if not isinstance(value, tuple):
                records[idx][key] = (value, None, None)

            column_value, probability, _ = records[idx][key]
            value_format = number_format if isinstance(column_value, float) else None

            if pd.notna(probability):
                color_idx = int((len(probability_formats) - 1) * probability)
                color = probability_formats[color_idx]
                worksheet.write(idx + 1, count, column_value, color)
            else:
                worksheet.write(idx + 1, count, column_value, value_format)

            count += 1

    for i, width in enumerate(get_col_widths(pd.DataFrame.from_records(records))):
        worksheet.set_column(i, i, width)


def get_col_widths(invoices, max_col_width=70):
    """ Get max length for every column and below max_column_width """
    return [
        min(
            max(
                [len(str(s[0])) for s in invoices[col].values if s is not np.nan]
                + [len(col)]
            ),
            max_col_width,
        )
        for col in invoices.columns
    ]


def normalize_probability(records: list):
    """Normalize the probabilities for every column inbetween range(min, max) of
    particulair column.

    Args:
        invoices ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Read
    probabilities = {}
    for idx, invoice in enumerate(records):
        probabilities[idx] = {k: v[1] for k, v in invoice.items()}

    # Normalize
    df = pd.DataFrame.from_dict(probabilities, orient="index")
    for col in df.columns:
        if not df[col].isnull().all():
            min_value, max_value = (
                df[col].min(),
                df[col].max(),
            )
            if min_value == max_value:
                df[col] = pd.Series([np.nan] * len(df[col]))
            else:
                df[col] = (df[col] - min_value) / (max_value - min_value)

    # Write
    normalized = df.to_dict("records")
    for idx, invoice in enumerate(records.copy()):
        for col in invoice:
            if invoice[col]:
                triplet = list(records[idx][col])
                triplet[1] = normalized[idx][col]
                records[idx][col] = tuple(triplet)

    return records
