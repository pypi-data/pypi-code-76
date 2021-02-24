import datetime as dt
import re
from unittest.mock import patch

import pytest
import requests
from scmdata.run import ScmRun

from netcdf_scm.citing import check_license_cmip5, check_license_cmip6
from netcdf_scm.citing.cmip5 import _get_cmip5_citation_key, get_cmip5_bibtex_citation
from netcdf_scm.citing.cmip6 import (
    _get_cmip6_citation_key,
    get_cmip6_bibtex_citation,
    get_license_info,
)
from netcdf_scm.errors import NoLicenseInformationError, NonStandardLicenseError


@pytest.fixture
def test_scmdata():
    out = ScmRun(
        data=[1, 2, 3],
        index=[10, 20, 30],
        columns={
            "model": "junk",
            "scenario": "junk",
            "variable": "junk",
            "region": "junk",
            "unit": "junk",
        },
    )

    out.metadata = {"junk key": "junk value"}

    return out


def test_get_license_info_single_key(test_scmdata):
    tlicense_info = "license information here"
    test_scmdata.metadata["license"] = tlicense_info

    res = get_license_info(test_scmdata)

    assert res == [tlicense_info]


def test_get_license_info_two_keys(test_scmdata):
    tlicense_info_1 = "license information here"
    tlicense_info_2 = "license information here"
    test_scmdata.metadata["(child) license"] = tlicense_info_1
    test_scmdata.metadata["(normalisation) license"] = tlicense_info_2

    res = get_license_info(test_scmdata)

    assert set(res) == {tlicense_info_1, tlicense_info_2}


def test_get_license_info_missing_license(test_scmdata):
    error_msg = re.escape("Metadata found: {}".format(test_scmdata.metadata))
    with pytest.raises(NoLicenseInformationError, match=error_msg):
        get_license_info(test_scmdata)


def test_check_license_missing_license(test_scmdata):
    error_msg = re.escape("Metadata found: {}".format(test_scmdata.metadata))
    with pytest.raises(NoLicenseInformationError, match=error_msg):
        check_license_cmip6(test_scmdata)


VALID_LICENSE_TXT = (
    "Creative Commons Attribution ShareAlike 4.0 International License. "
    "See website for terms of use governing CMIP6 output, including "
    "citation requirements and proper acknowledgment"
)


@pytest.mark.parametrize(
    "txt,exp_error",
    (
        (VALID_LICENSE_TXT, False),
        (
            "Creative Commons Attribution[]-ShareAlike 4.0 International License. "
            "See website for terms of use governing CMIP6 output, including "
            "citation requirements and proper acknowledgment",
            False,
        ),
        (
            "Creative Commons Attribution[]-ShareAlike 4.0 Non-Commercial License. "
            "See website for terms of use governing CMIP6 output, including "
            "citation requirements and proper acknowledgment",
            True,
        ),
        ("Nonsense", True),
    ),
)
def test_check_license_single_key(test_scmdata, txt, exp_error):
    test_scmdata.metadata["license"] = txt
    if exp_error:
        error_msg = re.escape("Non-standard licenses: {}".format({txt}))
        with pytest.raises(NonStandardLicenseError, match=error_msg):
            check_license_cmip6(test_scmdata)

    else:
        check_license_cmip6(test_scmdata)


@pytest.mark.parametrize(
    "txt_1,txt_2,exp_error_1,exp_error_2",
    (
        (VALID_LICENSE_TXT, VALID_LICENSE_TXT, False, False),
        ("Nonsense", VALID_LICENSE_TXT, True, False),
        (
            VALID_LICENSE_TXT,
            VALID_LICENSE_TXT.replace("International", "NonCommercial International"),
            False,
            True,
        ),
        (
            VALID_LICENSE_TXT,
            VALID_LICENSE_TXT.replace("Attribution", "Attribution-NonCommercial"),
            False,
            True,
        ),
        ("Nonsense", "More nonsense", True, True),
    ),
)
def test_check_license_multiple_keys(
    test_scmdata, txt_1, txt_2, exp_error_1, exp_error_2
):
    test_scmdata.metadata["(child) license"] = txt_1
    test_scmdata.metadata["(normalisation) license"] = txt_2
    if exp_error_1 or exp_error_2:
        if exp_error_1 and exp_error_2:
            error_msg = re.escape("Non-standard licenses: {}".format({txt_1, txt_2}))
        elif exp_error_1:
            error_msg = re.escape("Non-standard licenses: {}".format({txt_1}))
        else:
            error_msg = re.escape("Non-standard licenses: {}".format({txt_2}))

        with pytest.raises(NonStandardLicenseError, match=error_msg):
            check_license_cmip6(test_scmdata)

    else:
        check_license_cmip6(test_scmdata)


