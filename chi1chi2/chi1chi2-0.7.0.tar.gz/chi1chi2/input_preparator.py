#!/usr/bin/env python
import os
from optparse import OptionParser
from pathlib import Path

from chi1chi2.input.input_preparator import Input
from chi1chi2.utils.constants import XYZ_EXTENSION

usage = """
%prog [options]
this script prepares Lorentz tensor and charges for property calculations

required input:
- input file

default output:
- Lorentz tensor input (for the fortran program 'lorentz'; folder lorentz/)
- charge generation input (for the fortran program 'charge_generator'; folder charge/)
- individual molecule geometries (folder geom/)
- unit cell content geometry (folder geom/)
"""
parser = OptionParser(usage=usage)

parser.add_option("-i", "--input-file", dest="input_file", help="input file", action="store", type="string",
                  default=None)
parser.add_option("-r", "--radius", dest="radius_cutoff", help="input file", action="store", type="float",
                  default="100.")

(options, args) = parser.parse_args()

UNIT_CELL_FILE = "uc.xyz"
LORENTZ_DIR = "lorentz"
CHARGE_DIR = "charge"


def run():
    validate_input_file()

    cwd = Path.cwd()
    inp = Input.from_file(options.input_file)

    prepare_lorentz_tensor_input(cwd, inp)

    prepare_charges_input(cwd, inp)

    store_individual_molecules_geometries(cwd, inp)

    store_unit_cell_geometry(cwd, inp)


def validate_input_file():
    if options.input_file is None:
        parser.error("No input file given, provide input file")


def store_unit_cell_geometry(cwd, inp):
    with open(cwd / UNIT_CELL_FILE, 'w') as f:
        f.write(str(inp.get_fra_uc_molecules(inp.flags).to_xyz_molecule()))
        print(f"{f.name} xyz for generated unit cell written")


def store_individual_molecules_geometries(cwd, inp):
    for i, fra_molecule in enumerate(inp.fra_molecules):
        with open(cwd / ("o" + str(i + 1) + XYZ_EXTENSION), 'w') as f:
            f.write(str(fra_molecule.to_xyz_molecule()))
            print(f"{f.name} xyz for molecule {i + 1} written")
            print(f"charge of molecule {i + 1}: {fra_molecule.get_charge():.2f}")


def prepare_charges_input(cwd, inp):
    charge_dir = cwd / CHARGE_DIR
    if not os.path.exists(charge_dir):
        os.mkdir(str(charge_dir))
    for i, chg_inp in enumerate(inp.for_charge_generation(r_cut=float(options.radius_cutoff))):
        charge_inp_location = charge_dir / ("chg" + str(i + 1) + ".inp")
        with open(str(charge_inp_location), 'w') as f:
            f.write(chg_inp)
            print(f"{charge_inp_location.relative_to(cwd)} file for charge generation calculations written")


def prepare_lorentz_tensor_input(cwd, inp):
    if not os.path.exists(LORENTZ_DIR):
        os.mkdir(str(cwd / LORENTZ_DIR))
    lorentz_inp_location = cwd / LORENTZ_DIR / "lorentz.inp"
    with open(str(lorentz_inp_location), 'w') as f:
        f.write(inp.for_lorentz())
        print(f"{lorentz_inp_location.relative_to(cwd)} file for Lorentz tensor calculations written")


if __name__ == '__main__':
    run()
