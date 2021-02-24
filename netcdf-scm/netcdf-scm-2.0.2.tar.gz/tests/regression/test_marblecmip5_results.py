from os.path import join

import pytest
from click.testing import CliRunner

from netcdf_scm.cli import cli


@pytest.mark.parametrize("table_id", ["Amon", "Omon", "Lmon", "Emon"])
def test_crunching(
    tmpdir,
    update_expected_files,
    test_data_marble_cmip5_dir,
    test_marble_cmip5_crunch_output,
    run_crunching_comparison,
    table_id,
):
    INPUT_DIR = test_data_marble_cmip5_dir
    OUTPUT_DIR = str(tmpdir)
    REGIONS_TO_GET = [
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
            INPUT_DIR,
            OUTPUT_DIR,
            "marblecmip5 crunching regression test",
            "--drs",
            "MarbleCMIP5",
            "-f",
            "--small-number-workers",
            1,
            "--regions",
            ",".join(REGIONS_TO_GET),
            "--regexp",
            ".*{}.*".format(table_id),
        ],
    )
    assert result.exit_code == 0, result.output
    run_crunching_comparison(
        join(OUTPUT_DIR, "netcdf-scm-crunched", "cmip5"),
        join(test_marble_cmip5_crunch_output, table_id, "cmip5"),
        update=update_expected_files,
    )
