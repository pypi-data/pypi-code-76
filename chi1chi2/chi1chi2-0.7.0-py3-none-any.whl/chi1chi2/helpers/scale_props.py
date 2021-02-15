#!/usr/bin/env python3
import logging as log
import os
import sys
from collections import deque

import numpy as np
from numpy.linalg import norm

log.basicConfig(format="%(asctime)s %(message)s", datefmt="%d-%m-%Y %H:%M:%S")

ADDITIVE_SCHEME = "additive"
ADDITIVE_PLUS_SCHEME = "additive+"
HYBRID_SCHEME = "hybrid"

ALPHA = "alpha"
BETA = "beta"
STATIC = "static"
ETIQ_FORMAT = "{:.1f}"
LINE_SEPARATOR = os.linesep
HEAD_FORMAT = "{} {}" + LINE_SEPARATOR
FLOAT_FORMAT = "{: .5f}"


def beta_vec(beta):
    beta_vec = np.zeros(3)
    for i in range(3):
        for j in range(3):
            beta_vec[i] += (beta[i, j, j] + beta[j, i, j] + beta[j, j, i]) / 5.
    return beta_vec


def _wavelength_sorter(u):
    if u == "static":
        return float("inf")
    else:
        return float(u)


def _halve_etiq(et):
    if et == STATIC:
        return et
    return ETIQ_FORMAT.format(float(et) / 2)


def _read_props(file_name):
    pol_dict = {}
    bet_dict = {}
    with open(file_name) as fh:
        lines = fh.readlines()
    dip_line = lines[0]
    line_number = 1
    while line_number < len(lines):
        if lines[line_number].startswith(ALPHA):
            wavelength = lines[line_number].split()[1]
            alpha = []
            line_number += 1
            for i in range(3):
                alpha.append([float(u) for u in lines[line_number].split()[:3]])
                line_number += 1
            pol_dict[wavelength] = np.array(alpha).reshape((3, 3))
        if lines[line_number].startswith(BETA):
            wavelength = lines[line_number].split()[1]
            beta = []
            line_number += 1
            for i in range(3):
                beta.append([])
                for j in range(3):
                    beta[-1].append([float(u) for u in lines[line_number].split()[:3]])
                    line_number += 1
            bet_dict[wavelength] = np.array(beta).reshape((3, 3, 3))
        line_number += 1
    return dip_line, pol_dict, bet_dict


def additive_pol(pol_stat_b3lyp, pol_dyn_b3lyp, pol_stat_mp2):
    return pol_stat_mp2 + (pol_dyn_b3lyp - pol_stat_b3lyp)


def additive_plus_pol(pol_stat_b3lyp, pol_dyn_b3lyp, pol_stat_mp2):
    b1, B1 = diagonalize(pol_stat_b3lyp)
    b2, B2 = diagonalize(pol_dyn_b3lyp)
    delta = B2 - B1
    B = np.dot(b1.T, b2)

    b3, M1 = diagonalize(pol_stat_mp2)
    M1 += delta

    return _rotate_matrix(M1, np.dot(b3, B).T)


def _max_out_of_diagonal(tensor: np.ndarray):
    return max(abs(tensor[ij]) for ij in ((0, 1), (0, 2), (1, 2)))


def _get_min_ij(tensor: np.ndarray, tolerance=1e-5, large_number=1000):
    return min(((0, 1), (2, 0), (1, 2)),
               key=lambda ij: abs(tensor[ij]) if abs(tensor[ij]) > tolerance else large_number)


def _is_not_symmetric_3x3(tensor):
    for i, j in ((0, 1), (0, 2), (1, 2)):
        if not simeq(tensor[i, j], tensor[j, i]):
            return True
    return False


def simeq(a, b, tolerance=1e-5):
    return abs(a - b) < tolerance


def diagonalize(tensor: np.ndarray, tolerance=1e-5):
    if _is_not_symmetric_3x3(tensor):
        raise ValueError("non-symmetric 2nd rank tensor provided")
    rotation = np.identity(3)

    while _max_out_of_diagonal(tensor) > tolerance:
        i, j = _get_min_ij(tensor)
        rot = _get_rotation_ij(tensor, i, j)
        rotation = np.dot(rotation, rot)
        tensor = np.dot(rot.T, np.dot(tensor, rot))

    return rotation, tensor


def _get_rotation_ij(tensor, i, j, tolerance=1e-5):
    if abs((tensor[i, i] - tensor[j, j])) < tolerance:
        th = np.pi / 180.
    else:
        th = .5 * np.arctan(2 * tensor[i, j] / (tensor[i, i] - tensor[j, j]))
    rot = np.identity(3)
    rot[i, i] = np.cos(th)
    rot[j, j] = np.cos(th)
    rot[i, j] = -np.sin(th)
    rot[j, i] = np.sin(th)
    return rot


