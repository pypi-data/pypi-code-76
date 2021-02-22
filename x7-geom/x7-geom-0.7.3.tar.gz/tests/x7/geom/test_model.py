from typing import Generator

from x7.lib.annotations import tests
from x7.geom import model
from x7.geom.model import *
from x7.geom.geom import *
from x7.geom.colors import *
from x7.geom.transform import *
from x7.geom.testing import TestCaseGeomExtended
from x7.geom.typing import *


class TestExample(TestCaseGeomExtended):
    SAVE_MATCH = False

    def test_big_data(self):
        x = 'foobar\n'*12
        self.assertMatch(x)
        x = ['hello', ', ', 'goodbye', '. ']
        self.assertMatch(x, 1)


DC_EXPECTED = """
from x7.geom.geom import *
from x7.geom.model import *
from x7.geom.colors import *
from x7.geom.transform import *

val_1 = 'hello'
val_2 = 'goodbye'

model = something(val_1, val_2)
    indented1
    indented2, 
""".strip()


@tests(DumpContext)
class TestDumpContext(TestCaseGeomExtended):
    @tests(DumpContext.__init__)
    @tests(DumpContext.__enter__)
    @tests(DumpContext.__exit__)
    @tests(DumpContext.add_comma)
    @tests(DumpContext.append)
    @tests(DumpContext.extend)
    @tests(DumpContext.output)
    @tests(DumpContext.prefix)
    @tests(DumpContext.set_var)
    def test_init(self):
        dc = DumpContext()
        hello = dc.set_var('hello', 'val')
        goodbye = dc.set_var('goodbye', 'val')
        dc.append('something(%s, %s)' % (hello, goodbye))
        with dc:
            dc.extend(['indented1', 'indented2'])
        dc.add_comma()
        self.assertEqual(DC_EXPECTED, dc.output())


class TestCaseElem(TestCaseGeomExtended):
    """Helper class for testing elements"""
    SAVE_MATCH = False

    def make_elements(self) -> List[Elem]:
        """Construct list of elements for auto-testing"""
        unused(self)
        return []

    def enum_elems(self, tag, elems=None) -> Generator[Tuple[str, Elem], None, None]:
        elems = elems or self.make_elements()
        for e in elems:
            yield '%s:%s' % (tag, e.name), e

    def test_elem_str(self):
        for tag, e in self.enum_elems('str'):
            with self.subTest(tag):
                self.assertMatch(str(e), tag)

    def test_elem_repr(self):
        for tag, e in self.enum_elems('repr'):
            with self.subTest(tag):
                self.assertMatch(repr(e), tag)

    def test_elem_as_digi_points(self):
        for tag, e in self.enum_elems('as_digi_points'):
            with self.subTest(tag):
                self.assertMatch(list(e.as_digi_points()), tag)

    def test_elem_as_curves(self):
        for tag, e in self.enum_elems('as_curves'):
            with self.subTest(tag):
                self.assertMatch(list(e.as_curves()), tag)

    def test_elem_bbox_int(self):
        for tag, e in self.enum_elems('bbox_int'):
            with self.subTest(tag):
                self.assertMatch(e.bbox_int(), tag)

    def test_elem_bbox(self):
        for tag, e in self.enum_elems('bbox'):
            with self.subTest(tag):
                self.assertMatch(e.bbox(), tag)
            with self.subTest(tag+'.center'):
                self.assertEqual(e.bbox().center, e.center())

    def test_elem_control_path(self):
        for tag, e in self.enum_elems('control_path'):
            dc = self.simple_dc()
            with self.subTest(tag+'_sdc'):
                paths = e.control_paths(dc)
                self.assertEqual(1, len(paths))
                self.assertMatch(paths[0].points, tag+'_sdc')
            dc.set_matrix(Transform())
            with e.xform.push():
                e.xform.set_matrix(Transform())
                with self.subTest(tag):
                    paths = e.control_paths(dc)
                    self.assertEqual(1, len(paths))
                    self.assertMatch(paths[0].points, tag)

    def test_elem_copy(self):
        for tag, e in self.enum_elems('copy'):
            with self.subTest(tag):
                self.assertMatch(e.copy(), tag)

    def test_elem_draw(self):
        for tag, e in self.enum_elems('draw'):
            with self.subTest(tag):
                dc = self.simple_dc(21)
                dc.matrix.scale_bbox(e.bbox(), BBox(2, 2, 18, 18))
                e.draw(dc)
                # dc.show()
                self.assertMatch(dc.image(), tag)

    def test_elem_dump(self):
        for tag, e in self.enum_elems('dump'):
            with self.subTest(tag):
                context = DumpContext()
                e.dump(context)
                self.assertMatch(context.output(), tag)

    def test_elem_iter_elems(self):
        for tag, e in self.enum_elems('iter_elems'):
            with self.subTest(tag):
                xform = Transform().translate(1, 2)
                iterated = list(e.iter_elems('root', xform))
                self.assertEqual(1, len(iterated))
                ni, ei, xi = iterated[0]
                self.assertEqual(e, ei)
                self.assertEqual('root.' + e.name, ni)
                self.assertEqual(xform, xi)

    def test_elem_path(self):
        dc = self.simple_dc()
        for tag, e in self.enum_elems('path'):
            with self.subTest(tag):
                paths = e.paths(dc)
                self.assertEqual(1, len(paths))
                self.assertMatch(paths[0].points.tolist(), tag)

    def test_elem_restore(self):
        xform = Transform().rotate_about(17, Point(3.1, 1.4))
        for tag, e in self.enum_elems('dump'):
            with self.subTest(tag):
                other = e.transform(xform)
                self.assertNotEqual(e, other)
                other.restore(e)
                self.assertEqual(e, other)

    def test_elem_transform(self):
        xform = Transform().rotate_about(1.7, Point(2, -1))
        for tag, e in self.enum_elems('transform'):
            with self.subTest(tag):
                self.assertMatch(e.transform(xform), tag)


