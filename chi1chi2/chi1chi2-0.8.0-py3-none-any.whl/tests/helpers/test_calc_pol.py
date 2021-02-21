import os
from unittest import TestCase

import numpy as np

from chi1chi2.helpers.calc_pol import calc_distributed_polarizabilities


def path_for_test(file):
    return os.path.join(os.path.dirname(__file__), file)


DIR_LITE = path_for_test("calc_pol/lite")
DIR_ROMBERG = path_for_test("calc_pol/romberg")

mna_polarizability = np.array([[165.683, -17.005, 48.0261],
                               [-17.005, 120.492, -11.0442],
                               [48.0261, -11.0442, 81.9362]])


class TestCalcPol(TestCase):
    def test_should_calculate_atomic_polarizabilities_with_romberg(self):
        polarizabilities = calc_distributed_polarizabilities('mol', os.path.join(DIR_ROMBERG, 'tot.dat'), DIR_ROMBERG)
        actual_summed_polarizability = sum(polar for polar in polarizabilities)
        self.assertAlmostEqual(np.linalg.norm(mna_polarizability - actual_summed_polarizability), 0.2383, 3)

    def test_should_calculate_atomic_polarizabilities_with_lite(self):
        polarizabilities = calc_distributed_polarizabilities('mol', os.path.join(DIR_LITE, 'tot.dat'), DIR_LITE)
        actual_summed_polarizability = sum(polar for polar in polarizabilities)
        self.assertAlmostEqual(np.linalg.norm(mna_polarizability - actual_summed_polarizability), 0.1797, 3)
