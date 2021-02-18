from tempfile import TemporaryDirectory
import math
import re

import msgpack
import numpy as np

from homcloud.dipha import (
    DiphaInputFromFiltrationObject, DiphaOutputToIDiagramFile,
    DiphaOutputToBirthDeathPairs, execute_dipha
)
import homcloud.homccube as homccube


class FiltrationWithIndex(object):
    """Super class of AlphaFiltration and BitmapFiltration

    This class has common methods of subclasses.
    """

    def compute_diagram_and_save(self, outpath, parallels=1, algorithm=None):
        """Convert filtration into diagram, and save the diagram into out.
        """
        if not algorithm:
            algorithm = self.favorite_algorithm()

        if algorithm == "dipha":
            self.compute_diagram_by_dipha(outpath, parallels)
        elif algorithm.startswith("phat-"):
            self.compute_diagram_by_phat(outpath, algorithm)
        elif algorithm.startswith("homccube-"):
            self.compute_diagram_by_homccube(outpath, algorithm)
        else:
            raise(ValueError("unknown algorithm: {}".format(algorithm)))

    def compute_diagram_by_dipha(self, outpath, parallels=1,
                                 upper_dim=None, upper_value=None):
        with TemporaryDirectory() as tmpdir:
            dipha_input = DiphaInputFromFiltrationObject(self, tmpdir)
            dipha_output = DiphaOutputToIDiagramFile(outpath, dipha_input,
                                                     tmpdir)
            execute_dipha(dipha_input, dipha_output, parallels,
                          upper_dim=upper_dim, upper_value=upper_value)
            dipha_output.output()

    def compute_diagram_by_phat(self, outpath, algorithm):
        def write_idiagram(f, diagram_bytes, index_map):
            msgpack.dump({
                "diagram": diagram_bytes,
                "index-map": index_map.to_dict(),
            }, f, use_bin_type=True)

        def write_boundary_map(f, boundary_map_bytes):
            if boundary_map_bytes:
                f.write(boundary_map_bytes)

        matrix = self.build_phat_matrix()
        matrix.reduce(algorithm)
        with open(outpath, "wb") as f:
            write_idiagram(f, matrix.dipha_diagram_bytes(), self.index_map)
            write_boundary_map(f, matrix.boundary_map_byte_sequence())

    def compute_pdgm_and_save(self, path, algorithm=None, save_suppl_info=True):
        with open(path, "wb") as f:
            self.compute_pdgm(f, algorithm, save_suppl_info)

    def compute_pairs(self, algorithm=None, parallels=1, upper_dim=None, upper_value=None):
        def compute_pairs_by_phat():
            matrix = self.build_phat_matrix()
            matrix.reduce(algorithm)
            return matrix.birth_death_pairs(), matrix.boundary_map_byte_sequence()

        def format_pair(pair):
            d, birth, death = pair
            return (d, int(birth), (None if death == math.inf else int(death)))

        def compute_pairs_by_dipha():
            with TemporaryDirectory() as tmpdir:
                dipha_input = DiphaInputFromFiltrationObject(self, tmpdir)
                dipha_output = DiphaOutputToBirthDeathPairs(tmpdir)
                execute_dipha(dipha_input, dipha_output, parallels, upper_dim, upper_value)
                return [format_pair(pair) for pair in dipha_output.get_pairs()]

        def compute_pairs_by_homccube():
            return homccube.compute_pd(
                self.index_bitmap.astype(np.int32), self.periodicity,
                self.parse_homccube_algorithm(algorithm), False
            )

        algorithm = algorithm or self.favorite_algorithm()

        if algorithm.startswith("phat-"):
            return compute_pairs_by_phat()
        if algorithm.startswith("dipha"):
            return compute_pairs_by_dipha(), None
        if algorithm.startswith("homccube-"):
            return compute_pairs_by_homccube(), None

        raise(NotImplementedError("unknown alogrithm: {}".format(algorithm)))

    @staticmethod
    def parse_homccube_algorithm(algorithm):
        return int(re.match(r'homccube-(\d+)', algorithm).group(1))
