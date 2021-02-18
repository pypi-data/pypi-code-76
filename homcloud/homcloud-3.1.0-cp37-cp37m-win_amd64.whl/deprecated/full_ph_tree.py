import argparse
import itertools
import sys
import json
from collections import defaultdict
from operator import attrgetter

import msgpack
import numpy as np

from forwardable import forwardable

from homcloud.version import __version__
from homcloud.diagram import PD
import homcloud.utils as utils
from homcloud.index_map import IndexMap
from homcloud.visualize_3d import boundary_of_connected_simplices, ParaViewSimplexDrawer
from homcloud.compat import INFINITY
from homcloud.spatial_searcher import SpatialSearcher


if msgpack.version < (1, 0, 0):
    STRICT_MAP_KEY_OPTION = {}
else:
    STRICT_MAP_KEY_OPTION = {"strict_map_key": False}


def main(args=None):
    args = args or argument_parser().parse_args()
    diagram = PD.load_from_indexed_diphafile(args.input, args.degree)

    check_degree(args.degree, diagram)

    phtree = PHTrees(diagram, args.degree)
    phtree.construct_tree()

    with open(args.output, "wb") as f:
        write_phtree(f, phtree, diagram)

    if args.dump_json is not None:
        phtree_q = PHTreesForQuery.from_dict(phtree.to_dict(), diagram.index_map)
        with open(args.dump_json, "w") as f:
            json.dump(phtree_q.to_jsondict(), f)


def check_degree(degree, diagram):
    if not degree == diagram.index_map.dimension - 1:
        sys.stderr.write("degree should equal dimension - 1\n")
        exit(1)


def write_phtree(output, phtree, diagram):
    msgpack.pack({
        "trees": phtree.to_dict(),
        "index-map": diagram.index_map.to_dict(),
    }, output, use_bin_type=True)


def argument_parser():
    p = argparse.ArgumentParser(description="compute a full PH tree")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-d", "--degree", type=int, required=True, help="degree of PH")
    p.add_argument("-j", "--dump-json", help="json dump output")
    p.add_argument("input", help="input file")
    p.add_argument("output", help="output file")
    return p


class PHTrees(object):
    def __init__(self, diagram, degree):
        self.diagram = diagram
        self.simplices = map(frozenset, diagram.index_map.simplices)
        self.degree = degree
        self.nodes = []
        self.adjacent_nodes = defaultdict(list)
        self.outer_node = PHTrees.OuterNode()

    def construct_tree(self):
        for (time, simplex) in reversed(list(enumerate(self.simplices))):
            dim_simplex = len(simplex) - 1
            if dim_simplex == self.degree + 1:
                node = PHTrees.Node(simplex, time)
                self.nodes.append(node)
                for boundary_simplex in node.boundary():
                    self.adjacent_nodes[boundary_simplex].append(node)
            elif dim_simplex == self.degree:
                n1, n2 = self.get_adjacent_nodes(simplex)
                r1 = n1.root()
                r2 = n2.root()
                if r1 is r2:
                    continue
                elif r1.death_time > r2.death_time:
                    self.merge(r1, r2, time)
                else:
                    self.merge(r2, r1, time)

    def get_adjacent_nodes(self, simplex):
        nodes = self.adjacent_nodes[simplex]
        if len(nodes) == 2:
            return nodes
        elif len(nodes) == 1:
            return [nodes[0], self.outer_node]
        else:
            raise RuntimeError("Algorithm Error or Simplex Data error")

    @staticmethod
    def merge(parent, child, time):
        child.parent = child.shortcut = parent
        child.birth_time = time

    def to_dict(self):
        return {node.index(): node.to_dict() for node in self.nodes}

    class Node(object):
        def __init__(self, simplex, death_time):
            self.simplex = simplex
            self.death_time = death_time
            self.birth_time = None
            self.parent = self.shortcut = None

        def boundary(self):
            return [self.simplex.difference([el]) for el in self.simplex]

        def root(self):
            if self.parent is None:
                return self
            result = self.shortcut.root()
            self.shortcut = result
            return result

        @staticmethod
        def outer():
            return False

        def index(self):
            return self.death_time

        def to_dict(self):
            return {
                "index": self.index(), "birth-index": self.birth_time,
                "parent": self.parent.index(),
            }

    class OuterNode(object):
        def __init__(self):
            self.death_time = INFINITY

        def root(self):
            return self

        @staticmethod
        def outer():
            return True

        @staticmethod
        def index():
            return None


