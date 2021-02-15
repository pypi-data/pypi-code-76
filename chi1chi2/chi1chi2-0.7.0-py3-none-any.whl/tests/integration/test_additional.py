from tests.integration.test_runner import ITTests, _get_options, _get_analysis_options


class ITMNATests(ITTests):
    def test_rotation_consistency_check(self):
        params = {
            "case": "sthz2a5mpA",
            "options": _get_options(_get_analysis_options("sthz2a5mpA_m_qlft.out")),
            "module-method": ["chi1chi2.analyze", "run"]
        }
        self._run_it(params)
