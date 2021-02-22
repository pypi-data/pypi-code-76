from unittest import TestCase
import matplotlib.pyplot as plt
from x7.lib.annotations import tests
from x7.geom import testing
from x7.geom.bezier import ControlPoint
from x7.geom.colors import Pen, PenBrush, Brush
from x7.geom.geom import Point, Vector, PointRelative, BBox
from x7.geom.model import ElemRectangle
from x7.geom.testing import TestCaseGeomExtended
from x7.geom.transform import Transform


@tests(testing.ExtendedMatcherControlPoint)
class TestExtendedMatcherControlPoint(TestCaseGeomExtended):
    @tests(testing.ExtendedMatcherControlPoint.__init__)
    @tests(testing.ExtendedMatcherControlPoint.almost_equal)
    @tests(testing.ExtendedMatcherControlPoint.explain_mismatch)
    def test_cp(self):
        cp1 = ControlPoint(Point(1, 1), Vector(1, 1), Vector(-1, 1))
        cp2 = ControlPoint(Point(1, 1), Vector(1, 1), Vector(-1, 1))
        cp3 = ControlPoint(Point(1, 1), Vector(1, 1), Vector(-1, 1.000000001))
        cp4 = ControlPoint(Point(1, 1), Vector(1, 1), Vector(-1, 1.01))
        self.assertEqual(cp1, cp2)
        self.assertNotEqual(cp1, cp3)
        self.assertAlmostEqual(cp1, cp3)
        # TODO-self.assertNotAlmostEqual(cp1, cp4)
        with self.assertRaisesRegex(AssertionError, 'ControlPoint.*Point.*Vector.*Vector.*== ControlPoint.*Point.*Vector.*Vector'):
            self.assertNotEqual(cp1, cp2)
        with self.assertRaisesRegex(AssertionError, 'ControlPoint.*Point.*Vector.*Vector.*!= ControlPoint.*Point.*Vector.*Vector.*1.000000001'):
            self.assertEqual(cp1, cp3)
        with self.assertRaisesRegex(AssertionError, 'y: 1 != 1.01 within 7 places'):
            self.assertAlmostEqual(cp1, cp4)


@tests(testing.ExtendedMatcherGeomXY)
class TestExtendedMatcherGeomXY(TestCaseGeomExtended):
    @tests(testing.ExtendedMatcherGeomXY.__init__)
    @tests(testing.ExtendedMatcherGeomXY.almost_equal)
    @tests(testing.ExtendedMatcherGeomXY.explain_mismatch)
    def test_pt(self):
        zz = Point(0, 0)
        pt1 = PointRelative(1, 1, zz)
        pt2 = PointRelative(1, 1, zz)
        pt3 = PointRelative(1, 1.000000001, zz)
        pt4 = PointRelative(-1, 1.01, zz)
        self.assertEqual(pt1, pt2)
        self.assertNotEqual(pt1, pt3)
        self.assertAlmostEqual(pt1, pt3)
        # TODO-self.assertNotAlmostEqual(pt1, pt4)
        with self.assertRaisesRegex(AssertionError, 'PointRelative.* == PointRelative'):
            self.assertNotEqual(pt1, pt2)
        with self.assertRaisesRegex(AssertionError, 'PointRelative.* != PointRelative.*1.000000001'):
            self.assertEqual(pt1, pt3)
        with self.assertRaisesRegex(AssertionError, 'y: 1 != 1.01 within 7 places'):
            self.assertAlmostEqual(pt1, pt4)


@tests(testing.ExtendedMatcherPoint)
class TestExtendedMatcherPoint(TestCaseGeomExtended):
    @tests(testing.ExtendedMatcherPoint.__init__)
    @tests(testing.ExtendedMatcherPoint.almost_equal)
    @tests(testing.ExtendedMatcherPoint.explain_mismatch)
    def test_pt(self):
        pt1 = Point(1, 1)
        pt2 = Point(1, 1)
        pt3 = Point(1, 1.000000001)
        pt4 = Point(-1, 1.01)
        self.assertEqual(pt1, pt2)
        self.assertNotEqual(pt1, pt3)
        self.assertAlmostEqual(pt1, pt3)
        # TODO-self.assertNotAlmostEqual(pt1, pt4)
        with self.assertRaisesRegex(AssertionError, 'Point.* == Point'):
            self.assertNotEqual(pt1, pt2)
        with self.assertRaisesRegex(AssertionError, 'Point.* != Point.*1.000000001'):
            self.assertEqual(pt1, pt3)
        with self.assertRaisesRegex(AssertionError, 'y: 1 != 1.01 within 7 places'):
            self.assertAlmostEqual(pt1, pt4)


