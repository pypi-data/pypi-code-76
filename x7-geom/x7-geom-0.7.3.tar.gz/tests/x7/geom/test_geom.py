import math
from typing import cast
from unittest import TestCase

from x7.geom.testing import TestCaseGeomExtended
from x7.geom.transform import Transform
from x7.geom import geom
from x7.geom.geom import *
from x7.lib.annotations import tests
from x7.testing.extended import TestCaseExtended


class BogusBasePoint(BasePoint):    # pragma: nocover
    def __eq__(self, other):
        return super().__eq__(other)

    def copy(self) -> 'BasePoint':
        ...

    def round(self, digits=0) -> 'BasePoint':
        ...


@tests(BasePoint)
class TestBasePoint(TestCase):
    @tests(BasePoint.__init__)
    @tests(BasePoint.__str__)
    @tests(BasePoint.__repr__)
    @tests(BasePoint._namestr)
    @tests(BasePoint._repr)
    def test_basic(self):
        p = BogusBasePoint('foo')
        self.assertEqual('(0, 0)', str(p))
        self.assertEqual("BogusBasePoint(0, 0, 'foo')", repr(p))

    @tests(BasePoint.__eq__)
    @tests(BasePoint.copy)
    def test_abstracts(self):
        # TODO-maketests should not require tests for abstract methods
        pass

    @tests(BasePoint.__round__)
    @tests(BasePoint.round)
    def test_round(self):
        z = Point(0, 0)
        self.assertEqual(Point(1, 2), PointRelative(1.1234, 2.1234, z).round())
        self.assertEqual(Point(1.1, 2.1), PointRelative(1.1234, 2.1234, z).round(1))
        self.assertEqual(Point(1.14, 2.01), PointRelative(1.135, 2.0051, z).round(2))

    @tests(BasePoint.close)
    def test_close(self):
        base = Point(1, 2)
        self.assertTrue(base.close(Point(1, 2)))
        self.assertTrue(base.close(Point(1+5e-12, 2)))
        self.assertFalse(base.close(Point(1+1e-10, 2)))

    @tests(BasePoint.__add__)
    @tests(BasePoint.add_vector)
    def test_add(self):
        p = Point(0, 1)
        q = Point(3, 2)
        self.assertRaises(TypeError, lambda: p+q)
        v = Vector(-1, -2)
        self.assertEqual(Point(-1, -1), p+v)
        self.assertEqual(Point(-1, -1), v+p)

    @tests(BasePoint.__sub__)
    @tests(BasePoint.sub_vector)
    def test_sub(self):
        p = Point(0, 1)
        q = Point(3, 2)
        self.assertEqual(Vector(3, 1), q-p)
        self.assertEqual(Vector(-3, -1), p-q)
        v = Vector(-1, -2)
        self.assertEqual(Point(1, 3), p-v)
        self.assertRaises(TypeError, lambda: v-p)

    @tests(BasePoint.fixed)
    def test_fixed(self):
        p = BogusBasePoint('foo')
        self.assertEqual(Point(0, 0, 'fixed_foo'), p.fixed())
        q = PointRelative(4, 3, Point(1, 2), 'yup')
        self.assertEqual(Point(5, 5, 'fixed_yup'), q.fixed())

    @tests(BasePoint.mid)
    def test_mid(self):
        self.assertEqual(Point(3, 4), Point(1, 2).mid(Point(5, 6)))

    @tests(BasePoint.parse)
    def test_parse(self):
        p = Point(10, 10)
        q = PointRelative(2, 4, p)
        r = PointCalc(q, -1.5)

        # print(Point.parse((3, 4, 5, 6)))
        # print(Point.parse([p, q, r]))
        # print(Point.parse(((10, 10), p, 10, 10)))
        self.assertEqual([(3, 4), (5, 6)], Point.parse((3, 4, 5, 6)))
        self.assertEqual([(3, 4), (5, 6)], Point.parse(((3, 4), (5, 6))))
        self.assertEqual([p, q, r], Point.parse((p, q, r)))
        self.assertEqual([(11, 11), p, (2, 4)], Point.parse((11, 11, p, 2, 4)))
        self.assertEqual([(11, 11, 12), (2, 4)], Point.parse(((11, 11, 12), 2, 4), allow_thruples=True))
        with self.assertRaisesRegex(ValueError, 'tuples must be'):
            Point.parse(((11, 12, 13), 2, 4), allow_thruples=False)
        with self.assertRaisesRegex(ValueError, 'Missing y value for x=3'):
            Point.parse((3, ))
        with self.assertRaisesRegex(ValueError, 'y value for x=3 must be a number'):
            Point.parse((3, 'no'))
        with self.assertRaisesRegex(ValueError, r'tuples must be x,y or x,y,a, not \(3, 4, 5, 6\)'):
            Point.parse(((3, 4, 5, 6), 2, 4), allow_thruples=True)
        with self.assertRaisesRegex(ValueError, r"Expected x,y or \(x,y\) or Point, not 'no'"):
            # noinspection PyTypeChecker
            Point.parse(('no', ))

    @tests(BasePoint.xy)
    @tests(BasePoint.x)
    @tests(BasePoint.y)
    def test_xy(self):
        b = BogusBasePoint()
        self.assertEqual((0, 0), b.xy())
        self.assertEqual(0, b.x)
        self.assertEqual(0, b.y)
        pr = PointRelative(1, 2, Point(1, 2))
        self.assertEqual(2, pr.x)
        self.assertEqual(4, pr.y)

    @tests(BasePoint.v)
    def test_v(self):
        self.assertEqual(PointRelative(1.2, 3.4, Point(0, 0)).v, Vector(1.2, 3.4))

    @tests(geom.BasePoint.__iter__)
    def test_iter(self):
        p = Point(3, 4.5)
        self.assertEqual((3, 4.5), tuple(p))

    @tests(geom.BasePoint.__neg__)
    def test_neg(self):
        p = Point(3, -4.5)
        self.assertEqual((-3, 4.5), (-p).xy())


