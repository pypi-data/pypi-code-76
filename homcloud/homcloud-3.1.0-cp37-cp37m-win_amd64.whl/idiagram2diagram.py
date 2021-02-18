import argparse
import struct
import io
import math

import msgpack

from homcloud.diagram import PD, MINUS_INF
from homcloud.index_map import IndexMap
from homcloud.version import __version__
from homcloud.license import add_argument_for_license


def argument_parser():
    p = argparse.ArgumentParser(description="Convert .idiagram file to .diagram file")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_argument_for_license(p)
    p.add_argument("input", help="input file name")
    p.add_argument("output", help="output file name")
    return p


def convert(infile, outfile):
    unpacker = msgpack.Unpacker(infile, raw=False)
    idiagram_data = next(unpacker)
    dipha_diagram = io.BytesIO(idiagram_data["diagram"])
    pairs = []
    levels = idiagram_data["index-map"]["levels"]

    if not PD.is_valid_header(*struct.unpack("qq", dipha_diagram.read(16))):
        raise RuntimeError("This file is not a dipha PD file")
    num_pairs, = struct.unpack("q", dipha_diagram.read(8))

    def resolve(index):
        return levels[int(index)]

    for _ in range(num_pairs):
        d, birth, death = struct.unpack("qdd", dipha_diagram.read(24))
        if d < 0:
            pairs.append((d, resolve(birth), 0.0))
        elif death == math.inf:
            pairs.append((-d - 1, resolve(birth), 0.0))
        elif birth == MINUS_INF:
            pass
        else:
            birth_time = resolve(birth)
            death_time = resolve(death)
            if birth_time != death_time:
                pairs.append((d, birth_time, death_time))

    PD.write_dipha_diagram_header(outfile)
    outfile.write(struct.pack("q", len(pairs)))
    for pair in pairs:
        outfile.write(struct.pack("qdd", *pair))


def main(args=None):
    args = args or argument_parser().parse_args()
    with open(args.input, "rb") as infile:
        with open(args.output, "wb") as outfile:
            convert(infile, outfile)


if __name__ == "__main__":
    main()