@pytest.mark.parametrize(
    "model_name,restricted",
    (
        ("ACCESS1.0", False),
        ("INM-CM4", False),
        ("MIROC-ESM", True),
        ("MIROC-ESM-CHEM", True),
        ("MRI-CGCM3", True),
        ("NICAM.09", True),
    ),
)
def test_check_license_cmip5(test_scmdata, model_name, restricted):
    test_scmdata["climate_model"] = model_name

    if restricted:
        error_msg = re.escape(
            "Output is only available for non-commercial research and "
            "education purposes, see "
            "`<https://pcmdi.llnl.gov/mips/cmip5/docs/CMIP5_modeling_groups.pdf>`_"
        )

        with pytest.raises(NonStandardLicenseError, match=error_msg):
            check_license_cmip5(test_scmdata)

    else:
        check_license_cmip5(test_scmdata)


@patch("netcdf_scm.citing.cmip5._query_cmip5_doi")
def test_get_cmip5_bibtex_citation(mock_query_cmip5_doi):
    raw_response = "@misc{https://doi.org/10.1594/wdcc/cmip5.csa0c1,\n  doi = {10.1594/WDCC/CMIP5.CSA0C1},\n  url = {http://cera-www.dkrz.de/WDCC/CMIP5/Compact.jsp?acronym=CSA0c1},\n  author = {Bi, Dave and Dix, Martin and Marsland, Simon and O'Farrell, Siobhan and Uotila, Petteri and Hirst, Tony and Kowalczyk, Eva and Rashid, Harun and Sun, Zhian and Collier, Mark and Dommenget, Katja and Golebiewski, Maciej and Hannah, Nicholas and Fiedler, Russell and Franklin, Charmaine and Lewis, Sophie and Ma, Yimin and Petrelli, Paola and Stevens, Lauren and Sullivan, Arnold and Uhe, Peter and Vohralik, Peter and Watterson, Ian and Yan, Hailin and Zhou, Xiaobing},\n  keywords = {Climate, ACCESS1-0, CMIP5, IPCC, IPCC-AR5, IPCC-AR5_CMIP5, IPCC-DDC, climate simulation},\n  language = {en},\n  title = {ACCESS1-0 model output prepared for CMIP5 1pctCO2, served by ESGF},\n  publisher = {World Data Center for Climate (WDCC) at DKRZ},\n  year = {2016}\n}\n"

    mock_query_cmip5_doi.return_value = raw_response

    res = get_cmip5_bibtex_citation("ACCESS1.0", "1pctCO2")

    assert res == raw_response.replace(
        "https://doi.org/10.1594/wdcc/cmip5.csa0c1", "cmip5data_ACCESS1.0_1pctCO2"
    )


def test_get_cmip5_bibtex_citation_failure():
    model = "ACCESS1.0"
    scenario = "junk"
    error_msg = re.escape("No CMIP5 data for {} {}".format(model, scenario))
    with pytest.raises(ValueError, match=error_msg):
        get_cmip5_bibtex_citation(model, scenario)


