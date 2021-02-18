import itertools
from tempfile import TemporaryDirectory
import os
import math
from collections import defaultdict

import numpy as np
from forwardable import forwardable

import homcloud.utils as utils


class ParaViewColors(object):
    def __init__(self, n_colors):
        self.n_colors = n_colors
        self.color_scalars = np.linspace(0, 1.0, n_colors + 3)

    @property
    def various_colors(self):
        return self.color_scalars[:-3]

    def birth_color(self):
        return self.color_scalars[-2]

    def death_color(self):
        return self.color_scalars[-1]

    def output_lookup_table(self, f):
        f.write("LOOKUP_TABLE color_table {}\n".format(self.n_colors + 3))
        for x in np.linspace(0.0, 1.0, self.n_colors + 1):
            self.output_various_colors(f, x)
        self.output_birthdeath_colors(f)

    def output_various_colors(self, f, relative_value):
        f.write("{} {} {} 1.0\n".format(*self.color_spec(relative_value)))

    @staticmethod
    def color_spec(x):
        y, k = math.modf(x * 6)
        if k == 0 or k == 6:
            return (1, y, 0)
        if k == 1:
            return (1 - y, 1, 0)
        if k == 2:
            return (0, 1, y)
        if k == 3:
            return (0, 1 - y, 1)
        if k == 4:
            return (y, 0, 1)
        if k == 5:
            return (1, 0, 1 - y)
        return (0.5, 0.5, 0.5)

    @staticmethod
    def output_birthdeath_colors(f):
        f.write("0.8 0.8 0.8 1.0\n")
        f.write("1.0 1.0 1.0 1.0\n")


# TODO: this class requires unit tests
@forwardable()
class ParaViewDrawer(object):
    """
    This class represents the generator of a VTK file.

    Args:
        n_colors (int): The number of colors
        column_spec (dict[str, float or None]): The pairs of the names of
            the columns and default values.
    """
    def __init__(self, n_colors, column_spec):
        self.pvcolors = ParaViewColors(n_colors)
        self.lines = []
        self.colors = []
        self.columns = {name: list() for name in column_spec}
        self.default_values = {
            name: default_val for (name, default_val)
            in column_spec.items() if default_val is not None
        }
        self.vertices = []

    def_delegators("pvcolors", "various_colors,birth_color,death_color")

    def draw_line(self, p, q, color, **threshold_values):
        self.lines.append((p, q))
        self.append_attributes(color, threshold_values)

    def append_attributes(self, color, threshold_values):
        self.colors.append(color)
        for key in self.columns:
            self.columns[key].append(
                self.get_threshold_value(threshold_values, key)
            )

    def get_threshold_value(self, values, key):
        if key in values:
            return values[key]
        else:
            return self.default_values[key]

    def invoke(self, wait=True):
        with TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "tmp.vtk")
            self.output(path)
            utils.invoke_paraview(path, wait=wait)

    def output(self, path):
        with open(path, "w") as f:
            self.write(f)

    def write(self, f):
        self.output_header(f)
        self.output_polygon_data(f)
        self.output_line_colors(f)
        self.pvcolors.output_lookup_table(f)
        self.output_columns(f)

    @staticmethod
    def output_header(f):
        f.write("# vtk DataFile Version 2.0\n")
        f.write("volume optimal cycles\n")
        f.write("ASCII\n")

    def output_polygon_data(self, f):
        f.write("DATASET POLYDATA\n")
        self.output_points(f)
        self.output_vertices(f)
        self.output_lines(f)

    def output_vertices(self, f):
        if not self.vertices:
            return
        f.write("VERTICES {} {}\n".format(
            self.num_vertices(), self.num_vertices() * 2
        ))
        for v in self.vertices:
            f.write("1 {}\n".format(v))
        f.write("\n")

    def output_line_colors(self, f):
        f.write("CELL_DATA {}\n".format(len(self.colors)))
        f.write("SCALARS colors float 1\n")
        f.write("LOOKUP_TABLE color_table\n")
        for n in self.colors:
            f.write("{}\n".format(n))

    def output_columns(self, f):
        for (key, values) in self.columns.items():
            f.write("SCALARS {} float 1\n".format(key))
            f.write("LOOKUP_TABLE default\n")
            for value in values:
                f.write("{}\n".format(value))

    def num_lines(self):
        return len(self.lines)

    def num_vertices(self):
        return len(self.vertices)

    @staticmethod
    def reformat_point(point):
        if len(point) == 3:
            return point
        if len(point) == 2:
            return (point[0], point[1], 0)


