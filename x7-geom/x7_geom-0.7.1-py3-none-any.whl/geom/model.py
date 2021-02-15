"""
Code to describe models for animations
"""

import sys
import math
from abc import ABC, abstractmethod
from PIL import Image, ImagePath
from .drawing import DrawingContext
from .typing import *
from .colors import *
from .geom import *
from .transform import *
from x7.lib.iters import iter_rotate, xy_iter
from .bezier import *


class GeomInternalError(Exception):
    pass


ImagePathType = type(ImagePath.Path([]))

__all__ = [
    'Group', 'GroupBuilder',
    'Elem', 'ElemP1P2', 'ElemCurve', 'ElemEllipse', 'ElemRectangle', 'ElemRectangleRounded',
    'ElemWithHoles',
    'DumpContext', 'ControlPath', 'Path',
    'make_rounded_rect_cps', 'make_ellipse_cps',
    'gen_test_model',
    'ControlPoint', 'bez_split', 'bez', 'bez_path',      # bezier.__all__
]


class DumpContext(object):
    DEFAULT_IMPORTS = [
        'from x7.geom.geom import *',
        'from x7.geom.model import *',
        'from x7.geom.colors import *',
        'from x7.geom.transform import *',
    ]

    def __init__(self, use_vars=True):
        self.depth = 0
        self.lines = []
        self.vars = {}
        self.prefixes = {}
        self.use_vars = use_vars
        self.imports = [] + self.DEFAULT_IMPORTS

    def add_imports(self, imports):
        for i in imports:
            if i not in self.imports:
                self.imports.append(i)

    def output(self, just_lines=False):
        if just_lines:
            return '\n'.join(self.lines)

        var_lines = self.imports + ['']
        for var_value, var_name in sorted(self.vars.items(), key=lambda it: (it[1], it[0])):
            var_lines.append('%s = %s' % (var_name, var_value))
        var_lines.append('')
        self.lines[0] = 'model = ' + self.lines[0]
        return '\n'.join(var_lines + self.lines)

    def prefix(self):
        return '    ' * self.depth

    def __enter__(self):
        self.depth += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.depth -= 1

    def set_var(self, value, prefix='var'):
        if self.use_vars:
            value = repr(value)
            if value not in self.vars:
                self.prefixes[prefix] = self.prefixes.get(prefix, 0) + 1
                self.vars[value] = '%s_%d' % (prefix, self.prefixes[prefix])
            return self.vars[value]
        else:
            return repr(value)

    def append(self, line):
        self.lines.append(self.prefix() + line)

    def extend(self, lines):
        prefix = self.prefix()
        self.lines.extend([prefix + line for line in lines])

    def add_comma(self):
        self.lines[-1] += ','


class Path(object):
    """Primitive path object"""
    __slots__ = ('penbrush', 'closed', 'points')

    def __init__(self, penbrush: PenBrush, closed: bool, points: ImagePathType):
        self.penbrush = penbrush
        if not isinstance(closed, bool):
            raise TypeError("Expected bool, not %r" % closed)
        self.closed = closed
        self.points = points

    def iterxy(self):
        return xy_iter(self.points)

    def extend(self, more_points: ImagePathType, closed=False):
        curr_points = self.points.tolist()
        more_points = more_points.tolist()
        if closed:
            more_points.append(curr_points[-1])
        self.points = ImagePath.Path(curr_points + more_points)


class ControlPath(object):
    """Control path is list of Point/ControlPoint"""
    __slots__ = ('points', )

    def __init__(self, points: List[Union[Point, ControlPoint]]):
        self.points = points

    def __eq__(self, other):
        return type(self) == type(other) and self.points == other.points


