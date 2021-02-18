import json
import enum
import functools
from itertools import chain
from collections import defaultdict
import numpy as np


@enum.unique
class MapType(enum.Enum):
    bitmap = 1
    alpha = 2
    cubical = 3
    rips = 4
    abstract = 5


class IndexMap(object):
    """A class representing a map from index to the real birth time (called a level).

    This class is a baseclass of IndexMapForBitmap and IndexMapForAlphaFiltration.
    The main purpose is to save and load index-map information to and from
    a file or binary string.

    Instance variables:
    levels -- 1D ndarray from index birth time of each pixel/simplex to
              real birth time of each pixel/simplex.
              index birth times are 0,1, ..., number-of-pixels/simplices - 1
    dimension -- dimension of input data, 2, 3, or greater integers
    format_version -- index-map file format version number, int
    """

    def __init__(self, levels, dim, format_version):
        self.levels = levels
        self.dimension = dim
        self.format_version = format_version

    def resolve_levels(self, index):
        """Convert the list of indices to the list of birth/death times

        Args:
        index -- a list of indices (ndarray whose dtype is float)
        """
        return self.levels[np.array(index, dtype=int)]

    def resolve_level(self, index):
        """Convert a single index to the birth radius

        Args:
        index -- an integer of index
        """
        return self.levels[index]

    def resolve_pair(self, pair):
        """Convert a pair of indices to the birth and death time

        Args:
        pair -- a pair of indices
        """
        return (self.levels[pair[0]], self.levels[pair[1]])

    @staticmethod
    def load_from_dict(dict_):
        """Load an index map from the given dict object
        """
        dim = dict_.get("dimension", None)
        format_version = dict_.get("format-version", 0)
        if dict_["type"] == "bitmap":
            return IndexMapForBitmap(np.array(dict_["positions"]),
                                     np.array(dict_["levels"]),
                                     dim,
                                     dict_.get("levels-sign-flipped"),
                                     tuple(dict_["shape"]) if "shape" in dict_ else None,
                                     format_version)
        if dict_["type"] == "alpha":
            return IndexMapForAlphaFiltration(
                np.array(dict_["levels"]), np.array(dict_["points"]),
                dict_["simplices"], dict_.get("symbols"), dim, format_version
            )

        if dict_["type"] == "cubical":
            return IndexMapForCubical(np.array(dict_["levels"]),
                                      dict_["levels-sign-flipped"],
                                      dict_["shape"], dict_["cubes"], format_version)
        if dict_["type"] == "rips":
            return IndexMapForRips(np.array(dict_["levels"]), dim,
                                   dict_["edges"], dict_["symbols"], format_version)
        if dict_["type"] == "abstract":
            return IndexMapForAbstractFiltration(np.array(dict_["levels"]), dim,
                                                 dict_["symbols"], format_version)

    FORMAT_VERSION = 4


class IndexMapForBitmap(IndexMap):
    """A class representing a map from index birth time to the real birth times for
    bitmap filtrations.

    Instance variables:
    positions -- n-D ndarray represents a map from an index to the [x, y, ...]
                 coordinate of the pixel correspoinding the index
    levels_sign -- the sign of levels, for superlevel filtration, this is set to -1.0,
                 otherwise, this is set to 1.0. For old version (format_version <= 1),
                 this value is None.
    """

    def __init__(self, positions, levels, dim, levels_sign_flipped, shape=None,
                 format_version=IndexMap.FORMAT_VERSION):
        self.positions = positions
        self.levels_sign_flipped = levels_sign_flipped
        self.shape = shape
        IndexMap.__init__(self, levels, dim, format_version)

    def resolve(self, indices):
        """
        Returns a tuple of (real birth times) and (correspoding coordinates)
        computed from indices and map information.

        Args:
        indices -- 1D ndarray of int, the list of indices
        """
        indices = np.array(indices, dtype=int)
        return (self.levels[indices], self.positions[indices])

    def to_dict(self):
        """Return dict that represents the index object
        """
        return {
            "type": "bitmap",
            "positions": self.positions.tolist(),
            "levels": self.levels.tolist(),
            "levels-sign-flipped": self.levels_sign_flipped,
            "shape": list(self.shape),
            "format-version": self.format_version,
            "dimension": self.dimension,
        }

    @staticmethod
    def type():
        return MapType.bitmap

    def indexed_bitmap(self):
        bitmap = np.zeros(self.shape, dtype=int)
        for n, pos in enumerate(self.positions):
            bitmap[tuple(pos)] = n
        return bitmap


