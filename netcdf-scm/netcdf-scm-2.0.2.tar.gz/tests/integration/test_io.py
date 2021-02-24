import datetime as dt
import os
import re
import shutil

import numpy as np
import pytest
from scmdata import ScmRun

import netcdf_scm
from netcdf_scm.io import (
    _ALL_AVAILABLE_CUBES,
    get_scmcube_helper,
    load_mag_file,
    load_scmrun,
    save_netcdf_scm_nc,
)
from netcdf_scm.iris_cube_wrappers import (
    CMIP6Input4MIPsCube,
    CMIP6OutputCube,
    MarbleCMIP5Cube,
    ScmCube,
)


def _assert_scm_dataframe(scmdf, expected, **kwargs):
    d = scmdf.filter(**kwargs).timeseries()
    assert not d.empty
    np.testing.assert_allclose(d.values.squeeze(), expected)


def test_load_scmrun(test_data_netcdfscm_nc_file):
    loaded = load_scmrun(test_data_netcdfscm_nc_file)

    assert isinstance(loaded, ScmRun)
    assert (loaded["scenario"] == "rcp45").all()
    assert (loaded["climate_model"] == "ACCESS1-0").all()
    assert (loaded["variable"] == "tas").all()
    assert (loaded["variable_standard_name"] == "air_temperature").all()
    assert (loaded["unit"] == "K").all()
    assert (loaded["member_id"] == "r1i1p1").all()
    assert (loaded["mip_era"] == "CMIP5").all()
    assert (loaded["activity_id"] == "cmip5").all()

    _assert_scm_dataframe(loaded, 285.521667, region="World", year=2006, month=1)
    _assert_scm_dataframe(loaded, 279.19043, region="World|Land", year=2019, month=3)
    _assert_scm_dataframe(
        loaded, 287.103729, region="World|Northern Hemisphere", year=2032, month=11
    )
    _assert_scm_dataframe(
        loaded,
        290.850189,
        region="World|Northern Hemisphere|Ocean",
        year=2049,
        month=12,
    )

    assert (
        loaded.metadata["institution"]
        == "CSIRO (Commonwealth Scientific and Industrial Research Organisation, Australia), and BOM (Bureau of Meteorology, Australia)"
    )
    assert (
        loaded.metadata["title"] == "ACCESS1-0 model output prepared for CMIP5 RCP4.5"
    )
    np.testing.assert_allclose(
        loaded.metadata["land_fraction_northern_hemisphere"], 0.38912639
    )


def test_save_cube_and_load_scmrun(tmpdir, test_cmip6_output_file):
    base = CMIP6OutputCube()
    base.load_data_from_path(test_cmip6_output_file)
    out_file = os.path.join(tmpdir, "test_save_file.nc")

    save_netcdf_scm_nc(base.get_scm_timeseries_cubes(), out_file)

    loaded = load_scmrun(out_file)
    assert (loaded["scenario"] == "1pctCO2").all()
    assert (loaded["climate_model"] == "BCC-CSM2-MR").all()
    assert (loaded["variable"] == "rlut").all()
    assert (loaded["variable_standard_name"] == "toa_outgoing_longwave_flux").all()
    assert (loaded["unit"] == "W m^-2").all()
    assert (loaded["activity_id"] == "CMIP").all()
    assert (loaded["member_id"] == "r1i1p1f1").all()
    assert (loaded["mip_era"] == "CMIP6").all()
    assert (loaded["activity_id"] == "CMIP").all()

    _assert_scm_dataframe(loaded, 236.569464, region="World", year=1859, month=12)
    _assert_scm_dataframe(loaded, 242.988181, region="World|Ocean", year=1856, month=10)
    _assert_scm_dataframe(
        loaded, 235.025871, region="World|Southern Hemisphere", year=1853, month=6
    )
    _assert_scm_dataframe(
        loaded, 234.619657, region="World|Southern Hemisphere|Land", year=1850, month=1
    )

    assert loaded.metadata["crunch_netcdf_scm_version"] == (
        "{} (see Nicholls et al. (2021, https://doi.org/10.1002/gdj3.113), "
        "more info at gitlab.com/netcdf-scm/netcdf-scm)".format(netcdf_scm.__version__)
    )
    assert (
        loaded.metadata["institution"]
        == "Beijing Climate Center, Beijing 100081, China"
    )
    assert loaded.metadata["title"] == "BCC-CSM2-MR output prepared for CMIP6"
    np.testing.assert_allclose(
        loaded.metadata["land_fraction_northern_hemisphere"], 0.387551, rtol=1e-6
    )
    assert (
        loaded.metadata["source"]
        == "BCC-CSM 2 MR (2017):   aerosol: none  atmos: BCC_AGCM3_MR (T106; 320 x 160 longitude/latitude; 46 levels; top level 1.46 hPa)  atmosChem: none  land: BCC_AVIM2  landIce: none  ocean: MOM4 (1/3 deg 10S-10N, 1/3-1 deg 10-30 N/S, and 1 deg in high latitudes; 360 x 232 longitude/latitude; 40 levels; top grid cell 0-10 m)  ocnBgchem: none  seaIce: SIS2"
    )


