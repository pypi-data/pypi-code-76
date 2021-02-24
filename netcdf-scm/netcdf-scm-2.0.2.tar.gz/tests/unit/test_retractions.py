import json
import logging
import os.path
import re
from glob import glob
from unittest.mock import patch

import pandas as pd
import pytest

from netcdf_scm.iris_cube_wrappers import CMIP6OutputCube
from netcdf_scm.retractions import (
    _create_search_url,
    _perform_esgf_queries,
    check_depends_on_retracted,
    check_retracted_files,
    check_retractions,
)


def mock_resp(instances, retracted):
    docs = [{"instance_id": i, "retracted": r} for i, r in zip(instances, retracted)]
    return {"response": {"docs": docs}}, instances


@pytest.fixture()
def esgf_result(test_data_root_dir):
    # JSON output from an esgf query
    with open(os.path.join(test_data_root_dir, "retractions.json")) as fh:
        return json.load(fh)


@patch("netcdf_scm.retractions._perform_esgf_queries")
def test_check_retractions(mock_query):
    instance_ids = [
        "CMIP6.DAMIP.NASA-GISS.GISS-E2-1-G.hist.r1i1p1f1.Amon.tas.gn.v20191226",
        "CMIP6.DAMIP.NASA-GISS.GISS-E2-1-G.hist.r1i1p1f1.Amon.rsut.gn.v20191226",
    ]
    mock_query.return_value = [mock_resp(instance_ids, [False, True])]
    res = check_retractions(instance_ids, esgf_query_batch_size=50, nworkers=1)

    expected = [
        "CMIP6.DAMIP.NASA-GISS.GISS-E2-1-G.hist.r1i1p1f1.Amon.rsut.gn.v20191226"
    ]
    assert res == expected

    mock_query.assert_called_with(instance_ids, 50, 1)


@patch("netcdf_scm.retractions._perform_esgf_queries")
def test_check_retractions_couldnt_find(mock_query, caplog):
    instance_ids = [
        "CMIP6.DAMIP.NASA-GISS.GISS-E2-1-G.hist.r1i1p1f1.Amon.tas.gn.v20191226",
        "CMIP6.DAMIP.NASA-GISS.GISS-E2-1-G.hist.r1i1p1f1.Amon.rsut.gn.v20191226",
    ]

    mock_return_value = [mock_resp(instance_ids, [False, True])]
    # drop out one of the instance ids, as if the search didn't find results
    mock_return_value[0][0]["response"]["docs"] = mock_return_value[0][0]["response"][
        "docs"
    ][1:]
    mock_query.return_value = mock_return_value
    res = check_retractions(instance_ids, esgf_query_batch_size=50, nworkers=1)

    assert len(caplog.record_tuples) == 1
    name, level, msg = caplog.record_tuples[0]
    assert name == "netcdf_scm.retractions"
    assert level == logging.WARNING
    assert msg.startswith(
        "Couldn't find "
        "CMIP6.DAMIP.NASA-GISS.GISS-E2-1-G.hist.r1i1p1f1.Amon.tas.gn.v20191226 "
        "(search url: "
    )

    expected = [
        "CMIP6.DAMIP.NASA-GISS.GISS-E2-1-G.hist.r1i1p1f1.Amon.rsut.gn.v20191226"
    ]
    assert res == expected

    mock_query.assert_called_with(instance_ids, 50, 1)


@pytest.mark.parametrize(
    "search_kwargs,exp",
    (
        (
            {},
            "https://esgf.nci.org.au/esg-search/search?format=application%2Fsolr%2Bjson&offset=0&limit=100&type=Dataset&replica=False",
        ),
        (
            {"experiment_id": "ssp585"},
            "https://esgf.nci.org.au/esg-search/search?experiment_id=ssp585&format=application%2Fsolr%2Bjson&offset=0&limit=100&type=Dataset&replica=False",
        ),
        (
            {"experiment_id": "ssp585", "grid_label": "gn"},
            "https://esgf.nci.org.au/esg-search/search?experiment_id=ssp585&grid_label=gn&format=application%2Fsolr%2Bjson&offset=0&limit=100&type=Dataset&replica=False",
        ),
    ),
)
def test_search_url(search_kwargs, exp):
    res = _create_search_url(**search_kwargs)

    assert res == exp