class Elem(ABC):
    ELEM_IMPORTS = []   # Placeholder for additional imports required by Elem subclasses

    def __init__(self, name: str, penbrush: PenBrush, closed, xform: Optional[Transform] = None):
        self.name = name or ''
        self.penbrush = penbrush
        self.closed = closed
        self.xform: Transform = xform or Transform()
        if self.penbrush.filled:
            assert self.closed

    @abstractmethod
    def __str__(self):
        ...

    @abstractmethod
    def __repr__(self):
        ...

    @abstractmethod
    def __eq__(self, other):
        return type(self) is type(other) and self.name == other.name \
            and self.penbrush == other.penbrush and self.closed == other.closed \
            and self.xform == other.xform

    def draw_space(self, dc: DrawingContext):
        """
            Usage:
                with self.draw_space(dc):
                    ...
        """
        return dc.matrix.push().compose(self.xform)

    @abstractmethod
    def copy(self):
        """Return deep copy of self"""

    @abstractmethod
    def restore(self, other: 'Elem'):
        """Restore self from copy in other"""
        self.name = other.name
        self.penbrush = other.penbrush
        self.closed = other.closed
        self.xform = other.xform.copy()

    @abstractmethod
    def transform(self, matrix: Transform):
        """
            Return a copy of this shape transformed by matrix.  .transform(identity) is like .copy().

            It is sufficient to just update self.matrix, but transforming the points is preferred.
        """

    def center(self) -> Point:
        """Return the center of the bounding box of this shape"""
        return self.bbox().center

    def bbox(self) -> BBox:
        """Return the bounding box in external space"""
        bb = self.bbox_int()
        b1 = BBox(self.xform.transform_pt(bb.pll), self.xform.transform_pt(bb.phh))
        b2 = BBox(self.xform.transform_pt(bb.plh), self.xform.transform_pt(bb.phl))
        return b1 + b2

    @abstractmethod
    def bbox_int(self) -> BBox:
        """Return the bounding box of this shape in shape internal space"""

    @abstractmethod
    def bbox_int_update(self, bbox: BBox, context=None):
        """Update shape based on changes to bounding box, resize/scale/translate as needed"""

    @abstractmethod
    def paths(self, dc: DrawingContext) -> List[Path]:
        """
            The exterior path of the element.  End point is starting point if closed.
            TODO: define method to adjust how many segments per curve
        """
        ...

    @abstractmethod
    def control_paths(self, dc: DrawingContext) -> List[ControlPath]:
        """
            Just the control points, either as Point() for simple shapes like Rectangle or as
            ControlPoint() for curves

            :return:
        """
        ...

    def draw(self, draw: DrawingContext):
        """Draw the curves into the drawing context"""
        # Drawing modes:
        # PROD:
        # 	1. Outline only				not fill
        #   2. Fill only					closed & fill & color==None
        #   3. Fill and outline		closed & fill & color
        # DEBUG:
        #   1. Add red circles at points and black centerline
        # 	2. Add black border
        # 	3. Both
        # Non-prod:
        #   Skinny line for all

        if draw.show_cps:
            rad = Vector(5, 5)
            for path in self.control_paths(draw):
                for cp in path.points:
                    if isinstance(cp, ControlPoint):
                        draw.draw.line(cp.c.xy()+cp.l.xy(), fill='grey')
                        draw.draw.line(cp.c.xy()+cp.r.xy(), fill='grey')
                        draw.draw.ellipse((cp.l-rad).xy() + (cp.l+rad).xy(), outline='red', fill='grey')
                        draw.draw.ellipse((cp.r-rad).xy() + (cp.r+rad).xy(), outline='red', fill='grey')
                        draw.draw.rectangle((cp.c+rad).xy() + (cp.c-rad).xy(), outline='red', fill='grey')
                    elif isinstance(cp, BasePoint):
                        draw.draw.rectangle((cp+rad).xy() + (cp-rad).xy(), outline='red', fill='grey')
                    else:
                        raise TypeError('unknown control_path element: %r' % cp)

        for path in self.paths(draw):
            p = path.points
            do_fill = path.penbrush.filled
            do_outline = path.penbrush.stroked
            if draw.prod and do_outline:
                # TODO-draw_space?
                width = max(1, round(path.penbrush.stroke_width(draw.matrix)))
            else:
                width = 1
            # print('Elem.draw: prod=%s do_fill=%s do_outline=%s width=%s colors=%s' % (draw.prod, do_fill,
            #       do_outline, width, self.penbrush))
            if draw.shadow_color and path.penbrush.fill_color != TRANSPARENT:
                fill_color = draw.shadow_color
            else:
                fill_color = path.penbrush.fill_color
            # fill_color = self.fill
            if do_fill:
                draw.draw.polygon(p, fill=fill_color)
                if draw.showall:
                    print(draw.draw, dir(draw.draw))
                    draw.show()
                if do_outline:
                    draw.draw.line(p.tolist() + [p[0]], fill=path.penbrush.stroke_color, width=width, joint='curve')
            else:
                draw.draw.line(p, fill=path.penbrush.stroke_color, width=width, joint='curve')
            if draw.debug:
                if not do_outline:
                    pass
                # image.line(p.tolist() + [p[0]], fill='black', width=1)
                else:
                    # TODO-draw_space?
                    rad = max(1, round(path.penbrush.stroke_width(draw.matrix))) / 2
                    # rad = draw.stroke_width(path.penbrush.pen.width) / 2
                    if rad > 2:
                        # Don't need to fill anything if radius is quite small
                        for ti, (x, y) in enumerate(p):
                            # w = w0 + w0*ti/p_len
                            coords = (x - rad, y - rad, x + rad, y + rad)
                            if draw.prod:
                                draw.draw.ellipse(coords, fill=path.penbrush.stroke_color)
                            else:
                                draw.draw.ellipse(coords, outline='red', fill=path.penbrush.stroke_color)

    @abstractmethod
    def display(self, detail=1, prefix='') -> List:
        """Display debug details"""

    def dump_elem(self, dc: DumpContext, **kwargs) -> DumpContext:
        """Format the standard arguments for dump"""
        dc = dc or DumpContext()
        dc.add_imports(self.ELEM_IMPORTS)
        penbrush = dc.set_var(self.penbrush, 'pen')
        basic = '%s(%r, %s, closed=%r, ' % (
            type(self).__name__, self.name, penbrush, self.closed)
        if self.xform != Transform():
            xform = dc.set_var(self.xform, 'xform')
            basic += 'xform=%s, ' % xform
        items = list(kwargs.items())
        if isinstance(items[-1][1], type):
            key, val = items[-1]
            if val is list:
                final_arg = ['%s=[' % key]
            else:
                final_arg = ['%s=%s(' % (key, val.__name__)]
            items.pop()
        else:
            final_arg = []
        args = ['%s=%s' % (key, repr(val)) for key, val in items] + final_arg
        args = ', '.join(args)
        if final_arg:
            dc.append(basic + args)
        else:
            dc.append(basic + args + ')')
        return dc

    @abstractmethod
    def dump(self, context: DumpContext) -> DumpContext:
        """Dump output in python format"""

    def iter_elems(self, root='unknown', matrix=None):
        """Iterate over all elements (which is just this element)"""
        yield root + '.' + self.name, self, matrix

    @abstractmethod
    def as_digi_points(self):
        """Return generator of (dl, c, dr) for all curves"""
        ...

    def as_curves(self):
        cps = [cp.transform(self.xform) for cp in self.as_digi_points()]
        return [ElemCurve(self.name, self.penbrush, control_points=cps, closed=self.closed, xform=Transform())]