def additive_bet(pol_stat_b3lyp, pol_stat_mp2, bet_stat_b3lyp, bet_dyn_b3lyp, bet_stat_mp2):
    return bet_stat_mp2 + (bet_dyn_b3lyp - bet_stat_b3lyp)


def _sim_transf(matr1, matr2):
    _, tr1 = diagonalize(matr1)
    matr2_pr = _rotate_matrix(matr2, tr1)
    _, tr2 = diagonalize(matr2_pr)
    return tr1, np.dot(tr1, tr2)


def _rotate_matrix(matrix, rotation):
    return np.dot(rotation.T, np.dot(matrix, rotation))


def hybrid_pol(pol_stat_b3lyp, pol_dyn_b3lyp, pol_stat_mp2):
    """
    1) diagonalize both static and dynamic polarizability in the static level
    2) multiplicative scheme for diagonal scaling
    3) additive scheme for out-of-diagonal scaling
    :param pol_stat_b3lyp: static reference polarizability
    :param pol_dyn_b3lyp: dynamic reference polarizability
    :param pol_stat_mp2: static target polarizability
    :return: dynamic target polarizability
    """
    tr_b, tr_m = _sim_transf(pol_stat_b3lyp, pol_stat_mp2)
    pol_stat_b3lyp_pr = _rotate_matrix(pol_stat_b3lyp, tr_b)
    pol_dyn_b3lyp_pr = _rotate_matrix(pol_dyn_b3lyp, tr_b)
    pol_stat_mp2_pr = _rotate_matrix(pol_stat_mp2, tr_m)

    pol_dyn_mp2_pr = pol_stat_mp2_pr.copy()

    for i in range(3):
        pol_dyn_mp2_pr[i, i] *= pol_dyn_b3lyp_pr[i, i] / pol_stat_b3lyp_pr[i, i]
    for ij in ((0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)):
        pol_dyn_mp2_pr[ij] += (pol_dyn_b3lyp_pr[ij] - pol_stat_b3lyp_pr[ij])

    return _rotate_matrix(pol_dyn_mp2_pr, tr_m.T)


