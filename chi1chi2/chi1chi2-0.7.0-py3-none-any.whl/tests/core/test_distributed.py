import os
import unittest

import numpy as np

from chi1chi2.core.bulk_property import _scale_dist_v2
from chi1chi2.core.property import DistributedPolar, Polar, Hyper, diagonalize
from chi1chi2.core.property_reader import PropsMol
from chi1chi2.utils.constants import simeq


def file_for_test(file):
    return os.path.join(os.path.dirname(__file__), file)


MOLECULAR_PROPERTIES = file_for_test("prop2.dat")
NUMBER_OF_SUBMOLECULES = 5

properties = PropsMol.from_file(MOLECULAR_PROPERTIES)


class TestDistributed(unittest.TestCase):
    def test_read_polar_from_file(self):
        ref_polarizability = properties.get_or_static("static").polar_w

        distributed = DistributedPolar.from_file(file_for_test("dist2.dat"))

        self.assertTrue(all(simeq(ref_polarizability.tensor.reshape(9)[i],
                                  distributed.to_molecular_polar().tensor.reshape(9)[i],
                                  0.3)
                            for i in range(9)))

    def test_splitting_polar(self):
        polarizability = properties.get_or_static("static").polar_w
        expected_submolecule_polarizability = Polar(polarizability.tensor / NUMBER_OF_SUBMOLECULES)

        distributed = polarizability.to_distributed(NUMBER_OF_SUBMOLECULES)

        self.assertEqual(expected_submolecule_polarizability, distributed.polar_list[0])

    def test_splitting_hyperpol(self):
        hyper = properties.get_or_static("static").hyper_w
        expected_submolecule_hyperpol = Hyper(hyper.tensor / NUMBER_OF_SUBMOLECULES)

        distributed = hyper.to_distributed(NUMBER_OF_SUBMOLECULES)

        self.assertEqual(expected_submolecule_hyperpol, distributed.hyper_list[0])

    def test_scaling_polar(self):
        total = PropsMol.from_file(file_for_test("shg_scaling.dat"))
        distributed = DistributedPolar.from_file(file_for_test("dist_scaling.dat"))

        static = total.get_or_static('static')
        dynamic = total.get_or_static('1064.0')

        distributed_dynamic = _scale_dist_v2(static.polar_w, dynamic.polar_2w, distributed)

        for i, pol in enumerate(distributed_dynamic.polar_list):
            _, diag = diagonalize(pol.tensor)
            prop_values = np.diag(diag)
            self.assertTrue(all(prop_values > 0), f"negatively defined {i + 1}-th tensor: {pol}")

        recalculated_dynamic = distributed_dynamic.to_molecular_polar()
        difference = recalculated_dynamic.tensor - dynamic.polar_2w.tensor
        delta_iso = sum(np.diag(difference)) / 3.
        self.assertAlmostEqual(delta_iso, 0, 0,
                               f"delta_iso change too large: {delta_iso}")