@tests(Point)
class TestPoint(TestCase):
    @tests(Point.__init__)
    @tests(Point.__str__)
    @tests(Point.__repr__)
    def test_basic(self):
        p = Point(0, 0, 'foo')
        self.assertEqual('(0, 0)', str(p))
        self.assertEqual("Point(0, 0, 'foo')", repr(p))
        p = Point(0, 0)
        self.assertEqual('(0, 0)', str(p))
        self.assertEqual("Point(0, 0)", repr(p))

    @tests(Point.__eq__)
    def test_eq(self):
        p = Point(1, 2.5)
        q = Point(1, 2.5)
        self.assertEqual(p, q)
        self.assertIsNot(p, q)
        self.assertEqual(p, Point(1.0, 2.5))
        self.assertNotEqual(p, Point(1.001, 2.5))

    @tests(Point.__round__)
    def test___round__(self):
        self.assertEqual(Point(1, 2), round(Point(1.1234, 2.1234)))
        self.assertEqual(Point(1.1, 2.1), round(Point(1.1234, 2.1234), 1))
        self.assertEqual(Point(1.14, 2.01), round(Point(1.135, 2.0051), 2))

    @tests(Point.round)
    def test_round(self):
        self.assertEqual(Point(1, 2), Point(1.1234, 2.1234).round())
        self.assertEqual(Point(1.1, 2.1), Point(1.1234, 2.1234).round(1))
        self.assertEqual(Point(1.14, 2.01), Point(1.135, 2.0051).round(2))

    @tests(Point.setxy)
    def test_setxy(self):
        p = Point(3, 4)
        p.setxy(1, 2)
        self.assertEqual(Point(1, 2), p)

    @tests(Point.x)
    @tests(Point.y)
    @tests(Point.xy)
    def test_xy(self):
        p = Point(3, 4.5)
        self.assertEqual((3, 4.5), p.xy())
        self.assertEqual(3, p.x)
        self.assertEqual(4.5, p.y)

    @tests(Point.v)
    def test_v(self):
        self.assertEqual(Point(1.2, 3.4).v, Vector(1.2, 3.4))

    @tests(geom.Point.copy)
    @tests(geom.Point.restore)
    def test_copy(self):
        p = Point(3, 4.5)
        q = p.copy()
        p.setxy(1, 2)
        self.assertEqual((3, 4.5), q.xy())
        self.assertEqual(Point(1, 2), p)
        p.restore(q)
        self.assertEqual((3, 4.5), p.xy())

    @tests(geom.Point.set)
    def test_set(self):
        p = Point(3, 4)
        p.set(Point(1, 2))
        self.assertEqual(Point(1, 2), p)


@tests(PointCalc)
class TestPointCalc(TestCase):
    @tests(PointCalc.__init__)
    @tests(PointCalc.__str__)
    @tests(PointCalc.__repr__)
    @tests(PointCalc.xy)
    def test_basic(self):
        b = Point(1, 1)
        p = PointRelative(-1, 1, b)
        q = PointCalc(p, 2)
        self.assertEqual((-1, 3), q.xy())
        self.assertEqual('(-1, 3)', str(q))
        self.assertEqual('PointCalc(PointRelative(-1, 1, Point(1, 1)), 2)', repr(q))
        b = Point(1, 1, 'b')
        p = PointRelative(-1, 1, b, 'p')
        q = PointCalc(p, 2, 'q')
        self.assertEqual((-1, 3), q.xy())
        self.assertEqual('(-1, 3)', str(q))
        self.assertEqual("PointCalc(PointRelative(-1, 1, Point(1, 1, 'b'), 'p'), 2, 'q')", repr(q))

    @tests(PointCalc.copy)
    @tests(PointCalc.__eq__)
    def test_copy(self):
        b = Point(1, 1)
        p = PointRelative(-1, 1, b)
        q = PointCalc(p, 2)
        r = q.copy()
        self.assertEqual(q, r)
        p._x = 9
        self.assertEqual(q, r)
        q.scale = 3
        self.assertNotEqual(q, r)

    @tests(PointCalc.round)
    def test_round(self):
        b = Point(1.1, 1.2)
        p = PointRelative(-1.37, 1.81, b)
        q = PointCalc(p, 2.19)
        for idx in [0, 1]:
            self.assertAlmostEqual((-1.9, 5.2)[idx], q.round(1).xy()[idx])


