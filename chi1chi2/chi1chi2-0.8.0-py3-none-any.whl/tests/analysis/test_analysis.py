import unittest

import numpy as np

from chi1chi2.core.property import Chi, Chi2
from chi1chi2.core.property_reader import _exctract_non_zero_chi, _translate_chi_indices, \
    _extract_non_zero_chi2, _translate_chi2_indices
from chi1chi2.utils.constants import simeq


class TestAnalysis(unittest.TestCase):
    def test_refr_ind_orthogonal(self):
        chi1 = Chi(np.diag([1, 2, 3]))
        exptd_refr_ind = [np.sqrt(chi1.tensor[i, i] + 1) for i in range(3)]

        refr_ind, _ = chi1.refr_ind_rot_mat()

        self.assertListEqual(exptd_refr_ind, refr_ind)

    def test_refr_ind_monoclinic(self):
        raw_chi = np.array([1.8, 0, -.3, 0, 1, 0, -.3, 0, 2]).reshape((3, 3))
        chi1 = Chi(raw_chi)
        exptd_refr_ind = [1.60741166, 1.41421356, 1.79338444]

        refr_ind, _ = chi1.refr_ind_rot_mat()

        for i in range(3):
            self.assertTrue(simeq(exptd_refr_ind[i], refr_ind[i]))

    def test_should_translate_ind_chi_to_abc(self):
        chi = Chi(np.arange(1, 10).reshape((3, 3)))
        _, chi_indices = _exctract_non_zero_chi(chi)
        exptd_indices_translated = (
            "a'a'",
            "bb",
            "c*c*",
            "a'b",
            "a'c*",
            "bc*",
        )

        indices = _translate_chi_indices(chi_indices)

        self.assertTupleEqual(exptd_indices_translated, indices)

    def test_should_translate_ind_chi2_to_123(self):
        chi2 = Chi2(np.arange(1, 28).reshape((3, 3, 3)))
        _, chi_indices = _extract_non_zero_chi2(chi2)
        exptd_indices_translated = (
            "111", "112", "211", "113", "311", "122", "212", "222", "123", "213", "312", "133", "313", "223", "322",
            "233", "323", "333"
        )

        indices = _translate_chi2_indices(chi_indices)

        self.assertTupleEqual(exptd_indices_translated, indices)
