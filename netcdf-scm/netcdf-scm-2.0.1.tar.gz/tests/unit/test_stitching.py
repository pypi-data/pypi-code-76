import re

import numpy as np
import pytest
from scmdata import ScmRun

from netcdf_scm.stitching import (
    get_branch_time,
    get_parent_replacements,
    step_up_family_tree,
)


@pytest.fixture(scope="function")
def junk_data():
    out = ScmRun(
        np.arange(100),
        index=np.arange(1850, 1950),
        columns={
            "scenario": ["rcp26"],
            "experiment_id": ["rcp26"],
            "model": ["model1"],
            "climate_model": ["climate_model1"],
            "mip_era": ["CMIP6"],
            "region": ["World"],
            "variable": ["tas"],
            "unit": ["K"],
        },
    )

    out.metadata = {
        "branch_time_in_parent": 0.0,
        "parent_time_units": "days since 1850-01-01",
        "calendar": "365_day",
        "source_id": "UoM mocked data",
        "experiment_id": "rcp26",
        "netcdf-scm crunched file": "/path/to/mocked/rcp26/data_rcp26.nc",
    }

    return out


@pytest.fixture
def junk_data_picontrol(junk_data):
    out = junk_data.copy()
    out["scenario"] = "piControl"
    out["experiment_id"] = "piControl"
    out.metadata = {
        "other": "metadata",
        "goes": "here",
        "branch_time_in_parent": -1001.1,
        "parent_time_units": "days since 1850-01-01",
        "calendar": "365_day",
        "source_id": "UoM mocked data",
        "experiment_id": "piControl",
        "netcdf-scm crunched file": "/path/to/mocked/piControl/data_piControl.nc",
    }

    return out


def test_get_branch_time_cmip5_not_parent_error(junk_data):
    junk_data["mip_era"] = "CMIP5"

    error_msg = re.escape(
        "CMIP5 data does not contain information about the branch time "
        "in the child's time axis"
    )
    with pytest.raises(ValueError, match=error_msg):
        get_branch_time(junk_data, parent=False)


def test_get_branch_time_cmip5_no_parent_path_error(junk_data):
    junk_data["mip_era"] = "CMIP5"

    error_msg = re.escape("If using cmip5 data, you must provide `parent_path`")
    with pytest.raises(ValueError, match=error_msg):
        get_branch_time(junk_data)


def test_get_branch_time_cmip6_child_no_source_path_error(junk_data):
    error_msg = re.escape(
        "If not requesting parent data, you must provide `source_path`"
    )
    with pytest.raises(ValueError, match=error_msg):
        get_branch_time(junk_data, parent=False)


@pytest.mark.parametrize(
    "start,expected",
    (
        ("(child)", "(parent)"),
        ("(parent)", "(grandparent)"),
        ("(grandparent)", "(greatgrandparent)"),
        ("(greatgrandparent)", "(greatgreatgrandparent)"),
        ("(greatgreatgreatgreatgrandparent)", "(greatgreatgreatgreatgreatgrandparent)"),
    ),
)
def test_step_up_family_tree(start, expected):
    assert step_up_family_tree(start) == expected


@pytest.mark.parametrize(
    "start,expected,cmip5",
    (
        (
            {
                "parent_activity_id": "CMIP",
                "parent_experiment_id": "historical",
                "parent_mip_era": "CMIP6",
                "parent_source_id": "UoM",
                "parent_variant_label": "r1i1p1f1",
                "other_meta": "something",
            },
            {
                "parent_activity_id": "CMIP",
                "parent_experiment_id": "historical",
                "parent_mip_era": "CMIP6",
                "parent_source_id": "UoM",
                "parent_member_id": "r1i1p1f1",
            },
            False,
        ),
        (
            {
                "parent_activity_id": "C M I P",
                "parent_experiment_id": "p i C o n t r o l",
                "parent_mip_era": "C M I P 6",
                "parent_source_id": "C N R M - C M6-1-H R",
                "parent_variant_label": "r 1i1p1f 2",
            },
            {
                "parent_activity_id": "CMIP",
                "parent_experiment_id": "piControl",
                "parent_mip_era": "CMIP6",
                "parent_source_id": "CNRM-CM6-1-HR",
                "parent_member_id": "r1i1p1f2",
            },
            False,
        ),
        (
            {
                "parent_experiment": "piControl",
                "parent_experiment_id": "piControl",
                "parent_experiment_rip": "r1i1p1",
                "other_meta": "something",
            },
            {
                "parent_experiment": "piControl",
                "parent_experiment_id": "piControl",
                "parent_ensemble_member": "r1i1p1",
            },
            True,
        ),
    ),
)
def test_get_parent_replacements(junk_data, start, expected, cmip5):
    junk_data.metadata = start

    if cmip5:
        junk_data["mip_era"] = "CMIP5"
    else:
        junk_data["mip_era"] = "CMIP6"

    assert get_parent_replacements(junk_data) == expected


def test_get_parent_replacements_no_rip_error(junk_data):
    junk_data["mip_era"] = "CMIP5"
    error_msg = re.escape("No `parent_experiment_rip` in metadata")
    with pytest.raises(KeyError, match=error_msg):
        get_parent_replacements(junk_data)


def test_get_parent_replacements_no_parent_variant_label_error(junk_data):
    junk_data["mip_era"] = "CMIP6"
    error_msg = re.escape("No `parent_variant_label` in metadata")
    with pytest.raises(KeyError, match=error_msg):
        get_parent_replacements(junk_data)
