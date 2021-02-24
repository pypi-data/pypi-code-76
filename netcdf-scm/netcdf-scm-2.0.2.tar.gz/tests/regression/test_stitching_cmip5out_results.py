from os.path import join

import pytest
from click.testing import CliRunner

from netcdf_scm.cli import cli


@pytest.mark.parametrize(
    "out_format",
    (
        [
            "mag-files",
            "magicc-input-files-average-year-start-year",
            "magicc-input-files-point-start-year",
        ]
    ),
)
def test_stitching_and_normalise_results(
    tmpdir,
    update_expected_files,
    test_marble_cmip5_crunch_output,
    test_marble_cmip5_stitch_output,
    run_wrangling_comparison,
    out_format,
    normalisation_method,
):
    input_dir = test_marble_cmip5_crunch_output
    output_dir = join(str(tmpdir), normalisation_method)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "stitch",
            input_dir,
            output_dir,
            "cmip6output stitching with {} normalisation regression test".format(
                normalisation_method
            ),
            "--drs",
            "MarbleCMIP5",
            "-f",
            "--number-workers",
            1,
            "--out-format",
            out_format,
            # have to avoid files which will fail normalising
            "--regexp",
            ".*rcp45.*tas.*NorESM1.*",
            "--normalise",
            normalisation_method,
        ],
    )
    assert result.exit_code == 0, result.output

    run_wrangling_comparison(
        join(output_dir, "cmip5"),
        join(
            test_marble_cmip5_stitch_output,
            "normalised",
            normalisation_method,
            out_format,
            "cmip5",
        ),
        update=update_expected_files,
    )