class IndexMapForAlphaFiltration(IndexMap):
    """A class representing a map from index birth times to the real birth times for
    alpha filtrations.

    Instance variables:
    points -- list of coordinates of all points in the delaunay triagulation
    simplces -- list of simplices, indexed by the index-birth-time.
                In this variable, a simplex is repserented by the list of
                points. Each point is represented by an integer, the index
                in self.points.
    """

    def __init__(self, levels, points, simplices, symbols,
                 dim, format_version=IndexMap.FORMAT_VERSION):
        self.points = points
        self.simplices = simplices
        self.symbols = symbols or self.numeric_symbols()
        IndexMap.__init__(self, levels, dim, format_version)

    def numeric_symbols(self):
        n = self.points.shape[0]
        return list(map(str, range(n)))

    def set_symbols(self, syms):
        self.symbols = syms

    def resolve(self, indices):
        """
        Returns a tuple of (real birth times) and (correspoding simplices)
        computed from indices and map information.

        Args:
        indices -- 1D ndarray of int, the list of indices
        """
        simplices = [[self.points[simplex_index]
                      for simplex_index in self.simplices[int(index)]]
                     for index in indices]
        return (self.levels[np.array(indices, dtype=int)], simplices)

    def to_dict(self):
        """Return dict that represents the index object
        """
        return {
            "type": "alpha",
            "levels": self.levels.tolist(),
            "points": self.points.tolist(),
            "symbols": self.symbols,
            "simplices": self.simplices,
            "format-version": self.format_version,
            "dimension": self.dimension,
        }

    def resolve_simplex(self, simplex_index):
        simplex = self.simplices[simplex_index]
        return [self.points[point_index] for point_index in simplex]

    def centroid_of_simplex(self, simplex_index):
        return np.mean(self.resolve_simplex(simplex_index), axis=0)

    def simplex(self, i):
        return Simplex(i, self)

    @staticmethod
    def type():
        return MapType.alpha

    levels_sign_flipped = False

    def geometry_resolver(self, diagram):
        return AlphaGeometryResolver(self, diagram)


@functools.total_ordering
class Simplex(object):
    def __init__(self, index, index_map):
        self.index = index
        self.index_map = index_map

    def __eq__(self, other):
        return (isinstance(other, Simplex) and
                self.index_map is other.index_map and
                self.index == other.index)

    def __lt__(self, other):
        if not isinstance(other, Simplex):
            raise NotImplementedError
        if other.index_map is not self.index_map:
            raise NotImplementedError
        return self.index < other.index

    def __hash__(self):
        return hash((self.index, id(self.index_map)))

    def __repr__(self):
        return "index_map.Simplex(index={}, index_map={})".format(
            self.index, self.index_map
        )

    def vertices(self):
        return [Point(point, self.index_map) for point in self.index_map.simplices[self.index]]

    def point_coords(self):
        return [point.coord() for point in self.vertices()]

    def centroid(self):
        return np.mean(self.point_coords(), axis=0)

    def key(self):
        return tuple(sorted(self.index_map.simplices[self.index]))

    def frozen_key(self):
        return frozenset(self.index_map.simplices[self.index])

    def boundary_keys(self):
        if self.dim() == 0:
            return []
        s = tuple(sorted(self.index_map.simplices[self.index]))
        return [s[:i] + s[i + 1:] for i in range(len(s))]

    def dim(self):
        return len(self.index_map.simplices[self.index]) - 1

    def boundary_keys_orientation(self):
        return [(key, (-1)**i) for (i, key) in enumerate(self.boundary_keys())]

    def time(self):
        return self.index_map.levels[self.index]


