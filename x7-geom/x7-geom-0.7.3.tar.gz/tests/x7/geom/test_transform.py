import math
from unittest import TestCase

from x7.geom import transform
from x7.geom.transform import *
from x7.geom.geom import *
from x7.lib.annotations import tests
from x7.geom.testing import TestCaseGeomExtended


@tests(EmptyStackError)
class TestEmptyStackError(TestCase):
    pass


class TransformerDummy(Transformer):
    """Simple linear transformation"""
    def __init__(self, sx, sy, tx, ty):
        self.sx = sx
        self.sy = sy
        self.tx = tx
        self.ty = ty

    def transform_np_pts(self, np_pts: NumpyPoints):
        return [(x*self.sx+self.tx, y*self.sy+self.ty, 1) for x, y, z in np_pts.T]


@tests(Transformer)
class TestTransformer(TestCaseGeomExtended):
    @tests(Transform.transform_width)
    def test_transform_width(self):
        t = Transform().scale(-2, 3)
        self.assertEqual(2.5, t.transform_width(1))
        t = TransformerDummy(2, -2, 3, 4)
        self.assertEqual(2, t.transform_width(1))


@tests(Transform)
class TestTransform(TestCaseGeomExtended):
    @tests(Transform.__init__)
    @tests(Transform.__str__)
    @tests(Transform.__repr__)
    @tests(Transform.__eq__)
    def test_basic(self):
        t = Transform()
        self.assertEqual(t, Transform.identity())
        self.assertEqual('(1.0, 0.0, 0.0, 0.0, 1.0, 0.0)', str(t))
        self.assertEqual('Transform((1.0, 0.0, 0.0, 0.0, 1.0, 0.0))', repr(t))

    @tests(Transform.__enter__)
    @tests(Transform.__exit__)
    def test_with(self):
        t = Transform()
        s = t.copy()
        self.assertEqual(t, s)
        with t.push():
            self.assertEqual(1, len(t.stack))
            self.assertEqual(t, s)
            t.rotate(90)
            self.assertNotEqual(t, s)
        self.assertEqual(t, s)
        self.assertEqual(0, len(t.stack))
        with self.assertRaises(EmptyStackError):
            with t:
                pass

    @tests(Transform.as_6tuple)
    def test_as_6tuple(self):
        t = Transform()
        self.assertEqual((1.0, 0.0, 0.0, 0.0, 1.0, 0.0), t.as_6tuple())

    @tests(Transform.compose)
    def test_compose(self):
        t = Transform()
        s = Transform()
        t.compose(s)
        self.assertEqual(t, s)

    @tests(Transform.is_simple)
    @tests(Transform.simplify)
    def test_simplify(self):
        self.assertTrue(Transform().is_simple())
        self.assertTrue(Transform().translate(3, 4).is_simple())
        t = Transform().rotate(90).translate(3, 4)
        self.assertTrue(t.is_simple())
        a, b = t.simplify()
        self.assertTrue(a.is_simple())
        self.assertTrue(b.is_simple())

        t = Transform().rotate_about(45, Point(1, 2))
        self.assertFalse(t.is_simple())
        a, b = t.simplify()
        self.assertTrue(a.is_simple())
        self.assertFalse(b.is_simple())

        self.assertEqual(t, a.compose(b))

    @tests(Transform.copy)
    def test_copy(self):
        t = Transform()
        s = t.copy()
        self.assertEqual(t, s)
        self.assertIsNot(t, s)

    # noinspection DuplicatedCode
    @tests(Transform.pop)
    @tests(Transform.push)
    def test_pop(self):
        t = Transform()
        s = t.copy()
        self.assertEqual(t, s)
        t.push()
        self.assertEqual(1, len(t.stack))
        self.assertEqual(t, s)
        t.rotate(90)
        self.assertNotEqual(t, s)
        t.pop()
        self.assertEqual(t, s)
        self.assertEqual(0, len(t.stack))
        with self.assertRaises(EmptyStackError):
            t.pop()

    @tests(Transform.reset)
    def test_reset(self):
        t = Transform().rotate_about(37, Point(3, 5)).reset()
        self.assertEqual(t, Transform())

    @tests(Transform.rotate_mat)
    @tests(Transform.rotate)
    def test_rotate(self):
        t = Transform().rotate(90)
        self.assertAlmostEqual((0, 1), t.transform(-1, 0))
        t = Transform().rotate(270)
        self.assertAlmostEqual((0, -1), t.transform(-1, 0))
        t = Transform().rotate(-45)
        self.assertAlmostEqual((math.sqrt(1/2), math.sqrt(1/2)), t.transform(1, 0))

    @tests(Transform.rotate_mat_ccw)
    @tests(Transform.rotate_ccw)
    def test_rotate(self):
        t = Transform().rotate_ccw(90)
        self.assertAlmostEqual((0, 1), t.transform(1, 0))
        t = Transform().rotate_ccw(270)
        self.assertAlmostEqual((0, -1), t.transform(1, 0))
        t = Transform().rotate_ccw(45)
        self.assertAlmostEqual((math.sqrt(1/2), math.sqrt(1/2)), t.transform(1, 0))

    @tests(Transform.scale_mat)
    @tests(Transform.scale)
    def test_scale(self):
        t = Transform().scale(2, 3)
        self.assertAlmostEqual((2, 3), t.transform(1, 1))

    @tests(Transform.scale_vals)
    def test_scale_vals(self):
        self.assertEqual((2, 3), Transform().scale(2, 3).scale_vals())
        self.assertAlmostEqual((2, 3), Transform().scale(2, 3).rotate(15).scale_vals())

    @tests(Transform.compose_outer)
    def test_compose_outer(self):
        t = Transform().translate(1, 2).scale(2, 3)
        s = Transform().scale(2, 3).translate(1, 2)
        u = Transform().translate(1, 2).compose_outer(Transform().scale(2, 3))
        v = Transform().translate(1, 2).compose(Transform().scale(2, 3))
        self.assertNotEqual(t, s)
        self.assertEqual(t, u)
        self.assertEqual(s, v)

    @tests(Transform.set_matrix)
    def test_set_matrix(self):
        t = Transform().scale(2, 3)
        s = Transform()
        s.set_matrix(t)
        self.assertAlmostEqual((2, 3), s.transform(1, 1))

    @tests(Transform.transform)
    @tests(Transform.untransform)
    def test_untransform(self):
        origin = Point(1, 2)
        # moderately complex transformation
        t = Transform().rotate_about(30, origin).translate(2.5, -1.7)
        x, y = t.transform(3, 7)
        self.assertAlmostEqual(t.untransform(x, y), (3, 7))
        # Test again to use the cached version of inverse
        x, y = t.transform(1, 2)
        self.assertAlmostEqual(t.untransform(x, y), (1, 2))

    @tests(Transform.transform_width)
    def test_transform_width(self):
        t = Transform().scale(2, 3)
        self.assertEqual(2.5, t.transform_width(1))

    @tests(Transform.transform_pts)
    @tests(Transform.untransform_pts)
    def test_transform_pts(self):
        bb1 = BBox(1, 2, 3, 4)
        bb2 = BBox(3, 5, 7, 11)
        t = Transform().scale_bbox(bb1, bb2)
        self.assertAlmostEqual([], [])
        self.assertAlmostEqual([bb2.p1, bb2.p2], t.transform_pts([bb1.p1, bb1.p2]))
        self.assertAlmostEqual([bb1.p1.xy(), bb1.p2.xy()], t.untransform_pts([bb2.p1, bb2.p2]))

        self.assertAlmostEqual([bb2.p1.xy(), bb2.p2.xy()], t.transform_pts([bb1.p1.xy(), bb1.p2]))
        self.assertAlmostEqual(list(bb2.p1.xy()+bb2.p2.xy()), t.transform_pts([bb1.p1.xy(), bb1.p2], flatten=True))
        self.assertAlmostEqual(list(bb2.p1.xy()+bb2.p2.xy()), t.transform_pts([bb1.p1, bb1.p2], flatten=True))

    @tests(Transform.translate)
    @tests(Transform.translate_mat)
    def test_translate(self):
        t = Transform().translate(3, 7)
        self.assertEqual((10, 10), t.transform(7, 3))

    @tests(transform.Transform.canvas_fit)
    def test_canvas_fit(self):
        t = Transform.canvas_fit((1100, 1200), 2, (600, 500))
        self.assertEqual((600, 700), t.transform(0, 0))
        self.assertEqual((610, 690), t.transform(5, 5))

    @tests(transform.Transform.rotate_about)
    @tests(transform.Transform.transform_pt)
    def test_rotate_about(self):
        origin = Point(1, 2)
        t = Transform().rotate_about(30, origin)
        self.assertEqual(origin, t.transform_pt(origin))
        s = Transform().rotate(30)
        self.assertAlmostEqual(s.transform_pt(Point(1, 0))+Vector(1, 2), t.transform_pt(Point(2, 2)))
        t = Transform().rotate_about(90, Point(1, 2))
        self.assertAlmostEqual((1, 1), t.transform(2, 2))
        self.assertAlmostEqual((0, 2), t.transform(1, 1))

    @tests(transform.Transform.scale_bbox)
    def test_scale_bbox(self):
        bb1 = BBox(1, 2, 3, 4)
        bb2 = BBox(3, 5, 7, 11)
        t = Transform()
        t.scale_bbox(bb1, bb2)
        self.assertEqual(bb2.p1, t.transform_pt(bb1.p1))
        self.assertEqual(bb2.p2, t.transform_pt(bb1.p2))

        bb1 = BBox(0, 0, 1, 1)
        bb2 = BBox(0, 0, 2, 2)
        t = Transform()
        t.scale_bbox(bb1, bb2, True)
        self.assertEqual(bb2.center, t.transform_pt(bb1.center))


