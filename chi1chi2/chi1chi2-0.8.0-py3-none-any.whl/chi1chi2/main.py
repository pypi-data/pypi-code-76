#!/usr/bin/env python
from optparse import OptionParser

from chi1chi2.core.bulk_property import BulkProperties
from chi1chi2.core.property import Lorentz, DistributedPolar
from chi1chi2.core.property_reader import PropsMol, equalize_properties
from chi1chi2.input.input_preparator import Input
from chi1chi2.utils.constants import resolve_path, INP_FILENAME_PATTERN

usage = """
%prog [options]
main program for the chi1 and chi2 tensors calculations

required input:
- input file
- lorentz tensor
- property files (one for every molecule)
optional input:
- distributed polarizabilities (one for every molecule)
- name of the bulk properties (chi1, chi2)

default output:
- raw properties (chi1, chi2)
"""
parser = OptionParser(usage=usage)

parser.add_option("-i", "--input-file", dest="input_file", help="input file (R)", action="store", type="string",
                  default=None)
parser.add_option("-l", "--lorentz-file", dest="lorentz_file", help="lorentz tensorfile (R)", action="store",
                  type="string", default=None)
parser.add_option("-p", "--polar-prefix", dest="polar_prefix", help="polarizability files prefix (R)", action="store",
                  type="string", default=None)
parser.add_option("-d", "--distributed-prefix", dest="distributed_prefix",
                  help="distributed polarizability files prefix", action="store", type="string", default=None)
parser.add_option("-L", "--output-file-lft", dest="output_file_lft", help="output file lft", action="store",
                  type="string", default=None)
parser.add_option("-Q", "--output-file-qlft", dest="output_file_qlft", help="output file lft", action="store",
                  type="string", default=None)
parser.add_option("-m", "--distributed-multiplicative", dest="dist_multiplicative",
                  help="old way (multiplicative) to obtain dynamic atomic polarizabilities (deprecated)",
                  action="store_true", default=False)
parser.add_option("-o", "--old-distributed-format", dest="old_dist_fmt",
                  help="old distributed polarizability format (deprecated)", action="store_true", default=False)

(options, args) = parser.parse_args()


def run():
    validate_input_file()

    inp = Input.from_file(options.input_file)
    num_molecules = inp.num_molecules

    lorentz = Lorentz.from_file(options.lorentz_file)

    properties = [PropsMol.from_file(options.polar_prefix + str(i + 1) + ".dat") for i in range(num_molecules)]

    wave_lengths, properties = equalize_properties(properties)

    bulk = calculate_bulk_properties(inp, lorentz, num_molecules, properties, wave_lengths)

    properties = bulk.calc_chis()
    qlft_properties = bulk.calc_chis(qlft=True, multiplicative=options.dist_multiplicative)

    write_lft_properties(properties)

    write_qlft_properties(qlft_properties)

    print("next step -> analyze the results")


def validate_input_file():
    if any(opt is None for opt in (options.input_file, options.lorentz_file, options.polar_prefix)):
        parser.error("Provide required input parameters; check usage with --help")


def write_qlft_properties(qlft_properties):
    if qlft_properties is not None:
        if options.output_file_qlft is None:
            options.output_file_qlft = resolve_path(options.input_file, INP_FILENAME_PATTERN, "_qlft.out")
        with open(options.output_file_qlft, 'w') as f:
            f.write(str(qlft_properties))
            print(f"{options.output_file_qlft} written with Q-LFT properties")
        print("\nFINAL MACROSCOPIC PROPERTIES (CHI1, CHI2); Q-LFT approximation")
        print(str(qlft_properties))


def write_lft_properties(properties):
    if options.output_file_lft is None:
        options.output_file_lft = resolve_path(options.input_file, INP_FILENAME_PATTERN, "_lft.out")
    with open(options.output_file_lft, 'w') as f:
        f.write(str(properties))
        print(f"{options.output_file_lft} written with LFT properties")
    print("FINAL MACROSCOPIC PROPERTIES (CHI1, CHI2); LFT approximation")
    print(properties)


def calculate_bulk_properties(inp, lorentz, num_molecules, properties, wave_lengths):
    if options.distributed_prefix is not None:
        dist_stat_polar = [
            DistributedPolar.from_file(options.distributed_prefix + str(i + 1) + ".dat", legacy=options.old_dist_fmt)
            for i in range(num_molecules)]
        bulk = BulkProperties(inp, lorentz, wave_lengths, properties, dist_stat_polar)
    else:
        bulk = BulkProperties(inp, lorentz, wave_lengths, properties)
    return bulk


if __name__ == '__main__':
    run()