@functools.total_ordering
class Point(object):
    def __init__(self, index, index_map):
        self.index = index
        self.index_map = index_map

    def __eq__(self, other):
        return (isinstance(other, Point) and
                self.index_map is other.index_map and
                self.index == other.index)

    def __lt__(self, other):
        if not isinstance(other, Point):
            raise NotImplementedError
        if other.index_map is not self.index_map:
            raise NotImplementedError
        return self.index < other.index

    def __hash__(self):
        return hash((self.index, id(self.index_map)))

    def __repr__(self):
        return "index_map.Point(index={}, index_map={})".format(
            self.index, self.index_map
        )

    def coord(self):
        return self.index_map.points[self.index]


class IndexMapForCubical(IndexMap):
    def __init__(self, levels, levels_sign_flipped, shape, cubes,
                 format_version=IndexMap.FORMAT_VERSION):
        super().__init__(levels, len(shape), format_version)
        self.shape = shape
        self.cubes = cubes
        self.levels_sign_flipped = levels_sign_flipped
        self.required_bits = [int.bit_length(n - 1) + 1 for n in self.shape]

    def to_dict(self):
        return {
            "type": "cubical",
            "levels": self.levels.tolist(),
            "cubes": self.cubes,
            "shape": self.shape,
            "format-version": self.format_version,
            "dimension": self.dimension,
            "levels-sign-flipped": self.levels_sign_flipped
        }

    @staticmethod
    def type():
        return MapType.cubical

    def resolve(self, indices):
        return (self.levels[np.array(indices, dtype=int)],
                [self.decode_coords(self.cubes[index]) for index in indices])

    def decode_coords(self, cube):
        coords = [0] * self.dimension
        for k in range(self.dimension):
            coords[k] = (cube & ((1 << self.required_bits[k]) - 1)) >> 1
            cube >>= self.required_bits[k]
        return coords

    def decode_cube(self, cube):
        coords = [0] * self.dimension
        nondeg = [False] * self.dimension
        for k in range(self.dimension):
            bits = cube & ((1 << self.required_bits[k]) - 1)
            coords[k] = bits >> 1
            nondeg[k] = bool(bits & 1)
            cube >>= self.required_bits[k]
        return coords, nondeg

    def normalize_periodic(self, coords):
        return tuple(x % width for (x, width) in zip(coords, self.shape))

    def vertices(self, cube):
        coords, nondeg = self.decode_cube(cube)
        vertices = []

        def iter(k):
            if k == self.dimension:
                vertices.append(self.normalize_periodic(coords))
            else:
                if nondeg[k]:
                    for b in [0, 1]:
                        coords[k] += b
                        iter(k + 1)
                        coords[k] -= b
                else:
                    iter(k + 1)

        iter(0)
        return vertices

    def geometry_resolver(self, diagram):
        return CubicalGeometryResolver(self, diagram)


class IndexMapForRips(IndexMap):
    def __init__(self, levels, dim, edges, symbols, format_version=IndexMap.FORMAT_VERSION):
        super().__init__(levels, dim, format_version)
        self.edges = edges
        self.symbols = symbols or self.numeric_symbols(len(levels) - 1)

    def resolve(self, indices):
        return (self.levels[np.array(indices, dtype=int)],
                list(map(self.resolve_edge, indices)))

    def resolve_edge(self, idx):
        if idx == 0:
            return "*"
        edge = self.edges[idx]
        return (self.symbols[edge[0]], self.symbols[edge[1]])

    @staticmethod
    def numeric_symbols(n):
        return list(map(str, range(n)))

    @staticmethod
    def type():
        return MapType.rips

    levels_sign_flipped = False

    def to_dict(self):
        return {
            "type": "rips",
            "levels": self.levels.tolist(),
            "symbols": self.symbols,
            "edges": self.edges,
            "format-version": self.format_version,
            "dimension": self.dimension,
        }


class IndexMapForAbstractFiltration(IndexMap):
    def __init__(self, levels, dim, symbols,
                 format_version=IndexMap.FORMAT_VERSION):
        super().__init__(levels, dim, format_version)
        self.symbols = symbols

    def to_dict(self):
        return {
            "type": "abstract",
            "levels": self.levels.tolist(),
            "symbols": self.symbols,
            "format-version": self.format_version,
            "dimension": self.dimension,
        }

    def resolve(self, indices):
        """
        Returns a tuple of (real birth times) and (correspoding symbols)
        computed from indices and map information.

        Args:
        indices -- 1D ndarray of int, the list of indices
        """
        return (self.levels[np.array(indices, dtype=int)],
                [self.symbols[index] for index in indices])

    @staticmethod
    def type():
        return MapType.abstract

    levels_sign_flipped = False