class ElemCurve(Elem):
    OFFSET_PT_DEBUG = False
    OFFSET_PT_LIMIT = 100

    def __init__(self, name: str, penbrush: PenBrush,
                 control_points: List[ControlPoint], closed=True, xform: Optional[Transform] = None):
        super().__init__(name, penbrush, closed, xform)
        self.control_points = control_points[:]

    def __str__(self):
        return 'ElemCurve(%r, %s)' % (self.name, ', '.join(str(cp.round(2)) for cp in self.control_points))

    def __repr__(self):
        return 'ElemCurve(%r, %s)' % (self.name, ', '.join(repr(cp) for cp in self.control_points))

    def __eq__(self, other):
        return super().__eq__(other) and self.control_points == other.control_points

    def fixed(self):
        """Return copy with all points 'fixed'"""
        cps = [cp.fixed() for cp in self.control_points]
        return ElemCurve(self.name, self.penbrush, cps, self.closed, self.xform)

    def copy(self):
        """Return deep copy of self"""
        # TODO-This shouldn't really be 'fixed', but we don't have restore() for non-Point yet
        return self.fixed()

    def restore(self, other: 'ElemCurve'):
        """Restore self from copy in other"""
        super().restore(other)
        if len(self.control_points) == len(other.control_points):
            for cp, ocp in zip(self.control_points, other.control_points):
                cp.restore(ocp)
        else:
            msg = 'ElemCurve.restore: self=%d other=%d' % (len(self.control_points), len(other.control_points))
            raise GeomInternalError(msg)

    def control_points_transformed(self, matrix) -> List[ControlPoint]:
        return [cp.transform(matrix) for cp in self.control_points]

    def transform(self, matrix: Transform):
        """Return a copy of this shape transformed by matrix.  .transform(identity) is like .copy()"""
        with matrix.push():
            if self.xform:
                matrix.compose(self.xform)
            cps = [cp.transform(matrix) for cp in self.control_points]
            return ElemCurve(self.name, self.penbrush, cps, self.closed, None)

    def self_intersect(self) -> List['ElemCurve']:
        """Return list of new curves or [] if no intersections"""
        xformed = self.control_points_transformed(self.xform)
        curve_cps = bez_self_intersect(xformed, debug=True)
        return [ElemCurve(self.name + '_i%d' % idx, self.penbrush, cps, closed=self.closed)
                for idx, cps in enumerate(curve_cps)]

    @classmethod
    def offset_pt(cls, dl: Vector, pt: BasePoint, dr: Vector, offset):
        """Compute the new point that is offset from pt by <offset>"""
        if dl == Vector() or dr == Vector():
            # Do not attempt to offset if either vector is zero
            # TODO-should be smarter than this
            return pt
        dl = dl.unit()
        dr = dr.unit()
        if abs(dl.cross(dr)) < 1e-10:
            # Straight segment.  Theta[dl,dr] is 0 or 180
            # print('straight: ', dr, dr.normal(), dr.normal()*offset)
            v_offset = dl.normal()*offset
        else:
            # Angled segment.  -90 < theta[dr,v_offset] < 0 < theta[dr,v_offset] < 90
            v_offset = (dr+dl).unit()
            sin_theta = v_offset.cross(dl)
            scale = offset / sin_theta
            if abs(scale) > cls.OFFSET_PT_LIMIT:
                if cls.OFFSET_PT_DEBUG:
                    print('offset_pt: Limited %.4f to %f' % (scale, cls.OFFSET_PT_LIMIT))
                scale = cls.OFFSET_PT_LIMIT
                # TODO-introduce an arc at this point for outside edge
            v_offset = v_offset * scale
        return pt + v_offset

    def offset(self, offset):
        """Offset this curve by <offset>"""
        transformed = self.transform(Transform())
        points = [(cp.l, cp.c, cp.r) for cp in transformed.control_points]
        points = [pt for pts in points for pt in pts]
        if polygon_area(points) < 0:
            x_cps = [cp.reversed() for cp in reversed(transformed.control_points)]
        else:
            x_cps = transformed.control_points
        debug = False
        if debug:
            print('offset: %s' % offset)
            for cp in transformed.control_points:
                print('  ', cp)
        cps = []
        for cl, cm, cr in iter_rotate(x_cps, 3, -1):
            a, b, c, d, e = cl.r, cm.l, cm.c, cm.r, cr.l
            ab = a-b
            cb = c-b        # also -cm.dl
            bo = self.offset_pt(ab, b, cb, offset)
            co = self.offset_pt(cm.dl, cm.c, cm.dr, offset)
            cd = c-d
            ed = e-d
            do = self.offset_pt(cd, d, ed, offset)
            cps.append(ControlPoint(co, bo-co, do-co, cm.kind))
        if debug:
            print(' =>')
            for cp in cps:
                print('  ', cp)
        return ElemCurve(self.name+'_o', self.penbrush, cps, self.closed, None)

    def bbox_int(self):
        """Return the bounding box of this shape"""
        bb = self.control_points[0].bbox()
        for cp in self.control_points[1:]:
            bb = bb + cp.bbox()
        return bb

    def bbox_int_update(self, bbox: BBox, context=None):
        """Update shape based on changes to bounding box, resize/scale/translate as needed"""
        raise ValueError("Can't bbox_update a curve yet")

    def replace(self, curve, replacement):
        unused(self, curve, replacement)
        return 0

    def add_one(self):
        """
            Add a single control point, but don't change the shape of the curve.
            This is used by Morph to make two curves the same length
        """
        # Figure out where
        orig_len = len(self.control_points)
        cps = self.control_points
        dists = [((a.c-b.c).length(), idx) for idx, (a, b) in enumerate(iter_rotate(cps, 2))]
        dists = sorted(dists)
        left = (dists[-1][1]) % len(cps)
        right = (left + 1) % len(cps)
        # print('add_one: left=%d right=%d len=%d' % (left, right, len(cps)))
        l, m, r = bez_split(cps[left], cps[right])
        cps[left].restore(l)
        cps[right].restore(r)
        cps.insert(right, m)
        assert orig_len + 1 == len(self.control_points)

    def paths(self, dc: DrawingContext) -> List[Path]:
        """
            The extracted points from the digested curves.
        """
        with self.draw_space(dc):
            segments = 10 if dc.show_cps else dc.points_per_curve
            control_points = self.control_points_transformed(dc.matrix)
            if self.closed:
                extra = control_points  # Loop back to start
            else:
                extra = []  # Ignore start
            pts = []  # list(self.control_points[0].c.xy())
            skip = 0
            for p, q in zip(control_points, control_points[1:] + extra):
                bez_pts = bez((p.c, p.r, q.l, q.c), steps=segments)
                pts.extend(bez_pts[skip:])
                skip = 2  # Skip first point going forward, as it is same as last point

            return [Path(self.penbrush, self.closed, ImagePath.Path(pts))]

    def control_paths(self, dc) -> List[ControlPath]:
        """
            Just the control points
        """
        with self.draw_space(dc):
            return [ControlPath(self.control_points_transformed(dc.matrix))]

    def display(self, detail=1, prefix=''):
        """Display debug details"""
        print('%sElemCurve: %s %d points' % (prefix, self.name, len(self.control_points)))
        if detail:
            print('%s closed=%s pen=%s' % (prefix, self.closed, self.penbrush))
            for cp in self.control_points:
                print('%s  %r' % (prefix, cp))

    def dump(self, context: DumpContext) -> DumpContext:
        self.dump_elem(context, control_points=list)
        with context:
            for cp in self.control_points:
                context.append(repr(cp) + ',')
        context.append('])')
        return context

    def as_digi_points(self):
        return self.control_points


class ElemP1P2(Elem, ABC):
    def __init__(self, name: str, penbrush: PenBrush, p1: BasePoint, p2: BasePoint,
                 closed=True, xform: Optional[Transform] = None):
        assert closed is True
        super().__init__(name, penbrush, closed=True, xform=xform)
        self.p1 = p1.fixed()
        self.p2 = p2.fixed()

    def __str__(self):
        return '%s(%r, %r, %r)' % (type(self).__name__, self.name, self.p1, self.p2)

    def __repr__(self):
        return '%s(%r, %r, %r)' % (type(self).__name__, self.name, self.p1, self.p2)

    def __eq__(self, other):
        return super().__eq__(other) and self.p1 == other.p1 and self.p2 == other.p2

    def bbox_int(self) -> BBox:
        """Return the bounding box of this shape"""
        return BBox(self.p1, self.p2)

    def bbox_int_update(self, bbox: BBox, context=None):
        """Update shape based on changes to bounding box, resize/scale/translate as needed"""
        self.p1.restore(bbox.p1)
        self.p2.restore(bbox.p2)

    def copy(self):
        """Return copy of self"""
        p1 = self.p1.copy()
        p2 = self.p2.copy()
        return type(self)(self.name, self.penbrush, p1, p2, self.closed, xform=self.xform)

    def restore(self, other: 'ElemP1P2'):
        """Restore self from copy in other"""
        super().restore(other)
        self.p1.restore(other.p1)
        self.p2.restore(other.p2)

    def transform_pts(self, matrix: Transform, points: PointList) -> Tuple[Transform, PointList]:
        """Helper for .transform(): return residual rotation matrix and transform points"""
        with matrix.push().compose(self.xform) as xform:
            xlate, rotate = xform.simplify()
            points = [rotate.untransform_pt(xform.transform_pt(pt)) for pt in points]
            return rotate, points

    def transform(self, matrix: Transform):
        """Return a copy of this shape transformed by matrix.  .transform(identity) is like .copy()"""
        rotate, (p1, p2) = self.transform_pts(matrix, [self.p1, self.p2])
        return type(self)(self.name, self.penbrush, xform=rotate, p1=p1, p2=p2)

    def points(self) -> List[Point]:
        """Return all four corners as List[Point]"""

        p1 = self.p1
        p2 = self.p2
        p1x, p1y = p1.xy()
        p2x, p2y = p2.xy()
        return [p1, Point(p1x, p2y), p2, Point(p2x, p1y)]

    def points_transformed(self, matrix: Transform):
        return matrix.transform_pts(self.points())

    @abstractmethod
    def make_control_points(self) -> List[ControlPoint]:
        ...

    def control_points_transformed(self, matrix: Transform):
        return [cp.transform(matrix) for cp in self.make_control_points()]

    def control_paths(self, dc) -> List[ControlPath]:
        """
            Just the control points
        """
        with self.draw_space(dc):
            return [ControlPath(self.control_points_transformed(dc.matrix))]

    def as_digi_points(self):
        return self.make_control_points()


