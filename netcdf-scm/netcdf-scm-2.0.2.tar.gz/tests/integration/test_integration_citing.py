import re
from unittest.mock import patch

import pandas as pd
import pandas.testing as pdt
import pytest
from scmdata.run import ScmRun

from netcdf_scm.citing import check_licenses, get_citation_tables
from netcdf_scm.errors import NonStandardLicenseError


def make_scmrun(cm, mip_era):
    cols = {
        "climate_model": cm,
        "mip_era": mip_era,
        "model": "unspecified",
        "scenario": "unspecified",
        "variable": "tas",
        "unit": "K",
        "region": "World",
    }

    if mip_era == "CMIP6":
        cols["activity_id"] = "ScenarioMIP"
        cols["member_id"] = "r1i1p1f1"

    out = ScmRun(data=[1, 2, 3], index=[3, 4, 5], columns=cols)
    out.metadata = {"institution_id": "{}-institute".format(cm)}

    return out


@patch("netcdf_scm.citing.check_license_cmip6")
def test_check_licenses(mock_check_license_cmip6, caplog):
    def cmip6_check(inp):
        if inp.get_unique_meta("climate_model", no_duplicates=True).startswith("Nor"):
            raise NonStandardLicenseError

    mock_check_license_cmip6.side_effect = cmip6_check

    inp = [
        make_scmrun("ACCESS1.0", "CMIP5"),
        make_scmrun("MIROC-ESM", "CMIP5"),
        make_scmrun("ACCESS-CM2", "CMIP6"),
        make_scmrun("NorESM1", "CMIP6"),
    ]
    with pytest.warns(UserWarning) as record:
        res = check_licenses(inp)

    assert len(record) == 2

    assert str(record.list[0].message).startswith(
        "Non-standard license for MIROC-ESM\nLicense terms:"
    )
    assert str(record.list[1].message).startswith(
        "Non-standard license for NorESM1\nLicense terms:"
    )

    for r in res:
        assert r.get_unique_meta("climate_model", no_duplicates=True) in [
            "NorESM1",
            "MIROC-ESM",
        ]


