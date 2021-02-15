import itertools
import numpy as np
from x7.lib.iters import iter_rotate, xy_flatten
from .typing import *
from .geom import *
from .transform import *

try:
    import bezier as bz
    BzCurve = bz.Curve
except ModuleNotFoundError:
    bezier = None
    BzCurve = None


__all__ = [
    'ControlPoint',
    'bez_split', 'bez', 'bez_path', 'bez_intersect', 'bez_self_intersect',
]


class ControlPoint(object):
    """A Control Point for curves"""

    def __init__(self, c: BasePoint, dl: Vector, dr: Vector, kind='smooth'):
        self.c = c
        self.dl = dl
        self.dr = dr
        self.kind = kind

    def __str__(self):
        return repr((self.c, self.dl, self.dr, self.kind))

    def __repr__(self):
        return 'ControlPoint' + repr((self.c, self.dl, self.dr, self.kind))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.c == other.c and \
            self.dl == other.dl and self.dr == other.dr and self.kind == other.kind

    def close(self, other: 'ControlPoint', max_delta=1e-11):
        return (
            self.kind == other.kind and self.c.close(other.c, max_delta) and
            self.dl.close(other.dl, max_delta) and self.dr.close(other.dr, max_delta)
        )

    def reversed(self):
        """Return a reversed version of this ControlPoint"""
        return ControlPoint(self.c, self.dr, self.dl, self.kind)

    @staticmethod
    def reverse_list(cps: List['ControlPoint']):
        """Reverse the list and all cps in it"""
        return [cp.reversed() for cp in reversed(cps)]

    def fixed(self):
        return ControlPoint(self.c.fixed(), self.dl.fixed(), self.dr.fixed(), self.kind)

    def copy(self):
        return ControlPoint(self.c.copy(), self.dl.copy(), self.dr.copy(), self.kind)

    def bbox(self):
        bb = BBox(self.l, self.r)
        bb.grow(self.c)
        return bb

    def restore(self, copy):
        self.c = copy.c.copy()
        self.dl = copy.dl.copy()
        self.dr = copy.dr.copy()
        self.kind = copy.kind

    def transform(self, matrix: Transformer):
        t_c = matrix.transform_pt(self.c)
        t_l = matrix.transform_pt(self.l)
        t_r = matrix.transform_pt(self.r)
        cp = ControlPoint(t_c, t_l-t_c, t_r-t_c, self.kind)
        if not matrix.LINEAR:
            # Non-linear transform, fix dl/dr relationship
            if cp.kind == 'very-smooth':
                cp.dr = (cp.dr - cp.dl) / 2
                cp.dl = -cp.dr
            elif cp.kind == 'smooth':
                if cp.dl or cp.dr:
                    direction = (cp.dr - cp.dl).unit()
                    cp.dr = cp.dr.length() * direction
                    cp.dl = -cp.dl.length() * direction
        return cp

    def round(self, digits=0):
        return ControlPoint(self.c.round(digits), self.dl.round(digits), self.dr.round(digits), self.kind)

    @property
    def l(self) -> Point:
        return self.c + self.dl

    @property
    def r(self) -> Point:
        return self.c + self.dr


def bz_curve(cp1: ControlPoint, cp2: ControlPoint) -> BzCurve:
    nodes_a = np.array([tuple(p) for p in (cp1.c, cp1.r, cp2.l, cp2.c)]).T
    return bz.Curve(nodes_a, 3)


def bz_plot(curves: List, points: PointList):
    import matplotlib.pyplot as plt

    c_c: List[Tuple[BzCurve, str]] = [cc if isinstance(cc, tuple) else (cc, 'black') for cc in curves]

    fig, ax = plt.subplots(figsize=(8, 6))
    for curve, color in c_c:
        curve.plot(80, ax=ax, color=color)
    if points:
        x_vals, y_vals = zip(*BasePoint.parse(points))
        ax.plot(x_vals, y_vals, marker="o", linestyle="None", color="black")
    plt.show()


def bz_plot_curves(curves: List[List[ControlPoint]], color_by_segment=False):
    bz_curves = []
    pts = []
    colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'purple'] * 10
    for curve, color in zip(curves, colors):
        pts.extend(cp.c for cp in curve)
        if color_by_segment:
            bz_curves.extend([(bz_curve(a, b), color) for (a, b), color in zip(iter_rotate(curve), colors)])
        else:
            bz_curves.extend([(bz_curve(a, b), color) for a, b in iter_rotate(curve)])
        rounded = [cp.round(2) for cp in curve]
        formatted = ['{%s, %s, %s}' % (cp.c.xy(), cp.dl.xy(), cp.dr.xy()) for cp in rounded]
        print('   [%s],' % (', '.join(formatted)))
        # print(curve)
    # print(bz_curves)
    bz_plot(bz_curves, pts)