class ElemRectangle(ElemP1P2):
    def __init__(self, name: str, penbrush: PenBrush, p1: BasePoint, p2: BasePoint,
                 closed=True, xform: Optional[Transform] = None):
        assert closed is True
        super().__init__(name, penbrush, p1, p2, closed=True, xform=xform)

    def paths(self, dc: DrawingContext) -> List[Path]:
        """
            The path of the rectangle
        """
        with self.draw_space(dc):
            path = [p.xy() for p in self.points_transformed(dc.matrix)]
        path.append(path[0])
        return [Path(self.penbrush, self.closed, ImagePath.Path(path))]

    def control_paths(self, dc) -> List[ControlPath]:
        """
            Just the corner points
        """
        with self.draw_space(dc):
            return [ControlPath(self.points_transformed(dc.matrix))]

    def display(self, detail=1, prefix=''):
        """Display debug details"""
        print('%sElemRectangle: %s %s %s' % (prefix, self.name, self.p1.round(2).xy(), self.p2.round(2).xy()))
        if detail:
            print('%s closed=%s pen=%s' % (prefix, self.closed, self.penbrush))

    def dump(self, context: DumpContext) -> DumpContext:
        return self.dump_elem(context, p1=self.p1, p2=self.p2)

    def make_control_points(self) -> List[ControlPoint]:
        """Return list of ControlPoints"""
        return [ControlPoint(p, Vector(), Vector()) for p in self.points()]


def make_rounded_rect_cps(p1: Point, p2: Point, radius=5.0) -> List[ControlPoint]:
    bez_90 = 4/3 * math.tan(math.radians(90/4))
    p1x, p1y = p1.xy()
    p2x, p2y = p2.xy()
    pts = [p1, Point(p1x, p2y), p2, Point(p2x, p1y)]
    clipped = False
    cps = []
    for a, b, c in iter_rotate(pts, 3, -1):
        ab = a-b
        cb = c-b
        ab_len = ab.length()/2
        cb_len = cb.length()/2
        new_radius = min(radius, ab_len, cb_len)
        if new_radius <= radius:
            clipped = True
        ab = ab.unit()*new_radius if ab_len else Vector(0, 0)
        cb = cb.unit()*new_radius if cb_len else Vector(0, 0)
        ab_scale = min(ab_len - new_radius, new_radius)/new_radius if new_radius else 0
        cb_scale = min(cb_len - new_radius, new_radius)/new_radius if new_radius else 0
        bab = b+ab
        bcb = b+cb
        ab *= bez_90
        cb *= bez_90
        cps.append(ControlPoint(bab, dl=ab_scale * ab, dr=-ab))
        cps.append(ControlPoint(bcb, dl=-cb, dr=cb_scale * cb))
    # Look for clipped radius events and remove duplicate control points
    if clipped:
        out = []
        for a, b, c in iter_rotate(cps, 3):
            if b.c == c.c:
                b.dr = c.dr
            elif b.c == a.c:
                continue
            out.append(b)
        cps = out
    return cps


def make_ellipse_p1p2_cps(p1: BasePoint, p2: BasePoint) -> List[ControlPoint]:
    bb = BBox(p1, p2)
    return make_ellipse_cps(bb.center, bb.width/2, bb.height/2)


def make_ellipse_cps(center: Point, r_x, r_y=None) -> List[ControlPoint]:
    """Make 4 control points to create a circle"""
    bez_90 = 4/3 * math.tan(math.radians(90/4))
    r_y = r_x if r_y is None else r_y
    vr = Vector(r_x, 0)
    vrb = vr*bez_90
    vu = Vector(0, r_y)
    vub = vu*bez_90
    cps = [
        ControlPoint(center+vr, vub, -vub),
        ControlPoint(center-vu, vrb, -vrb),
        ControlPoint(center-vr, -vub, vub),
        ControlPoint(center+vu, -vrb, vrb),
    ]
    return cps


class ElemRectangleRounded(ElemP1P2):
    def __init__(self, name: str, penbrush: PenBrush, p1: BasePoint, p2: BasePoint, radius,
                 closed=True, xform: Optional[Transform] = None):
        assert closed is True
        super().__init__(name, penbrush=penbrush, p1=p1, p2=p2, closed=True, xform=xform)
        self.radius = radius

    def __str__(self):
        return 'ElemRectangleRounded(%r, %r, %r, %r)' % (self.name, self.p1, self.p2, self.radius)

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (type(self).__name__, self.name, self.p1, self.p2, self.radius)

    def __eq__(self, other):
        return super().__eq__(other) and self.radius == other.radius

    def copy(self):
        """Return deep copy of self"""
        p1 = self.p1.copy()
        p2 = self.p2.copy()
        return ElemRectangleRounded(self.name, self.penbrush, p1, p2, self.radius, self.closed, xform=self.xform)

    def restore(self, other: 'ElemRectangleRounded'):
        """Restore self from copy in other"""
        super().restore(other)
        self.p1.restore(other.p1)
        self.p2.restore(other.p2)
        self.radius = other.radius

    def transform(self, matrix: Transform):
        """Return a copy of this shape transformed by matrix.  .transform(identity) is like .copy()"""
        rotate, (p1, p2, p1r) = self.transform_pts(matrix, [self.p1, self.p2, self.p1+Vector(self.radius, 0)])
        radius = (p1r-p1).length()
        return ElemRectangleRounded(self.name, self.penbrush, xform=rotate, p1=p1, p2=p2, radius=radius)

    def make_control_points(self) -> List[ControlPoint]:
        return make_rounded_rect_cps(self.p1, self.p2, self.radius)

    def paths(self, dc: DrawingContext) -> List[Path]:
        """
            The path of the rectangle
        """
        with self.draw_space(dc):
            cps = self.make_control_points()
            path = bez_path(dc.matrix, cps, True)
            return [Path(self.penbrush, self.closed, ImagePath.Path(path))]

    def display(self, detail=1, prefix=''):
        """Display debug details"""
        print('%sElemRectangleRounded: %s %s %s %s' % (
            prefix, self.name, self.p1.round(2).xy(), self.p2.round(2).xy(), round(self.radius, 2)))
        if detail:
            print('%s closed=%s pen=%s' % (prefix, self.closed, self.penbrush))

    def dump(self, context: DumpContext) -> DumpContext:
        return self.dump_elem(context, p1=self.p1, p2=self.p2, radius=self.radius)


