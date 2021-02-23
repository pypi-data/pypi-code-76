#!/usr/bin/env python
# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains some tools for the estimation of the a priori state vector needed for optimal estimation.

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
import dill
from tqdm import tqdm

from sicor.Tools.EnMAP.LUT import read_lut_enmap_formatted, interpol_lut_c, get_data_file
from sicor.Tools.EnMAP.conversion import generate_filter
from sicor.Tools.EnMAP.metadata import varsol


def wv_band_ratio(data, fn_table, vza, sza, dem, aot, raa, intp_wvl, intp_fwhm, jday, month, idx, disable=False):
    """Band ratio water vapor retrieval.

    :param data:      image dataset
    :param fn_table:  path to radiative transfer LUT
    :param vza:       viewing zenitg angle
    :param sza:       sun zenith angle
    :param dem:       digital elevation model, same shape as data
    :param aot:       aerosol optical thicknessw
    :param raa:       relative azimuth angle
    :param intp_wvl:  instrument wavelengths
    :param intp_fwhm: instrument fwhm
    :param jday:      acquisition day
    :param month:     acquisition month
    :param idx:       indices of instrument channels, which should be used for retrieval
                      (should be approx. 870, 900 and 940 nm)
    :param disable:   if True, progressbar during retrieval is disabled; default: False
    :return:          water vapor image
    """
    cnt_land = len(np.ndarray.flatten(data[:, :, idx[1]]))
    num_bd = 2

    toa_sub = np.zeros((cnt_land, num_bd))
    toa_sub[:, 0] = np.ndarray.flatten(data[:, :, idx[1]])
    toa_sub[:, 1] = np.ndarray.flatten(data[:, :, idx[2]])
    cnt_land = len(toa_sub[:, 0])

    luts, axes_x, axes_y, wvl, lut1, lut2, xnodes, nm_nodes, ndim, x_cell = read_lut_enmap_formatted(file_lut=fn_table)

    wvl_lut = wvl
    s_norm = generate_filter(wvl_m=wvl_lut, wvl=intp_wvl, wl_resol=intp_fwhm)

    lut2_shape = np.array(lut2.shape)
    lut2_shape[6] = len(intp_wvl)
    lut2_res = np.zeros(lut2_shape)
    lut1_res = lut1[:, :, :, :, :, :, :, 0] @ s_norm
    for ii in range(lut2.shape[-1]):
        lut2_res[:, :, :, :, :, :, :, ii] = lut2[:, :, :, :, :, :, :, ii] @ s_norm

    dsol = varsol(jday, month)
    dn2rad = dsol * dsol * 0.1
    fac = 1 / dn2rad

    hsfs = [np.min(dem), np.max(dem)]
    cwvs = list(axes_x[1][4])
    rhos = [0.02, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    l_toa_lut = np.zeros((len(hsfs), len(cwvs), len(rhos), len(intp_wvl)))

    for ii, hsf in enumerate(hsfs):
        for jj, cwv in enumerate(cwvs):

            vtest = np.asarray([vza, sza, hsf, aot, raa, cwv])
            f_int = interpol_lut_c(lut1_res, lut2_res, xnodes, nm_nodes, ndim, x_cell, vtest, intp_wvl)

            f_int_l0 = f_int[0, :] * 1.e+3
            f_int_edir = f_int[1, :] * 1.e+3
            f_int_edif = f_int[2, :] * 1.e+3
            f_int_ss = f_int[3, :]

            f_int_ee = f_int_edir * np.cos(np.deg2rad(sza)) + f_int_edif

            for kk, rho in enumerate(rhos):
                l_toa = (f_int_l0 + f_int_ee * rho / np.pi / (1 - f_int_ss * rho)) * fac
                l_toa_lut[ii, jj, kk, :] = l_toa

    path_sol = get_data_file(module_name="sicor", file_basename="solar_irradiances_400_2500_1.dill")
    with open(path_sol, "rb") as fl:
        solar_lut = dill.load(fl)
    solar_res = solar_lut @ s_norm

    rfl_1_img = data[:, :, idx[0]] / solar_res[idx[0]]
    rfl_2_img = data[:, :, idx[1]] / solar_res[idx[1]]
    rfl_3_img = rfl_1_img + (rfl_2_img - rfl_1_img) * (intp_wvl[idx[2]] - intp_wvl[idx[0]]) / (
        intp_wvl[idx[1]] - intp_wvl[idx[0]])
    if np.min(rfl_3_img) <= 0:
        for ii in range(rfl_3_img.shape[0]):
            for jj in range(rfl_3_img.shape[1]):
                if rfl_3_img[ii, jj] <= 0:
                    rfl_3_img[ii, jj] = 0.001

    rfl_sl_img = rfl_2_img / rfl_3_img
    rfl_sl_gr = [np.min(rfl_sl_img[rfl_sl_img > 0.0]) * 0.9, np.max(rfl_sl_img) * 1.1]

    dim_sl = len(rfl_sl_gr)

    alog_rat_wv_lut = np.zeros((len(hsfs), len(cwvs), len(rhos), dim_sl))
    rat_wv_lut = l_toa_lut[:, :, :, idx[2]] / l_toa_lut[:, :, :, idx[1]]
    alog_rat_wv_lut[:, :, :, 0] = np.log(rat_wv_lut * rfl_sl_gr[0])
    alog_rat_wv_lut[:, :, :, 1] = np.log(rat_wv_lut * rfl_sl_gr[1])

    cf_arr = np.zeros((3, len(hsfs), len(rhos), dim_sl))
    for ii in range(len(hsfs)):
        for jj in range(len(rhos)):
            for kk in range(dim_sl):
                cf_arr[:, ii, jj, kk] = np.polyfit(x=alog_rat_wv_lut[ii, :, jj, kk], y=cwvs, deg=2)

    alog_rat_wv_img = np.log(toa_sub[:, 1] / toa_sub[:, 0] * np.ndarray.flatten(rfl_sl_img))

    if hsfs[1] != hsfs[0]:
        dem_fac = (dem - hsfs[0]) / (hsfs[1] - hsfs[0])
        dem_fac = np.ndarray.flatten(dem_fac)
    else:
        dem_fac = np.zeros(cnt_land)

    s0 = solar_res[idx[1]]
    ll_cal = np.pi * np.ndarray.flatten(data[:, :, idx[1]])[:] / (s0 * np.cos(np.deg2rad(sza)))
    wv_arr = np.empty(cnt_land)
    wv_arr[:] = np.nan

    for ind in tqdm(range(0, cnt_land), disable=disable):
        dem_fac_pix = dem_fac[ind]

        if ll_cal[ind] <= rhos[0]:
            ll_cal[ind] = rhos[0] + 0.01 * rhos[0]
        ll_cal_low = ll_cal[ind] >= rhos
        ll_cal_high = ll_cal[ind] <= rhos
        idx_low = np.where(ll_cal_low)
        idx_high = np.where(ll_cal_high)

        rfl_fac = (ll_cal[ind] - rhos[idx_low[0][-1]]) / (rhos[idx_high[0][0]] - rhos[idx_low[0][-1]])
        rfl_fac_pix = rfl_fac

        rfl_sl = np.ndarray.flatten(rfl_sl_img)[ind]
        rfl_sl_pix = (rfl_sl - rfl_sl_gr[0]) / (rfl_sl_gr[1] - rfl_sl_gr[0])

        cf_int = (1 - dem_fac_pix) * (1 - rfl_fac_pix) * (1 - rfl_sl_pix) * cf_arr[:, 0, idx_low[0][-1], 0] + (
                1 - dem_fac_pix) * (1 - rfl_fac_pix) * rfl_sl_pix * cf_arr[:, 0, idx_low[0][-1], 1] + (
                         1 - dem_fac_pix) * rfl_fac_pix * (1 - rfl_sl_pix) * cf_arr[:, 0, idx_high[0][0], 0] + (
                         1 - dem_fac_pix) * rfl_fac_pix * rfl_sl_pix * cf_arr[:, 0, idx_high[0][0], 1] + dem_fac_pix * (
                         1 - rfl_fac_pix) * (1 - rfl_sl_pix) * cf_arr[:, 1, idx_low[0][-1], 0] + dem_fac_pix * (
                         1 - rfl_fac_pix) * rfl_sl_pix * cf_arr[:, 1, idx_low[0][-1], 1] + dem_fac_pix * rfl_fac_pix * (
                         1 - rfl_sl_pix) * cf_arr[:, 1, idx_high[0][0],
                                           0] + dem_fac_pix * rfl_fac_pix * rfl_sl_pix * cf_arr[:, 1, idx_high[0][0], 1]

        wv = cf_int[2] + alog_rat_wv_img[ind] * cf_int[1] + alog_rat_wv_img[ind] * alog_rat_wv_img[ind] * cf_int[0]
        wv_arr[ind] = wv

    wv_arr_img = np.reshape(wv_arr, (data.shape[:2]))

    return wv_arr_img
