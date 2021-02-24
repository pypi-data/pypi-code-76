"""
Helper tools for citing CMIP6 of the `Coupled Model Intercomparison Project <https://www.wcrp-climate.org/wgcm-cmip>`_ data
"""
import datetime as dt
import functools
import json

import requests

from ..errors import NoLicenseInformationError, NonStandardLicenseError


def check_license_cmip6(scmdata):
    """
    Check the license information of a dataset

    Parameters
    ----------
    scmdata : :obj:`scmdata.ScmRun`
        Dataset of which to check the license information

    Raises
    ------
    NonStandardLicenseError
        The dataset's license is non-standard i.e. is not a
        `Creative Commons Attribution ShareAlike 4.0 International License <https://creativecommons.org/licenses/by-sa/4.0/>`_

    NoLicenseInformationError
        No license information could be found in ``scmdata.metadata``
    """
    licenses = get_license_info(scmdata)

    non_ccas4 = {
        license
        for license in licenses
        if not (
            ("Creative Commons Attribution" in license)
            and ("ShareAlike 4.0 International License" in license)
            and (
                "for terms of use governing CMIP6 output, including citation requirements and proper acknowledgment"
                in license
            )
            and ("NonCommercial" not in license)
        )
    }
    if non_ccas4:
        error_msg = "Non-standard licenses: {}".format(non_ccas4)
        raise NonStandardLicenseError(error_msg)


def get_license_info(scmdata):
    """
    Get the license information from a dataset's metadata.

    Parameters
    ----------
    scmdata : :obj:`scmdata.ScmRun`
        Dataset from which to get the license information

    Raises
    ------
    NoLicenseInformationError
        No license information could be found in ``scmdata.metadata``
    """
    licenses = [v for k, v in scmdata.metadata.items() if "license" in k]

    if not licenses:
        raise NoLicenseInformationError("Metadata found: {}".format(scmdata.metadata))

    return licenses


@functools.lru_cache()
def _get_cmip6_doi(drs_id):  # pragma: no cover
    params = (
        ("input", drs_id),
        ("wt", "json"),
    )
    response = requests.get(
        "https://cera-www.dkrz.de/WDCC/ui/cerasearch/cerarest/exportcmip6",
        params=params,
    )
    response.raise_for_status()

    cite_info = json.loads(response.text)
    doi = cite_info["identifier"]["id"]

    return doi


@functools.lru_cache()
def _query_cmip6(query_url):  # pragma: no cover
    headers = {
        "Accept": "application/x-bibtex",
    }

    response = requests.get(query_url, headers=headers)
    response.raise_for_status()

    return response.text


def get_cmip6_bibtex_citation(
    mip_era, activity_id, institute_id, model, scenario, version=None
):
    """
    Get CMIP5 bibtex citation

    Parameters
    ----------
    mip_era : str
        Mip era (should always be CMIP6)

    activity_id : str
        Activity id (e.g. ScenarioMIP)

    institute_id : str
        Institute which produced the output

    model : str
        Model of interest

    scenario : str
        Scenario of interest

    version : Union[str, None]
        Version of the dataset. If ``None``, today's date is used in accordance with the guidance provided by the CMIP6 citation guidelines
        `see e.g. footnote 1 here <https://cera-www.dkrz.de/WDCC/ui/cerasearch/cmip6?input=CMIP6.ScenarioMIP.CSIRO-ARCCSS.ACCESS-CM2.ssp585>`_

    Returns
    -------
    str
        Bibtex citation

    Raises
    ------
    ValueError
        No CMIP5 data is available for ``model`` ``scenario`` hence no
        citation can be provided.
    """
    drs_id = ".".join([mip_era, activity_id, institute_id, model, scenario])

    citation_key = _get_cmip6_citation_key(
        mip_era, activity_id, institute_id, model, scenario
    )
    try:
        doi = _get_cmip6_doi(drs_id)
        query_url = "https://doi.org/{}".format(doi)
        bib_tex_citation = _query_cmip6(query_url).replace(
            query_url.lower(), citation_key
        )

    except requests.exceptions.HTTPError as exc:
        raise ValueError(
            "No citation could be found for {}.\nError was: {}".format(drs_id, exc)
        )

    if version is None:
        version = dt.date.today().strftime("%Y%m%d")

    title = _get_title(bib_tex_citation)
    bib_tex_citation = bib_tex_citation.replace(
        title, "{}. Version {}".format(title, version)
    )

    return bib_tex_citation


def _get_title(bib_tex_citation):
    title = bib_tex_citation.split("title")[1].split("{")[1].split("}")[0]

    return title


def _get_cmip6_citation_key(mip_era, activity_id, institute_id, model, scenario):
    return "cmip6data_{}".format(
        "_".join([mip_era, activity_id, institute_id, model, scenario])
    )
