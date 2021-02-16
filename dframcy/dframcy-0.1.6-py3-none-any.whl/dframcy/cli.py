# coding: utf-8
from __future__ import unicode_literals

import json
import click
import spacy
from io import open
from pathlib import Path
from wasabi import Printer
from .dframcy import DframCy
from .utils import get_default_columns

messenger = Printer()
DEFAULT_COLUMNS = ",".join(get_default_columns())


@click.group()
def main():
    pass


@main.command()
@click.option(
    "--input_file", "-i", required=True, type=Path, help="Input text file path."
)
@click.option("--output_file", "-o", required=True, type=Path, help="Output file path.")
@click.option(
    "--format",
    "-f",
    default="csv",
    show_default=True,
    type=click.Choice(["json", "csv"], case_sensitive=False),
    help="Output file format (json/csv)",
)
@click.option(
    "--language_model",
    "-l",
    default="en_core_web_sm",
    show_default=True,
    type=str,
    help="Language model to be used.",
)
@click.option(
    "--columns",
    "-c",
    default=DEFAULT_COLUMNS,
    show_default=True,
    type=str,
    help="Annotations to be included in dataframe.",
)
@click.option(
    "--separate_entity_frame",
    "-s",
    default=False,
    show_default=True,
    type=bool,
    help="Save separate entity dataframe.",
)
def dframe(
    input_file, output_file, format, language_model, columns, separate_entity_frame
):
    format = format.lower()

    if output_file.is_dir():
        output_file = output_file.joinpath(input_file.stem + "." + str(format))
    if input_file.exists():
        with open(input_file, "r") as infile:
            text = infile.read().strip("\n").strip()

        nlp = spacy.load(language_model)
        dframcy = DframCy(nlp)
        doc = nlp(text)

        annotation_dataframe = dframcy.to_dataframe(
            doc=doc,
            columns=columns.split(","),
            separate_entity_dframe=separate_entity_frame,
        )

        if separate_entity_frame:
            token_annotation_dataframe, entity_dataframe = annotation_dataframe
        else:
            token_annotation_dataframe = annotation_dataframe
            entity_dataframe = None

        if format == "csv":
            token_annotation_dataframe.to_csv(output_file)
            if separate_entity_frame:
                entity_output_file = Path(
                    str(output_file).strip(".csv") + "_entity.csv"
                )
                entity_dataframe.to_csv(entity_output_file)
        elif format == "json":
            annotation_json = token_annotation_dataframe.to_json(orient="columns")
            json.dump(annotation_json, open(output_file, "w"))
            if separate_entity_frame:
                entity_output_file = Path(
                    str(output_file).strip(".json") + "_entity.json"
                )
                json.dump(entity_dataframe, open(entity_output_file, "w"))
    else:
        messenger.fail(
            "input file path: {} does not exist".format(input_file), exits=-1
        )