@tests(PointRelative)
class TestPointRelative(TestCase):
    @tests(PointRelative.__init__)
    @tests(PointRelative.__str__)
    @tests(PointRelative.__repr__)
    @tests(geom.PointRelative.xy)
    def test_basic(self):
        b = Point(1, 1)
        p = PointRelative(2, 3, b, 'foo')
        self.assertEqual((3, 4), p.xy())
        self.assertEqual('(3, 4)', str(p))
        self.assertEqual("PointRelative(2, 3, Point(1, 1), 'foo')", repr(p))
        p = PointRelative(2, 3, b)
        self.assertEqual((3, 4), p.xy())
        self.assertEqual('(3, 4)', str(p))
        self.assertEqual("PointRelative(2, 3, Point(1, 1))", repr(p))

    @tests(PointRelative.copy)
    def test_copy(self):
        b = Point(1, 1)
        p = PointRelative(2, 3, b, 'example')
        q = p.copy()
        r = PointRelative(2, 3, Point(1, 1), 'example')
        self.assertEqual(p, q)
        self.assertEqual(p, r)
        b.setxy(2, 2)
        self.assertEqual(p, q)
        self.assertNotEqual(p, r)
        p.dx = 4
        self.assertNotEqual(p, q)

    @tests(PointRelative.__eq__)
    def test_eq(self):
        b = Point(1, 1)
        p = PointRelative.fromxy(3, 4, b)
        self.assertEqual(PointRelative(2, 3, b), p)
        self.assertNotEqual(PointRelative(2, 3.1, b), p)

    @tests(PointRelative.fromxy)
    def test_fromxy(self):
        b = Point(1, 1)
        p = PointRelative.fromxy(3, 4, b)
        self.assertEqual(PointRelative(2, 3, b), p)

    @tests(PointRelative.round)
    def test_round(self):
        b = Point(1.12, 1.56)
        p = PointRelative(2.07, 3.07, b)
        self.assertEqual((3.0, 5.0), p.round().xy())
        self.assertEqual((3.2, 4.6), p.round(1).xy())


