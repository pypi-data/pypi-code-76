"""
Helper tools for citing CMIP5 of the `Coupled Model Intercomparison Project <https://www.wcrp-climate.org/wgcm-cmip>`_ data
"""
import functools
import os.path

import pandas as pd
import requests
import tqdm

from ..errors import NonStandardLicenseError


def check_license_cmip5(scmdata):
    """
    Check the license information of a CMIP5 dataset.

    This uses the information found at
    `<https://pcmdi.llnl.gov/mips/cmip5/docs/CMIP5_modeling_groups.pdf>`_.

    Parameters
    ----------
    scmdata : :obj:`scmdata.ScmRun`
        Dataset of which to check the license information

    Raises
    ------
    NonStandardLicenseError
        The dataset's license is non-standard i.e. is not a
        `Creative Commons Attribution ShareAlike 4.0 International License <https://creativecommons.org/licenses/by-sa/4.0/>`_
    """
    climate_model = scmdata.get_unique_meta("climate_model", no_duplicates=True)

    non_standard_model = any(
        [climate_model.startswith(v) for v in ("MIROC", "MRI", "NICAM")]
    )
    if non_standard_model:
        error_msg = (
            "Output is only available for non-commercial research and "
            "education purposes, see "
            "`<https://pcmdi.llnl.gov/mips/cmip5/docs/CMIP5_modeling_groups.pdf>`_"
        )
        raise NonStandardLicenseError(error_msg)


@functools.lru_cache()
def _query_cmip5_doi(doi):  # pragma: no cover
    headers = {
        "Accept": "application/x-bibtex",
    }

    response = requests.get(doi, headers=headers)
    response.raise_for_status()
    return response.text


def get_cmip5_bibtex_citation(model, scenario):
    """
    Get CMIP5 bibtex citation

    Parameters
    ----------
    model : str
        Model of interest

    scenario : str
        Scenario of interest

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
    cmip5_dois = _load_cmip5_dois().set_index(["climate_model", "scenario"])

    try:
        doi = cmip5_dois.loc[(model, scenario), "doi"].values[0]
    except KeyError:
        raise ValueError("No CMIP5 data for {} {}".format(model, scenario))

    citation_key = _get_cmip5_citation_key(model, scenario)

    bib_tex_citation = _query_cmip5_doi(doi).replace(doi.lower(), citation_key)

    return bib_tex_citation


def _get_cmip5_citation_key(model, scenario):
    return "cmip5data_{}_{}".format(model, scenario)


def _load_cmip5_dois():
    return pd.read_csv(
        os.path.join(
            os.path.dirname(__file__), "cmip5_climate-model_scenario_citations.csv"
        )
    )


def _determine_cmip5_modelling_group(model):  # pragma: no cover
    if model.startswith("ACCESS"):
        return "CSIRO-BOM"

    if model.startswith("BCC-"):
        return "BCC"

    if model.startswith("BESM"):
        return "INPE"

    if model.startswith("BNU-ESM"):
        return "GCESS"

    if model.startswith("Can"):
        return "CCCMA"

    if model.startswith("CCSM4(RSMAS)"):
        return "RSMAS"

    if model.startswith("CCSM4"):
        return "NCAR"

    if model.startswith("CESM1"):
        return "NSF-DOE-NCAR"

    if model.startswith("CFS"):
        return "COLA and NCEP"

    if model.startswith("CMCC"):
        return "CMCC"

    if model.startswith("CNRM"):
        return "CNRM-CERFACS"

    if model.startswith("CSIRO-Mk"):
        return "CSIRO-QCCCE"

    if model.startswith("EC-EARTH"):
        return "EC-EARTH"

    if model.startswith("FGOALS-g2"):
        return "LASG-CESS"

    if model.startswith("FGOALS-"):
        return "LASG-IAP"

    if model.startswith("FIO-"):
        return "FIO"

    if model.startswith("GEOS-5"):
        return "NASA GMAO"

    if model.startswith("GFDL-"):
        return "NOAA GFDL"

    if model.startswith("GISS-"):
        return "NASA GISS"

    if model.startswith("HadGEM2-AO"):
        return "NIMR/KMA"

    if model.startswith("HadCM3") or model.startswith("HadGEM2"):
        return "MOHC"

    if model.startswith("INM-CM4") or model.startswith("INMCM4"):
        return "INM"

    if model.startswith("IPSL-CM5"):
        return "IPSL"

    if model.startswith("MIROC"):
        return "MIROC"

    if model.startswith("MPI-ESM"):
        return "MPI-M"

    if model.startswith("MRI-"):
        return "MRI"

    if model.startswith("NICAM"):
        return "NICAM"

    if model.startswith("NorESM1"):
        return "NCC"

    raise NotImplementedError(model)


def _clean_ar5_html():  # pragma: no cover
    from bs4 import BeautifulSoup

    with open(
        os.path.join(os.path.dirname(__file__), "data", "ar5-ref-info.html")
    ) as fh:
        soup = BeautifulSoup(fh.read(), "lxml")

    model_doi_table = soup.find("table", attrs={"id": "customers"})
    model_doi_table_data = model_doi_table.tbody.find_all("tr")

    data = {
        "model": [],
        "scenario": [],
        "doi": [],
    }
    for i, tr in tqdm.tqdm(enumerate(model_doi_table_data)):
        if i == 0:
            headers = [th.text.replace("\n", " ").strip() for th in tr.find_all("th")]
            model_col = headers.index("Model")

        elif i > 1:
            cols = tr.find_all("td")
            if not cols:
                model_doi_table_data[i - 1]
                continue

            if len(cols) == len(headers):
                model = cols[model_col].text.replace("\n", " ").strip()
            else:
                model = cols[0].text.replace("\n", " ").strip()

            model = model.replace("(Journal)", "").replace("\n", " ").strip()
            print(model)

            for j, col in enumerate(cols):
                if j <= model_col:
                    continue

                links = col.find_all("a")
                for link in links:
                    experiment = link.text.replace("\n", " ").strip()

                    try:
                        colour = link.span.get("style")
                        if not colour.startswith("color:darkgreen"):
                            if colour.startswith("color:LightSlateGrey"):
                                continue

                            if colour.startswith("color:darkred"):
                                continue

                            raise ValueError(colour)

                    except AttributeError:
                        continue

                    doi = link.get("href").replace("\n", " ").strip()

                    data["model"].append(model)
                    data["scenario"].append(experiment)
                    data["doi"].append(doi)

    data = pd.DataFrame(data)
    data.to_csv(
        os.path.join(
            os.path.dirname(__file__), "cmip5_climate-model_scenario_citations.csv"
        ),
        index=False,
    )


if __name__ == "__main__":
    _clean_ar5_html()
