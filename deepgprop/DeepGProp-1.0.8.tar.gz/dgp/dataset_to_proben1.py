"""Obtain proben1-like partitions."""
from pathlib import Path

import click
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle

from dgp.settings import SEED


@click.command()
@click.argument(
    "file_path", type=Path,
)
@click.option(
    "-s",
    "--seed",
    type=click.INT,
    default=SEED,
    help="seed to initialize semi-random shuffle.",
)
def cli(file_path: Path, seed: int):
    """Split a dataset into 3 proben1-like partitions.

    Split the dataset given by ``FILE_PATH`` into 3 partitions of train (trn),
    validation (val) and test (tst).

    """
    if not file_path.exists() or not file_path.is_file():
        raise click.BadParameter(
            (
                "Dataset path provided does not exists or it is not a file "
                f"'{str(file_path)}'."
            ),
            param_hint="FILE_PATH",
        )

    np.random.seed(seed)

    dataset_path = file_path.resolve()
    dataset_directory = dataset_path.parent
    dataset_name = dataset_path.stem

    dataframe = pd.read_csv(str(file_path), dtype=str)
    dataframe["class"] = LabelEncoder().fit_transform(dataframe["class"])
    header = ",".join(list(dataframe.columns))

    for partition in range(1, 4):
        # pylint: disable=unbalanced-tuple-unpacking
        trn, val, tst = np.split(
            shuffle(dataframe),
            [int(0.5 * len(dataframe)), int(0.75 * len(dataframe))],
        )
        np.savetxt(
            str(dataset_directory / f"{dataset_name}{partition}.trn"),
            trn,
            fmt="%s",
            delimiter=",",
            header=header,
            comments="",
        )
        np.savetxt(
            str(dataset_directory / f"{dataset_name}{partition}.val"),
            val,
            fmt="%s",
            delimiter=",",
            header=header,
            comments="",
        )
        np.savetxt(
            str(dataset_directory / f"{dataset_name}{partition}.tst"),
            tst,
            fmt="%s",
            delimiter=",",
            header=header,
            comments="",
        )


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