@tests(Vector)
class TestVector(TestCaseGeomExtended):
    @tests(Vector.__init__)
    @tests(Vector.__str__)
    @tests(Vector.__repr__)
    def test_basic(self):
        v = Vector(1, 2)
        self.assertEqual('V(1, 2)', str(v))
        self.assertEqual('Vector(1, 2)', repr(v))

    @tests(Vector.__bool__)
    def test_bool(self):
        self.assertTrue(Vector(0.00001, 0))
        self.assertTrue(Vector(0, 0.00001))
        self.assertFalse(Vector(0, 0))
        self.assertFalse(Vector())

    @tests(Vector.__add__)
    def test_add(self):
        v = Vector(1, 2)
        w = Vector(3, 5)
        self.assertEqual(Vector(4, 7), v+w)
        self.assertEqual(Vector(4, 7), w+v)
        p = Point(1, 1)
        self.assertEqual(Point(2, 3), p+v)
        self.assertEqual(Point(2, 3), v+p)
        self.assertRaises(TypeError, lambda: v+3)
        # noinspection PyTypeChecker
        self.assertRaises(TypeError, lambda: 3+v)

    @tests(Vector.__eq__)
    def test_eq(self):
        v = Vector(1, 2)
        w = Vector(1, 2)
        u = Vector(2, 1)
        self.assertTrue(v == w)
        self.assertTrue(u != v)

    @tests(Vector.__mul__)
    @tests(Vector.__rmul__)
    def test_mul(self):
        v = Vector(2, 1)
        self.assertEqual(Vector(4, 2), v*2)
        self.assertEqual(Vector(4, 2), 2*v)

    @tests(Vector.__neg__)
    def test_neg(self):
        v = Vector(3, -4)
        self.assertEqual(Vector(-3, 4), -v)

    @tests(Vector.sub_vector)
    @tests(Vector.__sub__)
    def test_sub(self):
        v = Vector(5, 6)
        w = Vector(6, 5)
        self.assertEqual(Vector(-1, 1), v-w)
        self.assertEqual(Vector(1, -1), w-v)
        p = Point(1, 1)
        self.assertEqual(Point(-4, -5), p-v)
        self.assertRaises(TypeError, lambda: v-p)

    @tests(Vector.__truediv__)
    def test_truediv(self):
        v = Vector(1, 2)
        self.assertEqual(Vector(0.5, 1), v/2)

    @tests(Vector.fixed)
    def test_fixed(self):
        v = Vector(3, 4)
        self.assertEqual(Vector(3, 4), v.fixed())
        w = v.fixed()
        self.assertIsNot(v, w)

    @tests(Vector.length)
    def test_length(self):
        self.assertEqual(5, Vector(3, 4).length())

    @tests(Vector.close)
    def test_close(self):
        base = Vector(1, 2)
        self.assertTrue(base.close(Vector(1, 2)))
        self.assertTrue(base.close(Vector(1+5e-12, 2)))
        self.assertFalse(base.close(Vector(1+1e-10, 2)))

    @tests(Vector.cross)
    def test_cross(self):
        base = Vector(1, 0)
        self.assertEqual(base.cross(Vector(0, 1)), 1)
        self.assertEqual(base.cross(Vector(0, 3)), 3)
        self.assertEqual(base.cross(Vector(3, 0)), 0)
        base = Vector(0, 1)
        self.assertEqual(base.cross(Vector(1, 0)), -1)
        self.assertEqual(base.cross(Vector(2, 0)), -2)
        self.assertEqual(base.cross(Vector(0, 4)), 0)
        self.assertEqual(Vector(1, 1).cross(Vector(-1, 1)), 2)
        self.assertEqual(Vector(1, 1).cross(Vector(17, 17)), 0)
        self.assertAlmostEqual(base.cross(base.rotate(10)), base.rotate(10).cross(base.rotate(20)))
        self.assertAlmostEqual(base.cross(base.rotate(30)), base.rotate(20).cross(base.rotate(50)))

    @tests(Vector.angle)
    def test_angle(self):
        self.assertEqual(Vector(1, 0).angle(), 0)
        self.assertAlmostEqual(Vector(1, 1).angle(), 45)
        self.assertAlmostEqual(Vector(0, 1).angle(), 90)

    @tests(Vector.rotate)
    def test_rotate(self):
        self.assertAlmostEqual(Vector(1, 0).rotate(90), Vector(0, 1))
        self.assertAlmostEqual(Vector(1, 0).rotate(180), Vector(-1, 0))
        self.assertAlmostEqual(Vector(5, 0).rotate(270), Vector(0, -5))
        self.assertAlmostEqual(Vector(1, 0).rotate(360), Vector(1, 0))
        self.assertAlmostEqual(Vector(2, 3).rotate(90).rotate(45).rotate(90).rotate(45).rotate(90), Vector(2, 3))
        s2 = math.sqrt(2) / 2
        self.assertAlmostEqual(Vector(0, 1).rotate(-45), Vector(s2, s2))

    @tests(Vector.normal)
    def test_normal(self):
        self.assertEqual(Vector(0, -1), Vector(1, 0).normal())
        self.assertEqual(Vector(2, -1), Vector(1, 2).normal())

    @tests(Vector.__round__)
    def test___round__(self):
        self.assertEqual(Vector(1, 2), round(Vector(1.1234, 2.1234)))
        self.assertEqual(Vector(1.1, 2.1), round(Vector(1.1234, 2.1234), 1))
        self.assertEqual(Vector(1.14, 2.01), round(Vector(1.135, 2.0051), 2))

    @tests(Vector.round)
    def test_round(self):
        self.assertEqual(Vector(1, 2), Vector(1.1234, 2.1234).round())
        self.assertEqual(Vector(1.1, 2.1), Vector(1.1234, 2.1234).round(1))
        self.assertEqual(Vector(1.14, 2.01), Vector(1.135, 2.0051).round(2))

    @tests(Vector.setxy)
    def test_setxy(self):
        v = Vector(3, 4)
        v.setxy(5, 6)
        self.assertEqual(Vector(5, 6), v)

    @tests(geom.Vector.set)
    def test_set(self):
        v = Vector(3, 4)
        v.set(Vector(5, 6))
        self.assertEqual(Vector(5, 6), v)

    @tests(Vector.unit)
    def test_unit(self):
        self.assertEqual(Vector(1, 0), Vector(0.1, 0).unit())
        self.assertEqual(Vector(1, 0), Vector(12, 0).unit())
        self.assertAlmostEqual(math.sqrt(2)/2, Vector(1, 1).unit().xy()[0])
        self.assertAlmostEqual(math.sqrt(2)/2, Vector(1, 1).unit().xy()[1])
        self.assertRaises(ZeroDivisionError, lambda: Vector(0, 0).unit())

    @tests(Vector.x)
    @tests(Vector.y)
    @tests(Vector.xy)
    def test_xy(self):
        v = Vector(1.2, 3.4)
        self.assertEqual((1.2, 3.4), v.xy())
        self.assertEqual(1.2, v.x)
        self.assertEqual(3.4, v.y)

    @tests(Vector.p)
    def test_p(self):
        self.assertEqual(Point(1.2, 3.4), Vector(1.2, 3.4).p)

    @tests(geom.Vector.__iter__)
    def test_iter(self):
        v = Vector(3, 4.5)
        self.assertEqual((3, 4.5), tuple(v))

    @tests(geom.Vector.copy)
    def test_copy(self):
        v = Vector(1.2, 3.4)
        w = v.copy()
        v.setxy(0, 0)
        self.assertEqual((1.2, 3.4), w.xy())
        self.assertEqual((0, 0), v.xy())

    @tests(geom.Vector.dot)
    def test_dot(self):
        v = Vector(1.1, 10.01)
        w = Vector(2, 3)
        self.assertAlmostEqual(32.23, v.dot(w))
        self.assertAlmostEqual(32.23, w.dot(v))