@forwardable()
class PHTreesForQuery(object):
    def __init__(self, nodes, index_map):
        self.nodes = nodes
        self.index_map = index_map
        for node in nodes.values():
            if node.parent_index is not None:
                node.parent = self.nodes[node.parent_index]
                node.parent.children.append(node)

    class Volume(object):
        def resolve_simplex(self, simplex):
            return utils.deep_tolist(
                self.geom_resolver.vertex_indices_to_coords(simplex)
            )

        def volume_indices(self):
            return map(attrgetter("index"), self.volume())

        def boundary_simplices(self):
            return boundary_of_connected_simplices(self.volume_simplices())

        def boundary_points_indices(self):
            return set(itertools.chain.from_iterable(self.boundary_simplices()))

        def points_symbols(self):
            return self.geom_resolver.unique_vertices_symbols(self.volume_indices())

        def volume_simplices_symbols(self):
            return self.geom_resolver.cells_symbols(self.volume_indices())

        def volume_simplices(self):
            return [frozenset(self.index_map.simplices[node.index])
                    for node in self.volume()]

        def boundary_symbols(self):
            return [self.geom_resolver.vertices_to_symbols(s)
                    for s in self.boundary_simplices()]

        def boundary_points_symbols(self):
            return self.geom_resolver.vertices_to_symbols(self.boundary_points_indices())

        def points_in_volume(self):
            return utils.deep_tolist(
                self.geom_resolver.unique_vertices_coords(self.volume_indices())
            )

        points = points_in_volume

        def simplices_in_volume(self):
            return utils.deep_tolist(
                self.geom_resolver.cells_coords(self.volume_indices())
            )

        simplices = simplices_in_volume

        def boundary(self):
            return [self.resolve_simplex(s) for s in self.boundary_simplices()]

        def boundary_points(self):
            return self.resolve_simplex(self.boundary_points_indices())

        def draw_volume(self, drawer, color, values, draw_birth=False, draw_death=False):
            for b in self.boundary_simplices():
                drawer.draw_simplex(b, color, **values)
            if draw_birth:
                drawer.draw_simplex(self.birth_simplex(), drawer.birth_color(), **values)
            if draw_death:
                drawer.draw_simplex(self.death_simplex(), drawer.death_color(), **values)

    class Node(Volume):
        def __init__(self, index, birth_index, parent_index, index_map):
            self.index = index
            self.birth_index = birth_index
            self.parent_index = parent_index
            self.index_map = index_map
            self.parent = None
            self.children = []
            self.volume_cache = None
            self.geom_resolver = index_map.geometry_resolver(None)

        @classmethod
        def from_dict(cls, dic, index_map):
            return cls(dic["index"], dic["birth-index"], dic["parent"],
                       index_map)

        def birth_time(self):
            return self.index_map.levels[self.birth_index]

        def death_time(self):
            return self.index_map.levels[self.index]

        def birth_simplex(self):
            return self.index_map.simplices[self.birth_index]

        def death_simplex(self):
            return self.index_map.simplices[self.index]

        def volume(self):
            """Returns all descendants list.

            The list always contains self.
            """
            if self.volume_cache is None:
                self.volume_cache = [self] + list(itertools.chain.from_iterable([
                    child.volume() for child in self.children
                ]))
            return self.volume_cache

        def birth_death_pair(self):
            return (self.birth_time(), self.death_time())

        def living(self):
            return self.birth_time() < self.death_time()

        def count_living_descendants(self):
            return len(self.living_descendants())

        def living_descendants(self):
            """Return list of all descendant nodes who is living.

            The list always contains self if self is living.
            """
            return [node for node in self.volume() if node.living()]

        def depth_to(self, root):
            if self == root:
                return 0
            else:
                return 1 + self.parent.depth_to(root)

        def draw_descendants_volumes(self, points, path, draw_birth, draw_death):
            living_descendants = self.living_descendants()
            drawer = ParaViewSimplexDrawer(
                len(living_descendants), points,
                {"depth": None, "birth": None, "death": None}
            )

            for (node, color) in zip(living_descendants, drawer.various_colors):
                node.draw_volume(drawer, color, {
                    "depth": node.depth_to(self),
                    "birth": node.birth_time(),
                    "death": node.death_time()
                }, draw_birth, draw_death)

            drawer.output(path)

        def birth_position(self):
            return self.resolve_simplex(self.birth_simplex())

        birth_pos = birth_position

        def death_position(self):
            return self.resolve_simplex(self.death_simplex())

        death_pos = death_position

        def descendant_pairs_dicts(self):
            return [
                node.birth_death_time_dict() for node in self.living_descendants()
            ]

        def ancestor_pairs_dicts(self):
            return [node.birth_death_time_dict() for node in self.ancestors()]

        def ancestors(self):
            ret = []
            node = self
            while node is not None:
                ret.append(node)
                node = node.parent
            return ret

        def birth_death_time_dict(self):
            return {"birth-time": self.birth_time(), "death-time": self.death_time()}

        def children_dicts(self):
            return [child.to_jsondict(True, True, True)
                    for child in self.children if child.living()]

        def lifetime(self):
            return self.death_time() - self.birth_time()

        def to_jsondict(self, descendant_pairs=False, ancestor_pairs=False, children=False):
            return {
                "id": str(self.index),
                "parent": None if self.parent_index is None else str(self.parent_index),
                "birth-time": self.birth_time(), "death-time": self.death_time(),
                "points": self.points_in_volume(), "simplices": self.simplices_in_volume(),
                "boundary": self.boundary(), "boundary-points": self.boundary_points(),
                "points-symbols": self.points_symbols(),
                "simplices-symbols": self.volume_simplices_symbols(),
                "boundary-symbols": self.boundary_symbols(),
                "boundary-points-symbols": self.boundary_points_symbols(),
                "birth-simplex": self.birth_position(),
                "death-simplex": self.death_position(),
                "ancestors": self.ancestor_pairs_dicts() if ancestor_pairs else None,
                "descendants": self.descendant_pairs_dicts() if descendant_pairs else None,
                "children": self.children_dicts() if children else None,
            }

        def __repr__(self):
            """TODO: support inheritance
            """
            return "PHTreesForQuery.Node(birth={}, death={})".format(
                self.birth_time(), self.death_time()
            )

        def stable_volume(self, epsilon, cls):
            return cls(self, [
                child for child in self.children
                if child.birth_time() > self.birth_time() + epsilon
            ])

    @staticmethod
    def from_dict(dic, index_map, nodeclass=Node):
        nodes = {index: nodeclass.from_dict(nodedict, index_map)
                 for (index, nodedict) in dic.items()}
        return PHTreesForQuery(nodes, index_map)

    @classmethod
    def load_from_file(cls, f, nodeclass=Node):
        data = msgpack.unpack(f, raw=False, **STRICT_MAP_KEY_OPTION)

        index_map = IndexMap.load_from_dict(data["index-map"])
        phtree_q = cls.from_dict(data["trees"], index_map, nodeclass)
        return (phtree_q, index_map)

    def index_pairs(self):
        return [(node.birth_index, node.index) for node in self.nodes.values()]

    def birth_death_indices(self):
        births, deaths = zip(*self.index_pairs())
        return np.array(births, dtype=int), np.array(deaths, dtype=int)

    def to_jsondict(self):
        living_nodes = [node for node in self.nodes.values() if node.living()]
        return {
            "dim": self.index_map.dimension,
            "num-nodes": len(living_nodes),
            "nodes": {str(node.index): node.to_jsondict() for node in living_nodes}
        }

    class StableVolume(Volume):
        def __init__(self, root, subroots):
            self.root = root
            self.subroots = subroots
            self._volume = [root]
            for subroot in subroots:
                self._volume.extend(subroot.volume())
            self.index_map = root.index_map
            self.geom_resolver = root.geom_resolver

        def volume(self):
            return self._volume

        def_delegators("root", "lifetime,birth_time,death_time,birth_simplex,death_simplex,birth_position,death_position")


