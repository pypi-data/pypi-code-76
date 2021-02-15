from unittest import TestCase
from x7.lib.annotations import tests
from x7.lib import iters
from x7.lib.iters import t_range


@tests(iters)
class TestModIters(TestCase):
    """Tests for stand-alone functions in x7.geom.iters module"""

    @tests(t_range)
    def test_t_range(self):
        # TODO-should be using almostEquals from TestCaseExtended
        self.assertEqual([0, 0.5, 1.0], list(t_range(2)))
        self.assertEqual([1, 1.5, 2.0], list(t_range(2, 1, 2)))
        self.assertEqual([0, -0.5, -1.0], list(t_range(2, 0, -1)))
        self.assertEqual([0, 0.5], list(t_range(2, closed=False)))
        self.assertEqual([0.5, 1.0], list(t_range(2, closed_start=False)))
        self.assertEqual([0.5], list(t_range(2, closed=False, closed_start=False)))

    @tests(iters.iter_rotate)
    def test_iter_rotate(self):
        self.assertEqual([('c', 'a', 'b'), ('a', 'b', 'c'), ('b', 'c', 'a')], list(iters.iter_rotate('abc', 3, -1)))
        self.assertEqual([('a', 'b', 'c'), ('b', 'c', 'a'), ('c', 'a', 'b')], list(iters.iter_rotate('abc', 3, 0)))
        self.assertEqual([('a', 'b'), ('b', 'c'), ('c', 'a')], list(iters.iter_rotate('abc', 2, 0)))

        self.assertEqual([('c', 'a', 'b'), ('a', 'b', 'c')], list(iters.iter_rotate('abc', 3, -1, cycle=False)))
        self.assertEqual([('a', 'b', 'c'), ('b', 'c', 'a')], list(iters.iter_rotate('abc', 3, 0, cycle=False)))
        self.assertEqual([('a', 'b'), ('b', 'c')], list(iters.iter_rotate('abc', 2, 0, cycle=False)))

    @tests(iters.xy_flatten)
    def test_flatten_xy(self):
        self.assertEqual([1, 2, 3, 4], list(iters.xy_flatten([(1, 2), (3, 4)])))

    @tests(iters.xy_iter)
    def test_xyiter(self):
        self.assertEqual([(1, 2), (3, 4)], list(iters.xy_iter([1, 2, 3, 4])))

