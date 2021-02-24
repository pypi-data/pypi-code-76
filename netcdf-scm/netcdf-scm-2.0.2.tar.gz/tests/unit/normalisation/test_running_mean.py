from base_normalisation_unit import NormaliserTester

from netcdf_scm.normalisation import NormaliserRunningMean


class TestRunningMean(NormaliserTester):
    tclass = NormaliserRunningMean

    def test_method_name(self):
        assert self.tclass().method_name == "21-yr-running-mean"


class TestRunningMean30Year(NormaliserTester):
    tclass = NormaliserRunningMean

    def test_method_name(self):
        assert self.tclass(nyears=30).method_name == "30-yr-running-mean"
