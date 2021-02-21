#!/usr/bin/env python
from optparse import OptionParser

import numpy as np
from numpy.linalg import norm

from chi1chi2.core.property_reader import PropsBulk

usage = """
%prog [options]
(experimental feature!)
module for further analysis of the calculations results in the direction of phase matching
Given a spherical angle defining the vector of wave propagation (r) in the ab'c* reference frame:
- theta defined as the r's projection on the ab' plane with reference to a
- phi defined as the angle  between r and c*
and the base wavelength (lambda):
the effective refractive indices (from Fresnel equations, c.f. 1.7.3 of International Tables for Crystallography,
A. Authier) are calculated (for lambda and lambda/2) which further enable calculation of type I and type II phase
matching effective d values

required input:
- analysis output file
- base wavelength in nm
- list of theta, phi pairs separated by semicolon, i.e.: '0.0,0.0;0.0,90.0;45.0,-45.0' (parentheses obligatory!)
"""
parser = OptionParser(usage=usage)

parser.add_option("-i", "--input-file", dest="input_file", help="input file (R)", action="store", type="string",
                  default=None)
parser.add_option("-l", "--wave-length", dest="wave_length", help="basic wave length", action="store", type="string",
                  default=None)
parser.add_option("-a", "--angles", dest="angles", help="angles list", action="store", type="string", default=None)

(options, args) = parser.parse_args()


def run():
    _validate_input_file()

    all_properties = PropsBulk.from_file(options.input_file)

    static_eps = _get_properties_for_wave_length(all_properties, "static").polar_w
    _, reference_rotation = static_eps.refr_ind_rot_mat()

    properties = _get_properties_for_wave_length(all_properties, options.wave_length)

    eps_w = properties.polar_w.tensor + np.identity(3)
    eps_2w = properties.polar_2w.tensor + np.identity(3)

    n_w, rot_w = properties.polar_w.refr_ind_rot_mat(reference_rotation)
    n_2w, rot_2w = properties.polar_2w.refr_ind_rot_mat(reference_rotation)

    eps_w_diag = np.dot(rot_w.T, np.dot(eps_w, rot_w))
    eps_2w_diag = np.dot(rot_2w.T, np.dot(eps_2w, rot_2w))

    chi2_diag = properties.hyper_w.transform(rot_w).tensor

    theta_deg = "theta [deg]"
    phi_deg = "phi [deg]"
    npw = "n+ @w"
    nmw = "n- @w"
    nm2w = "n- @2w"
    phase_mismatch_i = "phase mismatch I"
    d_eff_i = "d_eff I [pm/V]"
    phase_mismatch_ii = "phase mismatch II"
    d_eff_ii = "d_eff II [pm/V]"
    print(", ".join((
        theta_deg,
        phi_deg,
        npw,
        nmw,
        nm2w,
        phase_mismatch_i,
        d_eff_i,
        phase_mismatch_ii,
        d_eff_ii,
    )))

    for th, ph in _parse_angles():
        k = np.array([
            np.sin(th) * np.cos(ph),
            np.sin(th) * np.sin(ph),
            np.cos(th)
        ])

        n_p_w, n_m_w = _calc_refractive_indices(k, n_w)
        _, n_m_2w = _calc_refractive_indices(k, n_2w)

        k_p_w = _calc_polarization_vector(eps_w_diag, k, n_p_w)
        k_m_w = _calc_polarization_vector(eps_w_diag, k, n_m_w)
        k_m_2w = _calc_polarization_vector(eps_2w_diag, k, n_m_2w)

        kk_p_w = norm(k * k_p_w)
        kk_m_w = norm(k * k_m_w)
        kk_m_2w = norm(k * k_m_2w)

        print(f"{np.rad2deg(th):{len(theta_deg)}.2f}, {np.rad2deg(ph):{len(phi_deg)}.2f}, "
              f"{n_p_w:{len(npw)}.3f}, {n_m_w:{len(nmw)}.3f}, {n_m_2w:{len(nm2w)}.3f}, "
              f"{abs(kk_m_2w - kk_p_w):{len(phase_mismatch_i)}.4f}, "
              f"{_calc_d_eff(chi2_diag, k_m_2w, k_p_w, k_p_w):{len(d_eff_i)}.2f}, "
              f"{abs(2 * kk_m_2w - kk_p_w - kk_m_w):{len(phase_mismatch_ii)}.4f}, "
              f"{_calc_d_eff_ii(chi2_diag, k_m_2w, k_m_w, k_p_w) :{len(d_eff_ii)}.2f}")


def _calc_d_eff_ii(chi2_diag, k_m_2w, k_m_w, k_p_w):
    return (_calc_d_eff(chi2_diag, k_m_2w, k_p_w, k_m_w) + _calc_d_eff(chi2_diag, k_m_2w, k_m_w, k_p_w)) / 2


def _calc_d_eff(chi2_diag, k1, k2, k3):
    d_eff = 0.
    for i in range(3):
        for j in range(3):
            for k in range(3):
                d_eff += .5 * chi2_diag[i, j, k] * k1[i] * k2[j] * k3[k]
    return d_eff


def _calc_polarization_vector(eps_w_diag, k, n_p_w):
    return _null_space(np.outer(k, k) + eps_w_diag / n_p_w ** 2 - np.identity(3)).reshape(3)


def _null_space(A, eps=1e-10):
    u, s, vh = np.linalg.svd(A)
    space = np.compress(s < eps, vh, axis=0)
    return space.T


def _calc_refractive_indices(k, n):
    nm2 = [n_i ** -2 for n_i in n]
    B = -k[0] ** 2. * (nm2[1] + nm2[2]) - k[1] ** 2. * (nm2[0] + nm2[2]) - k[2] ** 2. * (nm2[0] + nm2[1])
    C = k[0] ** 2. * nm2[1] * nm2[2] + k[1] ** 2. * nm2[0] * nm2[2] + k[2] ** 2. * nm2[0] * nm2[1]
    n_p = np.sqrt(2 / (-B - np.sqrt(B ** 2. - 4. * C)))
    n_m = np.sqrt(2 / (-B + np.sqrt(B ** 2. - 4. * C)))

    return n_p, n_m


def _parse_angles():
    if not options.angles:
        return tuple()

    return (tuple(np.deg2rad(float(e)) for e in element.split(",")[:2]) for element in options.angles.split(";"))


def _get_properties_for_wave_length(properties, wave_length):
    wave_length = "{0:.1f}".format(float(options.wave_length))
    if not options.wave_length or wave_length not in properties.props_dict:
        parser.error(
            f"cannot proceed without correct wavelength, available wavelengths: {properties.props_dict.keys()}")

    if wave_length == "static":
        return properties.props_dict.get("static")

    return properties.props_dict.get(wave_length)


def _validate_input_file():
    if not options.input_file:
        parser.error("Provide required input parameters; check usage with --help")


if __name__ == '__main__':
    run()