def bez_intersect(
        cpa1: ControlPoint, cpa2: ControlPoint,
        cpb1: ControlPoint, cpb2: ControlPoint,
        *, as_points=False, endpoints=False, do_plot=False) -> Union[List[Point], List[Tuple[float]]]:
    """
        Compute intersection(s) of curves A and B.

        :param cpa1: cp1 of curve A
        :param cpa2: cp2 of curve A
        :param cpb1: cp1 of curve B
        :param cpb2: cp2 of curve B
        :param as_points: Return List[Point] instead
        :param endpoints: Include endpoints in intersection set
        :param do_plot: (debugging) plot curves + points
        :return:Return 2 x N array of s- and t-parameters where intersections occur (possibly empty)
    """
    result = bez_intersect_new(cpa1, cpa2, cpb1, cpb2, endpoints=endpoints, do_plot=do_plot)
    if as_points:
        return [pt for pt, ta, tb in result]
    else:
        return list(zip(*[(ta, tb) for pt, ta, tb in result]))


def bez_intersect_new(
        cpa1: ControlPoint, cpa2: ControlPoint,
        cpb1: ControlPoint, cpb2: ControlPoint,
        *, endpoints=False, do_plot=False) -> List[Tuple[Point, float, float]]:
    """
        Compute intersection(s) of curves A and B.

        :param cpa1: cp1 of curve A
        :param cpa2: cp2 of curve A
        :param cpb1: cp1 of curve B
        :param cpb2: cp2 of curve B
        :param endpoints: Include endpoints in intersection set
        :param do_plot: (debugging) plot curves + points
        :return: List of (intersection-point, t-value for curve A, t-value for curve B)
    """
    curve_a = bz_curve(cpa1, cpa2)
    curve_b = bz_curve(cpb1, cpb2)
    try:
        intersections = curve_a.intersect(curve_b)
    except NotImplementedError as err:
        # bz.intersect will give up if there are too many "candidate" intersections
        print('WARNING: ', err)
        intersections = np.array([])
    if not endpoints and intersections.size:
        intersections = np.array(([(t, s) for t, s in intersections.T if (t, s) not in ((1, 0), (0, 1))])).T
    if intersections.size:
        points = curve_a.evaluate_multi(np.array(intersections[0]).T)
        points = [Point(x, y) for x, y in points.T]
    else:
        points = []
    if do_plot:
        bz_plot([curve_a, curve_b], points)

    return [(p, t, s) for p, (t, s) in zip(points, intersections.T.tolist())]


class BziNode(object):
    """A curve-curve intersection point with possibly many different edges"""

    def __init__(self, center: Tuple[float, float]):
        self._center = center
        self.edges = []

    def __str__(self):
        return 'Node@%s, %d edges' % (self.center.round(2), len(self.edges))

    @property
    def center(self):
        return Point(*self._center)

    def add_edge(self, edge: 'BziEdge'):
        assert edge.left is self or edge.right is self
        self.edges.append(edge)

    def any_edge(self, not_this_one: Optional['BziEdge'] = None) -> Optional['BziEdge']:
        """Return any edge, avoiding not_this_one and preferring left-pointing edges"""
        for edge in self.edges:
            if not edge.removed and edge.right == self and edge.right_right != not_this_one:
                return edge
        return None

    def add_cp(self, cp: ControlPoint):
        assert self._center == cp.c.xy()
        # self.edges.extend([cp.dl, cp.dr])


class BziEdge(object):
    """A sub-curve in a bezier intersection graph"""
    def __init__(self, left_left: Optional['BziEdge'], left: BziNode,
                 cps: List[ControlPoint], right: BziNode, right_right: Optional['BziEdge']):
        self.left_left: BziEdge = left_left
        self.left = left
        if len(cps) < 2:
            raise ValueError('Must have at least 2 points in cps, not %d' % len(cps))
        self.cps = cps[:]
        self.right = right
        self.right_right: BziEdge = right_right
        self.removed = False
        self.name = 'e?'
        self.left.add_edge(self)
        self.right.add_edge(self)

    def __str__(self):
        return '%s->%s' % (self.left.center.round(2).xy(), self.right.center.round(2).xy())

    def __repr__(self):
        return 'Edge %s %s: ll=%s l=%s cps=%d r=%s rr=%s' % (
            self.name, '-' if self.removed else '+',
            self.left_left.name, self.left.center.round(2).xy(),
            len(self.cps),
            self.right.center.round(2).xy(), self.right_right.name
        )

    def remove(self):
        self.removed = True

    def unremove(self):
        self.removed = False