class ParaViewSimplexDrawer(ParaViewDrawer):
    def __init__(self, n_colors, points, column_names):
        super().__init__(n_colors, column_names)
        self.points = [self.reformat_point(p) for p in points]

    def draw_simplex(self, simplex, color, **threshold_values):
        for edge in itertools.combinations(simplex, 2):
            self.draw_line(edge[0], edge[1], color, **threshold_values)

    def draw_vertex(self, vertex, color, **threshold_values):
        self.vertices.append(vertex)
        self.append_attributes(color, threshold_values)

    def draw_all_vertices(self, color, **threshold_values):
        for i in range(len(self.points)):
            self.draw_vertex(i, color, **threshold_values)

    def output_points(self, f):
        f.write("POINTS {} double\n".format(self.num_points()))
        for point in self.points:
            f.write("{} {} {}\n".format(point[0], point[1], point[2]))
        f.write("\n")

    def output_lines(self, f):
        f.write("LINES {} {}\n".format(self.num_lines(), self.num_lines() * 3))
        for line in self.lines:
            f.write("2 {} {}\n".format(line[0], line[1]))
        f.write("\n")

    def num_points(self):
        return len(self.points)


class ParaViewCubeDrawer(ParaViewDrawer):
    def __init__(self, n_colors, dims, column_names):
        super().__init__(n_colors, column_names)
        self.dims = dims
        assert len(dims) in [2, 3]

    @staticmethod
    def dvs(non_deg):
        n = len(non_deg)
        dvs = []

        def iter(k, dv):
            if k == n:
                dvs.append(dv.copy())
            else:
                if non_deg[k]:
                    for b in [0, 1]:
                        dv[k] = b
                        iter(k + 1, dv)
                else:
                    iter(k + 1, dv)
        iter(0, np.zeros(n, dtype=int))
        return dvs

    @staticmethod
    def dls(non_deg):
        n = len(non_deg)
        dls = []
        for k in range(n):
            if non_deg[k]:
                dl = np.zeros(n, dtype=int)
                dl[k] = 1
                dls.append(dl)
        return dls

    def draw_cube(self, coord, non_deg, color, **threshold_values):
        for dv in self.dvs(non_deg):
            for dl in self.dls(non_deg):
                if np.max(dv + dl) < 2:
                    self.draw_line(coord + dv, coord + dv + dl, color,
                                   **threshold_values)

    def ndim(self):
        return len(self.dims)

    def coord2index(self, coord):
        index = 0
        for k in range(self.ndim()):
            index = index * self.dims[k] + coord[k]
        return index

    def index2coord(self, index):
        coord = [0] * self.ndim()
        for k in reversed(range(self.ndim())):
            index, coord[k] = divmod(index, self.dims[k])
        return coord

    def output_points(self, f):
        f.write("POINTS {} double\n".format(self.num_points()))
        for k in range(self.num_points()):
            coord = self.index2coord(k)
            f.write("{} {} {}\n".format(*self.reformat_point(coord)))
        f.write("\n")

    def num_points(self):
        return int(np.prod(self.dims))

    def output_lines(self, f):
        f.write("LINES {} {}\n".format(self.num_lines(), self.num_lines() * 3))
        for line in self.lines:
            f.write("2 {} {}\n".format(self.coord2index(line[0]),
                                       self.coord2index(line[1])))
        f.write("\n")


class ParaViewSparseCubeDrawer(ParaViewDrawer):
    def __init__(self, n_colors, ndim, column_names):
        super().__init__(n_colors, column_names)
        self.ndim = ndim
        self.points = []
        assert ndim in [2, 3]

    def draw_cube(self, coord, non_deg, color, **threshold_values):
        indices, dvs = self.prepare_points(coord, non_deg)
        for dv in dvs:
            for dl in ParaViewCubeDrawer.dls(non_deg):
                if np.max(dv + dl) < 2:
                    self.draw_line(indices[tuple(dv)], indices[tuple(dv + dl)], color,
                                   **threshold_values)

    def draw_cell(self, cell, cube_geom_resolver, color, **threshold_values):
        coord, non_deg = cube_geom_resolver.resolve_cell(cell)
        self.draw_cube(coord, non_deg, color, **threshold_values)

    def prepare_points(self, coord, non_deg):
        dvs = ParaViewCubeDrawer.dvs(non_deg)
        indices = np.zeros([2] * self.ndim, dtype=int)
        for dv in dvs:
            indices[tuple(dv)] = len(self.points)
            self.points.append(np.flip(dv + coord))
        return indices, dvs

    def output_points(self, f):
        f.write("POINTS {} double\n".format(self.num_points()))
        for point in self.points:
            f.write("{} {} {}\n".format(point[0], point[1], point[2]))
        f.write("\n")

    def num_points(self):
        return len(self.points)

    def output_lines(self, f):
        f.write("LINES {} {}\n".format(self.num_lines(), self.num_lines() * 3))
        for line in self.lines:
            f.write("2 {} {}\n".format(line[0], line[1]))
        f.write("\n")

