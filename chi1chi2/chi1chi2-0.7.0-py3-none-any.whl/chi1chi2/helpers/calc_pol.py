#!/usr/bin/env python

import os
import re
import sys
from pathlib import Path

import numpy as np

POLARIZABILITY_FORMAT = "{:.10f} "

NO_ROMBERG_RANGE = range(1, 8)
ROMBERG_RANGE = range(1, 14)


def main():
    if len(sys.argv) < 2:
        print(
            'use molecule name as the first parameter, optionally second for file with total molecular polarizability')
        exit(2)
    if len(sys.argv) < 3:
        total_polarizability_file = "tot.dat"
    else:
        total_polarizability_file = sys.argv[2]
    return calc_distributed_polarizabilities(sys.argv[1], total_polarizability_file)


def read_polarizabilities(mol_name, file_range, directory):
    global atom_number
    dipole_by_field = []
    for n in file_range:
        file_name = str(Path(str(directory) + "/" + mol_name + str(n) + ".sumviz").resolve())
        with open(file_name) as fh:
            file_lines = fh.readlines()
        dipoles_found = False
        for line_number, line in enumerate(file_lines):
            if line.find("Atomic Dipole Moments") == 0:
                dipoles_found = True
                break
        if not dipoles_found:
            raise AssertionError(f"No atomic dipoles found in file {file_name}")
        line_number += 9
        dipoles = []
        atom_number = 0
        for j in range(3):
            current_atom = 0
            while True:
                try:
                    component = float(file_lines[line_number].strip().split()[3])
                    if j == 0:
                        dipoles.append(np.zeros(3))
                        atom_number += 1
                    dipoles[current_atom][j] = component
                except IndexError:
                    line_number += 5
                    break
                line_number += 1
                current_atom += 1
        dipole_by_field.append(dipoles)
    return atom_number, dipole_by_field