"""
    def test_elem_repr(self):
    def test_elem_str(self):
    def test_elem_as_digi_points(self):
    def test_elem_bbox(self):
    def test_elem_bbox_int(self):
    def test_elem_control_path(self):
    def test_elem_copy(self):
    def test_elem_draw(self):
    def test_elem_dump(self):
    def test_elem_path(self):
    def test_elem_restore(self):
    def test_elem_transform(self):
"""


@tests(Elem)
class TestElem(TestCaseElem):
    def make_elements(self) -> List[Elem]:
        unused(self)
        pen = PenBrush('green', 'yellow')
        return super().make_elements() + [
            ElemRectangle('r1', pen, Point(-1, -1), Point(4, 1), xform=Transform().rotate(10))
        ]

    @tests(Elem.__init__)
    @tests(Elem.__str__)
    @tests(Elem.__repr__)
    @tests(Elem.as_digi_points)
    @tests(Elem.bbox)
    @tests(Elem.bbox_int)
    # @tests(Elem.bbox_int_update)
    @tests(Elem.center)
    @tests(Elem.control_paths)
    @tests(Elem.copy)
    # @tests(Elem.display)
    @tests(Elem.draw)
    @tests(Elem.draw_space)
    @tests(Elem.dump)
    @tests(Elem.dump_elem)
    @tests(Elem.iter_elems)
    @tests(Elem.paths)
    @tests(Elem.restore)
    @tests(Elem.transform)
    def test_defaults(self):
        """Nothing special, just let the default tests run"""
        pass