@tests(Matrix)
class TestMatrix(TestCase):
    @tests(Matrix.__init__)
    @tests(Matrix.as_tuple3x3)
    def test_init(self):
        m = Matrix()
        self.assertEqual(((1, 0, 0), (0, 1, 0), (0, 0, 1)), m.as_tuple3x3())
        m = Matrix([(1, 2, 3), (4, 5, 6), (7, 8, 9)])
        self.assertEqual(((1, 2, 3), (4, 5, 6), (7, 8, 9)), m.as_tuple3x3())

    @tests(Matrix.__eq__)
    def test___eq__(self):
        m = Matrix()
        self.assertEqual(m, Matrix(((1, 0, 0), (0, 1, 0), (0, 0, 1))))
        self.assertNotEqual(m, Matrix(((1, 0, 0), (0, 1, 0), (0, 0, 2))))

    @tests(Matrix.__str__)
    @tests(Matrix.__repr__)
    def test___repr__(self):
        m = Matrix([(1.123, 2, 3), (4, 5, 6), (7, 8, 9)])
        self.assertEqual('((1.12, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0))', str(m))
        self.assertEqual('Transform(((1.123, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)))', repr(m))

    @tests(Matrix.copy)
    def test_copy(self):
        m = Matrix([(1, 0, 0), (0, 2, 0), (0, 0, 1)])
        n = m.copy()
        m.pre_dot_eq(m.ndmat)
        self.assertNotEqual(m, n)
        self.assertEqual(n, Matrix([(1, 0, 0), (0, 2, 0), (0, 0, 1)]))

    @tests(Matrix.inverse)
    def test_inverse(self):
        m = Matrix([(1, 0, 0), (0, 2, 0), (0, 0, 1)])
        n = Matrix([(1, 0, 0), (0, 1/2, 0), (0, 0, 1)])
        self.assertEqual(m.inverse(), n)
        self.assertEqual(n.inverse(), m)
        m = Matrix([(0, 1, 0), (1, 0, 0), (0, 0, 1)])
        self.assertEqual(m.inverse(), m)
        m = Matrix([(0, -1, 0), (1, 0, 0), (0, 0, 1)])
        n = Matrix([(0, 1, 0), (-1, 0, 0), (0, 0, 1)])
        self.assertEqual(m.inverse(), n)

    @tests(Matrix.post_dot_eq)
    def test_post_dot_eq(self):
        # post_dot_eq(self, ndmat)
        pass  # TODO-impl x7.geom.Matrix.post_dot_eq test

    @tests(Matrix.pre_dot_eq)
    def test_pre_dot_eq(self):
        # pre_dot_eq(self, ndmat)
        pass  # TODO-impl x7.geom.Matrix.pre_dot_eq test