class ElemEllipse(ElemP1P2):
    def __init__(self, name: str, penbrush: PenBrush, p1: BasePoint, p2: BasePoint,
                 closed=True, xform: Optional[Transform] = None):
        assert closed is True
        super().__init__(name, penbrush=penbrush, p1=p1, p2=p2, closed=True, xform=xform)

    def make_control_points(self) -> List[ControlPoint]:
        return make_ellipse_p1p2_cps(self.p1, self.p2)

    def paths(self, dc: DrawingContext) -> List[Path]:
        """
            The path of the ellipse
        """
        with self.draw_space(dc):
            cps = self.make_control_points()
            path = bez_path(dc.matrix, cps, True)
            return [Path(self.penbrush, self.closed, ImagePath.Path(path))]

    def display(self, detail=1, prefix=''):
        """Display debug details"""
        print('%sElemEllipse: %s %s %s' % (
            prefix, self.name, self.p1.round(2).xy(), self.p2.round(2).xy()))
        if detail:
            print('%s closed=%s pen=%s' % (prefix, self.closed, self.penbrush))

    def dump(self, context: DumpContext) -> DumpContext:
        return self.dump_elem(context, p1=self.p1, p2=self.p2)


class Group(Elem):
    def __init__(
            self,
            name,
            penbrush,
            hidden=False,
            xform: Transform = None,
            elems: Union[Dict[str, Elem], List[Elem], None] = None,
            points: Optional[Dict[str, BasePoint]] = None,
            closed=False,
            fix_names=False,
    ):
        super().__init__(name, penbrush, closed=closed, xform=xform)
        self.elems: Dict[str, Elem] = {}
        self.hidden = hidden
        self.points: Dict[str, BasePoint] = points or {}
        if elems:
            if isinstance(elems, (list, tuple)):
                for elem in elems:
                    self.add(elem.name, elem, fix_names)
            elif isinstance(elems, dict):
                self.elems = dict(elems)
            else:
                raise TypeError('List[Elem] or Dict[str,Elem] required, not %r' % elems)

    def __str__(self):
        return 'Group(%s, %d elems, %d points)' % (self.name, len(self.elems), len(self.points))

    def __repr__(self):
        return 'Group(%r, %r, %r, %r, %r, %r)' % (self.name, self.penbrush, self.hidden,
                                                  self.xform, self.elems, self.points)

    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.hidden == other.hidden and
            self.elems == other.elems and
            self.points == other.points
        )

    def paths(self, dc: DrawingContext) -> List[Path]:
        if self.hidden:
            return []

        paths = []
        with dc.matrix.push():
            if self.xform:
                dc.matrix.compose(self.xform)
            for name, elem in self.elems.items():
                paths.extend(elem.paths(dc))
        return paths

    def control_paths(self, dc) -> List[ControlPath]:
        if self.hidden:
            return []
        paths = []
        with self.draw_space(dc):
            for name, elem in self.elems.items():
                paths.extend(elem.control_paths(dc))
        return paths

    def as_digi_points(self):
        raise ValueError('Use .as_curves() instead')

    def as_curves(self):
        return [c.transform(self.xform) for e in self.elems.values() for c in e.as_curves()]

    def bbox_int(self) -> BBox:
        if not self.elems:
            raise GeomInternalError('Group.bbox_int on empty group')
        bbox = BBox(None)
        for elem in self.elems.values():
            bbox = bbox + elem.bbox()
        return bbox

    def bbox_int_update(self, bbox: BBox, context=None):
        raise ValueError("Can't bbox_int_update a Group yet")

    def copy(self):
        elems = dict(self.elems)
        points = dict(self.points)
        return Group(self.name, self.penbrush, self.hidden, self.xform.copy(), elems, points)

    def restore(self, other: 'Group'):
        self.name = other.name
        self.penbrush = other.penbrush
        self.hidden = other.hidden
        self.xform = other.xform
        self.elems = dict(other.elems)
        self.points = dict(other.points)

    def transform(self, matrix: Transform):
        xform = matrix.copy().compose(self.xform)
        return Group(self.name, self.penbrush, self.hidden, xform, dict(self.elems), dict(self.points))

    def add(self, name, elem, fixname=False):
        if fixname and '.' in name or name in self.elems:
            name = name.rpartition('.')[2]
            if name in self.elems:
                name = type(elem).__name__
                if name.startswith('Elem'):
                    name = name[4:]
                name = name.lower()
                num = 0
                while (name_try := '%s#%d' % (name, num)) in self.elems:
                    num += 1
                name = name_try
        if '.' in name:
            raise ValueError('name may not contain ".": %r' % name)
        if name in self.elems:
            raise ValueError('duplicate name: %r' % name)
        self.elems[name] = elem
        elem.name = name

    def display(self, detail=1, prefix=''):
        print('%sElemGroup: %r %s' % (prefix, self.name, 'hidden' if self.hidden else 'visible'))
        prefix += '  '
        if self.xform != Transform():
            print('%sTransform: %s' % (prefix, self.xform))
        for name, pt in sorted(self.points.items()):
            print('%sPoint: %s %s' % (prefix, name, pt))
        for name, elem in sorted(self.elems.items()):
            elem.display(detail=detail, prefix=prefix)

    def dump(self, context: Optional[DumpContext] = None) -> DumpContext:
        context = context or DumpContext()
        self.dump_elem(context, elems=list)
        with context:
            for name, elem in sorted(self.elems.items()):
                elem.dump(context)
                context.add_comma()
        context.append('])')
        return context

    def iter_elems(self, root=None, matrix=None) -> Iterator[Tuple[str, Elem, Transform]]:
        """Deep iteration, return raw elements with name & transform"""
        matrix = matrix or Transform()
        if self.xform:
            matrix.push()
            matrix.compose(self.xform)
        for elem in self.elems.values():
            yield from elem.iter_elems(root + '.' + self.name if root else self.name, matrix)
        if self.xform:
            matrix.pop()

    def iter_elems_transformed(self, root=None, matrix=None) -> List[Elem]:
        """Shallow iteration, return transformed elements"""
        matrix = matrix or Transform()
        with matrix.push():
            if self.xform:
                matrix.compose(self.xform)
            root = root + '.' + self.name if root else self.name
            for elem in self.elems.values():
                xf = elem.transform(matrix)
                xf.name = root + '.' + xf.name
                yield xf

    def lookup(self, tag: str) -> Elem:
        head, sep, tail = tag.partition('.')
        if head not in self.elems:
            raise KeyError('%s: expected %s' % (head, ', '.join(self.elems.keys())))
        item = self.elems[head]
        if tail:
            if isinstance(item, Group):
                return item.lookup(tail)
            else:
                raise ValueError('no sub-group found for %r' % tail)
        else:
            return item

    def replace(self, elem: Elem, replacement):
        """Replace this elem throughout the model.  Return count of replacements"""

        count = 0
        for name, e in list(self.elems.items()):
            if e == elem:
                print('Replacing %s with %s: %s' % (name, replacement.name, ','.join(self.elems.keys())))
                del self.elems[name]
                if replacement.name in self.elems:
                    raise ValueError("Cannot replace %r into Group(%r) because it already exists" % (
                        replacement.name, self.name))
                self.add(replacement.name, replacement)
                count += 1
            elif hasattr(e, 'replace'):
                count += e.replace(elem, replacement)
        return count

    def add_pt(self, name, pt):
        assert name not in self.points
        assert '.' not in name
        self.points[name] = pt
        pt.name = name
        return pt

    def lookup_pt(self, name):
        assert '.' not in name
        return self.points[name]


