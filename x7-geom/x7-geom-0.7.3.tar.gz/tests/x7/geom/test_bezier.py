from x7.geom.bezier import *
from x7.geom import bezier
from x7.geom.geom import Point, Vector, BBox, PointRelative
from x7.geom.transform import Transform
from x7.lib.annotations import tests
from x7.geom.testing import TestCaseGeomExtended


@tests(ControlPoint)
class TestControlPoint(TestCaseGeomExtended):
    @tests(ControlPoint.__init__)
    # @tests(ControlPoint.l)
    # @tests(ControlPoint.r)
    def test_init(self):
        cp = ControlPoint(Point(1, 2), Vector(3, 4), Vector(5, 6))
        self.assertEqual(cp.c, Point(1, 2))
        self.assertEqual(cp.dl, Vector(3, 4))
        self.assertEqual(cp.dr, Vector(5, 6))
        self.assertEqual(cp.kind, 'smooth')
        self.assertEqual(cp.l, Point(4, 6))
        self.assertEqual(cp.r, Point(6, 8))

    @tests(ControlPoint.reversed)
    def test_reversed(self):
        cp = ControlPoint(Point(1, 2), Vector(3, 4), Vector(5, 6))
        cr = cp.reversed()
        self.assertEqual(cp.c, cr.c)
        self.assertEqual(cp.l, cr.r)
        self.assertEqual(cp.r, cr.l)

    @tests(ControlPoint.__repr__)
    @tests(ControlPoint.__str__)
    def test_repr_str(self):
        cp = ControlPoint(Point(1, 2), Vector(3, 4), Vector(5, 6))
        self.assertEqual("(Point(1, 2), Vector(3, 4), Vector(5, 6), 'smooth')", str(cp))
        self.assertEqual("ControlPoint(Point(1, 2), Vector(3, 4), Vector(5, 6), 'smooth')", repr(cp))

    @tests(ControlPoint.__eq__)
    def test_eq(self):
        cp = ControlPoint(Point(1, 2), Vector(3, 4), Vector(5, 6))
        self.assertEqual(cp, ControlPoint(Point(1, 2), Vector(3, 4), Vector(5, 6)))
        self.assertNotEqual(cp, "not even close")
        self.assertNotEqual(cp, ControlPoint(Point(1, 1), Vector(3, 4), Vector(5, 6)))
        self.assertNotEqual(cp, ControlPoint(Point(1, 2), Vector(1, 4), Vector(5, 6)))
        self.assertNotEqual(cp, ControlPoint(Point(1, 2), Vector(3, 4), Vector(1, 6)))
        self.assertNotEqual(cp, ControlPoint(Point(1, 2), Vector(3, 4), Vector(5, 6), 'sharp'))

    @tests(ControlPoint.bbox)
    def test_bbox(self):
        cp = ControlPoint(Point(1, 2), Vector(3, 4), Vector(5, 6))
        self.assertEqual(BBox(1, 2, 6, 8), cp.bbox())
        cp = ControlPoint(Point(1, 2), Vector(-3, -4), Vector(5, 6))
        self.assertEqual(BBox(-2, -2, 6, 8), cp.bbox())

    @tests(ControlPoint.copy)
    def test_copy(self):
        cp = ControlPoint(Point(1, 2), Vector(3, 4), Vector(5, 6))
        cp.c.restore(Point(0, 0))
        self.assertEqual(ControlPoint(Point(0, 0), Vector(3, 4), Vector(5, 6)), cp)
        cp = ControlPoint(Point(1, 2), Vector(3, 4), Vector(5, 6))
        cpc = cp.copy()
        cp.c.restore(Point(0, 0))
        self.assertEqual(ControlPoint(Point(1, 2), Vector(3, 4), Vector(5, 6)), cpc)

    @tests(ControlPoint.fixed)
    def test_fixed(self):
        cp = ControlPoint(PointRelative(1, 2, Point(3, 4)), Vector(3, 4), Vector(5, 6))
        self.assertNotEqual(cp, ControlPoint(Point(4, 6), Vector(3, 4), Vector(5, 6)))
        self.assertEqual(cp.fixed(), ControlPoint(Point(4, 6), Vector(3, 4), Vector(5, 6)))

    @tests(ControlPoint.restore)
    def test_restore(self):
        cp1 = ControlPoint(Point(11, 12), Vector(13, 4), Vector(15, 6), 'sharp')
        cp2 = ControlPoint(Point(1, 2), Vector(3, 4), Vector(5, 6))
        cp1.restore(cp2)
        self.assertEqual(cp1, cp2)
        self.assertIsNot(cp1.c, cp2.c)

    @tests(ControlPoint.round)
    def test_round(self):
        cp1 = ControlPoint(Point(1.123, 2.247), Vector(2.55, 4.499), Vector(5.3, 6.0))
        cp2 = ControlPoint(Point(1, 2), Vector(3, 4), Vector(5, 6))
        self.assertEqual(cp2, cp1.round(0))

    @tests(ControlPoint.transform)
    def test_transform(self):
        cp = ControlPoint(Point(0, 0), Vector(1, 1), Vector(-1, -1), 'very-smooth')
        t = Transform().translate(1, 1).rotate(90).scale(2, 2)
        cpt = cp.transform(t)
        self.assertAlmostEqual(cpt.c, Point(2, -2))
        self.assertAlmostEqual(cpt.dl, Vector(2, -2))
        self.assertAlmostEqual(cpt.dr, Vector(-2, 2))
        self.assertEqual(cpt.kind, 'very-smooth')


