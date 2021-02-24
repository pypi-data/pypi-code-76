"""
Utilities for checking for retracted datasets
"""
import concurrent.futures
import glob
import logging
import os.path
from collections import defaultdict
from urllib.parse import urlencode

import pandas as pd
import pymagicc.io
import requests
import tqdm.autonotebook as tqdman

from .iris_cube_wrappers import CMIP6OutputCube

LOGGER = logging.getLogger(__name__)

ESGF_NODE = "esgf.nci.org.au"


def _create_search_url(**kwargs):
    kwargs.setdefault("format", "application/solr+json")
    kwargs.setdefault("offset", 0)
    kwargs.setdefault("limit", 100)
    kwargs.setdefault("type", "Dataset")
    kwargs.setdefault("replica", False)

    return "https://{}/esg-search/search?{}".format(
        ESGF_NODE, urlencode(kwargs, doseq=True)
    )


def _query_esgf(instance_ids):
    response = requests.get(_create_search_url(instance_id=instance_ids))
    response.raise_for_status()
    response_json = response.json()

    return response_json, instance_ids


def _perform_esgf_queries(instance_ids, esgf_query_batch_size, nworkers):
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=nworkers) as executor:
        for i in tqdman.tqdm(
            range(0, len(instance_ids), esgf_query_batch_size),
            desc="Querying ESGF (submitting jobs)",
        ):
            batch = instance_ids[i : i + esgf_query_batch_size]
            futures.append(executor.submit(_query_esgf, batch,))

        return [
            f.result()
            for f in tqdman.tqdm(
                concurrent.futures.as_completed(futures),
                total=len(futures),
                desc="Retrieving results from ESGF jobs",
            )
        ]


def check_retractions(instance_ids, esgf_query_batch_size=100, nworkers=8):
    """
    Check a list of ``instance_ids`` for any retracted datasets

    Notes
    -----
    This queries external ESGF servers. Please limit the number of parallel requests.

    Parameters
    ----------
    instance_ids : list of str
        Datasets to check. ``instance_id`` is the unique identifier for a dataset,
        for example `CMIP6.CMIP.CSIRO.ACCESS-ESM1-5.esm-hist.r1i1p1f1.Amon.rsut.gn.v20191128`

    esgf_query_batch_size : int
        Maximum number of ids to include in each query.

    nworkers : int
        Number of workers to parallel queries to ESGF.

    Returns
    -------
    list of str
        A list of retracted ``instance_ids``
    """
    response_jsons_search_instance_ids = _perform_esgf_queries(
        instance_ids, esgf_query_batch_size, nworkers
    )

    retracted_files = []
    for response_json, search_ids in response_jsons_search_instance_ids:
        found_ids = []
        for data_doc in response_json["response"]["docs"]:
            id_here = data_doc["instance_id"]
            found_ids.append(id_here)

            if data_doc["retracted"]:
                LOGGER.info("Processing dependents of retracted dataset: %s", id_here)
                retracted_files.append(id_here)

        if len(found_ids) != len(search_ids):
            missing_ids = set(search_ids) - set(found_ids)
            for mid in missing_ids:
                LOGGER.warning(
                    "Couldn't find %s (search url: %s)",
                    mid,
                    _create_search_url(instance_id=mid),
                )

    return retracted_files


def check_retracted_files(filenames_or_dir, filename_filter="*.nc", **kwargs):
    """
    Check if any files are retracted

    Notes
    -----
    This queries external ESGF servers. Please limit the number of parallel requests.

    Parameters
    ----------
    filenames_or_dir: list of str or str
        A list of filenames or a directory to check for any retractions. If a string
        is provided, it is assumed to reference a directory and any files within
        that directory matching the `filename_filter` will be checked.

    filename_filter: str
        If a directory is passed all files matching the filter will be checked.

    **kwargs : any
        Passed to :func:`check_retracted`

    Returns
    -------
    List of the retracted files
    """

    if isinstance(filenames_or_dir, str):
        if os.path.isdir(filenames_or_dir):
            fnames = glob.glob(
                os.path.join(filenames_or_dir, "**", filename_filter), recursive=True,
            )
        else:
            raise NotADirectoryError(filenames_or_dir)
    else:
        if not isinstance(filenames_or_dir, list):
            raise ValueError("filenames_or_dir should be a list of filenames")
        fnames = filenames_or_dir

    filepaths_instance_ids = []
    for fname in tqdman.tqdm(fnames):
        try:
            filepaths_instance_ids.append(
                (fname, CMIP6OutputCube.get_instance_id(fname))
            )
        except ValueError:
            LOGGER.exception("could not get instance_id from {}".format(fname))

    instance_ids = list(set([v[1] for v in filepaths_instance_ids]))

    retracted = check_retractions(instance_ids, **kwargs)

    retracted_files = []
    for fp, instance_id in filepaths_instance_ids:
        if instance_id in retracted:
            retracted_files.append(fp)

    return retracted_files