class ElemWithHoles(Elem):
    def __init__(self, name: str, penbrush: PenBrush,
                 outside: Elem, inside: List[Elem],
                 closed=True, xform: Optional[Transform] = None):
        super().__init__(name, penbrush, closed=closed, xform=xform)
        self.outside = outside
        self.inside = inside
        self.outside.penbrush = penbrush
        for elem in self.inside:
            elem.penbrush = penbrush

    def __str__(self):
        return 'ElemWithHoles(%s, %s, [%s])' % (
            self.name,
            self.outside.__class__.__name__,
            ', '.join(e.__class__.__name__ for e in self.inside)
        )

    def __repr__(self):
        return 'ElemWithHoles(%r, %r, %r, %r, %r, %r)' % (
            self.name, self.penbrush,
            self.outside, self.inside,
            self.closed, self.xform
        )

    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.outside == other.outside and
            self.inside == other.inside
        )

    def paths(self, dc: DrawingContext) -> List[Path]:
        with self.draw_space(dc):
            # TODO-make one continuous path:
            #       1. reorient if needed
            #       2. get insides
            #       3. join outside and inside
            #       4. return [
            #           4a. conjoined path with penbrush.fill
            #           4b. other edges with penbrush.pen
            #       ]
            edges = self.outside.paths(dc)
            assert len(edges) == 1
            edge_brush = PenBrush(self.penbrush.pen, None)
            edges[0].penbrush = edge_brush
            fill_brush = PenBrush(None, self.penbrush.brush)  # Just the fill component
            if fill_brush.brush:
                fill_path = Path(fill_brush, edges[0].closed, edges[0].points)
                for elem in self.inside:
                    paths = elem.paths(dc)
                    for path in paths:
                        path.penbrush = edge_brush
                        edges.extend(paths)
                        fill_path.extend(path.points, closed=True)
                return [fill_path] + edges
            else:
                for elem in self.inside:
                    paths = elem.paths(dc)
                    for path in paths:
                        path.penbrush = edge_brush
                    edges.extend(paths)
                return edges

    def control_paths(self, dc) -> List[ControlPath]:
        with self.draw_space(dc):
            paths = self.outside.control_paths(dc)
            for elem in self.inside:
                paths.extend(elem.control_paths(dc))
        return paths

    def as_digi_points(self):
        raise ValueError('Use .as_curves() instead')

    def as_curves(self):
        all_elems = [self.outside] + self.inside
        return [c.transform(self.xform) for e in all_elems for c in e.as_curves()]

    def bbox_int(self) -> BBox:
        bbox_outside = self.outside.bbox_int()
        debug = True
        if debug:
            bbox_inside = BBox(None)
            for elem in self.inside:
                bbox_inside = bbox_inside + elem.bbox()
            assert bbox_outside.contains(bbox_inside)
        return bbox_outside

    def bbox_int_update(self, bbox: BBox, context=None):
        raise ValueError("Can't bbox_int_update an ElemWithHoles yet")

    def copy(self):
        return ElemWithHoles(
            self.name, self.penbrush, self.outside.copy(),
            [e.copy() for e in self.inside], self.closed, self.xform.copy())

    def restore(self, other: 'ElemWithHoles'):
        self.name = other.name
        self.penbrush = other.penbrush
        self.closed = other.closed
        self.xform = other.xform
        self.outside = other.outside.copy()
        self.inside = [e.copy() for e in self.inside]

    def transform(self, matrix: Transform):
        xform = matrix.copy().compose(self.xform)
        return ElemWithHoles(
            self.name, self.penbrush, self.outside.copy(),
            [e.copy() for e in self.inside], self.closed, xform.copy())

    def display(self, detail=1, prefix=''):
        print('%sElemWithHoles: %r' % (prefix, self.name))
        prefix += '  '
        if self.xform != Transform():
            print('%sTransform: %s' % (prefix, self.xform))
        print('%sOutside:' % prefix)
        self.outside.display(detail=detail, prefix=prefix + '  ')
        print('%sOutside:' % prefix)
        for elem in sorted(self.inside):
            elem.display(detail=detail, prefix=prefix + '  ')

    def dump(self, context: Optional[DumpContext] = None) -> DumpContext:
        context = context or DumpContext()
        self.dump_elem(context, outside=self.outside, inside=list)
        with context:
            for elem in self.inside:
                elem.dump(context)
                context.add_comma()
        context.append('])')
        return context

    def iter_elems(self, root=None, matrix=None) -> Iterator[Tuple[str, Elem, Transform]]:
        """Deep iteration, return raw elements with name & transform"""
        matrix = matrix or Transform()
        with matrix.push().compose(self.xform):
            base = '%s.%s.' % (root, self.name) if root else self.name
            yield from self.outside.iter_elems(base + '.outside', matrix)
            for elem in self.inside:
                yield from elem.iter_elems(base + '.inside', matrix)

    def iter_elems_transformed(self, root=None, matrix=None) -> List[Elem]:
        """Shallow iteration, return transformed elements"""
        matrix = matrix or Transform()
        with matrix.push().compose(self.xform):
            base = '%s.%s' % (root, self.name) if root else self.name
            xf = self.outside.transform(matrix)
            xf.name = base+'.outside.'+xf.name
            yield xf
            for elem in self.inside:
                xf = elem.transform(matrix)
                xf.name = base+'.inside.'+xf.name
                yield xf

    def lookup(self, tag: str) -> Elem:
        head, sep, tail = tag.partition('.')
        if head == 'outside':
            if tail == self.outside.name:
                return self.outside
        elif head == 'inside':
            for elem in self.inside:
                if tail == elem.name:
                    return elem
        raise KeyError('%s: expected outside.%s or inside.{%s}, not %s' % (
            self.name, self.outside.name, ', '.join(e.name for e in self.inside), tag))

    def replace(self, elem: Elem, replacement):
        """Replace this elem throughout the model.  Return count of replacements"""
        unused(elem, replacement)
        raise NotImplementedError


