from unittest import TestCase
from x7.lib.annotations import tests
from x7.lib import subclasses


@tests(subclasses)
class TestModSubclasses(TestCase):
    """Tests for stand-alone functions in x7.lib.subclasses module"""

    @tests(subclasses.all_subclasses)
    @tests(subclasses.all_subclasses_gen)
    def test_all_subclasses(self):
        class A:
            pass

        class B(A):
            pass

        class C(B):
            pass

        class D(B):
            pass

        class E(A):
            pass

        self.assertEqual(subclasses.all_subclasses(A), [A, B, C, D, E])
        self.assertEqual(subclasses.all_subclasses(B), [B, C, D])
        self.assertEqual(subclasses.all_subclasses(E), [E])
        self.assertGreater(len(subclasses.all_subclasses(BaseException)), 50)   # 125 at last count