@tests(ElemCurve)
class TestElemCurve(TestCaseElem):
    def make_elements(self) -> List[Elem]:
        pen = PenBrush('black')
        cp_a = ControlPoint(Point(0, 0), Vector(0, 1), Vector(0, -1), 'smooth')
        cp_b = ControlPoint(Point(10, 0), Vector(0, 1), Vector(0, -1), 'smooth')
        return [
            ElemCurve('c1', pen, [cp_a, cp_b]),
            ElemCurve('c2', pen, [cp_b, cp_a]),
        ]

    @tests(ElemCurve.__init__)
    def test_init(self):
        e = ElemCurve('c3', PenBrush('black'), [])
        self.assertEqual(0, len(e.control_points))

    @tests(ElemCurve.control_points_transformed)
    def test_control_points_transformed(self):
        xform = Transform().rotate_about(10, Point(3, 4))
        for tag, e in self.enum_elems('control_points_transformed'):
            e = cast(ElemCurve, e)
            with self.subTest(tag):
                self.assertMatch(e.control_points_transformed(xform), tag)

    @tests(ElemCurve.fixed)
    def test_fixed(self):
        for tag, e in self.enum_elems('fixed'):
            e = cast(ElemCurve, e)
            with self.subTest(tag):
                self.assertMatch(e.fixed(), tag)

    @tests(ElemCurve.add_one)
    def test_add_one(self):
        pen = PenBrush('black')
        curve = ElemCurve('curve', pen, [
            ControlPoint(Point(0, 0), Vector(0, 1), Vector(0, -1), 'smooth'),
            ControlPoint(Point(10, 0), Vector(0, 1), Vector(0, -1), 'smooth'),
            ControlPoint(Point(10, 10), Vector(1, 1), Vector(1, -1), 'smooth'),
        ])
        expected = ElemCurve('curve', pen, [
            ControlPoint(Point(5.375, 5.0), Vector(2.625, 2.25), Vector(-2.625, -2.25), 'smooth'),
            ControlPoint(Point(0, 0), Vector(0.0, 0.5), Vector(0, -1), 'smooth'),
            ControlPoint(Point(10, 0), Vector(0, 1), Vector(0, -1), 'smooth'),
            ControlPoint(Point(10, 10), Vector(1, 1), Vector(0.5, -0.5), 'smooth'),
        ])
        curve.add_one()
        self.assertEqual(expected, curve)
        expected = ElemCurve('curve', pen, [
            ControlPoint(Point(5.375, 5.0), Vector(2.625, 2.25), Vector(-2.625, -2.25), 'smooth'),
            ControlPoint(Point(0, 0), Vector(0.0, 0.5), Vector(0, -1), 'smooth'),
            ControlPoint(Point(10, 0), Vector(0, 1), Vector(0.0, -0.5), 'smooth'),
            ControlPoint(Point(10.375, 5.0), Vector(-0.125, -2.75), Vector(0.125, 2.75), 'smooth'),
            ControlPoint(Point(10, 10), Vector(0.5, 0.5), Vector(0.5, -0.5), 'smooth'),
        ])
        curve.add_one()
        self.assertEqual(expected, curve)

    @tests(ElemCurve.bbox_int_update)
    def test_bbox_int_update(self):
        with self.assertRaises(ValueError):
            self.make_elements()[0].bbox_int_update(BBox(0, 0, 1, 1))

    @tests(ElemCurve.display)
    def test_display(self):
        # display(self, detail=1, prefix='')
        pass  # TODO-impl x7.geom.ElemCurve.display test

    @tests(ElemCurve.replace)
    def test_replace(self):
        # replace(self, curve, replacement)
        pass  # TODO-impl x7.geom.ElemCurve.replace test