@tests(BBox)
class TestBBox(TestCaseExtended):
    # noinspection PyTypeChecker
    @tests(BBox.__init__)
    @tests(BBox.as_tuple)
    def test_init(self):
        b = BBox(1, 2, 3, 4)
        self.assertEqual((1, 2, 3, 4), b.as_tuple())
        b = BBox((3, 4, 1, 2))
        self.assertEqual((1, 2, 3, 4), b.as_tuple())
        b = BBox(Point(1, 2), Point(3, 4))
        self.assertEqual((1, 2, 3, 4), b.as_tuple())
        with self.assertRaises(TypeError):
            BBox((3, 4, 1, 2), 1)
        with self.assertRaises(TypeError):
            BBox((3, 4, 1, 2), None, 1)
        with self.assertRaises(TypeError):
            BBox((3, 4, 1, 2), None, None, 1)
        with self.assertRaises(TypeError):
            BBox("error", 1)
        with self.assertRaises(TypeError):
            BBox(Point(1, 2), Point(3, 4), None, 1)
        with self.assertRaises(TypeError):
            BBox(Point(1, 2), "error")
        with self.assertRaises(TypeError):
            BBox("error", Point(3, 4))

    @tests(BBox.__round__)
    def test_round(self):
        c = BBox(1.234, 2, 3, 4)
        self.assertEqual((1.2, 2, 3, 4), tuple(round(c, 1)))

    @tests(BBox.__add__)
    @tests(BBox.__eq__)
    def test_add(self):
        b = BBox(1, 2, 3, 4)
        c = BBox(0, 1, 4, 5)
        n = BBox(None)
        self.assertEqual(c, b+c)
        self.assertEqual(c, c+b)
        self.assertEqual(c, c+n)
        self.assertEqual(c, n+c)
        self.assertEqual(n, n+n)

    @tests(BBox.__add__)
    def test_add_fails(self):
        b = BBox(1, 2, 3, 4)
        c = (0, 0, 0, 0)
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            b+c
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            c+b

    @tests(BBox.width)
    @tests(BBox.height)
    def test_wh(self):
        b = BBox(1, 2, 3, 6)
        self.assertEqual(2, b.width)
        self.assertEqual(4, b.height)

    @tests(BBox.__iter__)
    def test_iter(self):
        b = BBox(1, 2, 3, 4)
        self.assertEqual((1, 2, 3, 4), tuple(b))

    @tests(BBox.__str__)
    def test_str(self):
        b = BBox(5, 6, 7, 8.5)
        self.assertEqual('(5, 6, 7, 8.5)', str(b))

    @tests(BBox.__repr__)
    def test_repr(self):
        b = BBox(1, 2, 3, 4)
        self.assertEqual('BBox(xl=1, yl=2, xh=3, yh=4)', repr(b))

    @tests(BBox.copy)
    def test_copy(self):
        b = BBox(1, 2, 3, 4)
        c = b.copy()
        b.xl = 0
        self.assertEqual((1, 2, 3, 4), tuple(c))
        self.assertEqual((0, 2, 3, 4), tuple(b))

    @tests(BBox.expand)
    def test_expand(self):
        b = BBox(1, 2, 3, 4)
        self.assertEqual(BBox(0, 0, 4, 6), b.expand(1, 2))

    @tests(BBox.is_none)
    @tests(BBox.is_empty)
    def test_empty(self):
        b = BBox(None)
        self.assertTrue(b.is_none)
        self.assertTrue(b.is_empty)
        self.assertTrue(BBox(1, 1, 2, 1).is_empty)
        self.assertRaises(ValueError, lambda: b.pll)
        self.assertRaises(ValueError, lambda: b.plh)
        self.assertRaises(ValueError, lambda: b.phl)
        self.assertRaises(ValueError, lambda: b.phh)
        self.assertRaises(ValueError, lambda: b.center)
        self.assertRaises(ValueError, lambda: b.p1)
        self.assertRaises(ValueError, lambda: b.p2)
        self.assertEqual(0, b.width)
        self.assertEqual(0, b.height)

    @tests(BBox.area)
    def test_area(self):
        self.assertEqual(4, BBox(1, 2, 3, 4).area())
        self.assertEqual(0, BBox(1, 1, 2, 1).area())
        self.assertEqual(0, BBox(1, 1, 1, 2).area())
        self.assertEqual(0, BBox(None).area())

    @tests(BBox.size)
    def test_size(self):
        self.assertEqual((2, 2), BBox(1, 2, 3, 4).size())
        self.assertEqual((1, 0), BBox(1, 1, 2, 1).size())
        self.assertEqual((0, 1), BBox(1, 1, 1, 2).size())
        self.assertEqual((0, 0), BBox(None).size())

    @tests(BBox.grow)
    def test_grow(self):
        b = BBox(1, 2, 3, 4)
        b.grow(Point(5, 6))
        self.assertEqual((1, 2, 5, 6), tuple(b))
        b.grow(Point(0, 0))
        self.assertEqual((0, 0, 5, 6), tuple(b))
        b.grow(Point(2, 2))
        self.assertEqual((0, 0, 5, 6), tuple(b))
        b = BBox(None)
        self.assertEqual((None, None, None, None), tuple(b))
        b.grow(Point(0, 3))
        self.assertEqual((0, 3, 0, 3), tuple(b))

    @tests(BBox.transformed)
    def test_transformed(self):
        b = BBox(1, 1, 2, 4)
        t = Transform().rotate(90)
        self.assertAlmostEqual((1, -2, 4, -1), tuple(b.transformed(t)))

    @tests(BBox.contains_pt)
    def test_contains_pt(self):
        b = BBox(1, 2, 3, 4)
        self.assertTrue(b.contains_pt(Point(2, 3)))
        self.assertFalse(b.contains_pt(Point(1, 3)))
        self.assertFalse(b.contains_pt(Point(3, 3)))
        self.assertFalse(b.contains_pt(Point(2, 4)))
        self.assertFalse(b.contains_pt(Point(2, 2)))
        self.assertFalse(b.contains_pt(Point(0, 3)))
        self.assertFalse(b.contains_pt(Point(4, 3)))
        self.assertFalse(b.contains_pt(Point(2, 5)))
        self.assertFalse(b.contains_pt(Point(2, 1)))
        self.assertFalse(BBox(None).contains_pt(Point(0, 0)))

    @tests(BBox.contains)
    def test_contains(self):
        def contains(a, b):
            self.assertTrue(a.contains(b), msg='%r.contains(%r)' % (a, b))
            self.assertTrue(a.contains(a), msg='%r.contains(%r)' % (a, a))
            self.assertTrue(b.contains(b), msg='%r.contains(%r)' % (b, b))
            self.assertFalse(b.contains(a), msg='%r.contains(%r)' % (b, a))
        contains(BBox(0, 3, 10, 13), BBox(2, 5, 8, 8))
        contains(BBox(0, 3, 10, 13), BBox(0, 5, 8, 8))
        contains(BBox(1, 2, 3, 4), BBox(1, 2, 3, 3))
        self.assertRaises(ValueError, lambda: BBox(None).contains(BBox(1, 2, 3, 4)))
        self.assertRaises(ValueError, lambda: BBox(1, 2, 3, 4).contains(BBox(None)))

    @tests(BBox.touches_pt)
    def test_touches_pt(self):
        b = BBox(1, 2, 3, 4)
        self.assertFalse(b.touches_pt(Point(2, 3)))
        self.assertTrue(b.touches_pt(Point(1, 3)))
        self.assertTrue(b.touches_pt(Point(3, 3)))
        self.assertTrue(b.touches_pt(Point(2, 4)))
        self.assertTrue(b.touches_pt(Point(2, 2)))
        self.assertFalse(b.touches_pt(Point(0, 3)))
        self.assertFalse(b.touches_pt(Point(4, 3)))
        self.assertFalse(b.touches_pt(Point(2, 5)))
        self.assertFalse(b.touches_pt(Point(2, 1)))
        self.assertFalse(BBox(None).touches_pt(Point(0, 0)))

    @tests(BBox.touches)
    @tests(BBox.touches_side)
    @tests(BBox.overlaps)
    def test_touches_side(self):
        b = BBox(2, 12, 4, 14)
        xs = [0, 1, 2, 3, 4, 5, 6]
        ys = [10, 11, 12, 13, 14, 15, 16]
        expected = """
            . . . . . .
            . t T T t .
            . T o o T .
            . T o o T .
            . t T T t .
            . . . . . .
        """
        base_expected = expected.replace(' ', '').replace('\n', '')
        expected = list(reversed(base_expected))
        for xl, xh in zip(xs, xs[1:]):
            for yl, yh in zip(ys, ys[1:]):
                c = BBox(xl, yl, xh, yh)
                expect = expected.pop()
                msg = 'case %d(%s): %r touches %r' % (len(base_expected)-len(expected), expect, b, c)
                with self.subTest(msg.partition(':')[0]):
                    if expect in ('T', 't'):
                        self.assertTrue(b.touches(c), msg=msg)
                        self.assertTrue(c.touches(b), msg=msg)
                        if expect == 't':
                            self.assertFalse(b.touches_side(c), msg=msg)
                            self.assertFalse(c.touches_side(b), msg=msg)
                        else:
                            self.assertTrue(b.touches_side(c), msg=msg)
                            self.assertTrue(c.touches_side(b), msg=msg)
                        self.assertFalse(b.overlaps(c), msg=msg)
                        self.assertFalse(c.overlaps(b), msg=msg)
                    else:
                        self.assertFalse(b.touches(c), msg=msg)
                        self.assertFalse(c.touches(b), msg=msg)
                        self.assertFalse(b.touches_side(c), msg=msg)
                        self.assertFalse(c.touches_side(b), msg=msg)
                        msg = msg.replace('touches', 'overlaps')
                        if expect == 'o':
                            self.assertTrue(b.overlaps(c), msg=msg)
                            self.assertTrue(c.overlaps(b), msg=msg)
                        else:
                            self.assertFalse(b.overlaps(c), msg=msg)
                            self.assertFalse(c.overlaps(b), msg=msg)

        self.assertFalse(b.touches(b))      # Overlaps is non-zero, so no touchy-touchy
        self.assertFalse(b.touches(BBox(None)))
        self.assertFalse(BBox(None).touches(b))
        self.assertFalse(b.touches_side(BBox(None)))
        self.assertFalse(BBox(None).touches_side(b))
        self.assertRaises(ValueError, lambda: b.overlaps(BBox(None)))
        self.assertRaises(ValueError, lambda: BBox(None).overlaps(b))

    @tests(BBox.intersection)
    def test_intersection(self):
        b = BBox(1, 2, 11, 12)
        c = BBox(2, 4, 20, 40)
        self.assertEqual(c.intersection(b), b.intersection(c))
        self.assertEqual(BBox(2, 4, 11, 12), b.intersection(c))
        self.assertEqual(c, c.intersection(c))
        self.assertEqual(BBox(11, 12, 11, 12), b.intersection(BBox(11, 12, 21, 22)))
        self.assertEqual(BBox(1, 12, 2, 12), b.intersection(BBox(0, 12, 2, 22)))
        d = BBox(2, 3, 10, 11)
        self.assertEqual(d, d.intersection(b))
        self.assertEqual(d, b.intersection(d))
        e = BBox(20, 30, 40, 50)
        self.assertTrue(b.intersection(e).is_none)
        self.assertTrue(e.intersection(b).is_none)
        f = BBox(None)
        self.assertTrue(b.intersection(f).is_none)
        self.assertTrue(f.intersection(b).is_none)
        self.assertTrue(f.intersection(f).is_none)

    # noinspection PyStatementEffect
    @tests(BBox.__getitem__)
    def test_getitem(self):
        b = BBox(0, 1, 2, 3)
        for idx in range(4):
            self.assertEqual(idx, b[idx])
        with self.assertRaises(IndexError):
            b[4]
        with self.assertRaises(IndexError):
            b[-5]

    # noinspection PyStatementEffect
    @tests(BBox.__setitem__)
    def test_setitem(self):
        b = BBox(0, 1, 2, 3)
        for idx in range(4):
            b[idx] = 100+idx
        self.assertEqual((100, 101, 102, 103), b.as_tuple())

        with self.assertRaises(IndexError):
            b[4] = 3
        with self.assertRaises(IndexError):
            b[-5] = 3

    @tests(BBox.sort)
    def test_sort(self):
        b = BBox(0, 0, 1, 2)
        b.xl = 4
        b.yl = 3
        self.assertEqual((4, 3, 1, 2), b.as_tuple())
        b.sort()
        self.assertEqual((1, 2, 4, 3), b.as_tuple())

    @tests(BBox.p1)
    @tests(BBox.p2)
    @tests(BBox.center)
    @tests(BBox.pll)
    @tests(BBox.plh)
    @tests(BBox.phl)
    @tests(BBox.phh)
    def test_p1p2(self):
        b = BBox(1, 2, 3, 4)
        self.assertEqual(Point(1, 2), b.p1)
        self.assertEqual(Point(3, 4), b.p2)
        self.assertEqual(Point(2, 3), b.center)
        self.assertEqual(Point(1, 2), b.pll)
        self.assertEqual(Point(1, 4), b.plh)
        self.assertEqual(Point(3, 2), b.phl)
        self.assertEqual(Point(3, 4), b.phh)


