import subprocess
import os
import math
import struct

import msgpack


class DiphaInputFromFiltrationObject:
    def __init__(self, filtration, tmpdir):
        self.filtration = filtration
        self.tmpdir = tmpdir

    @property
    def index_map(self):
        return self.filtration.index_map.to_dict()

    def save_to_file(self):
        complex_path = os.path.join(self.tmpdir, "tmp.complex")
        with open(complex_path, "wb") as f:
            self.filtration.write_dipha_complex(f)
        return complex_path


class DiphaOutputToIDiagramFile:
    def __init__(self, outpath, dipha_input, tmpdir):
        self.outpath = outpath
        self.dipha_input = dipha_input
        self.tmpdir = tmpdir
        self.binary = None

    def dipha_diagram_path(self):
        return os.path.join(self.tmpdir, "tmp.diagram")

    def output(self):
        self.write_indexed_diagram(self.get_binary())

    def get_binary(self):
        if self.binary:
            return self.binary
        with open(self.dipha_diagram_path(), "rb") as f:
            return f.read()

    def write_indexed_diagram(self, binary):
        with open(self.outpath, "wb") as f:
            f.write(msgpack.packb({
                "diagram": binary,
                "index-map": self.dipha_input.index_map,
            }, use_bin_type=True))


class DiphaOutputToBirthDeathPairs:
    def __init__(self, tmpdir):
        self.tmpdir = tmpdir

    def dipha_diagram_path(self):
        return os.path.join(self.tmpdir, "tmp.diagram")

    def get_pairs(self):
        with open(self.dipha_diagram_path(), "rb") as f:
            f.read(16)  # skip header
            num_pairs, = struct.unpack("q", f.read(8))

            for _ in range(num_pairs):
                d, birth, death = struct.unpack("qdd", f.read(24))
                if d < 0:
                    yield (-d - 1, birth, math.inf)
                else:
                    yield (d, birth, death)


def execute_dipha(dipha_input, dipha_output, parallels=1, dual=False,
                  upper_dim=None, upper_value=None):
    run(dipha_input.save_to_file(), dipha_output.dipha_diagram_path(),
        parallels, dual, upper_dim, upper_value)


def run(inpath, outpath, parallels=1, dual=False, upper_dim=None, upper_value=None):
    options = []

    if os.environ.get("HOMCLOUD_SUPPRESS_MPI") == "1":
        mpi = []
    else:
        mpi = ["mpiexec", "-n", str(parallels)]
    if dual:
        options.append("--dual")
    if upper_dim is not None:
        options.extend(["--upper_dim", str(upper_dim + 1)])
    if upper_value is not None and upper_value != math.inf:
        options.extend(["--upper_value", str(upper_value)])

    subprocess.check_call(mpi + ["dipha"] + options + [inpath, outpath])