class ParaViewSparseBitmapDrawer(ParaViewDrawer):
    def __init__(self, n_colors, column_names):
        super().__init__(n_colors, column_names)
        self.vertices = []
        self.n_voxels = 0

    def draw_voxel(self, coord, color, **threshold_values):
        self.n_voxels += 1
        for d1 in (-0.4, 0.4):
            for d2 in (-0.4, 0.4):
                for d3 in (-0.4, 0.4):
                    r = (coord[0] + d1, coord[1] + d2, coord[2] + d3)
                    self.vertices.append(r)
        self.append_attributes(color, threshold_values)

    def output(self, path):
        with open(path, "w") as f:
            self.output_header(f)
            self.output_voxel_data(f)
            self.output_line_colors(f)
            self.pvcolors.output_lookup_table(f)
            self.output_columns(f)

    def output_voxel_data(self, f):
        f.write("DATASET UNSTRUCTURED_GRID\n")
        f.write("POINTS {} double\n".format(len(self.vertices)))
        for r in self.vertices:
            f.write(" ".join(map(str, r)))
            f.write("\n")
        f.write("CELLS {} {}\n".format(self.n_voxels, 9 * self.n_voxels))
        for n in range(self.n_voxels):
            f.write("8 {}\n".format(" ".join(map(str, range(n * 8, (n + 1) * 8)))))
        f.write("CELL_TYPES {}\n".format(self.n_voxels))
        for _ in range(self.n_voxels):
            f.write("11\n")


class ParaViewLinesDrawer(ParaViewDrawer):
    def __init__(self, n_colors, column_names):
        super().__init__(n_colors, column_names)
        self.points = []
        self.point2index = dict()
        self.lines = []

    def index_of(self, p):
        if p in self.point2index:
            return self.point2index[p]
        else:
            index = len(self.points)
            self.point2index[p] = index
            self.points.append(p)
            return index

    def draw_line(self, p1, p2, color, **threshold_values):
        index1 = self.index_of(p1)
        index2 = self.index_of(p2)
        self.lines.append((index1, index2))
        self.append_attributes(color, threshold_values)

    def output_points(self, f):
        f.write("POINTS {} double\n".format(self.num_points()))
        for point in self.points:
            point = self.reformat_point(point)
            f.write("{} {} {}\n".format(point[0], point[1], point[2]))
        f.write("\n")

    def num_points(self):
        return len(self.points)

    def output_lines(self, f):
        f.write("LINES {} {}\n".format(self.num_lines(), self.num_lines() * 3))
        for line in self.lines:
            f.write("2 {} {}\n".format(line[0], line[1]))
        f.write("\n")

    def draw_loop(self, path, color, **threshold_values):
        for k in range(len(path) - 1):
            self.draw_line(path[k], path[k + 1], color, **threshold_values)


class ParaViewPolyLineDrawer(ParaViewDrawer):
    def __init__(self, n_colors, points, column_names):
        super().__init__(n_colors, column_names)
        self.points = [self.reformat_point(p) for p in points]
        self.append_attributes(0, {})

    def output_points(self, f):
        f.write("POINTS {} double\n".format(self.num_points()))
        for point in self.points:
            f.write("{} {} {}\n".format(point[0], point[1], point[2]))
        f.write("\n")

    def output_lines(self, f):
        f.write("LINES 1 {}\n".format(self.num_points() + 1))
        f.write("{} ".format(self.num_points()))
        for k in range(self.num_points()):
            f.write(" {}".format(k))
        f.write("\n\n")

    def num_points(self):
        return len(self.points)


def boundary_of_connected_simplices(simplices):
    def boundaries(key):
        if len(key) == 1:
            return []
        return [key.difference([el]) for el in key]

    count = defaultdict(int)
    for simplex in simplices:
        for boundary in boundaries(simplex):
            count[boundary] += 1

    return [simplex for simplex, num in count.items() if num == 1]