class BziGraph(object):
    """Collection of intersections"""

    def __init__(self):
        self.nodes: Dict[tuple, BziNode] = {}       # Key: center point of intersection
        self.edges: List[BziEdge] = []

    def node(self, xy: Tuple[float, float], create=False):
        if create and xy not in self.nodes:
            self.nodes[xy] = BziNode(xy)
        return self.nodes[xy]

    def any_node(self) -> Optional[BziNode]:
        """Return the first non-empty node or None"""
        for node in self.nodes.values():
            if node.any_edge():
                return node
        return None

    def add_edge(self, left_left: Optional[BziEdge], left: BziNode,
                 cps: List[ControlPoint], right: BziNode, right_right: Optional[BziEdge]):
        """Create a new edge, add it to the graph and update relevant nodes & edges"""
        edge = BziEdge(left_left, left, cps, right, right_right)
        edge.name = 'e%d' % len(self.edges)
        self.edges.append(edge)
        if left_left and left_left.right_right is None:
            left_left.right_right = edge
        if right_right and right_right.left_left is None:
            right_right.left_left = edge
        return edge

    def validate(self):
        valid = True
        for node in self.nodes.values():
            count = len(node.edges)
            if count % 2 or count < 4:
                print('Invalid: node@%s: edge count=%d' % (node.center, count))
                valid = False
            for edge in node.edges:
                if edge not in node.edges:
                    print('Invalid: node@%s: edge missing from graph.edges' % node.center)
                    valid = False
        for edge in self.edges:
            if not edge.left_left:
                print('Invalid: edge: missing left_left')
                valid = False
            if not edge.right_right:
                print('Invalid: edge: missing right_right')
                valid = False
        if valid:
            print('BziGraph: apparently valid')
        return valid

    def print(self):
        print('Graph: %d nodes, %d edges' % (len(self.nodes), len(self.edges)))
        for loc, node in self.nodes.items():
            print('   Node@%s: %s' % (loc, node))
        for edge in self.edges:
            print('  ', repr(edge))


class CpBool(object):
    def __init__(self, cp: ControlPoint, node: Optional[BziNode]):
        self.cp = cp
        self.node = node

    def __str__(self):
        return '%s:%s' % (self.cp.round(2), self.node)

    def __repr__(self):
        return str(self)

    @staticmethod
    def array_print(cpbs: List['CpBool']):
        if cpbs:
            print('\n'.join(['  cpbs: ['] + ['    %s,' % cpb for cpb in cpbs] + [']']))


