from tests.integration.test_runner import ITTests, _get_options, _get_from_cif_options, _get_from_crystal_options, \
    _get_input_preparator_options, _get_main_options, _get_analysis_options


class ITMNATests(ITTests):
    def test_from_cif_MNA(self):
        params = {
            "case": "mna_input",
            "options": _get_options(_get_from_cif_options("mna.cif")),
            "module-method": ["chi1chi2.from_cif", "run"]
        }
        self._run_it(params)

    def test_from_crystal_MNA(self):
        params = {
            "case": "mna_crystal",
            "options": _get_options(_get_from_crystal_options("mna.inp", "opt.out", "opt.SCFLOG")),
            "module-method": ["chi1chi2.from_crystal", "run"]
        }
        self._run_it(params)

    def test_input_preparator_MNA(self):
        params = {
            "case": "mna_input_preparator",
            "options": _get_options(_get_input_preparator_options("mna.inp", "100.")),
            "module-method": ["chi1chi2.input_preparator", "run"]
        }
        self._run_it(params)

    def test_lft_MNA(self):
        params = {
            "case": "mna_lft",
            "options": _get_options(_get_main_options("mna.inp", "L.dat", "bchf", None, None, True)),
            "module-method": ["chi1chi2.main", "run"]
        }
        self._run_it(params)

    def test_lft_qlft_MNA(self):
        params = {
            "case": "mna_lft_qlft",
            "options": _get_options(_get_main_options("mna.inp", "L.dat", "bchf", None, "bp", True)),
            "module-method": ["chi1chi2.main", "run"]
        }
        self._run_it(params)

    def test_lft_analysis_MNA(self):
        params = {
            "case": "mna_analysis_lft",
            "options": _get_options(_get_analysis_options("mna_lft.out")),
            "module-method": ["chi1chi2.analyze", "run"]
        }
        self._run_it(params)

    def test_qlft_analysis_MNA(self):
        params = {
            "case": "mna_analysis_qlft",
            "options": _get_options(_get_analysis_options("mna_qlft.out")),
            "module-method": ["chi1chi2.analyze", "run"]
        }
        self._run_it(params)

    def test_lft_qlft_v2_MNA(self):
        params = {
            "case": "dast_lft_qlft_v2",
            "options": _get_options(_get_main_options("dast.inp", "L.dat", "bchf", None, "bp")),
            "module-method": ["chi1chi2.main", "run"]
        }
        self._run_it(params)

    def test_lft_qlft_v2_MNA_old_dist(self):
        params = {
            "case": "dast_lft_qlft_v2_old_dist",
            "options": _get_options(_get_main_options("dast.inp", "L.dat", "bchf", None, "bp",
                                                      multiplicative=False, old_dist_format=True)),
            "module-method": ["chi1chi2.main", "run"]
        }
        self._run_it(params)

    def test_qlft_analysis_v2_MNA(self):
        params = {
            "case": "mna_analysis_qlft_v2",
            "options": _get_options(_get_analysis_options("mna_qlft.out")),
            "module-method": ["chi1chi2.analyze", "run"]
        }
        self._run_it(params)
