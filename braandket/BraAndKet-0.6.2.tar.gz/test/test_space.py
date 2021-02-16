import unittest
import bnk


class SpaceTest(unittest.TestCase):

    def test0_space_repr(self):
        num_space = bnk.NumSpace(3)
        num_space_named = bnk.NumSpace(3, name='n')

        ket_space = bnk.KetSpace(3)
        ket_space_named = bnk.KetSpace(3, name='q')

        bra_space = ket_space.ct
        bra_space_named = ket_space_named.ct

        print(num_space)
        print(num_space_named)

        print(ket_space)
        print(ket_space_named)

        print(bra_space)
        print(bra_space_named)

        self.assertTrue(True)

    def test1_bra_space(self):
        ket_space = bnk.KetSpace(3, name='k')

        bra_space = ket_space.ct
        bra_space2 = bnk.BraSpace(ket_space)

        self.assertIs(bra_space, bra_space2, "Self-created BraSpace not equals.")
        self.assertIs(bra_space.ct, ket_space)
