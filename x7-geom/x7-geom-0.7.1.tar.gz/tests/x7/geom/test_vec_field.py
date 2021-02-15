from unittest import TestCase
from x7.geom import vec_field
from x7.geom.vec_field import *
from x7.geom.geom import *
from x7.lib.annotations import tests
from x7.testing.extended import TestCaseExtended


@tests(Mesh)
class TestMesh(TestCase):
    @tests(Mesh.__init__)
    def test_init(self):
        m = Mesh(BBox(0, 1, 5, 6), 11)
        self.assertEqual(m.bbox, BBox(0, 1, 5, 6))
        self.assertEqual(len(m.x_grid), 11)
        self.assertEqual(m.x_shape, (11, 11))
        self.assertEqual(m.x_grid[9, 9], 4.5)
        self.assertEqual(m.y_grid[9, 9], 5.5)

    @tests(Mesh.uniform)
    def test_uniform(self):
        m = Mesh(BBox(0, 1, 5, 6), 21)
        u = m.uniform(1)
        self.assertLessEqual(np.amax(u.vx), 1.0)
        self.assertGreaterEqual(np.amin(u.vx), -1.0)
        self.assertLessEqual(np.amax(u.vy), 1.0)
        self.assertGreaterEqual(np.amin(u.vy), -1.0)
        # TODO-this is a weak test, as it depends on the RNG too much
        self.assertLessEqual(abs(np.average(u.vx)), 0.1)

    @tests(Mesh.zeros)
    def test_zeros(self):
        u = Mesh(BBox(0, 1, 5, 6), 11).zeros()
        self.assertEqual(np.sum(np.abs(u.vx)), 0.0)
        self.assertEqual(np.sum(np.abs(u.vy)), 0.0)


@tests(VectorField)
class TestVectorField(TestCaseExtended):
    @tests(VectorField.__init__)
    @tests(VectorField.copy)
    def test_init(self):
        vf1 = Mesh(BBox(0, 0, 5, 5), 11).uniform(1)
        vf2 = vf1.copy()
        self.assertEqual(vf1, vf2)
        self.assertEqual(vf1.vx[1, 1], vf2.vx[1, 1])
        vf1.vx[1, 1] = 2.0
        self.assertNotEqual(vf1.vx[1, 1], vf2.vx[1, 1])

    @tests(VectorField.interp_coords)
    def test_interp_coords(self):
        # interp_coords(self, pts: numpy.ndarray)
        pass  # TODO-impl x7.geom.VectorField.interp_coords test

    @staticmethod
    def simple_vf():
        # Mesh with samples on integer points
        vf = Mesh(BBox(0, 0, 5, 5), 6).zeros()
        vf.vx[0, 0] = 1
        vf.vx[0, 1] = 2
        vf.vy[1, 0] = 2
        vf.vy[1, 1] = 4
        return vf

    @tests(VectorField.lookup)
    def test_lookup(self):
        vf = self.simple_vf()
        self.assertEqual((1, 0), vf.lookup(0, 0))
        self.assertEqual((2, 0), vf.lookup(0, 1))
        self.assertEqual((0, 2), vf.lookup(1, 0))
        self.assertEqual((0, 4), vf.lookup(1, 1))
        self.assertEqual((1.5, 0), vf.lookup(0, 0.5))
        self.assertEqual((0, 3), vf.lookup(1, 0.5))
        self.assertEqual((0.5, 1), vf.lookup(0.5, 0))
        self.assertEqual((1, 2), vf.lookup(0.5, 1))
        self.assertEqual((0.75, 1.5), vf.lookup(0.5, 0.5))

    @tests(VectorField.normalized)
    def test_normalized(self):
        vf = Mesh(BBox(0, 0, 5, 5), 6).uniform(2)
        vf.vx[1, 1] = 10
        vf.vy[1, 1] = 0
        vf = vf.normalized()
        self.assertEqual(vf.vx[1, 1], 1)
        self.assertEqual(vf.vy[1, 1], 0)

    @tests(VectorField.plot)
    def test_plot(self):
        # plot(self, title=None, ax=None)
        pass  # TODO-impl x7.geom.VectorField.plot test

    @tests(VectorField.quiver)
    def test_quiver(self):
        # quiver(self, ax)
        pass  # TODO-impl x7.geom.VectorField.quiver test

    @tests(VectorField.scaled)
    def test_scaled(self):
        vf = Mesh(BBox(0, 0, 5, 5), 6).zeros()
        vf.vx[1, 1] = 10
        vf.vy[1, 1] = 1
        vf = vf.scaled(2, 5)
        self.assertEqual(vf.vx[1, 1], 20)
        self.assertEqual(vf.vy[1, 1], 5)

    @tests(VectorField.smoothed)
    def test_smoothed(self):
        vf = self.simple_vf().smoothed()
        self.assertAlmostEqual(vf.vx[1, 1], 0.0365609058507249)
        self.assertAlmostEqual(vf.vy[1, 1], 0.9993314265864827)

    @tests(VectorField.transform_np_pts)
    def test_transform_np_pts(self):
        # points = [Point(1, 1), Point(1, 0), Point(0, -1)]
        points = [Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)]
        np_points = Transformer.points_to_np_points(points)
        np_point = Transformer.xy_to_np_point(0, 1)

        vf = self.simple_vf()
        self.assertEqual([(2.0, 1.0)], vf.transform_np_pts(np_point))
        self.assertEqual([(1, 0), (2, 1), (1, 2), (1, 5)], vf.transform_np_pts(np_points))


@tests(vec_field)
class TestModVecField(TestCase):
    """Tests for stand-alone functions in x7.geom.vec_field module"""

    @tests(animate)
    def test_animate(self):
        # animate()
        pass  # TODO-impl x7.geom.animate test

    @tests(main)
    def test_main(self):
        # main()
        pass  # TODO-impl x7.geom.main test
