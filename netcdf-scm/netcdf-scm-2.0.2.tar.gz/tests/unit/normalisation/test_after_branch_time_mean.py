from base_normalisation_unit import NormaliserTester

from netcdf_scm.normalisation import AfterBranchTimeMean


class TestRunningMean(NormaliserTester):
    tclass = AfterBranchTimeMean

    def test_method_name(self):
        assert self.tclass().method_name == "31-yr-mean-after-branch-time"
