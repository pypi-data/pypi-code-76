#!/usr/bin/env python
# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains LUT tools.

# Copyright (C) 2018  Niklas Bohn (GFZ, <nbohn@gfz-potsdam.de>),
# Maximilian Brell (GFZ, <maximilian.brell@gfz-potsdam.de>),
# Daniel Scheffler (GFZ, <daniel.scheffler@gfz-potsdam.de>)
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


from pkg_resources import resource_filename, Requirement, DistributionNotFound
import os
from os.path import isfile, join, dirname
import inspect
import sys
import numpy as np
from numba import jit
import urllib.request


def get_data_file(module_name, file_basename):
    """Load data file.

    :param module_name:   name of python module where data file is located
    :param file_basename: name of data file
    :return:              path to data file
    """
    try:
        fn = resource_filename(Requirement.parse(module_name), os.path.join("data", file_basename))
        if isfile(fn) is False:
            raise FileNotFoundError(fn, os.listdir(os.path.dirname(fn)))

    except (FileNotFoundError, DistributionNotFound):
        # noinspection PyProtectedMember
        fn = join(dirname(inspect.getfile(sys._getframe(1))), "data", file_basename)
        if isfile(fn) is False:
            raise FileNotFoundError((module_name, file_basename, fn))

    if isfile(fn) is False:
        raise FileNotFoundError(fn, file_basename)
    else:
        return fn


def download_LUT(path_LUT_default):
    """
    Download LUT file from remote GIT repository.

    :param path_LUT_default: directory where to store the LUT file
    :return:                 directory of downloaded LUT file
    """
    fname = "https://git.gfz-potsdam.de/EnMAP/sicor/-/raw/master/sicor/AC/data/EnMAP_LUT_MOD5_formatted_1nm"
    urllib.request.urlretrieve(fname, path_LUT_default)
    if os.path.isfile(path_LUT_default):
        fn_table = path_LUT_default
    else:
        raise FileNotFoundError("Download of LUT file failed. Please download it manually from "
                                "https://git.gfz-potsdam.de/EnMAP/sicor and store it at /sicor/AC/data/ directory. "
                                "Otherwise, the AC will not work.")

    return fn_table


