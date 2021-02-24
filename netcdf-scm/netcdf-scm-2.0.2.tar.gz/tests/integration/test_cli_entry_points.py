import pytest


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.parametrize(
    "entry_point",
    (
        ["netcdf-scm"],
        ["netcdf-scm", "crunch"],
        ["netcdf-scm", "wrangle"],
        ["netcdf-scm", "stitch"],
    ),
)
def test_entry_points(entry_point, script_runner):
    res = script_runner.run(*entry_point, "--help")
    assert res.success
    assert res.stdout
    assert res.stderr == ""