def test_all_available_cubes():
    expected = {}
    for c in dir(netcdf_scm.iris_cube_wrappers):
        try:
            tester = getattr(netcdf_scm.iris_cube_wrappers, c)
            if issubclass(tester, netcdf_scm.iris_cube_wrappers.ScmCube):
                if tester == netcdf_scm.iris_cube_wrappers._CMIPCube:
                    continue

                expected[c.replace("Cube", "")] = tester

        except TypeError:
            continue

    assert expected == _ALL_AVAILABLE_CUBES


@pytest.mark.parametrize(
    "drs,expected",
    (
        ("Scm", ScmCube),
        ("MarbleCMIP5", MarbleCMIP5Cube),
        ("CMIP6Input4MIPs", CMIP6Input4MIPsCube),
        ("CMIP6Output", CMIP6OutputCube),
    ),
)
def test_get_scmcube_helper(drs, expected):
    assert isinstance(get_scmcube_helper(drs), expected)


def test_get_scmcube_helper_none_error():
    error_msg = re.escape(
        "`drs` == 'None' is not supported yet. Please raise an issue at "
        "gitlab.com/netcdf-scm/netcdf-scm/ with your use case if you need this "
        "feature."
    )
    with pytest.raises(NotImplementedError, match=error_msg):
        get_scmcube_helper("None")


def test_get_scmcube_helper_unrecognised_error():
    error_msg = re.escape("Unrecognised drs: junk")
    with pytest.raises(KeyError, match=error_msg):
        get_scmcube_helper("junk")


@pytest.fixture
def test_mag_file_cmip6(test_cmip6_stitch_output):
    return os.path.join(
        test_cmip6_stitch_output,
        "mag-files-average-year-mid-year",
        "CMIP6",
        "ScenarioMIP",
        "BCC/BCC-CSM2-MR",
        "ssp126",
        "r1i1p1f1",
        "Amon",
        "tas",
        "gn",
        "v20190314",
        "netcdf-scm_tas_Amon_BCC-CSM2-MR_ssp126_r1i1p1f1_gn_1850-2100.MAG",
    )


@pytest.mark.parametrize("include_prefix", (True, False))
def test_load_mag_file_cmip6(test_mag_file_cmip6, include_prefix, tmpdir):
    if not include_prefix:
        load_name = os.path.join(
            tmpdir, test_mag_file_cmip6.replace("netcdf-scm_", "").strip(os.sep),
        )
        os.makedirs(os.path.dirname(load_name))
        shutil.copy(test_mag_file_cmip6, load_name)

    else:
        load_name = test_mag_file_cmip6

    res = load_mag_file(load_name, "CMIP6Output")

    assert res.get_unique_meta("scenario", no_duplicates=True) == "ssp126"
    assert res.get_unique_meta("climate_model", no_duplicates=True) == "BCC-CSM2-MR"
    assert res.get_unique_meta("activity_id", no_duplicates=True) == "ScenarioMIP"
    assert res.get_unique_meta("member_id", no_duplicates=True) == "r1i1p1f1"
    assert res.get_unique_meta("mip_era", no_duplicates=True) == "CMIP6"

    assert "todo" not in res.meta


