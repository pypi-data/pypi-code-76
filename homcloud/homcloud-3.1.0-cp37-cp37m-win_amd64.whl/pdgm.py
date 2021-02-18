import numpy as np
from cached_property import cached_property

import homcloud.geometry_resolver as geom_resolver
from homcloud.pdgm_format import PDGMReader


def empty_pd(degree=0, sign_flipped=False):
    empty_array = np.zeros((0, ))
    return SimplePDGM(degree, empty_array, empty_array, empty_array, sign_flipped)


class SimplePDGM(object):
    def __init__(self, degree, births, deaths, ess_births=np.array([]),
                 sign_flipped=False):
        self.degree = degree
        self.births = births
        self.deaths = deaths
        self.essential_births = ess_births
        self.sign_flipped = False


class PDGM(object):
    def __init__(self, reader, degree, load_indexed_pairs=True):
        self.pdgmreader = reader
        self.degree = degree
        self.load_pd()
        if load_indexed_pairs:
            self.load_indexed_pd()

    def load_pd(self):
        births, deaths, ess_births = \
            self.pdgmreader.load_pd_chunk("pd", self.degree)
        self.births = np.array(births)
        self.deaths = np.array(deaths)
        self.essential_births = np.array(ess_births)

    def load_indexed_pd(self):
        births, deaths, ess_births = \
            self.pdgmreader.load_pd_chunk("indexed_pd", self.degree)
        if births is None:
            return
        self.birth_indices = np.array(births, dtype=int)
        self.death_indices = np.array(deaths, dtype=int)
        self.essential_birth_indices = np.array(ess_births, dtype=int)

    @staticmethod
    def open(path, degree, load_indexed_pairs=True):
        return PDGM(PDGMReader.open(path), degree, load_indexed_pairs)

    def close(self):
        self.pdgmreader.close()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    @property
    def sign_flipped(self):
        return self.pdgmreader.metadata["sign_flipped"]

    @property
    def filtration_type(self):
        return self.pdgmreader.metadata["filtration_type"]

    @property
    def input_dim(self):
        return self.pdgmreader.metadata["dim"]

    @property
    def num_pairs(self):
        return len(self.births)

    @property
    def death_index_to_pair_number(self):
        return dict(zip(self.death_indices, range(self.num_pairs)))

    @property
    def death_index_to_birth_index(self):
        return dict(zip(self.death_indices, self.birth_indices))

    @cached_property
    def index_to_level(self):
        return self.pdgmreader.load_simple_chunk("index_to_level")

    @cached_property
    def index_to_pixel(self):
        return self.pdgmreader.load_simple_chunk("index_to_pixel")

    @cached_property
    def bitmap_information(self):
        return self.pdgmreader.load_bitmap_information_chunk()

    @cached_property
    def indexed_bitmap(self):
        assert self.filtration_type == "bitmap"
        shape = self.bitmap_information.shape
        bitmap = np.empty(shape, dtype=int)
        for (index, pixel) in enumerate(self.index_to_pixel):
            bitmap[tuple(pixel)] = index
        return bitmap

    @property
    def index_to_simplex(self):
        return self.pdgmreader.load_simple_chunk("index_to_simplex")

    def minmax_of_birthdeath_time(self):
        return (min(self.births.min(), self.deaths.min()),
                max(self.births.max(), self.deaths.max()))

    def count_pairs_in_rectangle(self, birth1, birth2, death1, death2):
        birth_min = min([birth1, birth2])
        birth_max = max([birth1, birth2])
        death_min = min([death1, death2])
        death_max = max([death1, death2])
        return np.sum((self.births >= birth_min) & (self.births <= birth_max) &
                      (self.deaths >= death_min) & (self.deaths <= death_max))

    @cached_property
    def boundary_map_chunk(self):
        return self.pdgmreader.load_boundary_map_chunk()

    def load_boundary_map(self):
        return self.boundary_map_chunk

    @property
    def boundary_map_bytes(self):
        return self.pdgmreader.load_chunk_bytes("boundary_map")

    def default_vertex_symbols(self):
        return [str(k) for k in range(self.num_vertices)]

    @cached_property
    def num_vertices(self):
        return self.pdgmreader.load_chunk("alpha_information")["num_vertices"]

    def simplicial_symbol_resolver(self):
        assert self.filtration_type in ["alpha", "simplicial"]

        return geom_resolver.SimplicialResolver(
            self.pdgmreader.load_simple_chunk("index_to_simplex"),
            self.pdgmreader.load_simple_chunk("vertex_symbols") or
            self.default_vertex_symbols(),
            self.boundary_map
        )

    alpha_symbol_resolver = simplicial_symbol_resolver

    def alpha_coord_resolver(self):
        assert self.filtration_type == "alpha"

        return geom_resolver.SimplicialResolver(
            self.pdgmreader.load_simple_chunk("index_to_simplex"),
            self.pdgmreader.load_simple_chunk("vertex_coordintes"),
            self.boundary_map
        )

    def cubical_geometry_resolver(self):
        assert self.filtration_type == "cubical"

        return geom_resolver.CubicalResolver(
            self.pdgmreader.load_chunk("bitmap_information")["shape"],
            self.pdgmreader.load_simple_chunk("index_to_cube"),
            self.boundary_map
        )

    def bitmap_geometry_resolver(self):
        assert self.filtration_type == "bitmap"

        return geom_resolver.BitmapResolver(self.index_to_pixel)

    def abstract_geometry_resolver(self):
        assert self.filtration_type == "abstract"

        return geom_resolver.AbstractResolver(
            self.pdgmreader.load_simple_chunk("index_to_symbol"),
            self.boundary_map
        )

    def geometry_resolver(self, use_symbol):
        if self.filtration_type == "alpha":
            if use_symbol:
                return self.alpha_symbol_resolver()
            else:
                return self.alpha_coord_resolver()
        elif self.filtration_type == "simplicial":
            return self.simplicial_symbol_resolver()
        elif self.filtration_type == "cubical":
            return self.cubical_geometry_resolver()
        elif self.filtration_type == "bitmap":
            return self.bitmap_geometry_resolver()
        elif self.filtration_type == "abstract":
            return self.abstract_geometry_resolver()
        else:
            raise(RuntimeError("Geometry resolver is unavailable for {}".format(
                self.filtration_type
            )))

    def boundary_map(self, cell_index):
        return self.boundary_map_chunk["map"][cell_index][1]

    @property
    def path(self):
        return self.pdgmreader.path

    @cached_property
    def birth_positions(self):
        return self.geometry_resolver(False).resolve_cells(self.birth_indices)

    @cached_property
    def death_positions(self):
        return self.geometry_resolver(False).resolve_cells(self.death_indices)

    @cached_property
    def essential_birth_positions(self):
        return self.geometry_resolver(False).resolve_cells(
            self.essential_birth_indices
        )

    def pairs_positions(self):
        return zip(self.births, self.deaths,
                   self.birth_positions, self.death_positions)
