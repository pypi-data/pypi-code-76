"""pandas smart_open utilities."""
import logging
from pathlib import Path
from typing import Any

import pandas as pd
import smart_open

from wpdatautil.pathlib import path_to_uri
from wpdatautil.timeit import Timer

log = logging.getLogger(__name__)


def read_parquet_path(path: Path, *, df_description: str = "dataframe", **kwargs: Any) -> pd.DataFrame:
    """Return a dataframe read from the given path using `smart_open`.

    :param path: This must be a `pathlib` or `s3path` path.
    :param df_description: Optional description of dataframe.
    :param kwargs: These are forwarded to `pd.read_parquet`.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    return read_parquet_uri(path_to_uri(path), df_description=df_description, **kwargs)


def write_parquet_path(df: pd.DataFrame, path: Path, *, df_description: str = "dataframe", **kwargs: Any) -> None:
    """Write the given dataframe to the given path using `smart_open`.

    :param df: Dataframe to write.
    :param path: This must be a `pathlib` or `s3path` path.
    :param df_description: Optional description of dataframe.
    :param kwargs: These are forwarded to `df.to_parquet`.
    """
    write_parquet_uri(df, uri=path_to_uri(path), df_description=df_description, **kwargs)


def read_parquet_uri(uri: str, *, df_description: str = "dataframe", **kwargs: Any) -> pd.DataFrame:
    """Return a dataframe read from the given URI using `smart_open`, thereby supporting both local and S3 URIs.

    `kwargs` are forwarded to `pd.read_parquet`.
    """
    timer = Timer()
    read_description = f"{df_description} from {uri} using smart-open"
    log.info(f"Reading {read_description}.")
    try:
        with smart_open.open(uri, "rb") as input_file:
            df = pd.read_parquet(input_file, **kwargs)
    except Exception as exception:  # pylint: disable=broad-except
        log.info(f"Error reading {read_description}: {exception.__class__.__qualname__}: {exception}")
        raise
    log.info(f"Read {read_description} in {timer}.")
    return df


def write_parquet_uri(df: pd.DataFrame, uri: str, *, df_description: str = "dataframe", **kwargs: Any) -> None:
    """Write the given dataframe to the given URI using `smart_open`, thereby supporting both local and S3 URIs.

    `kwargs` are forwarded to `df.to_parquet`.
    """
    timer = Timer()
    write_description = f"{df_description} to {uri} using smart-open"
    log.info(f"Writing {write_description}.")
    try:
        with smart_open.open(uri, "wb") as output_file:
            df.to_parquet(output_file, **kwargs)
    except Exception as exception:  # pylint: disable=broad-except
        log.info(f"Error writing {write_description}: {exception.__class__.__qualname__}: {exception}")
        raise
    log.info(f"Wrote {write_description} in {timer}.")