def read_lut_enmap_formatted(file_lut):
    """Read MODTRAN LUT.

    :param file_lut: path to LUT
    :return:         LUT of atmospheric functions, x and y axes grid points, LUT wavelengths
    """

    ndim = 6

    with open(file_lut, mode='rb') as fd:

        fd.seek(0, 0)
        cnt = np.fromfile(fd, dtype='int16', count=1)
        dim_wvl = cnt[0]
        fd.seek(2, 0)
        wvl = np.fromfile(fd, dtype='f4', count=cnt[0])

        cnt0 = cnt[0]*4+2
        fd.seek(cnt0, 0)
        cnt = np.fromfile(fd, dtype='int16', count=1)
        dim_vza = cnt[0]
        fd.seek(cnt0+2, 0)
        vza_arr = np.fromfile(fd, dtype='f4', count=cnt[0])

        cnt0 = cnt0+cnt[0]*4+2
        fd.seek(cnt0, 0)
        cnt = np.fromfile(fd, dtype='int16', count=1)
        dim_sza = cnt[0]
        fd.seek(cnt0+2, 0)
        sza_arr = np.fromfile(fd, dtype='f4', count=cnt[0])

        cnt0 = cnt0+cnt[0]*4+2
        fd.seek(cnt0, 0)
        cnt = np.fromfile(fd, dtype='int16', count=1)
        dim_hsf = cnt[0]
        fd.seek(cnt0+2, 0)
        hsf_arr = np.fromfile(fd, dtype='f4', count=cnt[0])

        cnt0 = cnt0+cnt[0]*4+2
        fd.seek(cnt0, 0)
        cnt = np.fromfile(fd, dtype='int16', count=1)
        dim_aot = cnt[0]
        fd.seek(cnt0+2, 0)
        aot_arr = np.fromfile(fd, dtype='f4', count=cnt[0])

        cnt0 = cnt0+6*4+2
        fd.seek(cnt0, 0)
        cnt = np.fromfile(fd, dtype='int16', count=1)
        dim_phi = cnt[0]
        fd.seek(cnt0+2, 0)
        phi_arr = np.fromfile(fd, dtype='f4', count=cnt[0])

        cnt0 = cnt0+cnt[0]*4+2
        fd.seek(cnt0, 0)
        cnt = np.fromfile(fd, dtype='int16', count=1)
        dim_cwv = cnt[0]
        fd.seek(cnt0+2, 0)
        cwv_arr = np.fromfile(fd, dtype='f4', count=cnt[0])

        cnt0 = cnt0+cnt[0]*4+2
        fd.seek(cnt0, 0)
        npar1 = np.fromfile(fd, dtype='int16', count=1)[0]

        cnt0 = cnt0+2
        fd.seek(cnt0, 0)
        npar2 = np.fromfile(fd, dtype='int16', count=1)[0]

        cnt_lut1 = 10584000
        lut1 = np.fromfile(fd, dtype='f4', count=cnt_lut1).reshape(
            (dim_vza, dim_sza, dim_hsf, dim_aot, dim_phi, 1, dim_wvl, npar1))

        cnt_lut2 = 42336000
        lut2 = np.fromfile(fd, dtype='f4', count=cnt_lut2).reshape(
            (dim_vza, dim_sza, dim_hsf, dim_aot, 1, dim_cwv, dim_wvl, npar2))

    dim_arr1 = np.array([dim_vza, dim_sza, dim_phi, dim_hsf, dim_aot, 1])
    dim_arr2 = np.array([dim_vza, dim_sza, 1, dim_hsf, dim_aot, dim_cwv])

    dim_max = max(dim_arr1)
    xnodes1 = np.zeros((dim_max, ndim))
    xnodes1[0:dim_arr1[0], 0] = vza_arr
    xnodes1[0:dim_arr1[1], 1] = sza_arr
    xnodes1[0:dim_arr1[2], 2] = phi_arr
    xnodes1[0:dim_arr1[3], 3] = hsf_arr
    xnodes1[0:dim_arr1[4], 4] = aot_arr
    xnodes1[0:dim_arr1[5], 5] = 1

    dim_max = max(dim_arr2)
    xnodes2 = np.zeros((dim_max, ndim))
    xnodes2[0:dim_arr2[0], 0] = vza_arr
    xnodes2[0:dim_arr2[1], 1] = sza_arr
    xnodes2[0:dim_arr2[2], 2] = 1
    xnodes2[0:dim_arr2[3], 3] = hsf_arr
    xnodes2[0:dim_arr2[4], 4] = aot_arr
    xnodes2[0:dim_arr2[5], 5] = cwv_arr

    dim_arr = np.zeros(ndim)
    dim_arr[0:4] = dim_arr1[[0, 1, 3, 4]]
    dim_arr[4] = dim_arr1[2]
    dim_arr[5] = dim_arr2[5]
    xnodes = np.zeros((np.max(dim_arr1), ndim))
    xnodes[:, 0:4] = xnodes1[:, [0, 1, 3, 4]]
    xnodes[:, 4] = xnodes1[:, 2]
    xnodes[:, 5] = xnodes2[:, 5]
    nm_nodes = 2**ndim

    x_cell = np.zeros((nm_nodes, ndim))
    cont = 0
    xx = [0, 1]

    for i in xx:
        for j in xx:
            for k in xx:
                for ii in xx:
                    for jj in xx:
                        for kk in xx:
                            x_cell[cont, :] = [i, j, k, ii, jj, kk]
                            cont = cont + 1

    elip = 0.0001
    dim_arr = np.asarray(dim_arr, dtype=int)
    vza_arr[0] = vza_arr[0] + elip
    vza_arr[dim_arr[0] - 1] = vza_arr[dim_arr[0] - 1] - elip
    sza_arr[0] = sza_arr[0] + elip
    sza_arr[dim_arr[1] - 1] = sza_arr[dim_arr[1] - 1] - elip
    hsf_arr[0] = hsf_arr[0] + elip
    hsf_arr[dim_arr[2] - 1] = hsf_arr[dim_arr[2] - 1] - elip
    aot_arr[0] = aot_arr[0] + elip
    aot_arr[dim_arr[3] - 1] = aot_arr[dim_arr[3] - 1] - elip
    phi_arr[0] = phi_arr[0] + elip
    phi_arr[dim_arr[4] - 1] = phi_arr[dim_arr[4] - 1] - elip
    cwv_arr[0] = cwv_arr[0] + elip
    cwv_arr[dim_arr[5] - 1] = cwv_arr[dim_arr[5] - 1] - elip

    l0_lut = lut1[:, :, :, :, :, :, :, 0]
    edir_lut = lut2[:, :, :, :, :, :, :, 0]
    edif_lut = lut2[:, :, :, :, :, :, :, 1]
    sab_lut = lut2[:, :, :, :, :, :, :, 2]

    l0_lut = np.squeeze(l0_lut, axis=5)
    edir_lut = np.squeeze(edir_lut, axis=4)
    edif_lut = np.squeeze(edif_lut, axis=4)
    sab_lut = np.squeeze(sab_lut, axis=4)

    luts = [l0_lut, edir_lut, edif_lut, sab_lut]

    axes_x_l0 = [vza_arr, sza_arr, hsf_arr, aot_arr, phi_arr]
    axes_x_e_s = [vza_arr, sza_arr, hsf_arr, aot_arr, cwv_arr]

    axes_x = [axes_x_l0, axes_x_e_s]

    axes_y_l0 = [np.arange(ii) for ii in np.asarray(l0_lut.shape[:-1])]
    axes_y_e_s = [np.arange(ii) for ii in np.asarray(edir_lut.shape[:-1])]

    axes_y = [axes_y_l0, axes_y_e_s]

    return luts, axes_x, axes_y, wvl, lut1, lut2, xnodes, nm_nodes, ndim, x_cell


