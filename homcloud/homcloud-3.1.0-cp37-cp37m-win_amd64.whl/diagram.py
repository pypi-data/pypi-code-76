import struct
import io
import os
import itertools
from operator import attrgetter
import warnings
import enum
import math

import numpy as np
import msgpack

from homcloud.index_map import IndexMap, MapType
from homcloud.pdgm_format import (
    PDGMReader,
    MAGIC_HEADER as PDGM_MAGIC_HEADER,
    MAGIC_HEADER_LENGTH as PDGM_MAGIC_HEADER_LENGTH
)


MINUS_INF = -math.inf


class PD(object):
    """Persistence diagram class

    Note that birth_indices, death_indices, birth_positions, death_positions,
    filtration_type, and index_map are available if and only if
    an index map information is given.

    Instance variables:
    births -- birth times, 1D ndarray of floats
    deaths -- death times, 1D ndarray of floats
    essential_births -- essential birth times, 1D ndarray of floats (deaths are infinity)
    birth_indices -- index birth times, 1D ndarray of int
    death_indices -- index death times, 1D ndarray of int
    birth_positions -- list of birth pixels or birth simplices
    death_positions -- list of death pixels or death simplices
    filtration_type -- index_map.MayType enum
    index_map -- index map defined in index_map module
    sign_flipped -- True if superlevel filtration, otherwise False
    """

    def __init__(self, births, deaths, degree=None,
                 essential_births=np.empty((0,)), boundary_map_dict=None,
                 sign_flipped=False):
        self.births = births
        self.deaths = deaths
        self.essential_births = essential_births
        self.birth_indices = self.death_indices = self.essential_birth_indices = None
        self.birth_positions = None
        self.death_positions = None
        self.filtration_type = None
        self.index_map = None
        self.path = None
        self.degree = degree
        self.sign_flipped = sign_flipped
        self.boundary_map_dict = boundary_map_dict

    MAGIC_DIPHA = 8067171840
    DIPHA_DIAGRAM_TYPE = 2

    @staticmethod
    def is_valid_header(magic, filetype):
        return magic == PD.MAGIC_DIPHA and filetype == PD.DIPHA_DIAGRAM_TYPE

    @staticmethod
    def write_dipha_diagram_header(f):
        f.write(struct.pack("qq", PD.MAGIC_DIPHA, PD.DIPHA_DIAGRAM_TYPE))

    @staticmethod
    def load_from_dipha(infile, d):
        """Create a PD object from dipha

        Args:
        infile -- io-like object
        d -- degree of persistent homology
        """
        if not PD.is_valid_header(*struct.unpack("qq", infile.read(16))):
            raise RuntimeError("This file is not a dipha PD file")
        num_pairs, = struct.unpack("q", infile.read(8))
        births = []
        deaths = []
        ess_births = []

        for _ in range(0, num_pairs):
            pair_d, birth, death = struct.unpack("qdd", infile.read(24))
            if (-pair_d - 1 == d) or (pair_d == d and death == np.inf):
                ess_births.append(birth)
            elif pair_d == d and birth == MINUS_INF:
                pass
            elif pair_d == d:
                births.append(birth)
                deaths.append(death)

        return PD(np.array(births), np.array(deaths), d, np.array(ess_births))

    @staticmethod
    def load_from_diphafile(inpath, d):
        """Creat a PD object from dipha file.

        Args:
        inpath -- dipha diagram file path
        d -- degree of persistence homology
        """
        with open(inpath, "rb") as f:
            return PD.load_from_dipha(f, d).set_path(inpath)

    @staticmethod
    def load_from_text(infile):
        """Create a PD object from text file

        Args:
        infile -- io-like object
        """
        births = []
        deaths = []
        for line in infile:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            birth, death = line.split()
            if death == "Inf":
                continue
            births.append(float(birth))
            deaths.append(float(death))

        return PD(np.array(births), np.array(deaths))

    @staticmethod
    def merge(pds):
        """Merge multiple PDs in on pd object.

        Args:
        pds: list of PD objects
        """
        if not pds:
            return PD.empty_pd()
        births = np.concatenate([pd.births for pd in pds])
        deaths = np.concatenate([pd.deaths for pd in pds])
        ess_births = np.concatenate([pd.essential_births for pd in pds])
        new_pd = PD(births, deaths, None, ess_births)

        return new_pd

    @staticmethod
    def empty_pd(sign_flipped=False):
        """Return a PD without any birth-death pair
        """
        return PD(np.zeros((0,)), np.zeros((0,)), sign_flipped=sign_flipped)

    @staticmethod
    def load_from_textfile(path):
        """Create a PD object from text file whose name is path

        Args:
        path -- input file path
        """
        with open(path) as f:
            return PD.load_from_text(f).set_path(path)

    @staticmethod
    def load_from_indexed_diphafile(inpath, d, load_bmap=False):
        """Create a PD object from idiagram file

        Args:
        inpath -- the path of input file
        d -- degree
        """
        with open(inpath, "rb") as f:
            return PD.load_from_indexed_dipha(f, d, load_bmap).set_path(inpath)

    @staticmethod
    def load_from_indexed_dipha(f, d, load_bmap=False):
        """Create a PD object from idiagram io-like object

        Args:
        f -- an io-like object, read data from this object
        d -- degree
        """
        unpacker = msgpack.Unpacker(f, raw=False)
        data = next(unpacker)
        pd = PD.load_from_dipha(io.BytesIO(data["diagram"]), d)
        pd.boundary_map_dict = PD.load_boundary_map(load_bmap, unpacker)
        pd.index_map = IndexMap.load_from_dict(data["index-map"])
        pd.restore_levels(pd.index_map)
        return pd

    @staticmethod
    def load_boundary_map(load_bmap, unpacker):
        if not load_bmap:
            return None

        try:
            return next(unpacker)
        except StopIteration:
            raise(RuntimeError("No boundary map information"))

    @staticmethod
    def load_from_pmtfile(path, d):
        with open(path, "rb") as f:
            return PD.load_from_pmt(f, d).set_path(path)

    @staticmethod
    def load_from_pmt(f, d):
        if d != 0:
            raise ValueError("degree for pmt file must be 0")
        dic = msgpack.unpack(f, raw=False)
        births = []
        deaths = []
        birth_poss = []
        death_poss = []
        for node in dic["nodes"]:
            if node["level"] != node["death_time"] and node["death_time"] is not None:
                births.append(node["level"])
                deaths.append(node["death_time"])
                birth_poss.append(node["pos"])
                death_poss.append(node["death_pos"])
        pd = PD(np.array(births), np.array(deaths), 0)
        pd.birth_positions = birth_poss
        pd.death_positions = death_poss
        pd.filtration_type = MapType.bitmap
        return pd

    @staticmethod
    def load_from_p2mtfile(path, d):
        with open(path, "rb") as f:
            return PD.load_from_p2mt(f, d).set_path(path)

    @staticmethod
    def load_from_p2mt(f, d):
        dic = msgpack.unpack(f, raw=False)
        if d == 0:
            nodes = dic["lower"]["nodes"]
        elif d == dic["dim"] - 1:
            nodes = dic["upper"]["nodes"]
        else:
            raise(RuntimeError("degree for p2mt file must be 0 or n-1"))
        births = list()
        deaths = list()
        birth_poss = list()
        death_poss = list()
        ess_births = list()
        ess_birth_poss = list()
        for node in nodes.values():
            if node["birth-time"] == node["death-time"]:
                continue
            if node["death-time"] is None:
                ess_births.append(node["birth-time"])
                ess_birth_poss.append(node["birth-pixel"])
            else:
                births.append(node["birth-time"])
                deaths.append(node["death-time"])
                birth_poss.append(node["birth-pixel"])
                death_poss.append(node["death-pixel"])
        pd = PD(np.array(births, dtype=float), np.array(deaths, dtype=float), d,
                np.array(ess_births, dtype=float))
        pd.birth_positions = birth_poss
        pd.death_positions = death_poss
        pd.essential_birth_positions = ess_birth_poss
        pd.filtration_type = MapType.bitmap
        pd.sign_flipped = dic["sign-flipped"]
        return pd

    @staticmethod
    def load_from_pdgm(f, degree):
        reader = PDGMReader(f)
        births, deaths, ess_births = reader.load_pd_chunk("pd", degree)
        pd = PD(np.array(births, dtype=float), np.array(deaths, dtype=float),
                degree, np.array(ess_births, dtype=float))
        birth_indices, death_indices, ess_birth_indices = reader.load_pd_chunk(
            "indexed_pd", degree
        )
        if birth_indices is not None:
            pd.birth_indices = np.array(birth_indices, dtype=int)
            pd.death_indices = np.array(death_indices, dtype=int)
            pd.essential_birth_indices = np.array(ess_birth_indices, dtype=int)

        if reader.filtration_type == "abstract":
            pd.filtration_type = MapType.abstract
            symbols = reader.load_simple_chunk("index_to_symbol")
            pd.birth_positions = [symbols[i] for i in pd.birth_indices]
            pd.death_positions = [symbols[i] for i in pd.death_indices]
            pd.essential_birth_positions = [symbols[i] for i in pd.essential_birth_indices]
        if reader.filtration_type == "rips":
            pd.filtration_type = MapType.rips

        pd.sign_flipped = reader.metadata["sign_flipped"]
        return pd

    @staticmethod
    def load_from_pdgm_file(path, degree):
        with open(path, "rb") as f:
            return PD.load_from_pdgm(f, degree).set_path(path)

    @staticmethod
    def load(filetype, path, degree, negate=False):
        filetype = PD.estimate_filetype(filetype, path)
        if filetype == PD.FileType.dipha_diagram:
            pd = PD.load_from_diphafile(path, degree)
        elif filetype == PD.FileType.idipha_diagram:
            pd = PD.load_from_indexed_diphafile(path, degree)
        elif filetype == PD.FileType.text:
            pd = PD.load_from_textfile(path)
        elif filetype == PD.FileType.persistence_merge_tree:
            pd = PD.load_from_pmtfile(path, degree)
        elif filetype == PD.FileType.p2mt:
            pd = PD.load_from_p2mtfile(path, degree)
        elif filetype == PD.FileType.pdgm:
            pd = PD.load_from_pdgm_file(path, degree)
        else:
            raise ValueError("Unkown file format: {}".format(path))
        if negate:
            pd.negate_birth_death_time()
        return pd

    @staticmethod
    def load_diagrams(typestr, paths, degree, negate):
        """Load diagrams from paths, merge them, and return merged diagram

        Args:
        typestr -- the type of input file, "dipha", "text", "idipha",
                   or None(autodetect)
        paths -- the list of input files
        degree -- degree of persistence homology
                  (not requred for "text" format)
        negate -- flip sign of birth/death times if True
        """
        diagrams = [PD.load(typestr, path, degree) for path in paths]
        if len(diagrams) != 1:
            diagram = PD.merge(diagrams)
        else:
            diagram = diagrams[0]

        if negate:
            diagram.negate_birth_death_time()

        return diagram

    @staticmethod
    def estimate_filetype(typestr, path):
        """Estimate file type from typestr and path and return
        an element of PD.FileType

        if the file type cannot be determined, returns PD.FileType.unknown
        args:
        typestr -- a string representing filetype, one of: None, "idipha",
                   "dipha", "text"
        path -- a filepath string
        """
        TABLE_TYPENAME = {
            "idipha": PD.FileType.idipha_diagram,
            "dipha": PD.FileType.dipha_diagram,
            "text": PD.FileType.text,
            "pmt": PD.FileType.persistence_merge_tree,
            "p2mt": PD.FileType.p2mt,
            "pdgm": PD.FileType.pdgm,
        }
        TABLE_EXTENSION = {
            ".idiagram": PD.FileType.idipha_diagram,
            ".diagram": PD.FileType.dipha_diagram,
            ".pmt": PD.FileType.persistence_merge_tree,
            ".p2mt": PD.FileType.p2mt,
            ".txt": PD.FileType.text,
            ".pdgm": PD.FileType.pdgm,
        }

        def check_file_header(path):
            with open(path, "rb") as f:
                if f.read(PDGM_MAGIC_HEADER_LENGTH) == PDGM_MAGIC_HEADER:
                    return PD.FileType.pdgm
                else:
                    return None

        _, ext = os.path.splitext(path)
        return(TABLE_TYPENAME.get(typestr) or
               check_file_header(path) or
               TABLE_EXTENSION.get(ext) or
               PD.FileType.unknown)

    def set_path(self, path):
        self.path = path
        return self

    def pairs(self):
        """Return birth-death pairs as a list of (2,)-ndarray
        """
        return np.array([self.births, self.deaths]).transpose()

    def pairs_positions(self):
        """Return birth-death pairs as a list of Pair objects.

        Pair object has additional information of birth/death simplices/pixels.
        The returned list is sorted by pairs' lifetime.
        """
        return sorted([
            Pair(birthtime, deathtime, birth_pos, death_pos)
            for (birthtime, deathtime, birth_pos, death_pos)
            in zip(self.births, self.deaths, self.birth_positions, self.death_positions)
        ], key=attrgetter("lifetime"), reverse=True)

    def lifetimes(self):
        """Return birth times of pairs as a 1D ndarray of floats
        """
        return self.deaths - self.births

    def restore_levels(self, index_map):
        """Restore real birth and death times from index map

        This method is used internally.
        """
        self.birth_indices = self.births.astype(int)
        self.death_indices = self.deaths.astype(int)
        self.essential_birth_indices = self.essential_births.astype(int)
        births, birth_poss = index_map.resolve(self.birth_indices)
        deaths, death_poss = index_map.resolve(self.death_indices)
        mask = (births != deaths) & (births != MINUS_INF)
        self.births = births[mask]
        self.deaths = deaths[mask]
        self.birth_positions = [birth_poss[i] for (i, b) in enumerate(mask) if b]
        self.death_positions = [death_poss[i] for (i, b) in enumerate(mask) if b]
        self.masked_birth_indices = self.birth_indices[mask]
        self.masked_death_indices = self.death_indices[mask]
        self.essential_births, self.essential_birth_positions = index_map.resolve(
            self.essential_birth_indices
        )
        self.filtration_type = index_map.type()
        self.sign_flipped = index_map.levels_sign_flipped

    def negate_birth_death_time(self):
        """Flip the sign of birth times and death times.

        If index_map says that the sign of levels in the index_map is already flipped,
        this method call do nothing.
        """
        if self.sign_flipped:
            return
        if self.index_map and not self.sign_flipped:
            warnings.warn("Flip sign unless your filtration is not superlevel")
        self.births *= -1
        self.deaths *= -1
        self.essential_births *= -1

    def minmax_of_birthdeath_time(self):
        """Return a pair of (min, max) of birth time and death time

        The return value will be used to determine the range of plotting.
        """
        return (min(self.births.min(), self.deaths.min()),
                max(self.births.max(), self.deaths.max()))

    def count_pairs_in_rectangle(self, birth1, birth2, death1, death2):
        birth_min = min([birth1, birth2])
        birth_max = max([birth1, birth2])
        death_min = min([death1, death2])
        death_max = max([death1, death2])

        return np.sum((self.births >= birth_min) & (self.births <= birth_max) &
                      (self.deaths >= death_min) & (self.deaths <= death_max))

    def cell_dim(self, idx):
        return self.boundary_map_dict["map"][idx][0]

    def cell_boundary(self, idx):
        return self.boundary_map_dict["map"][idx][1]

    def geometry_resolver(self):
        return self.index_map.geometry_resolver(self)

    class FileType(enum.Enum):
        text = 0
        dipha_diagram = 1
        idipha_diagram = 2
        persistence_merge_tree = 3
        p2mt = 4
        pdgm = 5
        unknown = -1


class Pair(object):
    def __init__(self, birth, death, birth_pos, death_pos):
        self.birth = birth
        self.death = death
        self.birth_pos = birth_pos
        self.death_pos = death_pos

    @property
    def lifetime(self):
        return self.death - self.birth

    def display_str(self):
        return "({0}, {1}) - ({2}, {3}) ({4}, {5})".format(
            self.birth, self.death,
            self.birth_pos[0], self.birth_pos[1],
            self.death_pos[0], self.death_pos[1]
        )

    def __repr__(self):
        return "Pair({})".format(self.display_str())
