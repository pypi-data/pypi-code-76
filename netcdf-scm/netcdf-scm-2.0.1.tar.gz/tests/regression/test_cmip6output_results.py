from os.path import join

import pytest
import regionmask
from click.testing import CliRunner

from netcdf_scm.cli import cli


@pytest.mark.parametrize("table_id", ["Amon", "AERmon", "Omon", "Lmon", "Emon"])
def test_crunching(
    tmpdir,
    update_expected_files,
    test_data_cmip6output_dir,
    test_cmip6_crunch_output,
    run_crunching_comparison,
    table_id,
):
    input_dir = test_data_cmip6output_dir
    output_dir = str(tmpdir)
    regions_to_get = [
        "World",
        "World|Northern Hemisphere",
        "World|Southern Hemisphere",
        "World|Land",
        "World|Ocean",
        "World|Northern Hemisphere|Land",
        "World|Southern Hemisphere|Land",
        "World|Northern Hemisphere|Ocean",
        "World|Southern Hemisphere|Ocean",
        "World|North Atlantic Ocean",
        "World|El Nino N3.4",
    ]

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "crunch",
            input_dir,
            output_dir,
            "cmip6output crunching regression test",
            "--drs",
            "CMIP6Output",
            "-f",
            "--small-number-workers",
            1,
            "--regions",
            ",".join(regions_to_get),
            "--regexp",
            ".*{}.*".format(table_id),
        ],
    )
    assert result.exit_code == 0, result.output
    run_crunching_comparison(
        join(output_dir, "netcdf-scm-crunched", "CMIP6"),
        join(test_cmip6_crunch_output, table_id, "CMIP6"),
        update=update_expected_files,
    )


def test_crunching_ar6regions(
    tmpdir,
    update_expected_files,
    test_data_cmip6output_dir,
    test_cmip6_crunch_output,
    run_crunching_comparison,
):
    input_dir = test_data_cmip6output_dir
    output_dir = str(tmpdir)
    regions_to_get = [
        "World|AR6|{}".format(v) for v in regionmask.defined_regions.ar6.all.abbrevs[:3]
    ]

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "crunch",
            input_dir,
            output_dir,
            "cmip6output crunching regression test",
            "--drs",
            "CMIP6Output",
            "-f",
            "--small-number-workers",
            1,
            "--regions",
            ",".join(regions_to_get),
            "--regexp",
            ".*NCAR.*tas.*",
        ],
    )
    assert result.exit_code == 0, result.output
    run_crunching_comparison(
        join(output_dir, "netcdf-scm-crunched", "CMIP6"),
        join(test_cmip6_crunch_output, "..", "ar6regions-crunching", "CMIP6"),
        update=update_expected_files,
    )