@tests(testing.ExtendedMatcherVector)
class TestExtendedMatcherVector(TestCaseGeomExtended):
    @tests(testing.ExtendedMatcherVector.__init__)
    @tests(testing.ExtendedMatcherVector.almost_equal)
    @tests(testing.ExtendedMatcherVector.explain_mismatch)
    def test_vec(self):
        vec1 = Vector(1, 1)
        vec2 = Vector(1, 1)
        vec3 = Vector(1, 1.000000001)
        vec4 = Vector(-1, 1.01)
        self.assertEqual(vec1, vec2)
        self.assertNotEqual(vec1, vec3)
        self.assertAlmostEqual(vec1, vec3)
        # TODO-self.assertNotAlmostEqual(vec1, vec4)
        with self.assertRaisesRegex(AssertionError, 'Vector.* == Vector'):
            self.assertNotEqual(vec1, vec2)
        with self.assertRaisesRegex(AssertionError, 'Vector.* != Vector.*1.000000001'):
            self.assertEqual(vec1, vec3)
        with self.assertRaisesRegex(AssertionError, 'y: 1 != 1.01 within 7 places'):
            self.assertAlmostEqual(vec1, vec4)


@tests(testing.PicklerExtensionGeom)
class TestPicklerExtensionGeom(TestCaseGeomExtended):
    SAVE_MATCH = False

    @tests(testing.PicklerExtensionGeom.__init__)
    @tests(testing.PicklerExtensionGeom.do_pickle)
    @tests(testing.PicklerExtensionGeom.methods)
    def test_picklers(self):
        data = [
            BBox(1, 2, 3, 4),
            Point(1, 2),
            Vector(3, 4),
            ControlPoint(Point(1, 2), Vector(3, 4), Vector(5, 6), 'sharp'),
            Pen('red', 1.5),
            Brush('blue'),
            PenBrush(Pen('green', 0.5), '#808080'),
            Transform((1.6, 2.5, 3.4, 4.3, 5.2, 6.1)),
            ElemRectangle('r1', PenBrush('red'), Point(1, 2), Point(-3, -4)),
        ]
        data_dict = {}
        for datum in data:
            name = type(datum).__name__
            data_dict[name] = datum
            with self.subTest(name=name):
                self.assertMatch(datum, case=name)
        self.assertMatch(data, case='all as list')
        self.assertMatch(data_dict, case='all as dict')
        self.assertMatch([Point(1, 2), Point(3, 4)], case='point list')
        self.assertMatch([Point(1, 2), Vector(3, 4)], case='point-vector list')
        self.assertMatch(dict(p1=Point(1, 2), p2=Point(3, 4)), case='point dict')
        self.assertMatch([Point(1, 2), Vector(3, 4), '5,6', 7.8], case='point-vector-str-float list')


@tests(testing.PlotMatchContextManager)
class TestPlotMatchContextManager(TestCase):
    @tests(testing.PlotMatchContextManager.__enter__)
    def test___enter__(self):
        # __enter__(self)
        pass  # TODO-impl x7.geom.testing.PlotMatchContextManager.__enter__ test

    @tests(testing.PlotMatchContextManager.__exit__)
    def test___exit__(self):
        # __exit__(self, exc_type, exc_val, exc_tb)
        pass  # TODO-impl x7.geom.testing.PlotMatchContextManager.__exit__ test

    @tests(testing.PlotMatchContextManager.__init__)
    def test___init__(self):
        # __init__(self, shrink, case, func, test_case: x7.testing.extended.TestCaseExtended)
        pass  # TODO-impl x7.geom.testing.PlotMatchContextManager.__init__ test


@tests(testing.TestCaseGeomExtended)
class TestTestCaseGeomExtended(TestCaseGeomExtended):
    SAVE_MATCH = False

    @tests(testing.TestCaseGeomExtended.assertMatchImage)
    def test_assertMatchImage(self):
        # assertMatchImage(self, new_data, case='0', func=None, cls=None)
        pass  # TODO-impl x7.geom.testing.TestCaseGeomExtended.assertMatchImage test

    @tests(testing.TestCaseGeomExtended.assertMatchPlot)
    def test_assertMatchPlot(self):
        # assertMatchPlot(self, shrink=10, case='0', func=None)
        with self.assertMatchPlot(shrink=10):
            plt.plot([1, 2, 3], [0, 3, 1])
            plt.title('Something')

    @tests(testing.TestCaseGeomExtended.simple_dc)
    def test_simple_dc(self):
        # simple_dc(size=1000) -> x7.geom.drawing.DrawingContext
        pass  # TODO-impl x7.geom.testing.TestCaseGeomExtended.simple_dc test


@tests(testing)
class TestModTesting(TestCase):
    """Tests for stand-alone functions in x7.geom.testing module"""

    @tests(testing.all_subclasses)
    def test_all_subclasses(self):
        # all_subclasses(cls)
        pass  # TODO-impl x7.geom.testing.all_subclasses test

    @tests(testing.fig_to_image)
    def test_fig_to_image(self):
        # fig_to_image(shrink=10) -> '__import__("PIL.Image").Image'
        pass  # TODO-impl x7.geom.testing.fig_to_image test
