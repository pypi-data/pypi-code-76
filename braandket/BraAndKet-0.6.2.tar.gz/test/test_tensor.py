import unittest
import numpy as np
import bnk


class QTensorTest(unittest.TestCase):
    def test0_init0_duplication(self):
        ket_space1 = bnk.KetSpace(1)
        ket_space2 = bnk.KetSpace(2)

        try:
            bnk.QTensor([ket_space1, ket_space2, ket_space1], np.zeros([1, 2, 1]))
            self.assertTrue(False, "Should raise ValueError when spaces duplicated")
        except ValueError:
            pass

        bra_space1 = ket_space1.ct
        bra_space1_copy = bnk.BraSpace(ket_space1)
        try:
            bnk.QTensor([bra_space1, ket_space2, bra_space1_copy], np.zeros([1, 2, 1]))
            self.assertTrue(False, "Should raise ValueError when spaces duplicated")
        except ValueError:
            pass

    def test0_init1_shape(self):
        space1 = bnk.KetSpace(2)
        space2 = bnk.KetSpace(3)

        spaces = (space1, space2)
        shapes = (2, 3)

        tensor = bnk.QTensor(spaces, np.zeros(shapes))
        self.assertTrue(tensor.values.shape == shapes)

        try:
            bnk.QTensor(spaces, np.zeros([2, 2]))
            self.assertTrue(False, "Should raise ValueError when spaces duplicated")
        except ValueError:
            pass