class GroupBuilder(object):
    """Convenience function to help when building shapes in code"""
    def __init__(
            self,
            name,
            pens_by_shape: PensByShape,
            shape_kind='edge',
            group: Group = None,
    ):
        self.name = name
        if not isinstance(pens_by_shape, PensByShape):
            raise TypeError('expected PensByShape, not %r' % pens_by_shape)
        self.pens_by_shape = pens_by_shape
        self.default_shape_kind = shape_kind
        self.hidden = False
        self.the_group = group or Group(name, PenBrush('default'))

    def point(self, name, x, y):
        return self.the_group.add_pt(name, Point(x, y))

    def add_pt(self, name, pt):
        return self.the_group.add_pt(name, pt)

    def lookup_pt(self, tag: str):
        return self.the_group.lookup_pt(tag)

    def add(self, name, elem):
        self.the_group.add(name, elem)

    def lookup(self, tag: str):
        return self.the_group.lookup(tag)

    def elem_any(self, elem_class: type, name: str, shape_kind=None, closed=None, **kwargs) -> Elem:
        """
            Internal function to create a sub-element and add to this group.  Call the more specific ones instead.
        """
        if isinstance(shape_kind, PenBrush):
            penbrush = shape_kind
        else:
            shape_kind = shape_kind or self.default_shape_kind
            penbrush = self.pens_by_shape[shape_kind]
        closed = penbrush.filled if closed is None else closed

        e = elem_class(name, penbrush=penbrush, closed=closed, **kwargs)
        self.add(name, e)
        return e

    def rect(self, name, p1, p2, shape_kind=None, closed=True) -> ElemRectangle:
        """
            Create a sub-element and add to this group.
            :param name:
            :param p1:      A corner of the rectangle
            :param p2:      The other corner
            :param shape_kind:	Either a shape_kind (edged, filled, ...) or a PenBrush() value
            :param closed: True if shape is closed.  Defaults to filled
            :return:
        """
        return cast(ElemRectangle, self.elem_any(ElemRectangle, name, shape_kind, closed, p1=p1, p2=p2))

    def rrect(self, name, p1, p2, radius, shape_kind=None, closed=True) -> ElemRectangleRounded:
        """
            Create a sub-element and add to this group.
            :param name:
            :param p1:      A corner of the rectangle
            :param p2:      The other corner
            :param radius:  Corner radius
            :param shape_kind:	Either a shape_kind (edged, filled, ...) or a PenBrush() value
            :param closed: True if shape is closed.  Defaults to filled
            :return:
        """
        elem = self.elem_any(ElemRectangleRounded, name, shape_kind, closed, p1=p1, p2=p2, radius=radius)
        return cast(ElemRectangleRounded, elem)

    def ellipse(self, name, p1, p2, shape_kind=None, closed=True) -> ElemEllipse:
        """
            Create a sub-element and add to this group.
            :param name:
            :param p1:      A corner of the bounding rectangle
            :param p2:      The other corner
            :param shape_kind:	Either a shape_kind (edged, filled, ...) or a PenBrush() value
            :param closed: True if shape is closed.  Defaults to filled
            :return:
        """
        return cast(ElemEllipse, self.elem_any(ElemEllipse, name, shape_kind, closed, p1=p1, p2=p2))

    def curve(self, name, cps: List[ControlPoint], shape_kind=None, closed=None) -> ElemCurve:
        """
            Create a sub-element and add to this group.
            :param name:
            :param cps:    The control points
            :param shape_kind:	Either a shape_kind (edged, filled, ...) or a PenBrush() value
            :param closed: True if shape is closed.  Defaults to filled
            :return:
        """
        return cast(ElemCurve, self.elem_any(ElemCurve, name, shape_kind, closed, control_points=cps))

    def group(self, name, pens_by_shape=None, shape_kind=None) -> 'GroupBuilder':
        pens_by_shape = pens_by_shape or self.pens_by_shape
        shape_kind = shape_kind or self.default_shape_kind
        g = GroupBuilder(name, pens_by_shape=pens_by_shape, shape_kind=shape_kind)
        self.add(name, g.the_group)
        return g

    def rotate_about_center(self, elem, angle, show=False, extra=''):
        """Rotate elem about its center point, add to group, and return it"""
        bbox = elem.bbox()
        center = bbox.center
        # print('%s.rotate_about(%s, %s)' % (elem.name, angle, center))
        new = elem.transform(Transform().rotate_about(angle, center))
        self.add(elem.name + '_r' + extra, new)
        if show:
            v = Vector(1, 1)
            self.ellipse(elem.name + '_c' + extra, center - v, center + v, elem.penbrush)
        return new

    def hide(self):
        self.hidden = True

    def draw(self, draw: DrawingContext):
        self.the_group.draw(draw)
        show_bb = False
        if show_bb:
            bb = self.the_group.bbox()
            e = ElemRectangle('random', PenBrush('red'), bb.p1, bb.p2)
            e.draw(draw)

    def display(self, detail=1, prefix=''):
        print('%sGroupBuilder: %s' % (prefix, self.name))
        prefix += '  '
        self.the_group.display(detail, prefix)

    def dump(self, dc: Optional[DumpContext] = None) -> DumpContext:
        dc = dc or DumpContext()
        self.the_group.dump(dc)
        return dc

    def iter_elems(self, root=None, matrix=None) -> Iterator[Tuple[str, Elem, Transform]]:
        return self.the_group.iter_elems(root, matrix)

    def iter_elems_transformed(self, root=None, matrix=None) -> List[Elem]:
        return self.the_group.iter_elems_transformed(root, matrix)

    def replace(self, elem, replacement):
        """Replace this elem throughout the model.  Return count of replacements"""

        return self.the_group.replace(elem, replacement)