def _rotate_hyper(hyper, rotation):
    rotated = np.zeros((3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for u in range(3):
                    for v in range(3):
                        for w in range(3):
                            rotated[i, j, k] += hyper[u, v, w] * rotation[u, i] * rotation[v, j] * rotation[w, k]
    return rotated


def hybrid_bet(pol_stat_b3lyp, pol_stat_mp2, bet_stat_b3lyp, bet_dyn_b3lyp, bet_stat_mp2):
    """
    1) transform to the eigenaxes of the static polarizabilities
    2) scale multiplicatively if 1/3 < abs(beta_dyn / beta_stat) < 3
    3) scale additively otherwise
    :param pol_stat_b3lyp: static reference polarizability
    :param pol_stat_mp2: static target polarizability
    :param bet_stat_b3lyp: static reference hyperpolarizability
    :param bet_dyn_b3lyp: dynamic reference hyperpolarizability
    :param bet_stat_mp2: static target hyperpolarizability
    :return: dynamic target hyperpolarizability
    """
    tr_b, tr_m = _sim_transf(pol_stat_b3lyp, pol_stat_mp2)
    bet_stat_b3lyp_pr = _rotate_hyper(bet_stat_b3lyp, tr_b)
    bet_dyn_b3lyp_pr = _rotate_hyper(bet_dyn_b3lyp, tr_b)
    bet_stat_mp2_pr = _rotate_hyper(bet_stat_mp2, tr_m)

    bet_dyn_mp2_pr = bet_stat_mp2_pr.copy()

    for i in range(3):
        for j in range(3):
            for k in range(3):
                fact = bet_dyn_b3lyp_pr[i, j, k] / bet_stat_mp2_pr[i, j, k]
                if 1 / 3 < abs(fact) < 3:
                    bet_dyn_mp2_pr[i, j, k] *= fact
                else:
                    bet_dyn_mp2_pr[i, j, k] += (bet_dyn_b3lyp_pr[i, j, k] - bet_stat_b3lyp_pr[i, j, k])

    return _rotate_hyper(bet_dyn_mp2_pr, tr_m.T)


def _scale(pol_dict_b3lyp, bet_dict_b3lyp, pol_dict_mp2, bet_dict_mp2, scaler_pol=additive_pol,
           scaler_bet=additive_bet):
    pol_stat_b3lyp = pol_dict_b3lyp[STATIC]
    bet_stat_b3lyp = bet_dict_b3lyp[STATIC]
    pol_stat_mp2 = pol_dict_mp2[STATIC]
    bet_stat_mp2 = bet_dict_mp2[STATIC]
    wavelengths = sorted(pol_dict_b3lyp, key=_wavelength_sorter, reverse=True)
    wavelengths.remove(STATIC)
    for wvl in wavelengths:
        pol_dict_mp2[wvl] = scaler_pol(pol_stat_b3lyp, pol_dict_b3lyp[wvl], pol_stat_mp2)
        if wvl in bet_dict_b3lyp.keys():
            bet_dict_mp2[wvl] = scaler_bet(pol_dict_b3lyp[wvl], pol_dict_mp2[wvl], bet_stat_b3lyp, bet_dict_b3lyp[wvl],
                                           bet_stat_mp2)
            log.warning("norm of vectorial beta for lambda: %s nm, b3lyp %.3f, mp2 %.3f",
                        wvl,
                        norm(beta_vec(bet_dict_b3lyp[wvl])),
                        norm(beta_vec(bet_dict_mp2[wvl])))
    return pol_dict_mp2, bet_dict_mp2


def _get_props_per_wavelength(wavelength, pol_dict, bet_dict):
    lines = deque()
    lines.append(HEAD_FORMAT.format(ALPHA, wavelength))
    for i in range(3):
        lines.append(" ".join(FLOAT_FORMAT.format(u) for u in pol_dict[wavelength][i, :]) + LINE_SEPARATOR)
    lines.append(LINE_SEPARATOR)
    half_wavelen = _halve_etiq(wavelength)
    if half_wavelen != wavelength:
        lines.append(HEAD_FORMAT.format(ALPHA, half_wavelen))
        for i in range(3):
            lines.append(" ".join(FLOAT_FORMAT.format(u) for u in pol_dict[half_wavelen][i, :]) + LINE_SEPARATOR)
        lines.append(LINE_SEPARATOR)
    lines.append(HEAD_FORMAT.format(BETA, wavelength))
    for i in range(3):
        for j in range(3):
            lines.append(" ".join(FLOAT_FORMAT.format(u) for u in bet_dict[wavelength][i, j, :]) + LINE_SEPARATOR)
    lines.append(LINE_SEPARATOR)
    return lines


def _write_props(dip_line, pol_dict, bet_dict, file_out):
    if pol_dict is None or bet_dict is None:
        raise ValueError("cannot write 'None' properties")
    lines = deque()
    lines.append(dip_line)
    for wvl in sorted(bet_dict.keys(), key=_wavelength_sorter, reverse=True):
        lines.extend(_get_props_per_wavelength(wvl, pol_dict, bet_dict))
    with open(file_out, 'w') as fh:
        fh.write("".join(lines))


def read_props_and_scale(file_b3lyp, file_mp2, scheme=ADDITIVE_SCHEME, file_out=None):
    _, pol_dict_b3lyp, bet_dict_b3lyp = _read_props(file_b3lyp)
    dip_line, pol_dict_mp2, bet_dict_mp2 = _read_props(file_mp2)
    pol_dict_new_mp2, bet_dict_new_mp2 = None, None
    if scheme == HYBRID_SCHEME:
        log.warning("Using hybrid scaling scheme.")
        pol_dict_new_mp2, bet_dict_new_mp2 = _scale(pol_dict_b3lyp, bet_dict_b3lyp, pol_dict_mp2, bet_dict_mp2)
    if scheme == ADDITIVE_SCHEME:
        log.warning("Using additive scaling scheme.")
        pol_dict_new_mp2, bet_dict_new_mp2 = _scale(pol_dict_b3lyp, bet_dict_b3lyp, pol_dict_mp2, bet_dict_mp2,
                                                    additive_pol, additive_bet)
    if scheme == ADDITIVE_PLUS_SCHEME:
        log.warning("Using additive+ (enhanced for polarizability and additive for hyperpolarizability scaling scheme.")
        pol_dict_new_mp2, bet_dict_new_mp2 = _scale(pol_dict_b3lyp, bet_dict_b3lyp, pol_dict_mp2, bet_dict_mp2,
                                                    additive_plus_pol, additive_bet)
    if file_out is None:
        file_out = file_mp2
    _write_props(dip_line, pol_dict_new_mp2, bet_dict_new_mp2, file_out)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        log.error("provide two files as input parameters: for b3lyp and mp2 properties, respectively")
        log.error("the script updates the second file by default")
        log.error("third parameter for scheme: 'hybrid', 'additive', 'additive+' (default)")
        exit(2)
    f_b3lyp, f_mp2 = sys.argv[1:3]
    sch = ADDITIVE_PLUS_SCHEME
    if len(sys.argv) == 4:
        sch = sys.argv[3]
    read_props_and_scale(f_b3lyp, f_mp2, scheme=sch)
