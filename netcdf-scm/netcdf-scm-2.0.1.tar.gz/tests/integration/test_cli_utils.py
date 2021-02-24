import pytest

from netcdf_scm.cli_utils import _match_regexp_list


@pytest.mark.parametrize(
    "regexp",
    (
        ".*tas.*",
        ".*/piControl/.*mon.*/(tas|fLUC)/(gr|gn)/.*",
        ".*/(piControl|.*)/.*mon.*/(tas|fLUC)/(gr|gn)/.*",
        ".*(.*).*/(piControl|.*)/.*mon.*/(tas|fLUC)/(gr|gn)/.*",
        # # this test takes ages to run because of the multiple capturing groups
        # # so off by default
        # ".*(.*).*/(piControl|.*)/.*mon.*(.*).*/(tas|fLUC)/(gr|gn)/.*",
    ),
)
@pytest.mark.parametrize(
    "inp_to_test",
    (
        (
            "./netcdf-scm/tests/test-data/cmip6output/CMIP6/ScenarioMIP/BCC/BCC-CSM2-MR/ssp126/r1i1p1f1/Amon/tas/gn/v20190314",
            "./netcdf-scm/tests/test-data/cmip6output/CMIP6/ScenarioMIP/BCC/BCC-CSM2-MR/ssp126/r1i1p1f1/Emon/fLUC/gn/v20190314",
            "./netcdf-scm/tests/test-data/cmip6output/CMIP6/ScenarioMIP/BCC/BCC-CSM2-MR/ssp126/r1i1p1f1/Omon/hfds/gn/v20190314",
        ),
    ),
)
@pytest.mark.parametrize("inp_scale_factor", (1, 2, 3, 4))
@pytest.mark.benchmark(max_time=1.0, min_rounds=1)
def test_regexp_match(benchmark, regexp, inp_to_test, inp_scale_factor):
    """
    Toy test function to examine the impact on match speed of using regexp
    of different complexity. Maybe one day we can update _match_regexp_list so
    it can handle super complex regexp using something like
    https://stackoverflow.com/a/42789508
    """
    inp_to_test = inp_to_test * inp_scale_factor

    res = benchmark(_match_regexp_list, inp_to_test, regexp)

    assert not any(["hdfs" in v for v in res])