@tests(transform)
class TestModTransform(TestCase):
    """Tests for stand-alone functions in x7.geom.transform module"""


def test():
    m = Transform()
    print(m)

    def do(what):
        locals()['m'] = m
        result = str(eval(what, globals(), locals()))
        if '\n' in result:
            result = '\n' + result
        print(what, '->', result)

    do('m.inverse')
    do('m.transform(2, 3)')
    do('m.translate_mat(1, 2)')
    do('m.translate(1, 0).translate(0, 2)')
    do('m.transform(2, 3)')
    do('m.inverse')
    do('m.reset().scale(2,3)')
    do('m.transform(2, 3)')
    do('m.translate(1, 2)')
    do('m.transform(2, 3)')
    do('m.inverse')
    do('m.reset().rotate(90)')
    do('m.transform(2, 3)')
    do('m.inverse')

    print()
    do('m.reset().translate(0, 1000).scale(1, -1).translate(1000,500).scale(10,10)')
    do('m.transform(0, 0)')  # 1000, 500
    do('m.transform(-100, -50)')  # 0, 1000
    do('m.transform(100, -50)')  # 2000, 1000
    do('m.transform_pts([(0,0), (-100, -50), (100, -50)])')
    print()
    pt = m.transform(100, -50)  # 2000, 1000
    pts = m.transform_pts([(0, 0), (-100, -50), (100, -50)])
    do('m.untransform(%s, %s)' % pt)
    do('m.untransform_pts(%s)' % pts)
    pts = [(1000, 500), (0, 1000), (2000, 1000)]
    do('m.untransform_pts(%s)' % pts)
    print()
    do('m.rotate(45)')
    do('m.transform(20, 0)')  # 1141, 641

    with m.push().rotate(45):
        do('m.transform(20, 0)')  # 1000, 700
    do('m.transform(20, 0)')  # 1141, 641