@pytest.mark.parametrize("version", (None, "YYYYMMDD"))
@patch("netcdf_scm.citing.cmip6._get_cmip6_doi")
@patch("netcdf_scm.citing.cmip6._query_cmip6")
def test_get_cmip6_bibtex_citation(mock_query_cmip6, mock_get_cmip6_doi, version):
    mip_era = "CMIP6"
    activity_id = "ScenarioMIP"
    institute_id = "CSIRO-ARCCSS"
    climate_model = "ACCESS-CM2"
    scenario = "ssp585"

    drs_id = ".".join([mip_era, activity_id, institute_id, climate_model, scenario])

    mock_doi = "10.22033/ESGF/CMIP6.4332"
    mock_get_cmip6_doi.return_value = mock_doi

    raw_response = "@misc{https://doi.org/10.22033/esgf/cmip6.4332,\n  doi = {10.22033/ESGF/CMIP6.4332},\n  url = {http://cera-www.dkrz.de/WDCC/meta/CMIP6/CMIP6.ScenarioMIP.CSIRO-ARCCSS.ACCESS-CM2.ssp585},\n  author = {Dix, Martin and Bi, Doahua and Dobrohotoff, Peter and Fiedler, Russell and Harman, Ian and Law, Rachel and Mackallah, Chloe and Marsland, Simon and O'Farrell, Siobhan and Rashid, Harun and Srbinovsky, Jhan and Sullivan, Arnold and Trenham, Claire and Vohralik, Peter and Watterson, Ian and Williams, Gareth and Woodhouse, Matthew and Bodman, Roger and Dias, Fabio Boeira and Domingues, Catia and Hannah, Nicholas and Heerdegen, Aidan and Savita, Abhishek and Wales, Scott and Allen, Chris and Druken, Kelsey and Evans, Ben and Richards, Clare and Ridzwan, Syazwan Mohamed and Roberts, Dale and Smillie, Jon and Snow, Kate and Ward, Marshall and Yang, Rui},\n  keywords = {CMIP6, climate, CMIP6.ScenarioMIP.CSIRO-ARCCSS.ACCESS-CM2.ssp585},\n  language = {en},\n  title = {CSIRO-ARCCSS ACCESS-CM2 model output prepared for CMIP6 ScenarioMIP ssp585},\n  publisher = {Earth System Grid Federation},\n  year = {2019}\n}\n"

    mock_query_cmip6.return_value = raw_response

    res = get_cmip6_bibtex_citation(
        mip_era, activity_id, institute_id, climate_model, scenario, version=version
    )

    mock_get_cmip6_doi.assert_called_with(drs_id)
    query_val = "https://doi.org/{}".format(mock_doi)
    mock_query_cmip6.assert_called_with(query_val)

    if version is None:
        expected_version = dt.date.today().strftime("%Y%m%d")
    else:
        expected_version = version

    assert res == raw_response.replace(
        query_val.lower(), "cmip6data_{}".format(drs_id.replace(".", "_"))
    ).replace(
        "CSIRO-ARCCSS ACCESS-CM2 model output prepared for CMIP6 ScenarioMIP ssp585",
        "CSIRO-ARCCSS ACCESS-CM2 model output prepared for CMIP6 ScenarioMIP ssp585. Version {}".format(
            expected_version
        ),
    )


@patch("netcdf_scm.citing.cmip6._get_cmip6_doi")
def test_get_cmip6_bibtex_citation_failure(mock_get_cmip6_doi):
    mock_get_cmip6_doi.side_effect = requests.exceptions.HTTPError("test message")
    mip_era = "CMIP6"
    activity_id = "ScenarioMIP"
    institute_id = "CSIRO-ARCCSS"
    climate_model = "ACCESS-CM2"
    scenario = "junk"

    drs_id = ".".join([mip_era, activity_id, institute_id, climate_model, scenario])

    error_msg = re.escape(
        "No citation could be found for {}.\nError was: test message".format(drs_id)
    )
    with pytest.raises(ValueError, match=error_msg):
        get_cmip6_bibtex_citation(
            mip_era, activity_id, institute_id, climate_model, scenario
        )


def test_get_citation_key_cmip5():
    model = "model"
    scenario = "scenario"
    exp = "cmip5data_{}_{}".format(model, scenario)
    res = _get_cmip5_citation_key(model, scenario)

    assert res == exp


def test_get_citation_key_cmip6():
    mip_era = "mip_era"
    activity_id = "activity_id"
    institute_id = "institute_id"
    model = "model"
    scenario = "scenario"
    exp = "cmip6data_{}_{}_{}_{}_{}".format(
        mip_era, activity_id, institute_id, model, scenario
    )
    res = _get_cmip6_citation_key(mip_era, activity_id, institute_id, model, scenario)

    assert res == exp
