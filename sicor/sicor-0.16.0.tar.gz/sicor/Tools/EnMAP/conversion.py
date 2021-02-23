#!/usr/bin/env python
# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains conversion tools.

# Copyright (C) 2018  Niklas Bohn (GFZ, <nbohn@gfz-potsdam.de>),
# German Research Centre for Geosciences (GFZ, <https://www.gfz-potsdam.de>)

# This software was developed within the context of the EnMAP project supported by the DLR Space Administration with
# funds of the German Federal Ministry of Economic Affairs and Energy (on the basis of a decision by the German
# Bundestag: 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.


import numpy as np


def generate_filter(wvl_m, wvl, wl_resol):
    """Generate norm array for wavelength resampling.

    :param wvl_m:    start wavelength grid
    :param wvl:      final wavelength grid
    :param wl_resol: resolution of final wavelength grid
    :return:         resampling norm
    """
    num_wvl_m = len(wvl_m)
    num_wvl = len(wvl)

    s_norm_m = np.zeros((num_wvl_m, num_wvl))
    exp_max = 2.
    exp_min = 2.
    exp_arr = exp_max + (exp_min - exp_max) * np.arange(0, 2100, 1) / (num_wvl - 1)
    c_arr = (1 / (2 ** exp_arr * np.log(2))) ** (1 / exp_arr)
    for bd in range(num_wvl):
        li1 = np.logical_and(wvl_m >= (wvl[bd] - 2. * wl_resol[bd]), wvl_m <= (wvl[bd] + 2. * wl_resol[bd]))
        li1 = np.where(li1)
        cnt = len(li1)
        if cnt > 0:
            tmp = np.abs(wvl[bd] - wvl_m[li1]) / (wl_resol[bd] * c_arr[bd])
            s = np.exp(-(tmp ** exp_arr[bd]))
            s_norm_m[li1, bd] = s / np.sum(s)

    return s_norm_m


def table_to_array(k_wi, a, b, col_wvl, col_k):
    """Convert refractive index table entries to numpy array.

    :param k_wi:    variable
    :param a:       start line
    :param b:       end line
    :param col_wvl: wavelength column in pandas table
    :param col_k:   k column in pandas table
    :return:        arrays of wavelengths and imaginary parts of refractive index
    """
    wvl_ = []
    k_ = []
    for ii in range(a, b):
        wvl = k_wi.at[ii, col_wvl]
        k = k_wi.at[ii, col_k]
        wvl_.append(wvl)
        k_.append(k)
    wvl_arr = np.asarray(wvl_)
    k_arr = np.asarray(k_)

    return wvl_arr, k_arr
