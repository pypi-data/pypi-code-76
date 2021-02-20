from math import sqrt

from x7.lib.annotations import tests

import x7.geom.plot_utils
from x7.geom.testing import TestCaseGeomExtended
from x7.geom import utils
from x7.geom.geom import Point, PointRelative, Vector
from x7.geom.utils import *


@tests(utils)
class TestModUtils(TestCaseGeomExtended):
    """Tests for stand-alone functions in x7.geom.utils module"""

    @tests(utils.arc)
    def test_arc(self):
        # arc(r, sa, ea, c=Point(0, 0), steps=-1) -> List[Tuple[float, float]]
        pass  # TODO-impl x7.geom.utils.arc test

    @tests(utils.check_point_list)
    def test_check_point_list(self):
        check_point_list([])
        check_point_list([Point(0, 0)])
        check_point_list([Point(0, 0), PointRelative(1, 2, Point(3, 4))])

    @tests(utils.check_point_list)
    def test_check_point_list_errors(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            check_point_list(['a'])
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            check_point_list([3.5])
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            check_point_list([(1, 2)])

    @tests(utils.circle)
    def test_circle(self):
        # circle(r, c=Point(0, 0)) -> List[Tuple[float, float]]
        pts = circle(1)
        self.assertEqual(361, len(pts))
        self.assertAlmostEqual(pts[180], (-1, 0))
        self.assertAlmostEqual(pts[0], pts[-1])
        pts = circle(1, Point(1, 0))
        self.assertEqual(361, len(pts))
        self.assertAlmostEqual(pts[180], (0, 0))
        self.assertAlmostEqual(pts[0], pts[-1])

    @tests(utils.min_rotation)
    def test_min_rotation(self):
        # min_rotation(target_degrees, source_degrees)
        self.assertEqual(10, min_rotation(20, 10))
        self.assertEqual(10, min_rotation(-340, 10))
        self.assertEqual(10, min_rotation(20, 370))

    @tests(utils.path_rotate)
    def test_path_rotate(self):
        # path_rotate(path: Iterable[ForwardRef('BasePoint')], angle, as_pt=False) -> List[Union[ForwardRef('BasePoint'), Tuple[float, float]]]
        path = [Point(0, 0), Point(1, 0)]
        self.assertAlmostEqual([Point(0, 0), Point(0, 1)], path_rotate(path, -90, as_pt=True))
        self.assertAlmostEqual([(0, 0), (0, 1)], path_rotate(path, -90))
        v = sqrt(2) / 2
        self.assertAlmostEqual([Point(0, 0), Point(v, v)], path_rotate(path, -45, as_pt=True))

    @tests(utils.path_rotate_ccw)
    def test_path_rotate(self):
        # path_rotate_ccw(path: Iterable[ForwardRef('BasePoint')], angle, as_pt=False) -> List[Union[ForwardRef('BasePoint'), Tuple[float, float]]]
        path = [Point(0, 1), Point(1, 0)]
        self.assertAlmostEqual([Point(-1, 0), Point(0, 1)], path_rotate_ccw(path, 90, as_pt=True))
        self.assertAlmostEqual([(-1, 0), (0, 1)], path_rotate_ccw(path, 90))
        v = sqrt(2) / 2
        self.assertAlmostEqual([Point(-v, v), Point(v, v)], path_rotate_ccw(path, 45, as_pt=True))

    @tests(utils.path_translate)
    def test_path_translate(self):
        path = [Point(0, 0), Point(1, 2)]
        self.assertEqual([Point(1, 3), Point(2, 5)], path_translate(path, Vector(1, 3), as_pt=True))
        self.assertEqual([(1, 3), (2, 5)], path_translate(path, Vector(1, 3)))
        self.assertEqual([Point(-1, -3), Point(0, -1)], path_translate(path, Point(-1, -3), as_pt=True))
        self.assertEqual([(-1, -3), (0, -1)], path_translate(path, Point(-1, -3)))

    @tests(utils.path_to_xy)
    def test_path_to_xy(self):
        self.assertEqual([(0, 0), (1, 2)], path_to_xy([Point(0, 0), Point(1, 2)]))

    @tests(utils.path_from_xy)
    def test_path_to_xy(self):
        self.assertEqual([Point(0, 0), Point(1, 2)], path_from_xy([(0, 0), (1, 2)]))

    @tests(x7.geom.plot_utils.plot)
    def test_plot(self):
        # plot(xy: Iterable[ForwardRef('BasePoint')], color='black', label=None, plotter=None)
        pass  # TODO-impl x7.geom.utils.plot test

    @tests(x7.geom.plot_utils.plot_show)
    def test_plot_show(self):
        # plot_show()
        pass  # TODO-impl x7.geom.utils.plot_show test
