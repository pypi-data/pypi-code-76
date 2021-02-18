import numpy as np

from homcloud.cubical_ext import CubeEncoder
import homcloud.visualize_3d as visualize_3d


class GeometryResolverBase(object):
    def boundary_cells(self, cell_indices):
        ret = set()
        for cell_index in cell_indices:
            for b in self.boundary_map(cell_index):
                if b in ret:
                    ret.remove(b)
                else:
                    ret.add(b)
        return ret

    def resolve_cells(self, cell_indices):
        return list(map(self.resolve_cell, cell_indices))

    def draw_cells(self, drawer, cells, color, **values):
        for cell in cells:
            self.draw_cell(drawer, cell, color, **values)

    def draw_boundary_cells(self, drawer, cells, color, **values):
        self.draw_cells(drawer, self.boundary_cells(cells), color, **values)


class CubicalResolver(GeometryResolverBase):
    def __init__(self, shape, index_to_cube, boundary_map):
        self.shape = shape
        self.cube_encoder = CubeEncoder(shape)
        self.index_to_cube = index_to_cube
        self.boundary_map = boundary_map

    @property
    def ndim(self):
        return len(self.shape)

    def resolve_cell(self, cell_index):
        return self.cube_encoder.decode_cube(self.index_to_cube[cell_index])

    def resolve_vertices(self, cell_indices):
        ret = set()

        def vertices_of_cube(cube_index):
            coord, nondeg = self.cube_encoder.decode_cube(self.index_to_cube[cube_index])

            def iter(k):
                if k == self.ndim:
                    ret.add(tuple(coord))
                    return
                if nondeg[k]:
                    iter(k + 1)
                    coord[k] += 1
                    iter(k + 1)
                    coord[k] -= 1
                else:
                    iter(k + 1)

            iter(0)
            return ret

        for cube_index in cell_indices:
            vertices_of_cube(cube_index)

        return list(ret)

    def boundary(self, cell_indices):
        return self.resolve_cells(self.boundary_cells(cell_indices))

    def boundary_vertices(self, cell_indices):
        return [
            list(vertex) for vertex
            in self.resolve_vertices(self.boundary_cells(cell_indices))
        ]

    def centroid(self, cell_index):
        coord, nondeg = self.decode_index(cell_index)
        return np.array(coord) + np.array(nondeg) / 2.0

    def draw_cell(self, drawer, cell_index, color, **values):
        coords, nondeg = self.decode_index(cell_index)
        drawer.draw_cube(coords, nondeg, color, **values)

    def decode_index(self, index):
        return self.cube_encoder.decode_cube(self.index_to_cube[index])


class AbstractResolver(GeometryResolverBase):
    def __init__(self, index_to_symbol, boundary_map):
        self.index_to_symbol = index_to_symbol
        self.boundary_map = boundary_map

    def resolve_cell(self, cell_index):
        return self.index_to_symbol[cell_index]

    def boundary(self, cell_indices):
        return self.resolve_cells(self.boundary_cells(cell_indices))


class SimplicialResolver(GeometryResolverBase):
    def __init__(self, index_to_simplex, vertices, boundary_map):
        self.index_to_simplex = index_to_simplex
        self.vertices = vertices
        self.boundary_map = boundary_map

    def resolve_cell(self, cell_index):
        return [self.vertices[i] for i in self.index_to_simplex[cell_index]]

    def resolve_vertices(self, cell_indices):
        vertices = []
        for cell_index in cell_indices:
            for vertex in self.index_to_simplex[cell_index]:
                vertices.append(vertex)

        return [self.vertices[v] for v in set(vertices)]

    def boundary(self, cell_indices):
        return self.resolve_cells(self.boundary_cells(cell_indices))

    def boundary_vertices(self, cell_indices):
        return self.resolve_vertices(self.boundary_cells(cell_indices))

    def draw_boundary(self, drawer, cell_indices, color, **thvalues):
        for b in self.boundary_cells(cell_indices):
            drawer.draw_simplex(self.index_to_simplex[b], color, **thvalues)

    def build_paraview_drawer(self, n_colors, column_names):
        return visualize_3d.ParaViewSimplexDrawer(
            n_colors, self.vertices, column_names
        )

    def centroid(self, cell_index):
        return np.mean(self.resolve_cell(cell_index), axis=0)

    def draw_cell(self, drawer, cell_index, color, **values):
        drawer.draw_simplex(self.index_to_simplex[cell_index], color, **values)


class BitmapResolver(GeometryResolverBase):
    def __init__(self, index_to_pixel):
        self.index_to_pixel = index_to_pixel

    def resolve_cell(self, cell_index):
        return self.index_to_pixel[cell_index]

    def boundary(self, cell_indices):
        raise RuntimeError("boundary is not implemented in bitmap")
