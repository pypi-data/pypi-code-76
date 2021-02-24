"""
Helper tools for citing `Coupled Model Intercomparison Project <https://www.wcrp-climate.org/wgcm-cmip>`_ data
"""
import os.path
import warnings

import pandas as pd
import tqdm.autonotebook as tqdman

from ..errors import NonStandardLicenseError
from ..iris_cube_wrappers import CMIP6OutputCube, MarbleCMIP5Cube
from ..retractions import _get_dependencies
from .cmip5 import (
    _determine_cmip5_modelling_group,
    _get_cmip5_citation_key,
    check_license_cmip5,
    get_cmip5_bibtex_citation,
)
from .cmip6 import (
    _get_cmip6_citation_key,
    check_license_cmip6,
    get_cmip6_bibtex_citation,
)


def check_licenses(scmruns):
    """
    Check datasets for non-standard licenses

    Non-standard licenses result in a warning

    Parameters
    ----------
    scmruns : list of :obj:`scmdata.ScmRun`
        Datasets to check the licenses of

    Returns
    -------
    list of :obj:`scmdata.ScmRun`
        Datasets with non-standard licenses
    """
    non_standard = []
    for scmrun in tqdman.tqdm(scmruns):
        mip_era = scmrun.get_unique_meta("mip_era", no_duplicates=True)

        try:
            if mip_era == "CMIP5":
                check_license_cmip5(scmrun)
            else:
                check_license_cmip6(scmrun)

        except NonStandardLicenseError as e:
            non_standard.append(scmrun)

            climate_model = scmrun.get_unique_meta("climate_model", no_duplicates=True)
            warnings.warn(
                "Non-standard license for {}\n"
                "License terms:\n\t{}".format(climate_model, e)
            )

    return non_standard


def get_citation_tables(database):
    """
    Get citation tables for a given set of CMIP data

    Parameters
    ----------
    database : list of :obj:`ScmRun`
        Set of CMIP data for which we want to create citation tables

    Returns
    -------
    dict of str: Union[List, pd.DataFrame]
        Dictionary containing the citation table and bibtex references
        for each MIP era used in ``database``

    Raises
    ------
    ValueError
        Any :obj:`ScmRun` in ``database`` has a ``mip_era`` other than "CMIP5"
        or "CMIP6"
    """
    cmip5_references = {
        "Climate Model": [],
        "Scenario": [],
        "Modelling Group": [],
        "Reference": [],
    }
    cmip5_bibtex = []

    cmip6_references = {
        "Climate Model": [],
        "Scenario": [],
        "Modelling Group": [],
        "Reference": [],
    }
    cmip6_bibtex = []

    for scmrun in tqdman.tqdm(database, desc="Datasets"):
        mip_era = scmrun.get_unique_meta("mip_era", no_duplicates=True)
        if mip_era not in ["CMIP5", "CMIP6"]:
            raise ValueError(
                "Cannot generate citation table for mip_era: {}".format(mip_era)
            )

        dependencies = _get_dependencies(scmrun.metadata)

        if not dependencies:
            raise ValueError("Could not find any dependencies for {}".format(scmrun))

        for dependency in tqdman.tqdm(
            dependencies, desc="Dependencies", total=len(dependencies), leave=False
        ):
            if mip_era == "CMIP5":
                cmip5_references, cmip5_bibtex = _process_cmip5_dependency(
                    dependency, cmip5_references, cmip5_bibtex
                )

            else:  # CMIP6 thanks to check above
                institute_id = set(
                    [v for k, v in scmrun.metadata.items() if "institution_id" in k]
                )

                if len(institute_id) != 1:  # pragma: no cover
                    raise AssertionError(
                        "More than one institute? {}".format(institute_id)
                    )

                institute_id = list(institute_id)[0]

                cmip6_references, cmip6_bibtex = _process_cmip6_dependency(
                    dependency, cmip6_references, cmip6_bibtex, institute_id
                )

    cmip5_references = (
        pd.DataFrame(cmip5_references)
        .set_index(["Modelling Group", "Climate Model", "Scenario"])
        .sort_index()
        .drop_duplicates()
    )
    cmip5_bibtex = list(set(cmip5_bibtex))

    cmip6_references = (
        pd.DataFrame(cmip6_references)
        .set_index(["Modelling Group", "Climate Model", "Scenario"])
        .sort_index()
        .drop_duplicates()
    )
    cmip6_bibtex = list(set(cmip6_bibtex))

    return {
        "cmip5_references": cmip5_references,
        "cmip5_bibtex": cmip5_bibtex,
        "cmip6_references": cmip6_references,
        "cmip6_bibtex": cmip6_bibtex,
    }


def _process_cmip5_dependency(dependency, references, bibtexs):
    helper = MarbleCMIP5Cube()

    path_bits = helper.process_path(os.path.dirname(dependency))
    climate_model = path_bits["model"]
    scenario = path_bits["experiment"]
    citation_key = _get_cmip5_citation_key(climate_model, scenario)

    ref = r"\citet{" + citation_key + "}"

    if ref not in references["Reference"]:
        model_group = _determine_cmip5_modelling_group(climate_model)

        references["Climate Model"].append(climate_model)
        references["Scenario"].append(scenario)
        references["Modelling Group"].append(model_group)
        references["Reference"].append(ref)

        bib_cite = get_cmip5_bibtex_citation(climate_model, scenario)

        bibtexs.append(bib_cite)

    return references, bibtexs


def _process_cmip6_dependency(dependency, references, bibtexs, institute_id):
    helper = CMIP6OutputCube()

    path_bits = helper.process_path(os.path.dirname(dependency))

    activity_id = path_bits["activity_id"]
    climate_model = path_bits["source_id"]
    scenario = path_bits["experiment_id"]

    citation_key = _get_cmip6_citation_key(
        path_bits["mip_era"], activity_id, institute_id, climate_model, scenario,
    )
    ref = r"\citet{" + citation_key + "}"

    if ref not in references["Reference"]:
        references["Climate Model"].append(climate_model)
        references["Scenario"].append(scenario)
        references["Modelling Group"].append(institute_id)
        references["Reference"].append(ref)

        bib_cite = get_cmip6_bibtex_citation(
            path_bits["mip_era"],
            activity_id,
            institute_id,
            climate_model,
            scenario,
            version=path_bits["version"],
        )

        bibtexs.append(bib_cite)

    return references, bibtexs