@tests(ElemEllipse)
class TestElemEllipse(TestCaseElem):
    def make_elements(self) -> List[Elem]:
        pen = PenBrush('red', 'blue')
        return [
            ElemEllipse('e1', pen, Point(1, -1), Point(-3, 4)),
            ElemEllipse('e2', pen, Point(1, 2), Point(3, -4))
        ]

    # noinspection DuplicatedCode
    @tests(ElemEllipse.__init__)
    @tests(ElemEllipse.__str__)
    @tests(ElemEllipse.__repr__)
    @tests(ElemEllipse.as_digi_points)
    @tests(ElemEllipse.bbox)
    @tests(ElemEllipse.bbox_int)
    # @tests(ElemEllipse.bbox_int_update)
    @tests(ElemEllipse.control_paths)
    @tests(ElemEllipse.copy)
    # @tests(ElemEllipse.display)
    @tests(ElemEllipse.draw)
    # @tests(ElemEllipse.draw_space)
    @tests(ElemEllipse.dump)
    # @tests(ElemEllipse.dump_elem)
    # @tests(ElemEllipse.iter_elems)
    @tests(ElemEllipse.paths)
    @tests(ElemEllipse.restore)
    @tests(ElemEllipse.transform)
    def test_defaults(self):
        """Nothing special, just let the default tests run"""
        pass

    @tests(ElemEllipse.display)
    def test_display(self):
        # display(self, detail=1, prefix='')
        pass  # TODO-impl x7.geom.ElemEllipse.display test

    @tests(ElemEllipse.make_control_points)
    def test_make_control_points(self):
        # make_control_points(self) -> List[x7.geom.ControlPoint]
        pass  # TODO-impl x7.geom.ElemEllipse.make_control_points test


@tests(ElemP1P2)
class TestElemP1P2(TestCaseElem):
    def make_elements(self) -> List[Elem]:
        pen = PenBrush('red', 'blue')
        return [
            ElemRectangle('r12', pen, Point(1, -1), Point(-3, 4)),
            ElemEllipse('e12', pen, Point(1, 2), Point(3, -4))
        ]

    # noinspection DuplicatedCode
    @tests(ElemP1P2.__init__)
    @tests(ElemP1P2.__str__)
    @tests(ElemP1P2.__repr__)
    @tests(ElemP1P2.as_digi_points)
    @tests(ElemP1P2.bbox)
    @tests(ElemP1P2.bbox_int)
    # @tests(ElemP1P2.bbox_int_update)
    @tests(ElemP1P2.control_paths)
    @tests(ElemP1P2.copy)
    # @tests(ElemP1P2.display)
    @tests(ElemP1P2.draw)
    # @tests(ElemP1P2.draw_space)
    @tests(ElemP1P2.dump)
    # @tests(ElemP1P2.dump_elem)
    # @tests(ElemP1P2.iter_elems)
    @tests(ElemP1P2.paths)
    @tests(ElemP1P2.restore)
    @tests(ElemP1P2.transform)
    def test_defaults(self):
        """Nothing special, just let the default tests run"""
        pass

    @tests(ElemP1P2.points)
    def test_points(self):
        # points(self) -> List[x7.geom.geom.Point]
        pass  # TODO-impl x7.geom.ElemP1P2.points test

    @tests(ElemP1P2.points_transformed)
    def test_points_transformed(self):
        # points_transformed(self, matrix: x7.geom.transform.Transform)
        pass  # TODO-impl x7.geom.ElemP1P2.points_transformed test


@tests(ElemRectangle)
class TestElemRectangle(TestCaseElem):
    def make_elements(self) -> List[Elem]:
        pen = PenBrush('red', 'blue')
        return [
            ElemRectangle('r1', pen, Point(1, -1), Point(-3, 4)),
            ElemRectangle('r2', pen, Point(1, 2), Point(3, -4))
        ]

    # noinspection DuplicatedCode
    @tests(ElemRectangle.__init__)
    @tests(ElemRectangle.__str__)
    @tests(ElemRectangle.__repr__)
    @tests(ElemRectangle.as_digi_points)
    @tests(ElemRectangle.bbox)
    @tests(ElemRectangle.bbox_int)
    # @tests(ElemRectangle.bbox_int_update)
    @tests(ElemRectangle.control_paths)
    @tests(ElemRectangle.copy)
    # @tests(ElemRectangle.display)
    @tests(ElemRectangle.draw)
    # @tests(ElemRectangle.draw_space)
    @tests(ElemRectangle.dump)
    # @tests(ElemRectangle.dump_elem)
    # @tests(ElemRectangle.iter_elems)
    @tests(ElemRectangle.paths)
    @tests(ElemRectangle.restore)
    @tests(ElemRectangle.transform)
    def test_defaults(self):
        """Nothing special, just let the default tests run"""
        pass

    @tests(ElemRectangle.__init__)
    def test___init__(self):
        # __init__(self, name: str, penbrush: x7.geom.colors.PenBrush, p1: x7.geom.geom.BasePoint, p2: x7.geom.geom.BasePoint, closed=True, xform: Union[x7.geom.transform.Transform, NoneType] = None)
        pass  # TODO-impl x7.geom.ElemRectangle.__init__ test

    @tests(ElemRectangle.display)
    def test_display(self):
        # display(self, detail=1, prefix='')
        pass  # TODO-impl x7.geom.ElemRectangle.display test