def gen_test_model_original() -> GroupBuilder:
    test = GroupBuilder('test', PensByShape())
    sub = test.group('sub', None)
    pt = test.point('point', 50, -50)

    outside = ElemCurve('out', PenBrush('pink', 'yellow'), control_points=[
        ControlPoint(Point(-80, 2), Vector(0, -50), Vector(0, 50)),
        ControlPoint(Point(-10, 2), Vector(0, 50), Vector(0, -50)),
    ])
    inside1 = ElemCurve('in', PenBrush('pink', 'yellow'), control_points=[
        ControlPoint(Point(-60, -20), Vector(0, -10), Vector(0, 10)),
        ControlPoint(Point(-30, -20), Vector(0, 10), Vector(0, -10)),
    ])
    inside1.control_points = ControlPoint.reverse_list(inside1.control_points)
    inside2 = ElemCurve('in', PenBrush('pink', 'yellow'), control_points=[
        ControlPoint(Point(-60, 20), Vector(0, -10), Vector(0, 10)),
        ControlPoint(Point(-30, 20), Vector(0, 10), Vector(0, -10)),
    ])

    whole = ElemWithHoles('whole', PenBrush(('blue', 5), 'orange'), outside, [inside1, inside2])
    sub.add('whole', whole)
    whole_xf = whole.transform(Transform().translate(100, 0))
    whole_xf.penbrush = PenBrush('green')
    sub.add('whole_xf', whole_xf)
    # return test

    sub.curve('c', shape_kind=PenBrush('blue'), closed=True, cps=[
        ControlPoint(Point(-50, -50), Vector(0, 100), Vector(0, -100)),
        ControlPoint(pt, Vector(0, -20), Vector(0, 20)),
    ])

    sub.curve('d', shape_kind=PenBrush(Pen('green', 1)), closed=False, cps=[
        ControlPoint(Point(-40, -40), Vector(), Vector(), 'sharp'),
        ControlPoint(Point(40, 40), Vector(), Vector(), 'sharp'),
        ControlPoint(Point(60, 20), Vector(), Vector(), 'sharp'),
    ])

    up = Vector(0, 1)
    rt = Vector(1, 0)

    radius = 30
    sub.curve('e', shape_kind=PenBrush(('yellow', 5)), closed=True, cps=[
        ControlPoint(Point(-50, 0), -up*radius, up*radius),
        ControlPoint(Point(0, 50), -rt*radius, rt*radius),
        ControlPoint(Point(50, 0), up*radius, -up*radius),
        ControlPoint(Point(0, -50), rt*radius, -rt*radius),
    ])

    for smooth in [1, 2, 4, 8, 16, 32, 64]:
        x, y = -60, 60

        cp_raw = [(x+10, y, -up*smooth), (x, y+10, rt*smooth), (x-10, y, up*smooth), (x, y-10, -rt*smooth)]
        sub.curve(
            'i%d' % smooth, shape_kind=PenBrush('green'), closed=True,
            cps=[ControlPoint(Point(x, y), v, -v) for x, y, v in cp_raw]
        )

    # noinspection DuplicatedCode
    j = sub.curve('j', [
        ControlPoint(Point(-80, -80), Vector(10, -10), Vector(-10, 10), 'very-smooth'),
        ControlPoint(Point(-80, -50), Vector(-10, -5), Vector(20, 10), 'smooth'),
        ControlPoint(Point(-30, -60), Vector(-30, 0), Vector(0, -30), 'sharp')
    ], PenBrush('black', 'grey'))

    jj = j.offset(-1)
    sub.add(jj.name, jj)

    j = sub.curve('j_rev', [
        ControlPoint(Point(80, -10), Vector(0, -30), Vector(-30, 0), 'sharp'),
        ControlPoint(Point(30, 0), Vector(20, 10), Vector(-10, -5), 'smooth'),
        ControlPoint(Point(30, -30), Vector(-10, 10), Vector(10, -10), 'very-smooth'),
    ], PenBrush('black', 'grey'))
    jj = j.offset(-1)
    sub.add(jj.name, jj)

    k = sub.rect('k', Point(50, -50), Point(75, -75), PenBrush(('red', 1), 'cyan'))
    sub.rotate_about_center(k, 45)

    le = sub.rrect('l', Point(-20, -30), Point(20, -70), 10, PenBrush('red', 'cyan'))
    le = sub.rotate_about_center(le, 10)
    sub.rotate_about_center(le, 10)

    off = Vector(0, 30)
    m = sub.ellipse('m', Point(-20, -5)+off, Point(20, 5)+off, PenBrush('black', 'grey'))
    if not False:
        for n in range(5):
            m = sub.rotate_about_center(m, 36, False)

    n = sub.curve('n', shape_kind=PenBrush('green', 'tan'), cps=[
        ControlPoint(Point(50, 60), Vector(0, -20), Vector(0, 20), 'smooth'),
        ControlPoint(Point(90, 60), Vector(0, 10), Vector(0, -10), 'smooth'),
    ])
    sub.rotate_about_center(n, 45)

    # for elem in sub.elems.values():
    #     elem.restore(elem.transform(Transform().rotate(10)))
    # print(test.dump().output())
    return test


def gen_test_model_offset() -> GroupBuilder:
    test = GroupBuilder('test', PensByShape())
    sub = test.group('sub', None)
    pt = test.point('point', 50, -50)
    unused(pt)

    # noinspection DuplicatedCode
    j = sub.curve('j', [
        ControlPoint(Point(-80, -80), Vector(10, -10), Vector(-10, 10), 'very-smooth'),
        ControlPoint(Point(-80, -50), Vector(-10, -5), Vector(20, 10), 'smooth'),
        ControlPoint(Point(-30, -60), Vector(-30, 0), Vector(0, -30), 'sharp')
        # ControlPoint(Point(-80, 0), Vector(0, -20), Vector(0, 20), 'very-smooth'),
        # ControlPoint(Point(80, 0), Vector(0, 40), Vector(0, -40), 'smooth'),
    ], PenBrush('black'))
    j.closed = True
    # [j.add_one() for _ in range(15)]

    if not False:
        jj = j.offset(-1)
        sub.add(jj.name, jj)

        jj = j.offset(-2)
        sub.add(jj.name, jj)

    jj = j.offset(-10)
    sub.add(jj.name, jj)

    jj = j.offset(10)
    sub.add(jj.name, jj)

    # for elem in sub.elems.values():
    #     elem.restore(elem.transform(Transform().rotate(10)))
    # print(test.dump().output())
    return test


def gen_test_model_add_one() -> GroupBuilder:
    sub = GroupBuilder('test', PensByShape())
    sub.point('point', 50, -50)

    c = sub.curve('c', shape_kind=PenBrush('blue'), closed=True, cps=[
        ControlPoint(Point(-50, -50), Vector(30, -30), Vector(-30, 30)),
        ControlPoint(Point(-50, 0), Vector(0, -20), Vector(0, 20)),
        ControlPoint(Point(50, 50), Vector(-50, 50), Vector(50, -50)),
    ])
    print(sub.dump().output())
    for n in range(8):
        c.add_one()

    # for elem in sub.elems.values():
    #     elem.restore(elem.transform(Transform().rotate(10)))
    print(sub.dump().output())
    return sub


def gen_test_model() -> GroupBuilder:
    # return gen_test_model_offset()
    return gen_test_model_original()
    # return gen_test_model_add_one()


def test_model():       # pragma: nocover
    preview = sys.platform == 'ios'
    test = gen_test_model()
    img = Image.new('RGBA', (1000, 1000), 'white')
    draw = DrawingContext(img, Transform((5, 0, 500, 0, -5, 500)))
    # print(draw.matrix)
    draw.grid()
    test.draw(draw)
    if preview:
        draw.show()

    img = Image.new('RGBA', (1000, 1000), 'white')
    cast(Point, test.lookup_pt('point')).setxy(30, -30)
    draw = DrawingContext(img, Transform.canvas_fit(img.size, 5, (500, 500)))
    draw.grid()
    draw.show_cps = True
    test.draw(draw)
    if preview:
        draw.show()
    as_digi_points = False
    if as_digi_points:
        for n, e, t in test.iter_elems():
            print(n, e)
            for dp in e.as_digi_points():
                print('   %r' % dp)

    if sys.platform == 'darwin':
        try:
            import importlib
            x7edit = importlib.import_module('x7.view.edit')
            x7edit.digitize(draw, test)   # , {'e', 'j', 'k', 'l', 'm'})
        except ModuleNotFoundError:
            pass


def main():     # pragma: nocover
    # test_points()
    # noinspection PyUnresolvedReferences
    import x7.geom.model
    x7.geom.model.test_model()


if __name__ == '__main__':      # pragma: nocover
    main()