@patch("netcdf_scm.citing.get_cmip5_bibtex_citation")
@patch("netcdf_scm.citing.get_cmip6_bibtex_citation")
def test_get_citation_tables(
    mock_get_cmip6_bibtex_citation, mock_get_cmip5_bibtex_citation
):
    def cmip5_bibtex_citation(model, scenario):
        if model.startswith("MIROC"):
            return "MIROC-ESM CMIP5 {} bibtex".format(scenario)

        return "ACCESS CMIP5 {} bibtex".format(scenario)

    mock_get_cmip5_bibtex_citation.side_effect = cmip5_bibtex_citation

    def cmip6_bibtex_citation(
        mip_era, activity_id, institute_id, model, scenario, version
    ):
        if model.startswith("Nor"):
            return "Nor CMIP6 {} {} bibtex".format(scenario, version)

        return "ACCESS CMIP6 {} {} bibtex".format(scenario, version)

    mock_get_cmip6_bibtex_citation.side_effect = cmip6_bibtex_citation

    access_cmip5 = make_scmrun("ACCESS1.0", "CMIP5")
    access_cmip5.metadata["(child) crunch_source_files"] = (
        "Files: ["
        "'/cmip5/ssp585/Amon/tas/ACCESS1.0/r1i1p1/tas_Amon_ACCESS1.0_ssp585_r1i1p1_200501-210012.nc'"
        "]"
    )
    access_cmip5.metadata["(parent) crunch_source_files"] = (
        "Files: ["
        "'/cmip5/historical/Amon/tas/ACCESS1.0/r1i1p1/tas_Amon_ACCESS1.0_historical_r1i1p1_185001-200412.nc'"
        "]"
    )

    miroc_cmip5 = make_scmrun("MIROC-ESM", "CMIP5")
    miroc_cmip5.metadata["crunch_source_files"] = (
        "Files: ["
        "'/cmip5/ssp585/Amon/tas/MIROC-ESM/r1i1p2/tas_Amon_MIROC-ESM_ssp585_r1i1p2_200501-230012.nc'"
        "]"
    )

    access_cmip6 = make_scmrun("ACCESS-CM2", "CMIP6")
    access_cmip6.metadata["crunch_source_files"] = (
        "Files: ["
        "'/CMIP6/CMIP/ACCESS-CM2-institute/ACCESS-CM2/historical/r1i1p1f1/Amon/tas/gn/v20190627/tas_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_185001-194912.nc', "
        "'/CMIP6/CMIP/ACCESS-CM2-institute/ACCESS-CM2/historical/r1i1p1f1/Amon/tas/gn/v20190627/tas_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_195001-201412.nc'"
        "]"
    )

    noresm_cmip6 = make_scmrun("NorESM1", "CMIP6")
    noresm_cmip6.metadata["(child) crunch_source_files"] = (
        "Files: ["
        "'/CMIP6/CMIP/NorESM1-institute/NorESM1/G6solar/r2i1p1f1/Amon/tas/gn/v20200101/tas_Amon_NorESM1_G6solar_r2i1p1f1_gn_201501-205012.nc'"
        "]"
    )
    noresm_cmip6.metadata["(parent) crunch_source_files"] = (
        "Files: ["
        "'/CMIP6/CMIP/NorESM1-institute/NorESM1/ssp585/r2i1p1f1/Amon/tas/gn/v20200101/tas_Amon_NorESM1_ssp585_r2i1p1f1_gn_201501-205012.nc'"
        "]"
    )
    noresm_cmip6.metadata["(grandparent) crunch_source_files"] = (
        "Files: ["
        "'/CMIP6/CMIP/NorESM1-institute/NorESM1/historical/r2i1p1f1/Amon/tas/gn/v20200101/tas_Amon_NorESM1_historical_r2i1p1f1_gn_185001-200412.nc'"
        "]"
    )
    noresm_cmip6.metadata["(greatgrandparent) crunch_source_files"] = (
        "Files: ["
        "'/CMIP6/CMIP/NorESM1-institute/NorESM1/piControl/r2i1p1f1/Amon/tas/gn/v20200101/tas_Amon_NorESM1_piControl_r2i1p1f1_gn_000101-010012.nc'"
        "]"
    )

    inp = [
        access_cmip5,
        miroc_cmip5,
        access_cmip6,
        noresm_cmip6,
    ]

    cmip5_references_exp = (
        pd.DataFrame(
            {
                "Modelling Group": ["CSIRO-BOM", "CSIRO-BOM", "MIROC"],
                "Climate Model": ["ACCESS1.0", "ACCESS1.0", "MIROC-ESM"],
                "Scenario": ["historical", "ssp585", "ssp585"],
                "Reference": [
                    r"\citet{cmip5data_ACCESS1.0_historical}",
                    r"\citet{cmip5data_ACCESS1.0_ssp585}",
                    r"\citet{cmip5data_MIROC-ESM_ssp585}",
                ],
            }
        )
        .set_index(["Modelling Group", "Climate Model", "Scenario"])
        .sort_index()
    )

    cmip6_references_exp = (
        pd.DataFrame(
            {
                "Modelling Group": [
                    "ACCESS-CM2-institute",
                    "NorESM1-institute",
                    "NorESM1-institute",
                    "NorESM1-institute",
                    "NorESM1-institute",
                ],
                "Climate Model": [
                    "ACCESS-CM2",
                    "NorESM1",
                    "NorESM1",
                    "NorESM1",
                    "NorESM1",
                ],
                "Scenario": [
                    "historical",
                    "G6solar",
                    "historical",
                    "piControl",
                    "ssp585",
                ],
                "Reference": [
                    r"\citet{cmip6data_CMIP6_CMIP_ACCESS-CM2-institute_ACCESS-CM2_historical}",
                    r"\citet{cmip6data_CMIP6_CMIP_NorESM1-institute_NorESM1_G6solar}",
                    r"\citet{cmip6data_CMIP6_CMIP_NorESM1-institute_NorESM1_historical}",
                    r"\citet{cmip6data_CMIP6_CMIP_NorESM1-institute_NorESM1_piControl}",
                    r"\citet{cmip6data_CMIP6_CMIP_NorESM1-institute_NorESM1_ssp585}",
                ],
            }
        )
        .set_index(["Modelling Group", "Climate Model", "Scenario"])
        .sort_index()
    )

    res = get_citation_tables(inp)

    pdt.assert_frame_equal(res["cmip5_references"], cmip5_references_exp)
    assert set(res["cmip5_bibtex"]) == set(
        [
            "ACCESS CMIP5 historical bibtex",
            "ACCESS CMIP5 ssp585 bibtex",
            "MIROC-ESM CMIP5 ssp585 bibtex",
        ]
    )

    pdt.assert_frame_equal(res["cmip6_references"], cmip6_references_exp)
    assert set(res["cmip6_bibtex"]) == set(
        [
            "Nor CMIP6 piControl v20200101 bibtex",
            "Nor CMIP6 historical v20200101 bibtex",
            "Nor CMIP6 ssp585 v20200101 bibtex",
            "Nor CMIP6 G6solar v20200101 bibtex",
            "ACCESS CMIP6 historical v20190627 bibtex",
        ]
    )


def test_get_citation_tables_no_dependencies():
    miroc_run = make_scmrun("MIROC-ESM", "CMIP5")
    inp = [
        miroc_run,
        make_scmrun("NorESM1", "CMIP6"),
    ]

    error_msg = re.escape("Could not find any dependencies for {}".format(miroc_run))
    with pytest.raises(ValueError, match=error_msg):
        get_citation_tables(inp)


def test_get_citation_tables_bad_mip_era():
    inp = [
        make_scmrun("ACCESS1.0", "dud mip"),
    ]

    error_msg = "Cannot generate citation table for mip_era: dud mip"
    with pytest.raises(ValueError, match=error_msg):
        get_citation_tables(inp)
