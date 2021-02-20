from x7.geom.testing import TestCaseGeomExtended
from x7.geom.geom import Point, Vector


class TestTestCaseExtendedWithPoint(TestCaseGeomExtended):
    def test_assertAlmostEqual_point_list(self):
        """Test that List[Point] works with assertAlmostEqual.  Should be tested in x7-testing, but easier here"""
        self.assertAlmostEqual([Point(0, 0)], [Point(0, 0)])
        self.assertAlmostEqual([Point(0, 0)], [Point(1e-9, -1e-9)])

    def test_assertAlmostEqual_vector_list(self):
        """Test that List[Vector] works with assertAlmostEqual."""
        self.assertAlmostEqual([Vector(0, 0)], [Vector(0, 0)])
        self.assertAlmostEqual([Vector(0, 0)], [Vector(1e-9, -1e-9)])