@pytest.mark.parametrize("batch_size", [5, 10])
@patch("netcdf_scm.retractions._query_esgf")
def test_retractions_batch_size(mock_query, batch_size):
    mock_query.side_effect = lambda ids: ({}, ids)
    instance_ids = [
        "CMIP6.DAMIP.NASA-GISS.GISS-E2-1-G.hist.r{}i1p1f1.Amon.tas.gn.v20191226".format(
            i
        )
        for i in range(30)
    ]

    res = _perform_esgf_queries(
        instance_ids, esgf_query_batch_size=batch_size, nworkers=1
    )

    assert len(res) == 30 // batch_size

    for i, r in enumerate(res):
        assert r[0] == {}
        assert len(r[1]) == batch_size


@patch("netcdf_scm.retractions._query_esgf")
def test_retractions_integration(mock_query, esgf_result):
    mock_query.side_effect = lambda ids: (esgf_result, ids)
    instance_ids = [
        "CMIP6.DAMIP.NASA-GISS.GISS-E2-1-G.hist.r1i1p1f1.Amon.tas.gn.v20191226",
        "CMIP6.DAMIP.NASA-GISS.GISS-E2-1-G.hist.r1i1p1f1.Amon.rsut.gn.v20191226",
    ]

    res = check_retractions(instance_ids, esgf_query_batch_size=50, nworkers=1)
    expected = [
        "CMIP6.DAMIP.NASA-GISS.GISS-E2-1-G.hist-aer.r2i1p1f2.Amon.rsut.gn.v20191226"
    ]
    assert res == expected

    mock_query.assert_called_with(instance_ids)


list_of_files_mark = pytest.mark.parametrize("list_of_files", [True, False])


@list_of_files_mark
@patch("netcdf_scm.retractions.check_retractions")
def test_check_retracted_files_mag(
    mock_check_retractions, test_cmip6_stitch_output, list_of_files
):
    _check_retracted_files(
        mock_check_retractions,
        test_cmip6_stitch_output,
        "*.MAG",
        list_of_files,
        expected_retracted=3,
    )


@list_of_files_mark
@patch("netcdf_scm.retractions.check_retractions")
def test_check_retracted_files_nc(
    mock_check_retractions, test_data_cmip6output_dir, list_of_files
):
    _check_retracted_files(
        mock_check_retractions,
        test_data_cmip6output_dir,
        "*.nc",
        list_of_files,
        expected_retracted=1,
    )


def _check_retracted_files(
    mock_check_retractions, test_dir, filter_txt, list_of_files, expected_retracted
):
    fnames = glob(os.path.join(test_dir, "**", filter_txt), recursive=True)
    instance_ids = list(set([CMIP6OutputCube.get_instance_id(f) for f in fnames]))
    mock_check_retractions.return_value = [
        "CMIP6.CMIP.BCC.BCC-CSM2-MR.historical.r1i1p1f1.Amon.tas.gn.v20181126"
    ]

    if list_of_files:
        fnames_or_dir = fnames
    else:
        fnames_or_dir = test_dir

    res = check_retracted_files(
        fnames_or_dir, filename_filter=filter_txt, esgf_query_batch_size=50, nworkers=1
    )

    mock_check_retractions.assert_called()
    _, call_args, call_kwargs = mock_check_retractions.mock_calls[0]
    assert call_kwargs == {"esgf_query_batch_size": 50, "nworkers": 1}
    assert sorted(call_args[0]) == sorted(instance_ids)

    assert len(res) == expected_retracted
    for f in res:
        assert "tas_Amon_BCC-CSM2-MR_historical_r1i1p1f1_gn" in f


def _check_depends_on_retracted_files_result(res):
    retracted_mag = res.loc[res["dependency_retracted"], "mag_file"].unique().tolist()
    assert len(retracted_mag) == 6

    def check_retracted_file(f):
        return (
            "tas_Amon_BCC-CSM2-MR_historical_r1i1p1f1_gn" in f
            or "tas_Amon_BCC-CSM2-MR_ssp126_r1i1p1f1_gn" in f
        )

    for f in retracted_mag:
        assert check_retracted_file(f) and f.endswith(".MAG")

    retracted_nc = (
        res.loc[res["dependency_retracted"], "dependency_file"].unique().tolist()
    )
    for f in retracted_nc:
        assert check_retracted_file(f) and f.endswith(".nc")

    assert (
        res["dependency_instance_id"]
        == res["dependency_file"].apply(CMIP6OutputCube.get_instance_id)
    ).all()