class GeometryResolverBase(object):
    def __init__(self, index_map, diagram):
        self.diagram = diagram
        self.index_map = index_map

    def boundary(self, cells):
        """
        """
        ret = defaultdict(bool)
        for cell in cells:
            for b in self.diagram.cell_boundary(cell):
                ret[b] = not ret[b]
        return [cell for (cell, cond) in ret.items() if cond]

    def draw_cells(self, drawer, cells, color, **kwargs):
        for idx in cells:
            self.draw_cell(drawer, idx, color, **kwargs)

    def unique_vertices_coords(self, cells):
        return self.vertex_indices_to_coords(self.unique_vertices(cells))

    def unique_vertices(self, cells):
        return set(chain.from_iterable(self.vertices(i) for i in cells))


class AlphaGeometryResolver(GeometryResolverBase):
    def vertex_indices_to_coords(self, indices):
        return [self.index_map.points[idx] for idx in indices]

    def vertices_coords(self, idx):
        return self.vertex_indices_to_coords(self.vertices(idx))

    def vertices(self, idx):
        return self.index_map.simplices[idx]

    def centroid(self, idx):
        return np.mean(self.vertices_coords(idx), axis=0)

    def cells_coords(self, simplices):
        return [self.vertices_coords(idx) for idx in simplices]

    def boundary_coords(self, simplices):
        return [self.vertices_coords(b) for b
                in self.boundary(simplices)]

    def boundary_vertices_coords(self, simplices):
        return self.vertex_indices_to_coords(self.boundary_vertices(simplices))

    def boundary_vertices(self, simplices):
        return self.unique_vertices(self.boundary(simplices))

    def draw_cell(self, drawer, idx, color, **kwargs):
        drawer.draw_simplex(self.index_map.simplices[idx], color, **kwargs)

    cell_coords = vertices_coords

    def unique_vertices_symbols(self, simplices):
        return self.vertices_to_symbols(self.unique_vertices(simplices))

    def vertices_to_symbols(self, indices):
        return [self.index_map.symbols[idx] for idx in indices]

    def cell_symbols(self, idx):
        return self.vertices_to_symbols(self.vertices(idx))

    def cells_symbols(self, simplices):
        return list(map(self.cell_symbols, simplices))

    def boundary_symbols(self, simplices):
        return self.cells_symbols(self.boundary(simplices))

    def boundary_vertices_symbols(self, simplices):
        return self.vertices_to_symbols(self.boundary_vertices(simplices))


class CubicalGeometryResolver(GeometryResolverBase):
    def centroid(self, idx):
        """Return a vertex coordinate of idx-th cell

        Note that this method does not return the centroid of the cube.
        This is because of rough implemetation.
        """
        return np.array(self.index_map.decode_coords(self.index_map.cubes[idx]))

    def draw_cell(self, drawer, idx, color, **kwargs):
        coords, nondeg = self.index_map.decode_cube(self.index_map.cubes[idx])
        drawer.draw_cube(coords, nondeg, color, **kwargs)

    def boundary_coords(self, cubes):
        return [self.index_map.decode_cube(self.index_map.cubes[idx])
                for idx in self.boundary(cubes)]

    def vertex_coords(self, idx):
        return self.index_map.vertices(self.index_map.cubes[idx])

    def boundary_vertices_coords(self, cubes):
        return self.unique_vertices(chain.from_iterable(
            self.vertex_coords(idx) for idx in self.boundary(cubes)
        ))

    def cells_coords(self, cubes):
        return [
            self.index_map.decode_cube(self.index_map.cubes[idx])
            for idx in cubes
        ]

    def unique_vertices_coords(self, cubes):
        return self.unique_vertices(chain.from_iterable(
            self.vertex_coords(idx) for idx in cubes)
        )

    def cell_coords(self, idx):
        return self.index_map.decode_coords(self.index_map.cubes[idx])

    @staticmethod
    def unique_vertices(vertices):
        return [list(v) for v in set(vertices)]