@pytest.mark.parametrize("include_prefix", (True, False))
def test_load_mag_file_cmip6_name_only(test_mag_file_cmip6, include_prefix, tmpdir):
    load_name = os.path.basename(test_mag_file_cmip6)
    if not include_prefix:
        load_name = load_name.replace("netcdf-scm_", "")

    load_name = os.path.join(tmpdir, load_name)
    shutil.copy(test_mag_file_cmip6, load_name)

    with pytest.warns(UserWarning) as record:
        res = load_mag_file(load_name, "CMIP6Output")

    assert len(record) == 3
    assert (
        record[0]
        .message.args[0]
        .startswith(
            "Couldn't determine cube metadata from path with the drs 'CMIP6Output'."
            "\nError:"
        )
    )
    assert record[1].message.args[0] == (
        "Can't set metadata for 'activity_id' from filename alone with the "
        "drs 'CMIP6Output'."
    )
    assert record[2].message.args[0] == (
        "Can't set metadata for 'mip_era' from filename alone with the drs "
        "'CMIP6Output'."
    )

    assert res.get_unique_meta("scenario", no_duplicates=True) == "ssp126"
    assert res.get_unique_meta("climate_model", no_duplicates=True) == "BCC-CSM2-MR"
    assert res.get_unique_meta("member_id", no_duplicates=True) == "r1i1p1f1"

    # can't be identified from filename alone
    assert "activity_id" not in res.meta
    assert "mip_era" not in res.meta

    assert "todo" not in res.meta


def test_load_mag_file_cmip6_garbled_name(test_mag_file_cmip6, tmpdir):
    load_name = os.path.join(tmpdir, "GARBLED.MAG")
    shutil.copy(test_mag_file_cmip6, load_name)

    with pytest.warns(UserWarning) as record:
        res = load_mag_file(load_name, "CMIP6Output")

    assert len(record) == 2
    assert (
        record[0]
        .message.args[0]
        .startswith(
            "Couldn't determine cube metadata from path with the drs 'CMIP6Output'.\n"
            "Error:"
        )
    )
    assert (
        record[1]
        .message.args[0]
        .startswith(
            "Couldn't determine cube metadata from filename either with the drs "
            "'CMIP6Output'.\nError:"
        )
    )

    assert res.get_unique_meta("scenario", no_duplicates=True) == "unspecified"
    assert res.get_unique_meta("climate_model", no_duplicates=True) == "unspecified"

    # can't be identified hence not included
    assert "activity_id" not in res.meta
    assert "mip_era" not in res.meta
    assert "member_id" not in res.meta

    assert "todo" not in res.meta


@pytest.fixture
def test_mag_file_marble_cmip5(test_marble_cmip5_stitch_output):
    return os.path.join(
        test_marble_cmip5_stitch_output,
        "normalised",
        "21-yr-running-mean",
        "mag-files",
        "cmip5",
        "rcp45",
        "Amon",
        "tas",
        "NorESM1-M",
        "r1i1p1",
        "netcdf-scm_tas_Amon_NorESM1-M_rcp45_r1i1p1_185001-230012.MAG",
    )


