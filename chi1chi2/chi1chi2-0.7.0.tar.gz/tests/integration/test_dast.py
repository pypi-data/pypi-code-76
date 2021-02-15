from tests.integration.test_runner import ITTests, _get_options, _get_from_fra_options, _get_from_crystal_options, \
    _get_input_preparator_options, _get_main_options, _get_analysis_options


class DASTITTests(ITTests):
    def test_from_fra_DAST(self):
        params = {
            "case": "dast_input",
            "options": _get_options(_get_from_fra_options("asym.fra")),
            "module-method": ["chi1chi2.from_fra", "run"]
        }
        self._run_it(params)

    def test_from_crystal_DAST(self):
        params = {
            "case": "dast_crystal",
            "options": _get_options(_get_from_crystal_options("dast.inp", "opt.out", "opt.SCFLOG")),
            "module-method": ["chi1chi2.from_crystal", "run"]
        }
        self._run_it(params)

    def test_input_preparator_DAST(self):
        params = {
            "case": "dast_input_preparator",
            "options": _get_options(_get_input_preparator_options("dast.inp", "100.")),
            "module-method": ["chi1chi2.input_preparator", "run"]
        }
        self._run_it(params)

    def test_lft_DAST(self):
        params = {
            "case": "dast_lft",
            "options": _get_options(_get_main_options("dast.inp", "L.dat", "bchf", None, None, True)),
            "module-method": ["chi1chi2.main", "run"]
        }
        self._run_it(params)

    def test_lft_qlft_DAST(self):
        params = {
            "case": "dast_lft_qlft",
            "options": _get_options(_get_main_options("dast.inp", "L.dat", "bchf", None, "bp", True)),
            "module-method": ["chi1chi2.main", "run"]
        }
        self._run_it(params)

    def test_lft_analysis_DAST(self):
        params = {
            "case": "dast_analysis_lft",
            "options": _get_options(_get_analysis_options("dast_lft.out")),
            "module-method": ["chi1chi2.analyze", "run"]
        }
        self._run_it(params)

    def test_qlft_analysis_DAST(self):
        params = {
            "case": "dast_analysis_qlft",
            "options": _get_options(_get_analysis_options("dast_qlft.out")),
            "module-method": ["chi1chi2.analyze", "run"]
        }
        self._run_it(params)

    def test_lft_qlft_v2_DAST(self):
        params = {
            "case": "dast_lft_qlft_v2",
            "options": _get_options(_get_main_options("dast.inp", "L.dat", "bchf", None, "bp")),
            "module-method": ["chi1chi2.main", "run"]
        }
        self._run_it(params)

    def test_lft_qlft_v2_DAST_old_dist(self):
        params = {
            "case": "dast_lft_qlft_v2_old_dist",
            "options": _get_options(_get_main_options("dast.inp", "L.dat", "bchf", None, "bp",
                                                      multiplicative=False, old_dist_format=True)),
            "module-method": ["chi1chi2.main", "run"]
        }
        self._run_it(params)

    def test_qlft_analysis_v2_DAST(self):
        params = {
            "case": "dast_analysis_qlft_v2",
            "options": _get_options(_get_analysis_options("dast_qlft.out")),
            "module-method": ["chi1chi2.analyze", "run"]
        }
        self._run_it(params)