@tests(ElemRectangleRounded)
class TestElemRectangleRounded(TestCaseElem):
    def make_elements(self) -> List[Elem]:
        pen = PenBrush('red', 'blue')
        return [
            ElemRectangleRounded('rr1', pen, Point(1, -1), Point(-3, 4), 0.2),
            ElemRectangleRounded('rr2', pen, Point(1, 2), Point(3, -4), 1)
        ]

    # noinspection DuplicatedCode
    @tests(ElemRectangleRounded.__init__)
    @tests(ElemRectangleRounded.__str__)
    @tests(ElemRectangleRounded.__repr__)
    @tests(ElemRectangleRounded.as_digi_points)
    @tests(ElemRectangleRounded.bbox)
    @tests(ElemRectangleRounded.bbox_int)
    # @tests(ElemRectangleRounded.bbox_int_update)
    @tests(ElemRectangleRounded.control_paths)
    @tests(ElemRectangleRounded.copy)
    # @tests(ElemRectangleRounded.display)
    @tests(ElemRectangleRounded.draw)
    # @tests(ElemRectangleRounded.draw_space)
    @tests(ElemRectangleRounded.dump)
    # @tests(ElemRectangleRounded.dump_elem)
    # @tests(ElemRectangleRounded.iter_elems)
    @tests(ElemRectangleRounded.paths)
    @tests(ElemRectangleRounded.restore)
    @tests(ElemRectangleRounded.transform)
    def test_defaults(self):
        """Nothing special, just let the default tests run"""
        pass

    @tests(ElemRectangleRounded.display)
    def test_display(self):
        # display(self, detail=1, prefix='')
        pass  # TODO-impl x7.geom.ElemRectangleRounded.display test

    @tests(ElemRectangleRounded.make_control_points)
    def test_make_control_points(self):
        # make_control_points(self) -> List[x7.geom.ControlPoint]
        pass  # TODO-impl x7.geom.ElemRectangleRounded.make_control_points test


