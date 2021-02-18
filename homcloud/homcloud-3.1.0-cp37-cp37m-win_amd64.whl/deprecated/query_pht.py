import argparse
import json
from tempfile import TemporaryDirectory
import os

from homcloud.version import __version__
import homcloud.utils as utils
import homcloud.full_ph_tree as full_ph_tree
from homcloud.argparse_common import parse_range, parse_bool


def argument_parser():
    p = argparse.ArgumentParser(description="Query phtree information")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-x", type=float, help="birth time of the pair")
    p.add_argument("-y", type=float, help="death time of the pair")
    p.add_argument("-X", "--x-range", type=parse_range, help="birth time of the pair")
    p.add_argument("-Y", "--y-range", type=parse_range, help="death time of the pair")
    p.add_argument("--ancestors", default=False, action="store_true",
                   help="store ancestors")
    p.add_argument("-j", "--json-output", help="output in json format")
    # p.add_argument("-v", "--vtk-output", help="output in vtk format")
    p.add_argument("-P", "--invoke-paraview", default=False, action="store_true",
                   help="invoke paraview for visualization")
    p.add_argument("--children", type=parse_bool, default=False,
                   help="show children (on/off) (default: off)")
    p.add_argument("input", help="input pht file")
    return p


def main(args=None):
    if not args:
        args = argument_parser().parse_args()

    check_args(args)

    with open(args.input, "rb") as f:
        resolver = full_ph_tree.TreeResolver.load(f)

    is_point_query = args.x is not None

    if is_point_query:
        query = PointQuery(args.x, args.y, resolver, args.ancestors, args.children)
    else:
        query = RectangleQuery(args.x_range, args.y_range, resolver,
                               args.ancestors, args.children)

    query.invoke()

    if args.json_output:
        with open(args.json_output, "w") as f:
            json.dump(query.to_jsondict(), f)

    if args.invoke_paraview:
        with TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "tmp.vtk")
            query.draw(path)
            utils.invoke_paraview(path, wait=True)


class Query(object):
    def __init__(self, resolver, ancestor_pairs, query_children):
        self.resolver = resolver
        self.nodes = []
        self.ancestor_pairs = ancestor_pairs
        self.query_children = query_children

    def to_jsondict(self):
        return {
            "format-version": Query.FORMAT_VERSION,
            "query": self.queryinfo_jsondict(),
            "dimension": self.dimension(),
            "num-volumes": len(self.nodes),
            "result": self.result_jsondicts(),
        }

    def dimension(self):
        return self.resolver.index_map.dimension

    def result_jsondicts(self):
        return [
            node.to_jsondict(descendant_pairs=True,
                             ancestor_pairs=self.ancestor_pairs,
                             children=self.query_children)
            for node in self.nodes
        ]

    FORMAT_VERSION = 1


class PointQuery(Query):
    def __init__(self, x, y, resolver, *opts):
        super().__init__(resolver, *opts)
        self.x = x
        self.y = y

    def invoke(self):
        self.nodes = [self.resolver.query_node(self.x, self.y)]

    def queryinfo_jsondict(self):
        return {
            "query-type": "single", "query-target": "phtree-volume-optimal-cycle",
            "degree": self.dimension() - 1, "birth": self.x, "death": self.y,
            "ancestor-pairs": self.ancestor_pairs, "query-children": self.query_children,
        }

    def draw(self, path):
        self.nodes[0].draw_descendants_volumes(self.resolver.index_map.points,
                                               path, False, False)


class RectangleQuery(Query):
    def __init__(self, x_range, y_range, resolver, *opts):
        super().__init__(resolver, *opts)
        self.x_range = x_range
        self.y_range = y_range

    def invoke(self):
        self.nodes = self.resolver.query_nodes_in_rectangle(
            self.x_range[0], self.x_range[1], self.y_range[0], self.y_range[1]
        )

    def queryinfo_jsondict(self):
        return {
            "query-type": "rectangle", "query-target": "phtree-volume-optimal-cycle",
            "degree": self.dimension() - 1,
            "birth-range": self.x_range, "death-range": self.y_range,
            "ancestor-pairs": self.ancestor_pairs, "query-children": self.query_children,
        }

    def draw(self, path):
        self.resolver.draw_volumes_of_nodes(self.nodes, path, True, True)


def check_args(args):
    bits = [args.x is None, args.y is None, args.x_range is None, args.y_range is None]
    if bits == [True, True, False, False] or bits == [False, False, True, True]:
        return
    raise(RuntimeError("You must specify (-x and -y) or (-X and -Y"))


if __name__ == "__main__":
    main()
