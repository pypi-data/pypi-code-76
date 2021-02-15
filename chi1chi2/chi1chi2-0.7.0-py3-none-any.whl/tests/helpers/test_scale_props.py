import os
import unittest
from tempfile import mkstemp

from chi1chi2.helpers.scale_props import read_props_and_scale, _read_props


def file_for_test(file):
    return os.path.join(os.path.dirname(__file__), file)


B3LYP_FILE = file_for_test("b.dat")
MP2_FILE = file_for_test("m.dat")
MP2_ADDIT_FILE = file_for_test("m_addit.dat")
MP2_HYBRID_FILE = file_for_test("m_hybrid.dat")


def _compare_dicts(self, prop_dict_ref, prop_dict):
    shape = prop_dict_ref["static"].shape
    n = None
    if shape == (3, 3):
        n = 9
    elif shape == (3, 3, 3):
        n = 27
    for wvl in prop_dict_ref.keys():
        prop_ref = prop_dict_ref[wvl].reshape(n).tolist()
        prop = prop_dict[wvl].reshape(n).tolist()
        [self.assertAlmostEqual(prop_ref[i], prop[i], places=5) for i in range(n)]


class TestScaling(unittest.TestCase):
    def test_additive_should_not_alter_the_some_props(self):
        _, tmp_file = mkstemp()
        try:
            dip_line_ref, pol_dict_ref, bet_dict_ref = _read_props(B3LYP_FILE)
            read_props_and_scale(B3LYP_FILE, B3LYP_FILE, scheme="additive", file_out=tmp_file)

            dip_line, pol_dict, bet_dict = _read_props(tmp_file)
        finally:
            os.remove(tmp_file)

        self.assertEqual(dip_line_ref, dip_line)
        _compare_dicts(self, pol_dict_ref, pol_dict)
        _compare_dicts(self, bet_dict_ref, bet_dict)

    def test_should_scale_additive(self):
        _, tmp_file = mkstemp()
        try:
            dip_line_ref, pol_dict_ref, bet_dict_ref = _read_props(MP2_ADDIT_FILE)
            read_props_and_scale(B3LYP_FILE, MP2_FILE, scheme="additive", file_out=tmp_file)

            dip_line, pol_dict, bet_dict = _read_props(tmp_file)
        finally:
            os.remove(tmp_file)

        self.assertEqual(dip_line_ref, dip_line)
        _compare_dicts(self, pol_dict_ref, pol_dict)
        _compare_dicts(self, bet_dict_ref, bet_dict)

    def test_should_scale_hybrid(self):
        _, tmp_file = mkstemp()
        try:
            dip_line_ref, pol_dict_ref, bet_dict_ref = _read_props(MP2_HYBRID_FILE)
            read_props_and_scale(B3LYP_FILE, MP2_FILE, scheme="hybrid", file_out=tmp_file)

            dip_line, pol_dict, bet_dict = _read_props(tmp_file)
        finally:
            os.remove(tmp_file)

        self.assertEqual(dip_line_ref, dip_line)
        _compare_dicts(self, pol_dict_ref, pol_dict)
        _compare_dicts(self, bet_dict_ref, bet_dict)