@tests(Group)
class TestGroup(TestCaseElem):
    def make_elements(self) -> List[Elem]:
        default = PenBrush('default')
        pen = PenBrush('red')
        g1 = Group('group1', default, elems=[
            ElemRectangleRounded('g1_rr1', pen, Point(1, -1), Point(-3, 4), 0.2),
        ])
        elems = []
        for cls in [TestElemCurve, TestElemEllipse, TestElemRectangle, TestElemRectangleRounded]:
            elems.extend(cls().make_elements())
        g2 = Group('group2', default, elems=elems)
        return [g1, g2]

    # noinspection DuplicatedCode
    @tests(Group.__init__)
    @tests(Group.__str__)
    @tests(Group.__repr__)
    @tests(Group.bbox)
    @tests(Group.bbox_int)
    # @tests(Group.bbox_int_update)
    @tests(Group.copy)
    # @tests(Group.display)
    @tests(Group.draw)
    # @tests(Group.draw_space)
    @tests(Group.dump)
    # @tests(Group.dump_elem)
    @tests(Group.restore)
    @tests(Group.transform)
    def test_defaults(self):
        """Nothing special, just let the default tests run"""
        pass

    @tests(Group.display)
    def test_display(self):
        # display(self, detail=1, prefix='')
        pass  # TODO-impl x7.geom.Group.display test

    @tests(Group.as_digi_points)
    def test_elem_as_digi_points(self):
        with self.assertRaises(ValueError):
            self.make_elements()[0].as_digi_points()

    @tests(Group.control_paths)
    def test_elem_control_path(self):
        dc = self.simple_dc()
        for tag, elem in self.enum_elems('control_paths'):
            paths = elem.control_paths(dc)
            self.assertTrue(all((isinstance(path_elem, ControlPath) for path_elem in paths)))
            self.assertMatch([path_elem.points for path_elem in paths], tag)

    @tests(Group.paths)
    def test_elem_path(self):
        for tag, elem in self.enum_elems('paths'):
            paths = elem.paths(self.simple_dc())
            paths = [(p.penbrush, p.closed, p.points.tolist()) for p in paths]
            self.assertMatch(paths, tag)

    @tests(Group.iter_elems)
    def test_elem_iter_elems(self):
        for tag, e in self.enum_elems('iter_elems'):
            with self.subTest(tag):
                xform = Transform().translate(1, 2)
                iterated = list(e.iter_elems('t_root', xform))
                self.assertMatch(iterated, tag)

    @tests(Group.iter_elems_transformed)
    def test_elem_iter_elems_transformed(self):
        for tag, e in self.enum_elems('iter_elems_xf'):
            e = cast(Group, e)
            with self.subTest(tag):
                xform = Transform().rotate_about(10, Point(1, 2))
                iterated = list(e.iter_elems_transformed('t_root', xform))
                self.assertMatch(iterated, tag)


@tests(model)
class TestModModel(TestCaseGeomExtended):
    """Tests for stand-alone functions in x7.geom.model module"""

    @tests(gen_test_model)
    def test_gen_test_model(self):
        # gen_test_model() -> x7.geom.Group
        pass  # TODO-impl x7.geom.gen_test_model test

    @tests(model.gen_test_model_add_one)
    def test_gen_test_model_add_one(self):
        # gen_test_model_add_one() -> x7.geom.Group
        pass  # TODO-impl x7.geom.gen_test_model_add_one test

    @tests(model.gen_test_model_original)
    def test_gen_test_model_original(self):
        # gen_test_model_original() -> x7.geom.Group
        pass  # TODO-impl x7.geom.gen_test_model_original test

    @tests(model.main)
    def test_main(self):
        # main()
        pass  # TODO-impl x7.geom.main test

    @tests(make_ellipse_cps)
    def test_make_ellipse_cps(self):
        # make_ellipse_cps(center: x7.geom.geom.Point, r_x, r_y=None) -> List[x7.geom.ControlPoint]
        pass  # TODO-impl x7.geom.make_ellipse_cps test

    @tests(model.make_ellipse_p1p2_cps)
    def test_make_ellipse_p1p2_cps(self):
        # make_ellipse_p1p2_cps(p1: x7.geom.geom.BasePoint, p2: x7.geom.geom.BasePoint) -> List[x7.geom.ControlPoint]
        pass  # TODO-impl x7.geom.make_ellipse_p1p2_cps test

    @tests(make_rounded_rect_cps)
    def test_make_rounded_rect_cps(self):
        # make_rounded_rect_cps(p1: x7.geom.geom.Point, p2: x7.geom.geom.Point, radius=5.0) -> List[x7.geom.ControlPoint]
        pass  # TODO-impl x7.geom.make_rounded_rect_cps test

    @tests(model.test_model)
    def test_test_model(self):
        # test_model()
        pass  # TODO-impl x7.geom.test_model test


# Delete this so that unittest.loader does not find it
del TestCaseElem