def calc_distributed_polarizabilities(mol_name, total_polarizability_file, path='.'):
    directory = Path(path).resolve()
    file_pattern = re.compile(f'^{mol_name}([0-9]|1[0-3]).sumviz$')

    output_range = sorted(
        map(lambda fn: int(file_pattern.match(fn).group(1)),
            (filter(lambda fn: file_pattern.match(fn) is not None,
                    os.listdir(directory))))
    )

    if output_range == list(ROMBERG_RANGE):
        use_romberg = True
    elif output_range == list(NO_ROMBERG_RANGE):
        use_romberg = False
    else:
        raise AssertionError(
            "expecting files with range 1..13 for use with Romberg procedure or 1..7 to use it without Romberg (lite)")

    molecular_polarizability = np.zeros((3, 3))
    with open(total_polarizability_file) as fh:
        for line_number in range(3):
            molecular_polarizability[line_number, :] = [float(u) for u in
                                                        fh.readline().split()[:3]]

    if use_romberg:
        fields = [.003, .006]
        atom_number, dipole_by_field = read_polarizabilities(mol_name, ROMBERG_RANGE, directory)

        alpha_x1 = [np.zeros((3, 3)) for i in range(atom_number)]
        alpha_x2 = [np.zeros((3, 3)) for i in range(atom_number)]
        alphas = [np.zeros((3, 3)) for i in range(atom_number)]
        for n in range(atom_number):
            alpha_x1[n][0, 0] = -(dipole_by_field[1][n][0] - dipole_by_field[4][n][0]) / 2. / fields[0]
            alpha_x1[n][1, 1] = -(dipole_by_field[2][n][1] - dipole_by_field[5][n][1]) / 2. / fields[0]
            alpha_x1[n][2, 2] = -(dipole_by_field[3][n][2] - dipole_by_field[6][n][2]) / 2. / fields[0]
            alpha_x1[n][0, 1] = -(dipole_by_field[2][n][0] - dipole_by_field[5][n][0]) / 2. / fields[0]
            alpha_x1[n][1, 0] = -(dipole_by_field[1][n][1] - dipole_by_field[4][n][1]) / 2. / fields[0]
            alpha_x1[n][0, 2] = -(dipole_by_field[3][n][0] - dipole_by_field[6][n][0]) / 2. / fields[0]
            alpha_x1[n][2, 0] = -(dipole_by_field[1][n][2] - dipole_by_field[4][n][2]) / 2. / fields[0]
            alpha_x1[n][1, 2] = -(dipole_by_field[3][n][1] - dipole_by_field[6][n][1]) / 2. / fields[0]
            alpha_x1[n][2, 1] = -(dipole_by_field[2][n][2] - dipole_by_field[5][n][2]) / 2. / fields[0]
            alpha_x2[n][0, 0] = -(dipole_by_field[7][n][0] - dipole_by_field[10][n][0]) / 2. / fields[1]
            alpha_x2[n][1, 1] = -(dipole_by_field[8][n][1] - dipole_by_field[11][n][1]) / 2. / fields[1]
            alpha_x2[n][2, 2] = -(dipole_by_field[9][n][2] - dipole_by_field[12][n][2]) / 2. / fields[1]
            alpha_x2[n][0, 1] = -(dipole_by_field[8][n][0] - dipole_by_field[11][n][0]) / 2. / fields[1]
            alpha_x2[n][1, 0] = -(dipole_by_field[7][n][1] - dipole_by_field[10][n][1]) / 2. / fields[1]
            alpha_x2[n][0, 2] = -(dipole_by_field[9][n][0] - dipole_by_field[12][n][0]) / 2. / fields[1]
            alpha_x2[n][2, 0] = -(dipole_by_field[7][n][2] - dipole_by_field[10][n][2]) / 2. / fields[1]
            alpha_x2[n][1, 2] = -(dipole_by_field[9][n][1] - dipole_by_field[12][n][1]) / 2. / fields[1]
            alpha_x2[n][2, 1] = -(dipole_by_field[8][n][2] - dipole_by_field[11][n][2]) / 2. / fields[1]
            alphas[n] = (4. * alpha_x1[n] - alpha_x2[n]) / 3.
    else:
        field = .003
        atom_number, dipole_by_field = read_polarizabilities(mol_name, NO_ROMBERG_RANGE, directory)
        alphas = [np.zeros((3, 3)) for i in range(atom_number)]
        for n in range(atom_number):
            alphas[n][0, 0] = -(dipole_by_field[1][n][0] - dipole_by_field[4][n][0]) / 2. / field
            alphas[n][1, 1] = -(dipole_by_field[2][n][1] - dipole_by_field[5][n][1]) / 2. / field
            alphas[n][2, 2] = -(dipole_by_field[3][n][2] - dipole_by_field[6][n][2]) / 2. / field
            alphas[n][0, 1] = -(dipole_by_field[2][n][0] - dipole_by_field[5][n][0]) / 2. / field
            alphas[n][1, 0] = -(dipole_by_field[1][n][1] - dipole_by_field[4][n][1]) / 2. / field
            alphas[n][0, 2] = -(dipole_by_field[3][n][0] - dipole_by_field[6][n][0]) / 2. / field
            alphas[n][2, 0] = -(dipole_by_field[1][n][2] - dipole_by_field[4][n][2]) / 2. / field
            alphas[n][1, 2] = -(dipole_by_field[3][n][1] - dipole_by_field[6][n][1]) / 2. / field
            alphas[n][2, 1] = -(dipole_by_field[2][n][2] - dipole_by_field[5][n][2]) / 2. / field

    atomic_polarizabilities_lines = ""
    for n in range(atom_number):
        for ii in ((0, 0), (1, 1), (2, 2)):
            atomic_polarizabilities_lines += POLARIZABILITY_FORMAT.format(alphas[n][ii])
        for ij in (((0, 1), (1, 0)), ((0, 2), (2, 0)), ((1, 2), (2, 1))):
            atomic_polarizabilities_lines += POLARIZABILITY_FORMAT.format((alphas[n][ij[0]] + alphas[n][ij[1]]) / 2)
        atomic_polarizabilities_lines += "\n"
    with open('pol_dist.dat', 'w') as fh:
        fh.write(atomic_polarizabilities_lines)

    summed_molecular_polarizability = sum(atomic_pol for atomic_pol in alphas)
    difference = molecular_polarizability - summed_molecular_polarizability
    print("molecular polarizability:\n", molecular_polarizability)
    print("summed molecular polarizability:\n", summed_molecular_polarizability)
    print("difference:\n", difference)
    print("norm of difference:\n", np.linalg.norm(difference))

    return alphas


if __name__ == '__main__':
    main()