def check_depends_on_retracted(mag_files, raise_on_mismatch=True, **kwargs):
    """
    Check if a ``.MAG`` file was calculated from now retracted data

    Notes
    -----
    This queries external ESGF servers. Please limit the number of parallel requests.

    Parameters
    ----------
    mag_files : list of str
        List of ``.MAG`` files to check

    raise_on_mismatch : bool
        If a file cannot be processed, should an error be raised? If ``False``, an
        error message is logged instead.

    **kwargs : any
        Passed to :func:`check_retractions`

    Returns
    -------
    pd.DataFrame
        Dataframe which describes the retracted status of each file in ``mag_files``. The columns are:

            - "mag_file": the files in ``mag_files``

            - "dependency_file": file which the file in the "mag_file" column depends on (note that
                                 the ``.MAG`` files may have more than one dependency so they may
                                 appear more than once in the "mag_file" column)

            - "dependency_instance_id": instance id (i.e. unique ESGF identifier) of the dependency file

            - "dependency_retracted": whether the dependency file has been retracted or not (``True`` if
                                      the file has been retracated)

        The list of retracted ``.MAG`` files can then be accessed with e.g.
        ``res.loc[res["dependency_retracted"], "mag_file"].unique()``

    Raises
    ------
    ValueError
        The ``.MAG`` file is not based on CMIP6 data (retractions cannot be checked
        automatically for CMIP5 data with netCDF-SCM).

    ValueError
        Metadata about a ``.MAG`` file's source is not included in the ``.MAG`` file.
    """
    no_source_data_files = []
    non_cmip6_data_files = []

    out_table = defaultdict(list)

    for mf in tqdman.tqdm(mag_files):
        LOGGER.debug("Processing %s", mf)

        metadata = pymagicc.io.read_mag_file_metadata(mf)
        dependency_files = _get_dependencies(metadata)

        if not dependency_files:
            no_source_data_files.append(mf)
            continue

        for df in dependency_files:
            try:
                instance_id = CMIP6OutputCube.get_instance_id(df)
            except ValueError:
                non_cmip6_data_files.append(mf)
                continue

            out_table["mag_file"].append(mf)
            out_table["dependency_file"].append(df)
            out_table["dependency_instance_id"].append(instance_id)

    if no_source_data_files:
        msg = "Could not determine source data for: {}".format(
            set(no_source_data_files)
        )
        if raise_on_mismatch:
            raise ValueError(msg)

        LOGGER.error(msg)

    if non_cmip6_data_files:
        msg = "Source data is not CMIP6 for: {}".format(set(non_cmip6_data_files))
        if raise_on_mismatch:
            raise ValueError(msg)

        LOGGER.error(msg)

    out_table = pd.DataFrame(out_table)

    instance_ids_retracted = check_retractions(
        out_table["dependency_instance_id"].unique().tolist(), **kwargs
    )

    out_table["dependency_retracted"] = out_table["dependency_instance_id"].isin(
        instance_ids_retracted
    )

    return out_table


def _get_dependencies(metadata):
    dependency_files = []

    for k in metadata:
        if "source_files" in k:
            dependency_files_key = [
                v.strip("]").strip("'")
                for g in metadata[k].split(";")
                for sg in g.split(", ")
                for v in sg.split("[")[1:]
            ]

            if any(["," in d for d in dependency_files_key]):
                raise ValueError(
                    "Bad processing of {}, got {}".format(
                        metadata, dependency_files_key
                    )
                )

            dependency_files += dependency_files_key

    LOGGER.debug("Dependent files %s", dependency_files)

    return dependency_files