def bez_self_intersect(orig_cps: List[ControlPoint], debug=False) -> List[List[ControlPoint]]:
    """Return list of replacement curves or [] if no self intersections"""

    # all_curves: list of all curve segments and their intersection t-values/xy-values
    all_curves: List[Tuple[ControlPoint, ControlPoint, List[Tuple[float, Tuple[float, float]]]]] = []
    for cpa, cpb in iter_rotate(orig_cps):
        left, middle, right = bez_split(cpa, cpb)
        intersection = bez_intersect_new(left, middle, middle, right)
        if intersection:
            # This segment self-intersects, so split it before adding to all_curves
            all_curves.extend([(left, middle, []), (middle, right, [])])
        else:
            all_curves.append((cpa, cpb, []))
    # bz_plot_curves([[a, b] for a, b, c in all_curves])

    found_ixs = False       # found any intersections?
    for a, b in itertools.combinations(all_curves, 2):
        ixs = bez_intersect_new(a[0], a[1], b[0], b[1], endpoints=False)
        if ixs:
            for pt, ta, tb in ixs:
                a[2].append((ta, pt.xy()))
                b[2].append((tb, pt.xy()))
            found_ixs = True
    if not found_ixs:
        if debug:
            print('self_intersect: none')
            bz_plot_curves([orig_cps], color_by_segment=True)
        return []       # No intersections found, return sentinel

    # Expand the intersections into full control points, creating graph nodes along the way
    graph = BziGraph()
    cpbs: List[CpBool] = []
    for a, b, intersections in all_curves:
        if debug:
            print('ac: ', a.round(2), b.round(2), intersections)
            CpBool.array_print(cpbs)
        t = 0.0
        local_cpbs = []
        next_node = None
        for t_ix, xy_ix in sorted(intersections):
            node_ix = graph.node(xy_ix, create=True)
            l, m, r = bez_split(a, b, (t_ix-t)/(1-t))
            if (m.c-node_ix.center).length() > 1e-10:
                raise ValueError('m.c!=ix.c by %s: %s != %s' % ((m.c-node_ix.center).length(), m.c, node_ix.center))
            local_cpbs.append(CpBool(l, next_node))
            next_node = node_ix
            a = m
            b = r
            t = t_ix
        local_cpbs.append(CpBool(a, next_node))
        local_cpbs.append(CpBool(b, None))
        if cpbs:
            if debug:
                print('cpbs_extend:', cpbs[-1].cp.c, local_cpbs[0].cp.c)
            assert cpbs[-1].cp.c == local_cpbs[0].cp.c
            cpbs[-1].cp.dr = local_cpbs[0].cp.dr
            cpbs.extend(local_cpbs[1:])
        else:
            cpbs.extend(local_cpbs)
    # Last ControlPoint is same as first, but has correct .dl, so copy .dl and remove last
    cpbs[0].cp.dl = cpbs[-1].cp.dl
    cpbs.pop()
    # Now, cps is a list of (ControlPoint, intersection-node)
    if debug:
        CpBool.array_print(cpbs)

    # Rotate so that an intersection is first in the list of control points
    first_ix = [ix for ix, cpb in enumerate(cpbs) if cpb.node][0]
    cpbs = cpbs[first_ix:] + cpbs[:first_ix]
    if debug:
        CpBool.array_print(cpbs)

    # Now, iterate over ControlPoints to create edges and attach them to nodes
    current_segment: List[ControlPoint] = []
    prev_node: Optional[BziNode] = None
    prev_edge: Optional[BziEdge] = None
    first_edge: Optional[BziEdge] = None
    for cpb in cpbs + cpbs[:1]:       # Loop around to first to close last edge
        if cpb.node is None:
            # No intersection, just extend current edge
            current_segment.append(cpb.cp)
        else:
            if current_segment:
                current_segment.append(cpb.cp)
                prev_edge = graph.add_edge(prev_edge, prev_node, current_segment, cpb.node, None)
                if first_edge is None:
                    first_edge = prev_edge
            current_segment = [cpb.cp]
            prev_node = cpb.node
    # Stitch up the last & first edges
    assert prev_edge.right_right is None
    assert first_edge.left_left is None
    prev_edge.right_right = first_edge
    first_edge.left_left = prev_edge
    if debug:
        graph.print()
    graph.validate()

    # Now, graph contains nodes & all edges, so time to walk the graph.
    # We can start at any node.  Each time we get to a node, we can leave by any edge that
    # is not pointed to by the current edge's "through" pointers (left_left and right_right),
    # cleaning up as we move along.

    curves = []
    while first_node := graph.any_node():
        edges: List[BziEdge] = []
        edge = first_node.any_edge()
        if debug:
            print('walk: start=%s / %s' % (first_node, edge))
        if edge.right == first_node:
            # we are iterating to the left
            while True:         # do-while loop
                edges.append(edge)
                match = [idx for idx, e in enumerate(edges) if edge.left == e.right]
                if debug:
                    print(' next edge: ', edge)
                    if match:
                        print('-> match:', match)
                    # print('edges:', edges, ' match:', match)
                edge.remove()
                if match:
                    for keep in edges[:match[0]]:
                        keep.unremove()
                    edges = edges[match[0]:]
                    cps: List[ControlPoint] = edges[0].cps[:]
                    if debug:
                        print('   ', ', '.join(str(cp.c.round(2)) for cp in cps))
                    for edge in edges[1:]:
                        eps = 1e-11
                        if cps[-1].c.close(edge.cps[0].c, max_delta=eps):
                            ecps = edge.cps[:]
                            if debug:
                                print(' -1 == 0')
                            cps[-1] = cps[-1].copy()
                            cps[-1].dr = ecps[0].dr
                            cps[-1].kind = 'sharp'
                            # cps.extend(edge.cps[1:])
                            cps = cps + ecps[1:]
                        elif cps[0].c.close(edge.cps[0].c, max_delta=eps):
                            raise ValueError('bez_self_intersect: 0==0')
                        elif cps[0].c.close(edge.cps[-1].c, max_delta=eps):
                            ecps = edge.cps[:]
                            if debug:
                                print(' 0 == -1')
                            ecps[-1] = ecps[-1].copy()
                            ecps[-1].dr = cps[0].dr
                            ecps[-1].kind = 'sharp'
                            # cps.extend(edge.cps[1:])
                            cps = ecps + cps[1:]
                        elif cps[-1].c.close(edge.cps[-1].c, max_delta=eps):
                            raise ValueError('bez_self_intersect: -1==-1')
                        else:
                            msg = 'expected one of {%s, %s} to match one of {%s, %s} within %s' % (
                                cps[0].c.round(5), cps[-1].c.round(5),
                                edge.cps[0].c.round(5), edge.cps[-1].c.round(5),
                                eps
                            )
                            raise ValueError('bez_self_intersect: nothing close enough\n' + msg)

                        if debug:
                            print('   ', ', '.join(str(cp.c.round(2)) for cp in cps))
                    cps[0] = cps[0].copy()
                    cps[0].dl = cps[-1].dl
                    cps[0].kind = 'sharp'
                    cps = cps[:-1]
                    curves.append(cps)
                    break

                # TODO-any_edge is not quite the right approach, but good enough for now
                next_edge = edge.left.any_edge(not_this_one=edge)
                edge = next_edge
        else:
            raise NotImplementedError("can't handle right iteration yet")

    if debug:
        print('self_intersect:')
        bz_plot_curves(curves)
    return curves