class TreeResolver(object):
    def __init__(self, phtree, spatial_searcher, index_map):
        self.phtree = phtree
        self.spatial_searcher = spatial_searcher
        self.index_map = index_map

    @staticmethod
    def load(f, nodeclass=PHTreesForQuery.Node):
        (phtree_q, index_map) = PHTreesForQuery.load_from_file(f, nodeclass)
        nodes = list(phtree_q.nodes.values())
        spatial_searcher = SpatialSearcher(
            nodes,
            np.array([n.birth_time() for n in nodes]),
            np.array([n.death_time() for n in nodes])
        )
        return TreeResolver(phtree_q, spatial_searcher, index_map)

    def query_node(self, birth, death):
        return self.spatial_searcher.nearest_pair(birth, death)

    def query_nodes_in_rectangle(self, xmin, xmax, ymin, ymax):
        return self.spatial_searcher.in_rectangle(xmin, xmax, ymin, ymax)

    def draw_volumes_of_nodes(self, nodes, path, draw_birth, draw_death):
        drawer = ParaViewSimplexDrawer(len(nodes), self.index_map.points, {})
        for node, color in zip(nodes, drawer.various_colors):
            node.draw_volume(drawer, color, dict(), draw_birth, draw_death)
        drawer.output(path)


if __name__ == "__main__":
    main()