@tests(bezier)
class TestModModel(TestCaseGeomExtended):
    """Tests for stand-alone functions in x7.geom.model module"""

    @tests(bez)
    def test_bez(self):
        # bez(raw_pts: Iterable[Union[ForwardRef('BasePoint'), Tuple[numbers.Number, numbers.Number]]], steps=80, as_xy=False)
        pass  # TODO-impl x7.geom.bez test

    @tests(bez_path)
    def test_bez_path(self):
        # bez_path(transform: x7.geom.transform.Transform, cps: List[ForwardRef('ControlPoint')], closed: bool, steps=20)
        pass  # TODO-impl x7.geom.bez_path test

    # noinspection DuplicatedCode
    @tests(bez_self_intersect)
    def test_bez_self_intersect(self):
        # bez_split(cp1: 'ControlPoint', cp2: 'ControlPoint', t=0.5) -> Tuple[ForwardRef('ControlPoint'), ForwardRef('ControlPoint'), ForwardRef('ControlPoint')]
        curve = [
            ControlPoint(Point(0, 0), Vector(0, 1), Vector(0, -1)),
            ControlPoint(Point(2, 0), Vector(0, -1), Vector(0, 1)),
        ]
        self.assertEqual([], bez_self_intersect(curve))

        curve = [
            ControlPoint(Point(0, 0), Vector(0, -1), Vector(0, 1)),
            ControlPoint(Point(2, 0), Vector(0, -1), Vector(0, 1)),
        ]
        expected = [
            [
                ControlPoint(Point(1.0, 0.0), Vector(0.5, 0.25), Vector(0.5, -0.25), 'sharp'),
                ControlPoint(Point(2, 0), Vector(0.0, -0.5), Vector(0.0, 0.5), 'smooth')
            ],
            [
                ControlPoint(Point(1.0, 0.0), Vector(-0.5, 0.25), Vector(-0.5, -0.25), 'sharp'),
                ControlPoint(Point(0, 0), Vector(0.0, -0.5), Vector(0.0, 0.5), 'smooth')
            ]]

        self.assertEqual(expected, bez_self_intersect(curve))

    @tests(bez_split)
    def test_bez_split(self):
        # bez_split(cp1: 'ControlPoint', cp2: 'ControlPoint', t=0.5) -> Tuple[ForwardRef('ControlPoint'), ForwardRef('ControlPoint'), ForwardRef('ControlPoint')]
        pass  # TODO-impl x7.geom.bez_split test