# noinspection DuplicatedCode
def test_self_intersect():
    curve = [
        ControlPoint(Point(0, 0), Vector(0, 1), Vector(0, -1)),
        ControlPoint(Point(2, 0), Vector(0, -1), Vector(0, 1)),
    ]
    bez_self_intersect(curve)

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
        ]
    ]
    if bez_self_intersect(curve) != expected:
        print('Mismatch')
        bez_self_intersect(curve, debug=True)

    test_other_stuff = not False
    if test_other_stuff:
        curve = [
            ControlPoint(Point(0, 0), Vector(0, 1), Vector(0, -1)),
            ControlPoint(Point(1, 1), Vector(-0.5, 0), Vector(0.5, 0)),
            ControlPoint(Point(2, 0), Vector(0, -1), Vector(0, 1)),
        ]
        bez_self_intersect(curve, debug=True)

        curve = [
            ControlPoint(Point(0, 0), Vector(0, 1), Vector(0, -1)),
            ControlPoint(Point(0.5, 1), Vector(-.1, 0), Vector(0.1, 0)),
            ControlPoint(Point(1, -1), Vector(-0.2, 0), Vector(0.2, 0)),
            ControlPoint(Point(1.5, 1), Vector(-.1, 0), Vector(0.1, 0)),
            ControlPoint(Point(2, 0), Vector(0, -1), Vector(0, 1)),
        ]
        bez_self_intersect(curve, debug=True)

        curve = [
            ControlPoint(Point(-1, -1), Vector(-1, 1), Vector(1, -1)),
            ControlPoint(Point(-1, 1), Vector(1, 1), Vector(-1, -1)),
            ControlPoint(Point(1, 1), Vector(1, -1), Vector(-1, 1)),
            ControlPoint(Point(1, -1), Vector(-1, -1), Vector(1, 1)),
        ]
        bez_self_intersect(curve, debug=True)

        for radius in [-1, 0.5]:        # Note: radius==0 causes divide by zero
            up = Vector(0, 4)
            left = Vector(4, 0)
            curve = [
                ControlPoint(Point(radius, 0), up, -up),
                ControlPoint(Point(0, radius), -left, left),
                ControlPoint(Point(-radius, 0), -up, up),
                ControlPoint(Point(0, -radius), left, -left),
            ]
            print(' - '*30)
            print('self_intersect: clover: r=%s pts=%d' % (radius, len(curve)))
            bz_plot_curves([curve], color_by_segment=True)
            bez_self_intersect(curve, debug=True)

    print(' - ' * 30)
    print('self_intersect: gui example')
    curve = [
        ControlPoint(Point(206.6, -0.8), Vector(0.0, -50.0), Vector(0.0, 50.0), 'smooth'),
        ControlPoint(Point(196.6, 9.2), Vector(50.0, 0.0), Vector(-50.0, 0.0), 'smooth'),
        ControlPoint(Point(186.6, -0.8), Vector(0.0, 50.0), Vector(0.0, -50.0), 'smooth'),
        ControlPoint(Point(196.6, -10.8), Vector(-50.0, 0.0), Vector(50.0, 0.0), 'smooth'),
    ]
    bez_self_intersect(curve, debug=True)