@tests(Line)
class TestLine(TestCaseExtended):
    @tests(Line.__init__)
    def test_init(self):
        l = Line(Point(0, 0), Vector(3, 4))
        self.assertEqual((0, 0), l.origin.xy())
        self.assertEqual((3, 4), l.direction.xy())

    @tests(Line.__eq__)
    def test_eq(self):
        l0 = Line(Point(1, 2), Vector(3, 4))
        self.assertEqual(l0, Line(Point(1, 2), Vector(3, 4)))
        self.assertNotEqual(l0, Line(Point(1.0001, 2), Vector(3, 4)))

    @tests(Line.__str__)
    def test_str(self):
        l = Line(Point(1, 2), Vector(3, 4))
        self.assertEqual(str(l), '(1, 2) @ V(3, 4)')

    @tests(Line.__repr__)
    def test_repr(self):
        l = Line(Point(1, 2), Vector(3, 4))
        self.assertEqual(repr(l), 'Line(Point(1, 2), Vector(3, 4))')

    @tests(Line.p1)
    @tests(Line.p2)
    @tests(Line.from_pts)
    def test_from_pts(self):
        l0 = Line(Point(0, 0), Vector(3, 4))
        l1 = Line.from_pts(Point(0, 0), Point(6, 8))
        self.assertEqual(l0.origin, l1.origin)
        self.assertEqual(0, l0.direction.cross(l1.direction))

    @tests(Line.p1)
    @tests(Line.p2)
    def test_p1p2(self):
        l0 = Line(Point(1, 2), Vector(3, 4))
        self.assertEqual(l0.p1, Point(1, 2))
        self.assertEqual(l0.p2, Point(4, 6))

    @tests(Line.midpoint)
    def test_midpoint(self):
        l0 = Line(Point(1, 2), Vector(2, 4))
        self.assertEqual(Point(2, 4), l0.midpoint)

    @tests(Line.__add__)
    def test_add(self):
        l0 = Line(Point(1, 2), Vector(3, 4))
        self.assertEqual(l0+Vector(1, 2), Line(Point(2, 4), Vector(3, 4)))

    @tests(Line.__sub__)
    def test_sub(self):
        l0 = Line(Point(1, 2), Vector(3, 4))
        self.assertEqual(l0-Vector(1, 2), Line(Point(0, 0), Vector(3, 4)))

    @tests(Line.closest)
    def test_closest(self):
        l = Line(Point(1, 1), Vector(-1, -1))
        self.assertAlmostEqual(Point(2, 2).xy(), l.closest(Point(3, 1)).xy())

    @tests(Line.intersection)
    def test_intersection(self):
        l = Line(Point(0, 0), Vector(1, 1))
        m = Line(Point(0, 2), Vector(-1, 1))
        self.assertAlmostEqual(Point(1, 1), l.intersection(m))
        self.assertRaises(ParallelLineError, lambda: l.intersection(Line(Point(2, 3), Vector(2, 2))))

    @tests(Line.parallel)
    def test_parallel(self):
        self.assertTrue(Line(Point(0, 0), Vector(1, 1)).parallel(Line(Point(1, 2), Vector(1, 1))))
        self.assertTrue(Line(Point(0, 0), Point(2, 1)).parallel(Line(Point(1, 2), Point(3, 3))))

    @tests(Line.segment_bbox)
    def test_segment_bbox(self):
        l = Line(Point(1, 2), Point(3, 4))
        self.assertEqual(l.segment_bbox(), BBox(1, 2, 3, 4))

    @tests(Line.segment_intersection)
    def test_segment_intersection(self):
        l = Line(Point(0, 0), Point(2, 2))
        m = Line(Point(0, 2), Point(2, 0))
        n = Line(Point(1, 1), Point(2, 0))
        nn = Line(Point(0, 2), Point(1, 1))
        o = Line(Point(1.1, 0.9), Point(2, 0))
        self.assertAlmostEqual((Point(1, 1), 0.5, 0.5), l.segment_intersection(m))
        self.assertAlmostEqual((Point(1, 1), 0.5, 0.0), l.segment_intersection(n))
        self.assertAlmostEqual((Point(1, 1), 0.5, 1.0), l.segment_intersection(nn))
        self.assertIsNone(l.segment_intersection(o))
        self.assertIsNone(o.segment_intersection(l))
        self.assertIsNone(l.segment_intersection(Line(Point(5, 7), Point(9, 9))))
        self.assertRaises(ParallelLineError, lambda: l.segment_intersection(Line(Point(1, 0), Vector(2, 2))))
        # TODO-this should result in a segment of overlap
        self.assertRaises(ParallelLineError, lambda: l.segment_intersection(Line(Point(1, 1), Vector(2, 2))))
        # TODO-this should result in Point(2,2) intersection
        # self.assertRaises(ParallelLineError, lambda: l.segment_intersection(Line(Point(2, 2), Vector(2, 2))))


