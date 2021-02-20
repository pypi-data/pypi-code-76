"""
Extended test case that includes x7.geom classes (Point, Vector, ControlPoint)
"""

from typing import Union

from x7.geom.drawing import DrawingContext
from x7.geom.geom import *
from x7.geom.model import *
from x7.geom.colors import *
from x7.geom.transform import *

from x7.testing import support
from x7.testing import extended


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


class PicklerExtensionGeom(support.PicklerExtension):
    """
        Helper object to add geom types to Pickler
    """

    def __init__(self, pickler: support.Pickler):
        super().__init__(pickler)
        self.primitives = (BBox, Point, Vector, ControlPoint, Pen, Brush, PenBrush, Transform)
        self.types = (Elem, )

    def methods(self):
        meths = dict()
        for primitive in self.primitives:
            meths[primitive.__name__] = primitive
        for elem in all_subclasses(Elem):
            meths[elem.__name__] = elem
        # TODO-remove this
        # from pprint import pp
        # pp(dict(PicklerExtensionGeom=meths), sort_dicts=True)
        return meths

    def do_pickle(self, data, prefix: str):
        """Pickle data and return str if possible, else return None"""
        def is_tuple_str_elem_transform(item):
            return isinstance(item, tuple) \
                   and len(item) == 3 \
                   and isinstance(item[0], str) \
                   and isinstance(item[1], Elem) \
                   and isinstance(item[2], Transform)

        def dump_one_elem(elem: Elem):
            """Dump a single Elem"""
            dctx = DumpContext(use_vars=False)
            dctx.depth = len(prefix)//4
            elem.dump(dctx)
            return dctx.output(just_lines=True).lstrip()

        if isinstance(data, Elem):
            return dump_one_elem(data)
        elif isinstance(data, list):
            if all(isinstance(d, Elem) for d in data):
                dc = DumpContext(use_vars=False)
                dc.append('[')
                dc.depth = len(prefix)//4 + 1
                for e in data:
                    e.dump(dc)
                    dc.add_comma()
                dc.depth = 0
                dc.append('%s]' % prefix)
                return dc.output(just_lines=True)
            elif all(is_tuple_str_elem_transform(d) for d in data):
                dc = DumpContext(use_vars=False)
                dc.append('[')
                dc.depth = len(prefix)//4 + 1
                for s, e, t in data:
                    ed = dump_one_elem(e)
                    if ed.count('\n') == 0:
                        dc.append('(%r, %s, %r),' % (s, ed, t))
                    else:
                        dc.append('(%r,' % s)
                        dc.depth += 1
                        e.dump(dc)
                        dc.add_comma()
                        dc.append('%r),' % t)
                        dc.depth -= 1
                dc.depth = 0
                dc.append('%s]' % prefix)
                return dc.output(just_lines=True)
        return None


class ExtendedMatcherControlPoint(extended.ExtendedMatcher):
    """Extended matcher for geom.ControlPoint"""
    ATTRS = ('c', 'dl', 'dr', 'kind')

    def __init__(self, test_case: 'TestCaseGeomExtended'):
        super().__init__(test_case, ControlPoint)

    def almost_equal(self, first, second, places=None, delta=None) -> Union[bool, str]:
        vals_f = [getattr(first, attr) for attr in self.ATTRS]
        vals_s = [getattr(second, attr) for attr in self.ATTRS]
        # TODO-not quite right.  It should understand what was different by attr name
        return self.test_case.almostEqual(vals_f, vals_s, places, delta)

    def explain_mismatch(self, new_data, old_data) -> extended.ExplainReturn:
        vals_n = [getattr(new_data, attr) for attr in self.ATTRS]
        vals_o = [getattr(old_data, attr) for attr in self.ATTRS]
        if all(n.close(o) for n, o in zip(vals_n, vals_o)):
            return True, None
        return False, None


class ExtendedMatcherGeomXY(extended.ExtendedMatcher):
    """Extended matcher for anim.geom.BasePoint or .Vector"""
    KLASS = None

    def __init__(self, test_case: extended.TestCaseExtended):
        super().__init__(test_case, self.KLASS)

    def almost_equal(self, first, second, places=None, delta=None) -> Union[bool, str]:
        almost_x = self.test_case.almostEqualFloat(first.x, second.x)
        almost_y = self.test_case.almostEqualFloat(first.y, second.y)
        msg = []
        if almost_x is not True:
            msg.append('x: ' + almost_x)
        if almost_y is not True:
            msg.append('y: ' + almost_y)
        return ', '.join(msg) if msg else True

    def explain_mismatch(self, new_data, old_data) -> extended.ExplainReturn:
        close: bool = new_data.close(old_data)
        return close, None


class ExtendedMatcherPoint(ExtendedMatcherGeomXY):
    KLASS = BasePoint


class ExtendedMatcherVector(ExtendedMatcherGeomXY):
    KLASS = Vector


class TestCaseGeomExtended(extended.TestCaseExtended):
    PICKLERS = [support.PicklerExtensionImage, PicklerExtensionGeom]
    MATCHERS = [extended.ExtendedMatcherImage, ExtendedMatcherPoint, ExtendedMatcherVector, ExtendedMatcherControlPoint]

    @staticmethod
    def simple_dc(size=1000) -> DrawingContext:
        # noinspection PyPackageRequirements
        from PIL import Image
        image = Image.new('RGBA', (size, size), 'white')
        dc = DrawingContext(image, None)
        dc.points_per_curve = 5
        return dc