@jit(nopython=True)
def interpol_lut_c(lut1, lut2, xnodes, nm_nodes, ndim, x_cell, vtest, intp_wvl):
    """Multidimensional LUT interpolation.

    :param lut1:     Path radiance LUT
    :param lut2:     Solar irradiance, spherical albedo and transmittance LUT
    :param xnodes:   Gridpoints for each LUT dimension
    :param nm_nodes: Overall number of LUT gridpoints (2**ndim)
    :param ndim:     Dimension of LUT
    :param x_cell:   Interpolation grid (nm_nodes x n_dim)
    :param vtest:    Atmospheric state vector (interpolation point)
    :param intp_wvl: wavelengths for which interpolation should be conducted
    :return:         Path radiance, solar irradiance, spherical albedo and transmittance interpolated at vtest
    """

    lim = np.zeros((2, ndim), np.int8)

    # TODO compute that on the full cube
    for ii in range(ndim):
        if vtest[ii] >= xnodes[:, ii].max():
            vtest[ii] = 0.99 * xnodes[-1, ii]

        wh = np.where(vtest[ii] < xnodes[:, ii])[0]
        lim[0, ii] = wh[0] - 1
        lim[1, ii] = wh[0]

    lut_cell = np.zeros((5, nm_nodes, len(intp_wvl)))

    cont = 0
    for i in range(2):
        iv = lim[i, 0]

        for j in range(2):
            jv = lim[j, 1]

            for k in range(2):
                kv = lim[k, 2]

                for ii in range(2):
                    iiv = lim[ii, 3]

                    for jj in range(2):
                        jjv = lim[jj, 4]

                        for kk in range(2):
                            kkv = lim[kk, 5]

                            lut_cell[0, cont, :] = \
                                lut1[iv, jv, kv, iiv, jjv, 0, :]

                            for ind in range(1, 5):
                                lut_cell[ind, cont, :] = \
                                    lut2[iv, jv, kv, iiv, 0, kkv, :, ind - 1]

                            cont += 1

    for i in range(ndim):
        vtest[i] = (vtest[i] - xnodes[lim[0, i], i]) / (xnodes[lim[1, i], i] - xnodes[lim[0, i], i])

    # weights = np.abs(np.prod(vtest - x_cell[::-1, :], axis=1)).reshape(1, nm_nodes, 1)  # unsupported by numba
    diffs = vtest - x_cell[::-1, :]
    weights = np.abs(np.array([np.prod(diffs[i]) for i in range(nm_nodes)])).reshape(1, nm_nodes, 1)
    f_int = np.sum(weights * lut_cell, axis=1)

    return f_int


def download_LUT(path_LUT_default):
    """
    Download LUT file from remote GIT repository.

    :param path_LUT_default: directory where to store the LUT file
    :return:                 directory of downloaded LUT file
    """
    fname = "https://git.gfz-potsdam.de/EnMAP/sicor/-/raw/master/sicor/AC/data/EnMAP_LUT_MOD5_formatted_1nm"
    urllib.request.urlretrieve(fname, path_LUT_default)
    if os.path.isfile(path_LUT_default):
        fn_table = path_LUT_default
    else:
        raise FileNotFoundError('Download of LUT file failed. Please download it manually from'
                                'https://git.gfz-potsdam.de/EnMAP/sicor and store it at /sicor/AC/data/'
                                'directory. Otherwise, the AC will not work.')

    return fn_table