@tests(geom.ParallelLineError)
class TestParallelLineError(TestCase):
    def test_ple(self):
        l = Line(Point(0, 0), Point(2, 2))
        self.assertRaises(ParallelLineError, lambda: l.segment_intersection(Line(Point(1, 0), Vector(2, 2))))


@tests(geom.SupportsRound)
class TestSupportsRound(TestCase):
    @tests(geom.SupportsRound.__round__)
    def test___round__(self):
        x = geom.SupportsRound()
        self.assertEqual(round(x), 0.0)


@tests(geom.VectorRelative)
class TestVectorRelative(TestCase):
    @tests(geom.VectorRelative.__bool__)
    def test_bool(self):
        self.assertTrue(VectorRelative(Point(1, 1), Point(0, 0)))
        self.assertFalse(VectorRelative(Point(0, 0), Point(0, 0)))

    @tests(geom.VectorRelative.__eq__)
    def test_eq(self):
        self.assertEqual(VectorRelative(Point(1, 2), Point(3, 4)), VectorRelative(Point(1, 2), Point(3, 4)))
        self.assertNotEqual(VectorRelative(Point(1, 2), Point(3, 4)), VectorRelative(Point(1, 2), Point(3, 4.1)))

    @tests(geom.VectorRelative.__init__)
    @tests(geom.VectorRelative.__repr__)
    @tests(geom.VectorRelative.__str__)
    @tests(geom.VectorRelative.x)
    @tests(geom.VectorRelative.y)
    @tests(geom.VectorRelative.xy)
    def test_init(self):
        p1 = Point(1, 1)
        p2 = Point(3, 4)
        v = VectorRelative(p1, p2)
        self.assertEqual(v.xy(), (-2, -3))
        self.assertEqual(v.x, -2)
        self.assertEqual(v.y, -3)
        self.assertEqual('VectorRelative(Point(1, 1), Point(3, 4))', repr(v))
        self.assertEqual('V((1, 1)-(3, 4))', str(v))

        v2 = VectorRelative(p2, p1)
        self.assertEqual(v2.xy(), (2, 3))

    @tests(geom.VectorRelative.__iter__)
    def test_iter(self):
        self.assertEqual([1, 2], list(VectorRelative(Point(2, 4), Point(1, 2))))

    @tests(geom.VectorRelative.__round__)
    @tests(geom.VectorRelative.round)
    def test_round(self):
        self.assertEqual(VectorRelative(Point(2, 4), Point(1, 2)), VectorRelative(Point(2, 4), Point(1, 2)).round())
        self.assertEqual(VectorRelative(Point(2, 4), Point(1, 2)), VectorRelative(Point(2, 4), Point(0.9, 2.1)).round())
        self.assertEqual(VectorRelative(Point(2, 4), Point(1, 2)), round(VectorRelative(Point(2, 4), Point(1, 2))))
        self.assertEqual(VectorRelative(Point(2, 4), Point(1, 2)), round(VectorRelative(Point(2, 4), Point(0.9, 2.1))))

    @tests(geom.VectorRelative.copy)
    def test_copy(self):
        v = VectorRelative(Point(2, 4), Point(1, 2))
        w = v.copy()
        self.assertEqual(v, w)
        cast(Point, v._p1).setxy(0, 0)
        self.assertNotEqual(v, w)

    @tests(geom.VectorRelative.set)
    @tests(geom.VectorRelative.setxy)
    def test_set_fails(self):
        v = VectorRelative(Point(2, 4), Point(1, 2))
        with self.assertRaises(NotImplementedError):
            v.set(v.fixed())
        with self.assertRaises(NotImplementedError):
            v.setxy(0, 0)


@tests(geom)
class TestModGeom(TestCase):
    """Tests for stand-alone functions in x7.geom.geom module"""

    @tests(polygon_area)
    def test_polygon_area(self):
        pts = [Point(1, 1), Point(2, 1), Point(2, 2), Point(1, 2)]
        self.assertEqual(1.0, polygon_area(pts))
        self.assertEqual(-1.0, polygon_area(list(reversed(pts))))

        pts = '00 30 33 23 22 12 13 03'
        pts = [Point(int(a), int(b)) for a, b in pts.split()]
        self.assertEqual(8.0, polygon_area(pts))