def test_intersect():
    a = ControlPoint(Point(0, 0), Vector(), Vector(2, 2))
    b = ControlPoint(Point(4, 0), Vector(-2, 2), Vector())
    c = ControlPoint(Point(0, 2), Vector(), Vector(2, -2))
    d = ControlPoint(Point(4, 2), Vector(-2, -2), Vector())
    bez_intersect(a, b, c, d, do_plot=True)

    a = ControlPoint(Point(0, 0), Vector(), Vector(8, 8))
    b = ControlPoint(Point(4, 0), Vector(-8, 8), Vector())
    l, m, r = bez_split(a, b)
    p = bez_intersect(l, m, m, r, as_points=True, endpoints=True, do_plot=True)
    print(p)

    a = ControlPoint(Point(0, 0), Vector(), Vector(18, 0))
    b = ControlPoint(Point(4, 0), Vector(-18, 0), Vector())
    l, m, r = bez_split(a, b)
    p = bez_intersect(l, m, m, r, as_points=True, do_plot=True)
    print(p)

    test_null_curves = False
    if test_null_curves:
        a = ControlPoint(Point(0, 0), Vector(), Vector())
        b = ControlPoint(Point(0, 0), Vector(), Vector())
        l, m, r = bez_split(a, b)
        p = bez_intersect(l, m, m, r, as_points=True, do_plot=True)
        print(p)


def bez_split(cp1: ControlPoint, cp2: ControlPoint, t=0.5)\
        -> Tuple[ControlPoint, ControlPoint, ControlPoint]:
    """Split bezier curve in half.  Returns three new control points"""
    def mid(p: BasePoint, q: BasePoint):
        return p + t*(q-p)

    a, b, c, d = cp1.c, cp1.r, cp2.l, cp2.c
    ab = mid(a, b)
    bc = mid(b, c)
    cd = mid(c, d)
    abc = mid(ab, bc)
    bcd = mid(bc, cd)
    abcd = mid(abc, bcd)

    left = ControlPoint(a, cp1.dl, ab-a)
    middle = ControlPoint(abcd, abc-abcd, bcd-abcd)
    right = ControlPoint(d, cd-d, cp2.dr)

    return left, middle, right


def bez(raw_pts: PointList, steps=80, as_xy=False):
    """Generate (x, y) points from bezier control points"""
    (ax, ay), (bx, by), (cx, cy), (dx, dy) = (p.xy() if isinstance(p, BasePoint) else p for p in raw_pts)

    path = [(ax, ay)]
    # steps = 10
    # f(t) = (1-t)^3*p1 + 3*t*(1-t)^2 + 3*t^2*(1-t)*p3 + t^3*p4x
    for ti in range(1, steps):
        t = ti / steps
        t2 = t * t
        t3 = t * t2
        s = 1 - t
        s2 = s * s
        s3 = s * s2
        s2t = s2 * t
        st2 = s * t2
        x = s3 * ax + 3 * s2t * bx + 3 * st2 * cx + t3 * dx
        y = s3 * ay + 3 * s2t * by + 3 * st2 * cy + t3 * dy
        path.append((x, y))
    path.append((dx, dy))
    if not as_xy:
        # Flatten the path
        path = list(xy_flatten(path))
    # print(path)
    return path


def bez_path(transform: Transform, cps: List[ControlPoint], closed: bool, steps=20):
    """Return List[(x,y)...] for bezier transformed via draw.matrix"""
    if not cps:
        return []
    pts = []
    if closed:
        extra = cps
    else:
        extra = []
    for p, q in zip(cps, cps[1:] + extra):
        curve_pts = transform.transform_pts([p.c, p.r, q.l, q.c])
        bez_pts = bez(curve_pts, steps=steps, as_xy=False)
        if pts:
            pts.extend(bez_pts[2:])  # Skip first point, as it is already there
        else:
            pts.extend(bez_pts)
    return pts


if __name__ == '__main__':
    test_self_intersect()
    # test_intersect()
