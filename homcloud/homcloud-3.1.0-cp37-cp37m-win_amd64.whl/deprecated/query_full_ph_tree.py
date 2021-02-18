import argparse
import re
from itertools import chain
import json
import warnings

from homcloud.version import __version__
from homcloud.argparse_common import parse_bool
import homcloud.full_ph_tree as full_ph_tree


def argument_parser():
    p = argparse.ArgumentParser(description="query PH trees created by full_ph_tree")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-c", "--command", action="append", default=[], help="commands")
    p.add_argument("-C", "--color", default="1 0 0", help="color used by write-*")
    p.add_argument("-B", "--draw-birth-simplices", type=parse_bool, default=False,
                   help="draw birth simplices (True/False, default: False)")
    p.add_argument("-D", "--draw-death-simplices", type=parse_bool, default=False,
                   help="draw death simplices (True/False, default: False)")
    p.add_argument("input", help="input file path (.pht)")
    return p


class Main:
    def __init__(self, args):
        self.args = args
        self.resolver = None

    def run(self):
        with open(self.args.input, "rb") as f:
            self.resolver = full_ph_tree.TreeResolver.load(f)

        if self.args.command:
            for cmd in self.args.command:
                self.exec_command(cmd)
        else:
            print("OK")
            self.command_loop()

    def command_loop(self):
        while True:
            line = input()
            self.exec_command(line)

    def exec_command(self, line):
        command = re.split(r"\s+", line.strip())
        if command[0] in ["anc", "ancestors"]:
            self.query_ancestors(float(command[1]), float(command[2]))
        elif command[0] in ["q", "quit"]:
            exit(0)
        elif command[0] in ["des", "descendants"]:
            self.query_descendants(float(command[1]), float(command[2]))
        elif command[0] in ["wdes", "write-descendants"]:
            with open(command[3], "w") as f:
                self.write_descendant_markers(float(command[1]), float(command[2]), f)
        elif command[0] in ["ddv", "draw-descendants-volumes"]:
            self.draw_descendants_volumes(float(command[1]), float(command[2]), command[3])
        elif command[0] in ["dvr", "draw-volumes-in-rectangle"]:
            self.draw_volumes_in_rectangle(float(command[1]), float(command[2]),
                                           float(command[3]), float(command[4]),
                                           command[5])
        elif command[0] in ["wvpr", "write-volume-points-in-rectangle"]:
            self.write_volumes_points_in_rectangle(float(command[1]), float(command[2]),
                                                   float(command[3]), float(command[4]),
                                                   command[5])
        elif command[0] in ["wvsr", "write-volume-simplices-in-rectangle"]:
            self.write_volume_simplices_in_rectangle(float(command[1]), float(command[2]),
                                                     float(command[3]), float(command[4]),
                                                     command[5])
        elif command[0] in ["json", "dump-json"]:
            self.dump_json(command[1])
        elif command[0] in ["h", "help"]:
            self.show_help()
        else:
            print("Unknown command: {}".format(command[0]))

    @staticmethod
    def show_help():
        print("quit(q): Quit program")
        print("help(h): Show this help")
        print("ancestors(anc) BIRTH DEATH: List the ancestors of (BIRTH, DEATH)")
        print("descendants(des) BIRTH DEATH: List the subgraph of (BIRTH, DEATH)")
        print("write-descendants(wdes) BIRTH DEATH OUTPUT: Write descendants of (BIRTH, DEATH) " +
              "to OUTPUT in line-marker format")
        print("draw-descendants-volumes(ddv) BIRTH DEATH OUTPUT: Write descendants volumes of " +
              "(BIRTH, DEATH) to OUTPUT in vtk format")
        print("draw-volumes-in-rectangle(dvr) XMIN XMAX YMIN YMAX OUTPUT: " +
              "Write volumes in the given rectangle to OUTPUT in vtk format")
        print("write-volume-points-in-rectangle(wvpr) XMIN XMAX YMIN YMAX OUTPUT: " +
              "Write points in volumes in the given rectangle to OUTPUT in plain format")
        print("write-volume-simplices-in-rectangle(wvsr) XMIN XMAX YMIN YMAX OUTPUT: " +
              "Write simplices in volumes in the given triangle to OUTPUT in plain format")
        print("dump-json: OUTPUT: Write all information to OUTPUT in json format")

    def query_ancestors(self, birth, death):
        node = self.resolver.query_node(birth, death)
        while node:
            print(node.birth_death_pair())
            node = node.parent

    def query_descendants(self, birth, death):
        def visit_node(node):
            for child in node.children:
                if not child.living():
                    continue
                print("{} -> {}".format(node.birth_death_pair(), child.birth_death_pair()))
                visit_node(child)

        visit_node(self.resolver.query_node(birth, death))

    def write_descendant_markers(self, birth, death, f):
        def visit_node(node):
            for child in node.children:
                if not child.living():
                    continue
                f.write("point {} {} {}\n".format(
                    child.birth_time(), child.death_time(), self.args.color
                ))
                f.write("line {} {} {} {} 0 0 0\n".format(
                    node.birth_time(), node.death_time(),
                    child.birth_time(), child.death_time()
                ))
                visit_node(child)

        visit_node(self.resolver.query_node(birth, death))

    def draw_descendants_volumes(self, birth, death, path):
        root = self.resolver.query_node(birth, death)
        root.draw_descendants_volumes(self.resolver.index_map.points, path,
                                      self.args.draw_birth_simplices,
                                      self.args.draw_death_simplices)

    def draw_volumes_in_rectangle(self, xmin, xmax, ymin, ymax, path):
        nodes = self.resolver.query_nodes_in_rectangle(xmin, xmax, ymin, ymax)
        self.resolver.draw_volumes_of_nodes(nodes, path,
                                            self.args.draw_birth_simplices,
                                            self.args.draw_death_simplices)

    def write_volumes_points_in_rectangle(self, xmin, xmax, ymin, ymax, path):
        def point_to_string(point):
            return " ".join(str(coord) for coord in point)

        with open(path, "w") as f:
            for node in self.resolver.query_nodes_in_rectangle(xmin, xmax, ymin, ymax):
                for point in node.points_in_volume():
                    print(point_to_string(point), file=f)
                print(file=f)

    def write_volume_simplices_in_rectangle(self, xmin, xmax, ymin, ymax, path):
        def print_simplex(simplex, f):
            print(" ".join(str(p) for p in chain.from_iterable(simplex)), file=f)

        with open(path, "w") as f:
            for node in self.resolver.query_nodes_in_rectangle(xmin, xmax, ymin, ymax):
                for simplex in node.simplices_in_volume():
                    print_simplex(simplex, f)
                print(file=f)

    def dump_json(self, path):
        with open(path, "w") as f:
            json.dump(self.resolver.phtree.to_jsondict(), f)


def main(args=None):
    warnings.warn("homcloud.query_full_ph_tree is now obsolete")
    args = args or argument_parser().parse_args()
    Main(args).run()


if __name__ == "__main__":
    main()