@patch("netcdf_scm.retractions.check_retractions")
def test_check_depends_on_retracted(mock_check_retractions, test_cmip6_stitch_output):
    fnames = glob(os.path.join(test_cmip6_stitch_output, "**", "*.MAG"), recursive=True)

    mock_check_retractions.return_value = [
        "CMIP6.CMIP.BCC.BCC-CSM2-MR.historical.r1i1p1f1.Amon.tas.gn.v20181126"
    ]

    res = check_depends_on_retracted(fnames, esgf_query_batch_size=50, nworkers=1)

    assert isinstance(res, pd.DataFrame)
    assert res.columns.tolist() == [
        "mag_file",
        "dependency_file",
        "dependency_instance_id",
        "dependency_retracted",
    ]

    mock_check_retractions.assert_called()
    _, _, call_kwargs = mock_check_retractions.mock_calls[0]
    assert call_kwargs == {"esgf_query_batch_size": 50, "nworkers": 1}

    _check_depends_on_retracted_files_result(res)


@patch("netcdf_scm.retractions.check_retractions")
@pytest.mark.parametrize("raise_on_mismatch", (True, False))
def test_check_depends_on_retracted_not_cmip6(
    mock_check_retractions,
    raise_on_mismatch,
    caplog,
    test_marble_cmip5_stitch_output,
    test_cmip6_stitch_output,
):
    fnames_cmip5 = glob(
        os.path.join(test_marble_cmip5_stitch_output, "**", "*.MAG"), recursive=True
    )
    fnames_cmip6 = glob(
        os.path.join(test_cmip6_stitch_output, "**", "*.MAG"), recursive=True
    )

    def call():
        return check_depends_on_retracted(
            fnames_cmip5 + fnames_cmip6, raise_on_mismatch=raise_on_mismatch
        )

    if raise_on_mismatch:
        error_msg = re.escape(
            "Source data is not CMIP6 for: {}".format(set(fnames_cmip5))
        )
        with pytest.raises(ValueError, match=error_msg):
            call()
    else:
        mock_check_retractions.return_value = [
            "CMIP6.CMIP.BCC.BCC-CSM2-MR.historical.r1i1p1f1.Amon.tas.gn.v20181126"
        ]

        res = call()
        _check_depends_on_retracted_files_result(res)

        assert len(caplog.record_tuples) == 1
        name, level, msg = caplog.record_tuples[0]
        assert name == "netcdf_scm.retractions"
        assert level == logging.ERROR
        assert msg.startswith("Source data is not CMIP6 for: ")

        mock_check_retractions.assert_called()


@patch("netcdf_scm.retractions.check_retractions")
@patch("netcdf_scm.retractions.pymagicc.io.read_mag_file_metadata")
@pytest.mark.parametrize("raise_on_mismatch", (True, False))
def test_check_depends_on_retracted_no_metadata(
    mock_read_mag_file_metadata, mock_check_retractions, raise_on_mismatch, caplog
):
    tfpath = "/CMIP6/C4MIP/BCC/BCC-CSM2-MR/1pctCO2-bgc/r1i1p1f1/Amon/tas/gn/v20190321/tas_Amon_BCC-CSM2-MR_1pctCO2-bgc_r1i1p1f1_gn_185001-200012.nc"

    def get_metadata(fname):
        if fname.startswith("c"):
            return {"(child) crunch_source_files": ("Files: " "['{}']".format(tfpath))}

        return {}

    mock_read_mag_file_metadata.side_effect = get_metadata

    fnames = ["a.MAG", "b.MAG", "c.MAG"]
    fnames_dud = fnames[:2]
    error_msg = re.escape(
        "Could not determine source data for: {}".format(set(fnames_dud))
    )

    def call():
        check_depends_on_retracted(fnames, raise_on_mismatch=raise_on_mismatch)

    if raise_on_mismatch:
        with pytest.raises(ValueError, match=error_msg):
            call()
    else:
        call()
        assert len(caplog.record_tuples) == 1
        name, level, msg = caplog.record_tuples[0]
        assert name == "netcdf_scm.retractions"
        assert level == logging.ERROR
        assert msg.startswith("Could not determine source data for: ")

        mock_check_retractions.assert_called()
        mock_check_retractions.assert_called_with(
            [CMIP6OutputCube.get_instance_id(tfpath)]
        )