@pytest.mark.parametrize("include_prefix", (True, False))
def test_load_mag_file_cmip5(test_mag_file_marble_cmip5, include_prefix, tmpdir):
    if not include_prefix:
        load_name = os.path.join(
            tmpdir, test_mag_file_marble_cmip5.replace("netcdf-scm_", "").strip(os.sep),
        )
        os.makedirs(os.path.dirname(load_name))
        shutil.copy(test_mag_file_marble_cmip5, load_name)

    else:
        load_name = test_mag_file_marble_cmip5

    res = load_mag_file(load_name, "MarbleCMIP5")

    assert res.get_unique_meta("scenario", no_duplicates=True) == "rcp45"
    assert res.get_unique_meta("climate_model", no_duplicates=True) == "NorESM1-M"
    assert res.get_unique_meta("member_id", no_duplicates=True) == "r1i1p1"
    assert res.get_unique_meta("mip_era", no_duplicates=True) == "CMIP5"
    assert res.get_unique_meta("activity_id", no_duplicates=True) == "cmip5"

    assert "todo" not in res.meta


@pytest.mark.parametrize("include_prefix", (True, False))
def test_load_mag_file_cmip5_name_only(
    test_mag_file_marble_cmip5, include_prefix, tmpdir
):
    load_name = os.path.basename(test_mag_file_marble_cmip5)
    if not include_prefix:
        load_name = load_name.replace("netcdf-scm_", "")

    load_name = os.path.join(tmpdir, load_name)
    shutil.copy(test_mag_file_marble_cmip5, load_name)

    with pytest.warns(UserWarning) as record:
        res = load_mag_file(load_name, "MarbleCMIP5")

    assert len(record) == 3
    assert (
        record[0]
        .message.args[0]
        .startswith(
            "Couldn't determine cube metadata from path with the drs 'MarbleCMIP5'."
            "\nError:"
        )
    )
    assert record[1].message.args[0] == (
        "Can't set metadata for 'activity_id' from filename alone with the "
        "drs 'MarbleCMIP5'."
    )
    assert record[2].message.args[0] == (
        "Can't set metadata for 'mip_era' from filename alone with the drs "
        "'MarbleCMIP5'."
    )

    assert res.get_unique_meta("scenario", no_duplicates=True) == "rcp45"
    assert res.get_unique_meta("climate_model", no_duplicates=True) == "NorESM1-M"
    assert res.get_unique_meta("member_id", no_duplicates=True) == "r1i1p1"

    # can't be identified from filename alone
    assert "activity_id" not in res.meta
    assert "mip_era" not in res.meta

    assert "todo" not in res.meta


def test_load_mag_file_cmip5_garbled_name(test_mag_file_marble_cmip5, tmpdir):
    load_name = os.path.join(tmpdir, "GARBLED.MAG")
    shutil.copy(test_mag_file_marble_cmip5, load_name)

    with pytest.warns(UserWarning) as record:
        res = load_mag_file(load_name, "MarbleCMIP5")

    assert len(record) == 2
    assert (
        record[0]
        .message.args[0]
        .startswith(
            "Couldn't determine cube metadata from path with the drs 'MarbleCMIP5'.\n"
            "Error:"
        )
    )
    assert (
        record[1]
        .message.args[0]
        .startswith(
            "Couldn't determine cube metadata from filename either with the drs "
            "'MarbleCMIP5'.\nError:"
        )
    )

    assert res.get_unique_meta("scenario", no_duplicates=True) == "unspecified"
    assert res.get_unique_meta("climate_model", no_duplicates=True) == "unspecified"

    # can't be identified hence not included
    assert "activity_id" not in res.meta
    assert "mip_era" not in res.meta
    assert "member_id" not in res.meta

    # # TODO: turn this on once we have an easy way to drop meta in scmdata
    # assert "todo" not in res.meta


def test_days_since_1_handling(test_marble_cmip5_crunch_output):
    tfile = os.path.join(
        test_marble_cmip5_crunch_output,
        "Amon",
        "cmip5",
        "piControl",
        "Amon",
        "tas",
        "NorESM1-M",
        "r1i1p1",
        "netcdf-scm_tas_Amon_NorESM1-M_piControl_r1i1p1_070001-120012.nc",
    )
    loaded = load_scmrun(tfile)

    assert isinstance(loaded, ScmRun)
    assert (loaded["scenario"] == "piControl").all()
    assert loaded["time"].tolist()[0] == dt.datetime(700, 1, 16, 12, 0)
