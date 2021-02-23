#!/usr/bin/env python
# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains the radiative transfer forward operator including a three phases of water retrieval.

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


import logging
import numpy as np
import pandas as pd
import dill
from multiprocessing import Pool
from itertools import product
from time import time
import warnings
from contextlib import closing
from tqdm import tqdm
import os
import pkgutil
import platform

from py_tools_ds.processing.progress_mon import ProgressBar

from sicor.Tools.EnMAP.metadata import varsol
from sicor.Tools.EnMAP.LUT import get_data_file, read_lut_enmap_formatted, interpol_lut_c, download_LUT
from sicor.Tools.EnMAP.conversion import generate_filter, table_to_array
from sicor.Tools.EnMAP.optimal_estimation import invert_function
from sicor.Tools.EnMAP.multiprocessing import SharedNdarray, initializer, mp_progress_bar
from sicor.Tools.EnMAP.a_priori import wv_band_ratio
from sicor.Tools.EnMAP.segmentation import SLIC_segmentation


# Generic
class FoGen(object):
    """Forward operator for input TOA radiance data formatted according to options file
       (i.e., not in standard EnMAP L1B format)."""

    def __init__(self, data, options, dem=None, logger=None):
        """Instance of forward operator object.

        :param data:    ndarray containing data
        :param options: dictionary with EnMAP specific options
        :param logger:  None or logging instance
        :param dem:     digital elevation model to be provided in advance; default: None
        """
        self.logger = logger or logging.getLogger(__name__)
        self.cpu = options["retrieval"]["cpu"]
        self.disable_progressbars = options["retrieval"]["disable_progressbars"]
        self.instrument = options["sensor"]["name"]
        self.data = data

        if self.instrument == "EnMAP":
            self.data_fg = data[:, :, :88]

        # get observation metadata
        self.logger.info("Getting observation metadata...")
        self.jday = options["metadata"]["jday"]
        self.month = options["metadata"]["month"]
        self.dsol = varsol(jday=self.jday, month=self.month)
        self.dn2rad = self.dsol * self.dsol * 0.1
        self.fac = 1 / self.dn2rad

        self.sza = np.full(self.data.shape[:2], options["metadata"]["sza"])
        self.vza = np.full(self.data.shape[:2], options["metadata"]["vza"])

        if dem is None:
            self.hsf = np.full(self.data.shape[:2], options["metadata"]["hsf"])
        else:
            self.hsf = dem

        self.saa = np.zeros(np.full(self.data.shape[:2], options["metadata"]["saa"]).shape)

        for ii in range(self.saa.shape[0]):
            for jj in range(self.saa.shape[1]):
                if np.full(self.data.shape[:2], options["metadata"]["saa"])[ii, jj] < 0:
                    self.saa[ii, jj] = 360 + np.full(self.data.shape[:2],
                                                     options["metadata"]["saa"])[ii, jj]
                else:
                    self.saa[ii, jj] = np.full(self.data.shape[:2],
                                               options["metadata"]["saa"])[ii, jj]

        self.raa = np.abs(np.full(self.data.shape[:2],
                                  options["metadata"]["vza"]) - self.saa)

        for ii in range(self.raa.shape[0]):
            for jj in range(self.raa.shape[1]):
                if self.raa[ii, jj] > 180:
                    self.raa[ii, jj] = 360 - self.raa[ii, jj]

        # check if observation metadata values are within LUT value ranges
        self.logger.info("Checking if observation metadata values are within LUT value ranges...")
        try:
            assert np.min(self.vza) >= 0 and np.max(self.vza) <= 40
        except AssertionError:
            raise AssertionError("vza not in LUT range, must be between 0 and 40. check input value!")

        try:
            assert np.min(self.sza) >= 0 and np.max(self.sza) <= 70
        except AssertionError:
            raise AssertionError("sza not in LUT range, must be between 0 and 70. check input value!")

        try:
            assert np.min(self.hsf) >= 0 and np.max(self.hsf) <= 8
        except AssertionError:
            raise AssertionError("surface elevation not in LUT range, must be between 0 and 8. check input value!")

        try:
            assert 0.05 <= options["metadata"]["aot"] <= 0.8
        except AssertionError:
            raise AssertionError("aot not in LUT range, must be between 0.05 and 0.8. check input value!")

        self.pt = np.zeros((self.data.shape[0], self.data.shape[1], 5))
        self.pt[:, :, 0] = self.vza
        self.pt[:, :, 1] = self.sza
        self.pt[:, :, 2] = self.hsf
        self.pt[:, :, 3] = np.full(self.data.shape[:2], options["metadata"]["aot"])
        self.pt[:, :, 4] = self.raa

        self.par_opt = ["water vapor", "intercept", "slope", "liquid water", "ice"]
        self.state_dim = len(self.par_opt)

        self.prior_mean, self.use_prior_mean, self.ll, self.ul, self.prior_sigma, self.unknowns = [], [], [], [], [], []

        for key in options["retrieval"]["state_vector"].keys():
            self.prior_mean.append(options["retrieval"]["state_vector"][key]["prior_mean"])
            self.use_prior_mean.append(options["retrieval"]["state_vector"][key]["use_prior_mean"])
            self.ll.append(options["retrieval"]["state_vector"][key]["ll"])
            self.ul.append(options["retrieval"]["state_vector"][key]["ul"])
            self.prior_sigma.append(options["retrieval"]["state_vector"][key]["prior_sigma"])

        # Thompson et al. (2018) and Kou et al. (1993)
        for key in options["retrieval"]["unknowns"].keys():
            self.unknowns.append(options["retrieval"]["unknowns"][key]["sigma"])

        self.oe_gnform = options["retrieval"]["inversion"]["gnform"]
        self.oe_full = options["retrieval"]["inversion"]["full"]
        self.oe_maxiter = options["retrieval"]["inversion"]["maxiter"]
        self.oe_eps = options["retrieval"]["inversion"]["eps"]

        # wvl
        self.wvl = np.array(options["sensor"]["fit"]["wvl_center"])
        self.fwhm = np.array(options["sensor"]["fit"]["fwhm"])

        # vnir wvl
        if self.instrument == "EnMAP":
            self.wvl_vnir = self.wvl[:88]
            self.fwhm_vnir = self.fwhm[:88]

        # fit wvl
        self.fit_wvl = np.array(options["sensor"]["fit"]["idx"])
        self.wvl_sel = self.wvl[self.fit_wvl]
        self.fwhm_sel = self.fwhm[self.fit_wvl]
        self.snr_fit = np.array(options["sensor"]["fit"]["snr"])

        # get solar irradiances for absorption feature shoulders wavelengths
        self.logger.info("Getting solar irradiances for absorption feature shoulders wavelengths...")
        new_kur_fn = get_data_file(module_name="sicor", file_basename="newkur_EnMAP.dat")
        new_kur = pd.read_table(new_kur_fn, delim_whitespace=True)
        freq_0 = 10e6 / self.wvl_sel[0]
        freq_1 = 10e6 / self.wvl_sel[-1]
        solar_0 = np.zeros(1)
        solar_1 = np.zeros(1)

        for ii in range(1, new_kur.shape[0]):
            if int(freq_0) - int(new_kur.at[ii, "FREQ"]) == 0:
                solar_0 = new_kur.at[ii, "SOLAR"]
            if int(freq_1) - int(new_kur.at[ii, "FREQ"]) == 0:
                solar_1 = new_kur.at[ii, "SOLAR"]

        self.s0 = float(solar_0) * (10e6 / self.wvl_sel[0]) ** 2
        self.s1 = float(solar_1) * (10e6 / self.wvl_sel[-1]) ** 2

        # load RT LUT
        self.logger.info("Loading RT LUT...")
        if os.path.isfile(options["retrieval"]["fn_LUT"]):
            self.fn_table = options["retrieval"]["fn_LUT"]
        else:
            self.path_sicorlib = os.path.dirname(pkgutil.get_loader("sicor").path)
            if os.path.isfile(os.path.join(self.path_sicorlib, "AC", "data", "EnMAP_LUT_MOD5_formatted_1nm")):
                self.fn_table = os.path.join(self.path_sicorlib, "AC", "data", "EnMAP_LUT_MOD5_formatted_1nm")
            else:
                raise FileNotFoundError("LUT file was not found. Make sure to indicate path in options file or to "
                                        "store the LUT at /sicor/AC/data/ directory, otherwise, the AC will not work.")

        luts, axes_x, axes_y, wvl, lut1, lut2, xnodes, nm_nodes, ndim, x_cell = read_lut_enmap_formatted(
            file_lut=self.fn_table)

        self.wvl_lut = wvl

        # resample LUT to instrument wavelengths
        self.logger.info("Resampling LUT to instrument wavelengths...")

        self.s_norm_fit = generate_filter(wvl_m=self.wvl_lut, wvl=self.wvl_sel, wl_resol=self.fwhm_sel)
        self.s_norm_full = generate_filter(wvl_m=self.wvl_lut, wvl=self.wvl, wl_resol=self.fwhm)

        self.xnodes = xnodes
        self.nm_nodes = nm_nodes
        self.ndim = ndim
        self.x_cell = x_cell

        lut2_all_res_fit = np.zeros((5, 6, 4, 6, 1, 7, len(self.wvl_sel), 4))
        lut2_all_res_full = np.zeros((5, 6, 4, 6, 1, 7, len(self.wvl), 4))

        lut1_res_fit = lut1[:, :, :, :, :, :, :, 0] @ self.s_norm_fit
        lut1_res_full = lut1[:, :, :, :, :, :, :, 0] @ self.s_norm_full

        for ii in range(4):
            lut2_all_res_fit[:, :, :, :, :, :, :, ii] = lut2[:, :, :, :, :, :, :, ii] @ self.s_norm_fit
            lut2_all_res_full[:, :, :, :, :, :, :, ii] = lut2[:, :, :, :, :, :, :, ii] @ self.s_norm_full

        self.lut1_fit = lut1_res_fit
        self.lut1_full = lut1_res_full
        self.lut2_fit = lut2_all_res_fit
        self.lut2_full = lut2_all_res_full

        # calculate absorption coefficients of liquid water and ice
        self.logger.info("Calculating absorption coefficients of liquid water and ice...")
        warnings.filterwarnings("ignore")
        path_k = get_data_file(module_name="sicor", file_basename="k_liquid_water_ice.xlsx")
        k_wi = pd.read_excel(io=path_k, engine='openpyxl')
        wvl_water, k_water = table_to_array(k_wi=k_wi, a=0, b=982, col_wvl="wvl_6", col_k="T = 20°C")
        interp_kw = np.interp(x=self.wvl_sel, xp=wvl_water, fp=k_water)
        self.kw = interp_kw

        wvl_ice, k_ice = table_to_array(k_wi=k_wi, a=0, b=135, col_wvl="wvl_4", col_k="T = -7°C")
        interp_ki = np.interp(x=self.wvl_sel, xp=wvl_ice, fp=k_ice)
        self.ki = interp_ki

        self.abs_co_w = 4 * np.pi * self.kw / self.wvl_sel
        self.abs_co_i = 4 * np.pi * self.ki / self.wvl_sel

        # load mean solar exoatmospheric irradiances
        self.logger.info("Calculating mean solar exoatmospheric irradiances...")
        path_sol = get_data_file(module_name="sicor", file_basename="solar_irradiances_400_2500_1.dill")

        with open(path_sol, "rb") as fl:
            solar_lut = dill.load(fl)

        self.solar_res = solar_lut @ self.s_norm_fit

    def surface_model(self, xx):
        """Nonlinear surface reflectance model using the Beer-Lambert attenuation law for the retrieval of liquid water
           and ice path lengths.

        :param xx: state vector, must be in the order [vapor, intercept, slope, liquid, ice]
        :return:   modeled surface reflectance
        """
        # modeling of surface reflectance
        attenuation = np.exp(-xx[3] * 1e7 * self.abs_co_w - xx[4] * 1e7 * self.abs_co_i)
        rho = (xx[1] + xx[2] * self.wvl_sel) * attenuation

        return rho

    def toa_rad(self, xx, pt, perturb=None):
        """Model TOA radiance for a given atmospheric state by interpolating in the LUT and applying the simplified
           solution of the RTE. Here, the atmospheric state also contains path lengths of liquid water and ice. The
           needed surface reflectance values are derived from the nonlinear Beer-Lambert surface reflectance model.

        :param xx: state vector
        :param pt: model parameter vector
        :param perturb: perturbance factor for calculating perturbed TOA radiance; default None
        :return:   modeled TOA radiance, modeled surface reflectance
        """
        # LUT interpolation
        vtest = np.asarray([pt[0], pt[1], pt[2], pt[3], pt[4], xx[0]])

        f_int = interpol_lut_c(lut1=self.lut1_fit,
                               lut2=self.lut2_fit,
                               xnodes=self.xnodes,
                               nm_nodes=self.nm_nodes,
                               ndim=self.ndim,
                               x_cell=self.x_cell,
                               vtest=vtest,
                               intp_wvl=self.wvl_sel)

        f_int_l0 = f_int[0, :] * 1.e+3
        f_int_edir = f_int[1, :] * 1.e+3
        f_int_edif = f_int[2, :] * 1.e+3
        f_int_ss = f_int[3, :]

        f_int_ee = f_int_edir * np.cos(np.deg2rad(pt[1])) + f_int_edif

        # modeling of surface reflectance
        rho = self.surface_model(xx=xx)

        # modeling of TOA radiance
        if perturb:
            f_int_toa = (f_int_l0 + f_int_ee * rho / np.pi / (1 - f_int_ss * rho * perturb)) * self.fac
        else:
            f_int_toa = (f_int_l0 + f_int_ee * rho / np.pi / (1 - f_int_ss * rho)) * self.fac

        return f_int_toa

    def surf_ref(self, dt, xx, pt, mode=None):
        """Model surface reflectance for a given atmospheric state by interpolating in the LUT and applying the
           simplified solution of the RTE. Here, the atmospheric state also contains path lengths of liquid water and
           ice.

        :param dt:   measurement vector
        :param xx:   water vapor from state vector
        :param pt:   model parameter vector
        :param mode: if vnir, interpolation is done for EnMAP vnir bands; if swir, it is done for swir bands
        :return:     modeled surface reflectance
        """
        # LUT interpolation
        vtest = np.asarray([pt[0], pt[1], pt[2], pt[3], pt[4], xx[0]])

        if mode == "full":
            f_int = interpol_lut_c(lut1=self.lut1_full,
                                   lut2=self.lut2_full,
                                   xnodes=self.xnodes,
                                   nm_nodes=self.nm_nodes,
                                   ndim=self.ndim,
                                   x_cell=self.x_cell,
                                   vtest=vtest,
                                   intp_wvl=self.wvl)
        else:
            f_int = interpol_lut_c(lut1=self.lut1_fit,
                                   lut2=self.lut2_fit,
                                   xnodes=self.xnodes,
                                   nm_nodes=self.nm_nodes,
                                   ndim=self.ndim,
                                   x_cell=self.x_cell,
                                   vtest=vtest,
                                   intp_wvl=self.wvl_sel)

        f_int_l0 = f_int[0, :] * 1.e+3 * self.fac
        f_int_edir = f_int[1, :] * 1.e+3 * self.fac
        f_int_edif = f_int[2, :] * 1.e+3 * self.fac
        f_int_ss = f_int[3, :]

        f_int_ee = f_int_edir * np.cos(np.deg2rad(pt[1])) + f_int_edif

        # modeling of surface reflectance
        xterm = np.pi * (dt - f_int_l0) / f_int_ee
        rho = xterm / (1. + f_int_ss * xterm)

        return rho

    def drdn_drtb(self, xx, pt, rdn):
        """Calculate Jacobian of radiance with respect to unknown radiative transfer model parameters.

        :param xx:  state vector
        :param pt:  model parameter vector
        :param rdn: forward modeled TOA radiance for the current state vector xx
        :return:    Jacobian of unknown radiative transfer model parameters
        """
        kb_rt = []
        eps = 1e-5
        perturb = (1.0 + eps)
        unknowns = ["skyview", "water_vapor_absorption_coefficients"]

        for unknown in unknowns:
            if unknown == "skyview":
                # perturb the sky view
                rdne = self.toa_rad(xx=xx, pt=pt, perturb=perturb)
                dx = (rdne - rdn) / eps
                kb_rt.append(dx)
            elif unknown == "water_vapor_absorption_coefficients":
                xx_perturb = xx.copy()
                xx_perturb[0] = xx[0] * perturb
                rdne = self.toa_rad(xx=xx_perturb, pt=pt)
                dx = (rdne - rdn) / eps
                kb_rt.append(dx)

        kb_rt = np.array(kb_rt).T

        return kb_rt

    def drdn_dsurfaceb(self, xx, pt, rdn):
        """Calculate Jacobian of radiance with respect to unknown surface model parameters.

        :param xx:  state vector
        :param pt:  model parameter vector
        :param rdn: forward modeled TOA radiance for the current state vector xx
        :return:    Jacobian of unknown surface model parameters
        """
        kb_surface = []
        eps = 1e-5
        perturb = (1.0 * eps)
        unknowns = ["liquid_water_absorption_coefficients", "ice_absorption_coefficients"]

        for ii, unknown in enumerate(unknowns):
            xx_perturb = xx.copy()
            xx_perturb[ii+1] = xx[ii+1] * perturb
            rdne = self.toa_rad(xx=xx_perturb, pt=pt)
            dx = (rdne - rdn) / eps
            kb_surface.append(dx)

        kb_surface = np.array(kb_surface).T

        return kb_surface

    def calc_kb(self, xx, pt, num_bd, sb):
        """Derivative of measurement with respect to unmodeled & unretrieved unknown variables, e.g. S_b. This is the
        concatenation of Jacobians with respect to parameters of the surface and the radiative transfer model.

        :param xx:     state vector
        :param pt:     model parameter vector
        :param num_bd: number of instrument bands
        :param sb:     unknown model parameter error covariance matrix
        :return:       Jacobian of unknown model parameters
        """
        kb = np.zeros((num_bd, sb.shape[0]), dtype=float)

        # calculate the radiance at the current state vector
        rdn = self.toa_rad(xx=xx, pt=pt)
        drdn_drtb = self.drdn_drtb(xx=xx, pt=pt, rdn=rdn)
        drdn_dsurfaceb = self.drdn_dsurfaceb(xx=xx, pt=pt, rdn=rdn)
        kb[:, :2] = drdn_drtb
        kb[:, 2:] = drdn_dsurfaceb

        return kb

    def calc_se(self, xx, dt, pt, sb, num_bd, snr, unknowns):
        """Calculate the total uncertainty of the observation, including both the instrument noise and the uncertainty
           due to unmodeled variables. This is the S_epsilon matrix of Rodgers et al.

        :param xx:       state vector
        :param dt:       measurement vector
        :param pt:       model parameter vector
        :param sb:       unknown model parameter error covariance matrix
        :param num_bd:   number of instrument bands
        :param snr:      signal-to-noise ratio for each instrument band
        :param unknowns: if True, uncertainties due to unknown forward model parameters are added to S_epsilon;
                         default: False
        :return:         measurement error covariance matrix
        """
        if self.instrument == "AVIRIS":
            nedl = abs(snr[:, 0] * np.sqrt(snr[:, 1] + dt) + snr[:, 2])
            sy = np.identity(num_bd) * nedl
        else:
            sy = np.identity(num_bd) * ((dt / snr) ** 2)

        if not unknowns:
            return sy
        else:
            kb = self.calc_kb(xx=xx, pt=pt, num_bd=num_bd, sb=sb)
            se = sy + kb.dot(sb).dot(kb.T)

            return se


# EnMAP
class Fo(object):
    """
    Forward operator for input TOA radiance data in standard EnMAP L1B format.
    """
    def __init__(self, enmap_l1b, options, logger=None):
        """
        Instance of forward operator object.

        :param enmap_l1b: EnMAP Level-1B object
        :param options:   dictionary with EnMAP specific options
        :param logger:    None or logging instance
        """
        self.logger = logger or logging.getLogger(__name__)
        self.cpu = options["retrieval"]["cpu"]
        self.disable_progressbars = options["retrieval"]["disable_progressbars"]
        self.instrument = options["sensor"]["name"]
        self.data_vnir = enmap_l1b.vnir.data
        self.data_swir = enmap_l1b.swir.data
        self.resamp_alg = options["sensor"]["resamp_alg"]
        self.land_only = options["retrieval"]["land_only"]

        if self.land_only:
            logger.info("SICOR is applied to land pixels only. This may result in edge effects, e.g., at coastlines...")
            self.water_mask_vnir = enmap_l1b.vnir.mask_landwater[:, :]
            self.water_mask_swir = enmap_l1b.transform_vnir_to_swir_raster(array_vnirsensorgeo=self.water_mask_vnir,
                                                                           resamp_alg=self.resamp_alg,
                                                                           respect_keystone=False)
            self.data_vnir[self.water_mask_vnir != 1] = 0.0
            self.data_swir[self.water_mask_swir != 1] = 0.0
        else:
            logger.info("SICOR is applied to land AND water pixels.")

        # transform vnir array data to swir sensor geometry to enable first guess retrievals for liquid water and ice
        logger.info("Transforming VNIR data to SWIR sensor geometry to enable first guess retrievals for liquid water "
                    "and ice...")
        self.data_vnir_trans = enmap_l1b.transform_vnir_to_swir_raster(array_vnirsensorgeo=self.data_vnir,
                                                                       resamp_alg=self.resamp_alg,
                                                                       respect_keystone=False)

        # get observation metadata
        self.logger.info("Getting observation metadata...")
        self.jday = enmap_l1b.meta.observation_datetime.day
        self.month = enmap_l1b.meta.observation_datetime.month
        self.dsol = varsol(jday=self.jday, month=self.month)
        self.dn2rad = self.dsol * self.dsol * 0.1
        self.fac = 1 / self.dn2rad

        self.sza = np.full(enmap_l1b.swir.data.shape[:2], enmap_l1b.meta.geom_sun_zenith)
        self.vza = np.full(enmap_l1b.swir.data.shape[:2], enmap_l1b.meta.geom_view_zenith)
        self.raa = np.zeros(enmap_l1b.swir.data.shape[:2])

        if enmap_l1b.meta.geom_sun_azimuth < 0:
            self.saa = 360 + enmap_l1b.meta.geom_sun_azimuth
        else:
            self.saa = enmap_l1b.meta.geom_sun_azimuth

        self.geom_rel_azimuth = np.abs(enmap_l1b.meta.geom_view_zenith - self.saa)
        if self.geom_rel_azimuth > 180:
            self.raa[:, :] = 360 - self.geom_rel_azimuth
        else:
            self.raa[:, :] = self.geom_rel_azimuth

        # get dem for each detector, if no dem is provided by the L1B object the algorithm falls back to an average
        # elevation given in the EnPT config file
        self.hsf = {}

        for detector_name in enmap_l1b.detector_attrNames:
            detector = getattr(enmap_l1b, detector_name)
            if detector.dem.size == 0:
                self.hsf[detector_name] = np.full(detector.data.shape[:2], (enmap_l1b.cfg.average_elevation / 1000))
            else:
                self.hsf[detector_name] = detector.dem[:, :] / 1000

        # check if observation metadata values are within LUT value ranges
        self.logger.info("Checking if observation metadata values are within LUT value ranges...")
        try:
            assert np.min(self.vza) >= 0 and np.max(self.vza) <= 40
        except AssertionError:
            raise AssertionError("vza not in LUT range, must be between 0 and 40. check input value!")

        try:
            assert np.min(self.sza) >= 0 and np.max(self.sza) <= 70
        except AssertionError:
            raise AssertionError("sza not in LUT range, must be between 0 and 70. check input value!")

        try:
            assert np.min(self.hsf["swir"]) >= 0 and np.max(self.hsf["swir"]) <= 8
        except AssertionError:
            raise AssertionError("surface elevation not in LUT range, must be between 0 and 8. check input value!")

        try:
            assert 0.05 <= options["retrieval"]["default_aot_value"] <= 0.8
        except AssertionError:
            raise AssertionError("aot not in LUT range, must be between 0.05 and 0.8. check input value!")

        self.pt = np.zeros((self.data_swir.shape[0], self.data_swir.shape[1], 5))
        self.pt[:, :, 0] = self.vza
        self.pt[:, :, 1] = self.sza
        self.pt[:, :, 2] = self.hsf["swir"]
        self.pt[:, :, 3] = np.full(self.data_swir.shape[:2], options["retrieval"]["default_aot_value"])
        self.pt[:, :, 4] = self.raa

        self.pt_vnir = np.zeros((self.data_vnir.shape[0], self.data_vnir.shape[1], 5))
        self.pt_vnir[:, :, 0] = self.vza
        self.pt_vnir[:, :, 1] = self.sza
        self.pt_vnir[:, :, 2] = self.hsf["vnir"]
        self.pt_vnir[:, :, 3] = np.full(self.data_vnir.shape[:2], options["retrieval"]["default_aot_value"])
        self.pt_vnir[:, :, 4] = self.raa

        self.par_opt = ["water vapor", "intercept", "slope", "liquid water", "ice"]
        self.state_dim = len(self.par_opt)

        self.prior_mean, self.use_prior_mean, self.ll, self.ul, self.prior_sigma, self.unknowns = [], [], [], [], [], []

        for key in options["retrieval"]["state_vector"].keys():
            self.prior_mean.append(options["retrieval"]["state_vector"][key]["prior_mean"])
            self.use_prior_mean.append(options["retrieval"]["state_vector"][key]["use_prior_mean"])
            self.ll.append(options["retrieval"]["state_vector"][key]["ll"])
            self.ul.append(options["retrieval"]["state_vector"][key]["ul"])
            self.prior_sigma.append(options["retrieval"]["state_vector"][key]["prior_sigma"])

        # Thompson et al. (2018) and Kou et al. (1993)
        for key in options["retrieval"]["unknowns"].keys():
            self.unknowns.append(options["retrieval"]["unknowns"][key]["sigma"])

        self.oe_gnform = options["retrieval"]["inversion"]["gnform"]
        self.oe_full = options["retrieval"]["inversion"]["full"]
        self.oe_maxiter = options["retrieval"]["inversion"]["maxiter"]
        self.oe_eps = options["retrieval"]["inversion"]["eps"]

        # fit wvl
        self.fit_wvl = np.array(options["sensor"]["fit"]["idx"])
        self.wvl_sel = np.array(enmap_l1b.swir.detector_meta.wvl_center[self.fit_wvl])
        self.fwhm_sel = np.array(enmap_l1b.swir.detector_meta.fwhm[self.fit_wvl])
        self.snr_fit = np.array(options["sensor"]["fit"]["snr"])

        # vnir wvl
        self.wvl_vnir = np.array(enmap_l1b.vnir.detector_meta.wvl_center[:])
        self.fwhm_vnir = np.array(enmap_l1b.vnir.detector_meta.fwhm[:])

        # swir wvl
        self.wvl_swir = np.array(enmap_l1b.swir.detector_meta.wvl_center[:])
        self.fwhm_swir = np.array(enmap_l1b.swir.detector_meta.fwhm[:])

        # get solar irradiances for absorption feature shoulders wavelengths
        self.logger.info("Getting solar irradiances for absorption feature shoulders wavelengths...")
        new_kur_fn = get_data_file(module_name="sicor", file_basename="newkur_EnMAP.dat")
        new_kur = pd.read_csv(new_kur_fn, delim_whitespace=True)
        freq_0 = 10e6 / self.wvl_sel[0]
        freq_1 = 10e6 / self.wvl_sel[-1]
        solar_0 = np.zeros(1)
        solar_1 = np.zeros(1)

        for ii in range(1, new_kur.shape[0]):
            if int(freq_0) - int(new_kur.at[ii, "FREQ"]) == 0:
                solar_0 = new_kur.at[ii, "SOLAR"]
            if int(freq_1) - int(new_kur.at[ii, "FREQ"]) == 0:
                solar_1 = new_kur.at[ii, "SOLAR"]

        self.s0 = float(solar_0) * (10e6 / self.wvl_sel[0]) ** 2
        self.s1 = float(solar_1) * (10e6 / self.wvl_sel[-1]) ** 2

        # load RT LUT
        # check if LUT file is available
        self.logger.info("Loading RT LUT...")
        if os.path.isfile(options["retrieval"]["fn_LUT"]):
            self.fn_table = options["retrieval"]["fn_LUT"]
        else:
            self.path_sicorlib = os.path.dirname(pkgutil.get_loader("sicor").path)
            self.path_LUT_default = os.path.join(self.path_sicorlib, "AC", "data", "EnMAP_LUT_MOD5_formatted_1nm")
            if os.path.isfile(self.path_LUT_default):
                self.fn_table = self.path_LUT_default
            else:
                self.logger.info("LUT file was not found locally. Try to download it from Git repository...")
                self.fn_table = download_LUT(path_LUT_default=self.path_LUT_default)

        # check if LUT is a regular file (not only an LFS pointer)
        try:
            assert os.path.getsize(self.fn_table) > 1000
            self.logger.info("LUT file was properly downloaded and is available for AC!")
        except AssertionError:
            self.logger.info("LUT file only represents an LFS pointer. Try to download it from Git repository...")
            self.fn_table = download_LUT(path_LUT_default=self.path_LUT_default)

        luts, axes_x, axes_y, wvl, lut1, lut2, xnodes, nm_nodes, ndim, x_cell = read_lut_enmap_formatted(
            file_lut=self.fn_table)

        self.wvl_lut = wvl
        self.xnodes = xnodes
        self.nm_nodes = nm_nodes
        self.ndim = ndim
        self.x_cell = x_cell

        # resampling LUT to EnMAP wavelengths
        self.logger.info("Resampling LUT to EnMAP wavelengths...")

        self.s_norm_fit = generate_filter(wvl_m=self.wvl_lut, wvl=self.wvl_sel, wl_resol=self.fwhm_sel)
        self.s_norm_vnir = generate_filter(wvl_m=self.wvl_lut, wvl=self.wvl_vnir, wl_resol=self.fwhm_vnir)
        self.s_norm_swir = generate_filter(wvl_m=self.wvl_lut, wvl=self.wvl_swir, wl_resol=self.fwhm_swir)

        lut2_all_res_fit = np.zeros((5, 6, 4, 6, 1, 7, len(self.wvl_sel), 4))
        lut2_all_res_vnir = np.zeros((5, 6, 4, 6, 1, 7, len(self.wvl_vnir), 4))
        lut2_all_res_swir = np.zeros((5, 6, 4, 6, 1, 7, len(self.wvl_swir), 4))

        lut1_res_fit = lut1[:, :, :, :, :, :, :, 0] @ self.s_norm_fit
        lut1_res_vnir = lut1[:, :, :, :, :, :, :, 0] @ self.s_norm_vnir
        lut1_res_swir = lut1[:, :, :, :, :, :, :, 0] @ self.s_norm_swir

        for ii in range(4):
            lut2_all_res_fit[:, :, :, :, :, :, :, ii] = lut2[:, :, :, :, :, :, :, ii] @ self.s_norm_fit
            lut2_all_res_vnir[:, :, :, :, :, :, :, ii] = lut2[:, :, :, :, :, :, :, ii] @ self.s_norm_vnir
            lut2_all_res_swir[:, :, :, :, :, :, :, ii] = lut2[:, :, :, :, :, :, :, ii] @ self.s_norm_swir

        self.lut1_fit = lut1_res_fit
        self.lut1_vnir = lut1_res_vnir
        self.lut1_swir = lut1_res_swir
        self.lut2_fit = lut2_all_res_fit
        self.lut2_vnir = lut2_all_res_vnir
        self.lut2_swir = lut2_all_res_swir

        # calculate absorption coefficients of liquid water and ice
        warnings.filterwarnings("ignore")
        self.logger.info("Calculating absorption coefficients of liquid water and ice...")
        path_k = get_data_file(module_name="sicor", file_basename="k_liquid_water_ice.xlsx")
        k_wi = pd.read_excel(io=path_k, engine='openpyxl')
        wvl_water, k_water = table_to_array(k_wi=k_wi, a=0, b=982, col_wvl="wvl_6", col_k="T = 20°C")
        interp_kw = np.interp(x=self.wvl_sel, xp=wvl_water, fp=k_water)
        self.kw = interp_kw

        wvl_ice, k_ice = table_to_array(k_wi=k_wi, a=0, b=135, col_wvl="wvl_4", col_k="T = -7°C")
        interp_ki = np.interp(x=self.wvl_sel, xp=wvl_ice, fp=k_ice)
        self.ki = interp_ki

        self.abs_co_w = 4 * np.pi * self.kw / self.wvl_sel
        self.abs_co_i = 4 * np.pi * self.ki / self.wvl_sel

        # calculate mean solar exoatmospheric irradiances
        self.logger.info("Calculating mean solar exoatmospheric irradiances...")
        path_sol = get_data_file(module_name="sicor", file_basename="solar_irradiances_400_2500_1.dill")

        with open(path_sol, "rb") as fl:
            solar_lut = dill.load(fl)

        self.solar_res = solar_lut @ self.s_norm_fit

        # perform first guess water vapor retrieval based on a common band ratio using VNIR data
        warnings.filterwarnings("ignore")
        if self.use_prior_mean[0]:
            self.cwv_fg = np.full(self.data_vnir.shape[:2], self.prior_mean[0])
        else:
            logger.info("Performing first guess water vapor retrieval based on a common band ratio using VNIR data...")
            self.cwv_fg = wv_band_ratio(data=self.data_vnir,
                                        fn_table=self.fn_table,
                                        vza=self.pt[:, :, 0].mean(),
                                        sza=self.pt[:, :, 1].mean(),
                                        dem=self.hsf["vnir"].mean(),
                                        aot=self.pt[:, :, 3].mean(),
                                        raa=self.pt[:, :, 4].mean(),
                                        intp_wvl=self.wvl_vnir,
                                        intp_fwhm=self.fwhm_vnir,
                                        jday=self.jday,
                                        month=self.month,
                                        idx=[73, 76, 81],
                                        disable=self.disable_progressbars)

            self.cwv_fg[np.isnan(self.cwv_fg)] = self.prior_mean[0]

        # transform CWV first guess map to SWIR sensor geometry to enable segmentation and 3 phases of water retrieval
        logger.info("Transforming CWV first guess map to SWIR sensor geometry to enable segmentation and 3 phases of "
                    "water retrieval...")
        self.cwv_fg_trans = enmap_l1b.transform_vnir_to_swir_raster(array_vnirsensorgeo=self.cwv_fg,
                                                                    resamp_alg=self.resamp_alg,
                                                                    respect_keystone=False)

        self.cwv_fg_trans[self.cwv_fg_trans == 0.0] = self.prior_mean[0]

        # perform first guess liquid water retrieval based on the NDWI
        if self.use_prior_mean[3]:
            self.liq_fg = np.full(self.data_swir.shape[:2], self.prior_mean[3])
        else:
            logger.info("Performing first guess liquid water retrieval based on the NDWI...")
            ndwi = np.zeros(self.data_swir.shape[:2])

            for ii in tqdm(range(self.data_swir.shape[0]), disable=self.disable_progressbars):
                for jj in range(self.data_swir.shape[1]):
                    ndwi[ii, jj] = (self.data_vnir_trans[ii, jj, 72] - self.data_swir[ii, jj, 94]) / \
                                   (self.data_vnir_trans[ii, jj, 72] + self.data_swir[ii, jj, 94])

            self.liq_fg = 0.49585423 * ndwi ** 2 - 0.0396154 * ndwi - 0.0174602
            self.liq_fg[np.isnan(self.liq_fg)] = self.prior_mean[3]

        # perform first guess ice retrieval based on the NDSI
        if self.use_prior_mean[4]:
            self.ice_fg = np.full(self.data_swir.shape[:2], self.prior_mean[4])
        else:
            logger.info("Performing first guess ice retrieval based on the NDSI...")
            ndsi = np.zeros(self.data_swir.shape[:2])
            self.ice_fg = np.zeros(self.data_swir.shape[:2])

            for ii in tqdm(range(self.data_swir.shape[0]), disable=self.disable_progressbars):
                for jj in range(self.data_swir.shape[1]):
                    ndsi[ii, jj] = (self.data_vnir_trans[ii, jj, 29] - self.data_swir[ii, jj, 57]) / \
                                   (self.data_vnir_trans[ii, jj, 29] + self.data_swir[ii, jj, 57])
                    if ndsi[ii, jj] > 0.9:
                        self.ice_fg[ii, jj] = 0.25
                    else:
                        self.ice_fg[ii, jj] = 0.0

        # perform calculation of first guess for intercept and slope of absorption feature continuum
        logger.info("Calculating first guess for intercept and slope of absorption feature continuum...")
        if self.use_prior_mean[1] and self.use_prior_mean[2]:
            self.intercept_fg = np.full(self.data_swir.shape[:2], self.prior_mean[1])
            self.slope_fg = np.full(self.data_swir.shape[:2], self.prior_mean[2])
        else:
            y1 = np.zeros((self.data_swir.shape[:2]))
            y2 = np.zeros((self.data_swir.shape[:2]))
            self.intercept_fg = np.zeros((self.data_swir.shape[:2]))
            self.slope_fg = np.zeros((self.data_swir.shape[:2]))

            y1[:, :] = (np.pi * self.data_swir[:, :, self.fit_wvl][:, :, 0]) / \
                       (self.s0 * np.cos(np.deg2rad(self.pt[:, :, 1])))
            y2[:, :] = (np.pi * self.data_swir[:, :, self.fit_wvl][:, :, -1]) / \
                       (self.s1 * np.cos(np.deg2rad(self.pt[:, :, 1])))

            self.intercept_fg[:, :] = y2 - ((y1 - y2) / (self.wvl_sel[0] - self.wvl_sel[-1])) * self.wvl_sel[-1]
            self.slope_fg[:, :] = (y1 - y2) / (self.wvl_sel[0] - self.wvl_sel[-1])

        # do optional image segmentation to enhance processing speed
        self.segmentation = options["retrieval"]["segmentation"]
        self.n_pca = options["retrieval"]["n_pca"]
        self.segs = options["retrieval"]["segs"]

        if self.segmentation:
            self.logger.info("Segmenting SWIR L1B spectra to enhance processing speed...")
            self.X, self.segs, self.labels = SLIC_segmentation(data_rad_all=self.data_swir,
                                                               n_pca=self.n_pca,
                                                               segs=self.segs)

            # prepare segmented SWIR L1B data cube
            self.logger.info("Preparing segmented SWIR L1B data cube...")
            if self.land_only:
                self.labels[self.water_mask_swir != 1] = -1
                self.lbl = np.unique(self.labels)[1:]
                self.segs = len(self.lbl)

            self.rdn_subset = np.zeros((1, self.segs, self.data_swir.shape[2]))
            self.cwv_fg_subset = np.zeros((1, self.segs))
            self.liq_fg_subset = np.zeros((1, self.segs))
            self.ice_fg_subset = np.zeros((1, self.segs))
            self.intercept_fg_subset = np.zeros((1, self.segs))
            self.slope_fg_subset = np.zeros((1, self.segs))
            self.dem_subset = np.zeros((1, self.segs))
            self.pt_subset = np.zeros((1, self.segs, self.pt.shape[2]))

            if self.land_only:
                for ii, lbl in enumerate(self.lbl):
                    self.rdn_subset[:, ii, :] = self.X[self.labels.flat == lbl, :].mean(axis=0)
                    self.cwv_fg_subset[:, ii] = self.cwv_fg_trans.flatten()[self.labels.flat == lbl].mean(axis=0)
                    self.liq_fg_subset[:, ii] = self.liq_fg.flatten()[self.labels.flat == lbl].mean(axis=0)
                    self.ice_fg_subset[:, ii] = self.ice_fg.flatten()[self.labels.flat == lbl].mean(axis=0)
                    self.intercept_fg_subset[:, ii] = self.intercept_fg.flatten()[self.labels.flat == lbl].mean(axis=0)
                    self.slope_fg_subset[:, ii] = self.slope_fg.flatten()[self.labels.flat == lbl].mean(axis=0)
                    self.dem_subset[:, ii] = self.hsf["swir"].flatten()[self.labels.flat == lbl].mean(axis=0)
                    self.pt_subset[:, ii, :] = self.pt.reshape(
                        self.pt.shape[0] * self.pt.shape[1], self.pt.shape[2])[self.labels.flat == lbl, :].mean(axis=0)
            else:
                for ii in range(self.segs):
                    self.rdn_subset[:, ii, :] = self.X[self.labels.flat == ii, :].mean(axis=0)
                    self.cwv_fg_subset[:, ii] = self.cwv_fg_trans.flatten()[self.labels.flat == ii].mean(axis=0)
                    self.liq_fg_subset[:, ii] = self.liq_fg.flatten()[self.labels.flat == ii].mean(axis=0)
                    self.ice_fg_subset[:, ii] = self.ice_fg.flatten()[self.labels.flat == ii].mean(axis=0)
                    self.intercept_fg_subset[:, ii] = self.intercept_fg.flatten()[self.labels.flat == ii].mean(axis=0)
                    self.slope_fg_subset[:, ii] = self.slope_fg.flatten()[self.labels.flat == ii].mean(axis=0)
                    self.dem_subset[:, ii] = self.hsf["swir"].flatten()[self.labels.flat == ii].mean(axis=0)
                    self.pt_subset[:, ii, :] = self.pt.reshape(
                        self.pt.shape[0] * self.pt.shape[1], self.pt.shape[2])[self.labels.flat == ii, :].mean(axis=0)

    def surface_model(self, xx):
        """
        Nonlinear surface reflectance model using the Beer-Lambert attenuation law for the retrieval of liquid water
        and ice path lengths.

        :param xx: state vector, must be in the order [vapor, intercept, slope, liquid, ice]
        :return:   modeled surface reflectance
        """
        # modeling of surface reflectance
        attenuation = np.exp(-xx[3] * 1e7 * self.abs_co_w - xx[4] * 1e7 * self.abs_co_i)
        rho = (xx[1] + xx[2] * self.wvl_sel) * attenuation

        return rho

    def toa_rad(self, xx, pt, perturb=None):
        """
        Forward model for calculating TOA radiance for a given atmospheric state by interpolating in the LUT and
        applying the simplified solution of the RTE. The needed surface reflectance values are derived from the
        nonlinear Beer-Lambert surface reflectance model.

        :param xx:      state vector
        :param pt:      forward model parameter vector
        :param perturb: perturbance factor for calculating perturbed TOA radiance; default None
        :return:        modeled TOA radiance
        """
        # LUT interpolation
        vtest = np.asarray([pt[0], pt[1], pt[2], pt[3], pt[4], xx[0]])
        f_int = interpol_lut_c(lut1=self.lut1_fit,
                               lut2=self.lut2_fit,
                               xnodes=self.xnodes,
                               nm_nodes=self.nm_nodes,
                               ndim=self.ndim,
                               x_cell=self.x_cell,
                               vtest=vtest,
                               intp_wvl=self.wvl_sel)

        f_int_l0 = f_int[0, :] * 1.e+3
        f_int_edir = f_int[1, :] * 1.e+3
        f_int_edif = f_int[2, :] * 1.e+3
        f_int_ss = f_int[3, :]

        f_int_ee = f_int_edir * np.cos(np.deg2rad(pt[1])) + f_int_edif

        # modeling of surface reflectance
        rho = self.surface_model(xx=xx)

        # modeling of TOA radiance
        if perturb:
            f_int_toa = (f_int_l0 + f_int_ee * rho / np.pi / (1 - f_int_ss * rho * perturb)) * self.fac
        else:
            f_int_toa = (f_int_l0 + f_int_ee * rho / np.pi / (1 - f_int_ss * rho)) * self.fac

        return f_int_toa

    def surf_ref(self, dt, xx, pt, mode=None):
        """
        Invert the simplified solution of the RTE algebraically to calculate the surface reflectance for a given
        atmospheric state by interpolating in the multidimensional LUT.

        :param dt:   measurement vector
        :param xx:   estimated water vapor
        :param pt:   forward model parameter vector
        :param mode: if vnir, interpolation is done for EnMAP vnir bands; if swir, it is done for swir bands
        :return:     modeled surface reflectance
        """
        # LUT interpolation
        vtest = np.asarray([pt[0], pt[1], pt[2], pt[3], pt[4], xx])

        if mode == "vnir":
            f_int = interpol_lut_c(lut1=self.lut1_vnir,
                                   lut2=self.lut2_vnir,
                                   xnodes=self.xnodes,
                                   nm_nodes=self.nm_nodes,
                                   ndim=self.ndim,
                                   x_cell=self.x_cell,
                                   vtest=vtest,
                                   intp_wvl=self.wvl_vnir)
        elif mode == "swir":
            f_int = interpol_lut_c(lut1=self.lut1_swir,
                                   lut2=self.lut2_swir,
                                   xnodes=self.xnodes,
                                   nm_nodes=self.nm_nodes,
                                   ndim=self.ndim,
                                   x_cell=self.x_cell,
                                   vtest=vtest,
                                   intp_wvl=self.wvl_swir)
        else:
            f_int = interpol_lut_c(lut1=self.lut1_fit,
                                   lut2=self.lut2_fit,
                                   xnodes=self.xnodes,
                                   nm_nodes=self.nm_nodes,
                                   ndim=self.ndim,
                                   x_cell=self.x_cell,
                                   vtest=vtest,
                                   intp_wvl=self.wvl_sel)

        f_int_l0 = f_int[0, :] * 1.e+3 * self.fac
        f_int_edir = f_int[1, :] * 1.e+3 * self.fac
        f_int_edif = f_int[2, :] * 1.e+3 * self.fac
        f_int_ss = f_int[3, :]

        f_int_ee = f_int_edir * np.cos(np.deg2rad(pt[1])) + f_int_edif

        # calculation of surface reflectance
        xterm = np.pi * (dt - f_int_l0) / f_int_ee
        rho = xterm / (1. + f_int_ss * xterm)

        return rho

    def drdn_drtb(self, xx, pt, rdn):
        """
        Calculate Jacobian of radiance with respect to unknown forward model parameters.

        :param xx:  state vector
        :param pt:  forward model parameter vector
        :param rdn: modeled TOA radiance for the current state vector xx
        :return:    Jacobian of unknown forward model parameters
        """
        kb_rt = []
        eps = 1e-5
        perturb = (1.0 + eps)
        unknowns = ["skyview", "water_vapor_absorption_coefficients"]

        for unknown in unknowns:
            if unknown == "skyview":
                # perturb the sky view
                rdne = self.toa_rad(xx=xx, pt=pt, perturb=perturb)
                dx = (rdne - rdn) / eps
                kb_rt.append(dx)
            elif unknown == "water_vapor_absorption_coefficients":
                xx_perturb = xx.copy()
                xx_perturb[0] = xx[0] * perturb
                rdne = self.toa_rad(xx=xx_perturb, pt=pt)
                dx = (rdne - rdn) / eps
                kb_rt.append(dx)

        kb_rt = np.array(kb_rt).T

        return kb_rt

    def drdn_dsurfaceb(self, xx, pt, rdn):
        """
        Calculate Jacobian of radiance with respect to unknown surface model parameters.

        :param xx:  state vector
        :param pt:  forward model parameter vector
        :param rdn: modeled TOA radiance for the current state vector xx
        :return:    Jacobian of unknown surface model parameters
        """
        kb_surface = []
        eps = 1e-5
        perturb = (1.0 * eps)

        unknowns = ["liquid_water_absorption_coefficients", "ice_absorption_coefficients"]

        for ii, unknown in enumerate(unknowns):
            xx_perturb = xx.copy()
            xx_perturb[ii+3] = xx[ii+3] * perturb
            rdne = self.toa_rad(xx=xx_perturb, pt=pt)
            dx = (rdne - rdn) / eps
            kb_surface.append(dx)

        kb_surface = np.array(kb_surface).T

        return kb_surface

    def calc_kb(self, xx, pt, num_bd, sb):
        """
        Derivative of measurement with respect to unmodeled & unretrieved unknown variables, e.g. S_b. This is the
        concatenation of Jacobians with respect to parameters of the surface and the forward model.

        :param xx:     state vector
        :param pt:     forward model parameter vector
        :param num_bd: number of instrument bands
        :param sb:     unknown forward model parameter error covariance matrix
        :return:       Jacobian of unknown forward model parameters
        """
        kb = np.zeros((num_bd, sb.shape[0]), dtype=float)

        # calculate the radiance at the current state vector
        rdn = self.toa_rad(xx=xx, pt=pt)
        drdn_drtb = self.drdn_drtb(xx=xx, pt=pt, rdn=rdn)
        drdn_dsurfaceb = self.drdn_dsurfaceb(xx=xx, pt=pt, rdn=rdn)
        kb[:, :2] = drdn_drtb
        kb[:, 2:] = drdn_dsurfaceb

        return kb

    def calc_se(self, xx, dt, pt, sb, num_bd, snr, unknowns):
        """
        Calculate the total uncertainty of the observation, including both the instrument noise and the uncertainty
        due to unmodeled variables. This is the S_epsilon matrix of Rodgers et al.

        :param xx:       state vector
        :param dt:       measurement vector
        :param pt:       forward model parameter vector
        :param sb:       error covariance matrix of unknown forward model parameters
        :param num_bd:   number of instrument bands
        :param snr:      signal-to-noise ratio for each instrument band
        :param unknowns: if True, uncertainties due to unknown forward model parameters are added to S_epsilon;
                         default: False
        :return:         measurement error covariance matrix
        """
        sy = np.identity(num_bd) * ((dt / snr) ** 2)

        if not unknowns:
            return sy
        else:
            kb = self.calc_kb(xx=xx, pt=pt, num_bd=num_bd, sb=sb)
            se = sy + kb.dot(sb).dot(kb.T)

            return se


class FoFunc(object):
    """
    Forward operator function function including the nonlinear Beer-Lambert model for the surface reflectance.
    """
    def __init__(self, fo):
        """
        Instance of forward operator function.

        :param fo: Forward operator
        """
        self.fo = fo

    @staticmethod
    def __norm__(aa, bb):
        """
        Calculate L2 norm between measured and modeled values.

        :param aa: measured values
        :param bb: modeled values
        :return:   L2 norm
        """
        return (aa - bb) ** 2

    @staticmethod
    def __d_bb_norm__(aa, bb):
        """
        Calculate derivative of L2 norm between measured and modeled values.

        :param aa: measured values
        :param bb: modeled values
        :return:   derivative of L2 norm
        """
        return -2 * (aa - bb)

    def __call__(self, xx, pt, dt, model_output=False):
        """
        Call forward operator function.

        :param xx:           state vector
        :param pt:           forward model parameter vector
        :param dt:           measurement vector
        :param model_output: if True, modeled TOA radiance is returned, else, L2 norm; default: False
        :return:             if model_output=False, L2 norm is returned, else, modeled TOA radiance
        """
        ff = self.fo.toa_rad(xx=xx, pt=pt)

        if model_output is True:
            return ff
        else:
            f = (np.sum(self.__norm__(aa=dt, bb=ff)))
            n = float(len(dt))

            return f / n


# noinspection PyUnresolvedReferences
def __minimize__(fo, opt_func, unknowns=False, logger=None):
    """
    Minimize value of cost function using optimal estimation.

    :param fo:       forward operator
    :param opt_func: forward operator function
    :param unknowns: if True, forward model unknown uncertainties are calculated and propagated into Se; default: False
    :param logger:   None or logging instance
    :return:         solution state vector as well as optional measures of retrieval uncertainty
    """
    logger = logger or logging.getLogger(__name__)

    # set up multiprocessing
    warnings.filterwarnings("always")
    processes = fo.cpu

    if platform.system() == "Windows" and processes > 1:
        logger.warning('Multiprocessing is currently not available on Windows.')
    if platform.system() == "Windows" or processes == 1:
        logger.info("Singleprocessing on 1 cpu")
    else:
        logger.info("Setting up multiprocessing...")
        logger.info("Multiprocessing on %s cpu's" % processes)

    globs = dict()
    globs["__instrument__"] = fo.instrument
    globs["__land_only__"] = fo.land_only
    if fo.land_only:
        globs["__water_mask__"] = fo.water_mask_swir
    globs["__segmentation__"] = fo.segmentation

    if fo.segmentation:
        opt_pt = np.array(fo.pt_subset)
        opt_data = fo.rdn_subset[:, :, fo.fit_wvl]
        opt_cwv_fg = fo.cwv_fg_subset
        opt_liq_fg = fo.liq_fg_subset
        opt_ice_fg = fo.ice_fg_subset
        opt_intercept_fg = fo.intercept_fg_subset
        opt_slope_fg = fo.slope_fg_subset
        globs["__pt__"] = opt_pt
        globs["__data__"] = opt_data
    else:
        opt_pt = np.array(fo.pt)
        opt_data = fo.data_swir[:, :, fo.fit_wvl]
        opt_cwv_fg = fo.cwv_fg_trans
        opt_liq_fg = fo.liq_fg
        opt_ice_fg = fo.ice_fg
        opt_intercept_fg = fo.intercept_fg
        opt_slope_fg = fo.slope_fg
        globs["__pt__"] = opt_pt
        globs["__data__"] = opt_data

    # prepare arguments for optimal estimation
    logger.info("Preparing optimal estimation input...")
    globs["__state_dim__"] = fo.state_dim
    xa = np.zeros((opt_data.shape[0], opt_data.shape[1], fo.state_dim))
    ll = np.zeros(fo.state_dim)
    ul = np.zeros(fo.state_dim)
    sa_arr = np.zeros(fo.state_dim)

    for ii in range(xa.shape[0]):
        for jj in range(xa.shape[1]):
            xa[ii, jj, :] = np.array([opt_cwv_fg[ii, jj], opt_intercept_fg[ii, jj], opt_slope_fg[ii, jj],
                                      opt_liq_fg[ii, jj], opt_ice_fg[ii, jj]])

    for dd in range(fo.state_dim):
        ll[dd] = fo.ll[dd]
        ul[dd] = fo.ul[dd]
        sa_arr[dd] = fo.prior_sigma[dd]

    sa = np.diagflat(pow(sa_arr, 2))
    sb = np.diagflat(pow(np.array(fo.unknowns), 2))

    globs["__xa__"] = xa
    globs["__ll__"] = ll
    globs["__ul__"] = ul
    globs["__sa__"] = sa
    globs["__sb__"] = sb

    globs["__fit_wvl__"] = fo.fit_wvl
    globs["__forward__"] = opt_func

    globs["__cwv_model__"] = SharedNdarray(dims=list(opt_data.shape[:2]))
    globs["__liq_model__"] = SharedNdarray(dims=list(opt_data.shape[:2]))
    globs["__ice_model__"] = SharedNdarray(dims=list(opt_data.shape[:2]))
    globs["__intercept_model__"] = SharedNdarray(dims=list(opt_data.shape[:2]))
    globs["__slope_model__"] = SharedNdarray(dims=list(opt_data.shape[:2]))
    globs["__toa_model__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [fo.fit_wvl.shape[0]])

    globs["__sx__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [fo.state_dim] + [fo.state_dim])
    globs["__scem__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [fo.state_dim] + [fo.state_dim])
    globs["__srem__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [fo.state_dim] + [fo.state_dim])

    if fo.oe_full:
        globs["__jacobian__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [fo.fit_wvl.shape[0]] + [fo.state_dim])
        globs["__convergence__"] = SharedNdarray(dims=list(opt_data.shape[:2]))
        globs["__iterations__"] = SharedNdarray(dims=list(opt_data.shape[:2]))
        globs["__gain__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [fo.state_dim] + [fo.fit_wvl.shape[0]])
        globs["__averaging_kernel__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [fo.state_dim] + [fo.state_dim])
        globs["__cost_function__"] = SharedNdarray(dims=list(opt_data.shape[:2]))
        globs["__dof__"] = SharedNdarray(dims=list(opt_data.shape[:2]))
        globs["__information_content__"] = SharedNdarray(dims=list(opt_data.shape[:2]))
        globs["__retrieval_noise__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [fo.state_dim] + [fo.state_dim])
        globs["__smoothing_error__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [fo.state_dim] + [fo.state_dim])

    globs["__snr__"] = fo.snr_fit
    globs["__inv_func__"] = invert_function(fo.toa_rad)
    globs["__calc_se__"] = fo.calc_se
    globs["__unknowns__"] = unknowns
    globs["__gnform__"] = fo.oe_gnform
    globs["__full__"] = fo.oe_full
    globs["__maxiter__"] = fo.oe_maxiter
    globs["__eps__"] = fo.oe_eps

    rng = list(product(np.arange(0, opt_data.shape[0], 1), np.arange(0, opt_data.shape[1], 1)))
    mp_fun = __oe__

    # start optimization
    logger.info("Optimization...")
    t0 = time()
    # check if operating system is 'Windows'; in that case, multiprocessing is currently not working
    # TODO: enable Windows compatibility for multiprocessing

    if platform.system() == "Windows" or processes == 1:
        initializer(globals(), globs)
        [mp_fun(ii) for ii in tqdm(rng, disable=fo.disable_progressbars)]
    else:
        with closing(Pool(processes=processes, initializer=initializer, initargs=(globals(), globs,))) as pl:
            results = pl.map_async(mp_fun, rng, chunksize=1)
            if not fo.disable_progressbars:
                bar = ProgressBar(prefix='\tprogress:')
            while True:
                if not fo.disable_progressbars:
                    mp_progress_bar(iter_list=rng, results=results, bar=bar)
                if results.ready():
                    results.get()
                    break
    t1 = time()

    cwv_model = globs["__cwv_model__"].np
    liq_model = globs["__liq_model__"].np
    ice_model = globs["__ice_model__"].np
    intercept_model = globs["__intercept_model__"].np
    slope_model = globs["__slope_model__"].np
    toa_model = globs["__toa_model__"].np

    sx = globs["__sx__"].np
    scem = globs["__scem__"].np
    srem = globs["__srem__"].np

    # optional optimal estimation output
    if fo.oe_full:
        jacobian = globs["__jacobian__"].np
        convergence = globs["__convergence__"].np
        iterations = globs["__iterations__"].np
        gain = globs["__gain__"].np
        averaging_kernel = globs["__averaging_kernel__"].np
        cost_function = globs["__cost_function__"].np
        dof = globs["__dof__"].np
        information_content = globs["__information_content__"].np
        retrieval_noise = globs["__retrieval_noise__"].np
        smoothing_error = globs["__smoothing_error__"].np
    else:
        jacobian = None
        convergence = None
        iterations = None
        gain = None
        averaging_kernel = None
        cost_function = None
        dof = None
        information_content = None
        retrieval_noise = None
        smoothing_error = None

    # simple validation of optimization output
    warnings.filterwarnings("always")

    cwv_check = np.sum(cwv_model - xa[:, :, 0])
    liq_check = np.sum(liq_model - xa[:, :, 3])
    ice_check = np.sum(ice_model - xa[:, :, 4])

    if cwv_check == 0 or liq_check == 0 or ice_check == 0:
        logger.warning("Optimization failed and returned first guess values. Please check for errors in the input"
                       "data, the options file, or the processing code.")

    logger.info("Done!")
    logger.info("Runtime: %.2f" % (t1 - t0) + " s")

    res = {"cwv_model": cwv_model,
           "liq_model": liq_model,
           "ice_model": ice_model,
           "intercept_model": intercept_model,
           "slope_model": slope_model,
           "toa_model": toa_model,
           "sx": sx,
           "scem": scem,
           "srem": srem,
           "jacobian": jacobian,
           "convergence": convergence,
           "iterations": iterations,
           "gain": gain,
           "averaging_kernel": averaging_kernel,
           "cost_function": cost_function,
           "dof": dof,
           "information_content": information_content,
           "retrieval_noise": retrieval_noise,
           "smoothing_error": smoothing_error}

    return res


# noinspection PyUnresolvedReferences
def __oe__(ii):
    """
    Minimize value of cost function using optimal estimation.

    :param ii: index of input spectrum
    """
    i1, i2 = ii

    if not __segmentation__ and __land_only__ and __water_mask__[i1, i2] != 1:
        __cwv_model__[i1, i2] = np.nan
        __liq_model__[i1, i2] = np.nan
        __ice_model__[i1, i2] = np.nan
        __intercept_model__[i1, i2] = np.nan
        __slope_model__[i1, i2] = np.nan
        __toa_model__[i1, i2, :] = np.full(len(__fit_wvl__), np.nan)
        __sx__[i1, i2, :, :] = np.full((__state_dim__, __state_dim__), np.nan)
        __scem__[i1, i2, :, :] = np.full((__state_dim__, __state_dim__), np.nan)
        __srem__[i1, i2, :, :] = np.full((__state_dim__, __state_dim__), np.nan)

        if __full__:
            __jacobian__[i1, i2, :, :] = np.full((len(__fit_wvl__), __state_dim__), np.nan)
            __convergence__[i1, i2] = np.nan
            __iterations__[i1, i2] = np.nan
            __gain__[i1, i2, :, :] = np.full((__state_dim__, len(__fit_wvl__)), np.nan)
            __averaging_kernel__[i1, i2, :, :] = np.full((__state_dim__, __state_dim__), np.nan)
            __cost_function__[i1, i2] = np.nan
            __dof__[i1, i2] = np.nan
            __information_content__[i1, i2] = np.nan
            __retrieval_noise__[i1, i2, :, :] = np.full((__state_dim__, __state_dim__), np.nan)
            __smoothing_error__[i1, i2, :, :] = np.full((__state_dim__, __state_dim__), np.nan)
    else:
        se = __calc_se__(xx=__xa__[i1, i2, :],
                         dt=__data__[i1, i2, :],
                         pt=__pt__[i1, i2, :],
                         sb=__sb__,
                         num_bd=len(__fit_wvl__),
                         snr=__snr__,
                         unknowns=__unknowns__)

        res = __inv_func__(yy=__data__[i1, i2, :],
                           fparam=__pt__[i1, i2, :],
                           ll=__ll__,
                           ul=__ul__,
                           xa=__xa__[i1, i2, :],
                           sa=__sa__,
                           se=se,
                           gnform=__gnform__,
                           full=__full__,
                           maxiter=__maxiter__,
                           eps=__eps__)

        model = __forward__(xx=res[0], pt=__pt__[i1, i2, :], dt=__data__[i1, i2, :], model_output=True)

        __cwv_model__[i1, i2] = res[0][0]
        __liq_model__[i1, i2] = res[0][3]
        __ice_model__[i1, i2] = res[0][4]
        __intercept_model__[i1, i2] = res[0][1]
        __slope_model__[i1, i2] = res[0][2]
        __toa_model__[i1, i2, :] = model

        # a posteriori covariance matrix
        __sx__[i1, i2, :, :] = res[4]

        # correlation error matrix
        cem = np.zeros((__state_dim__, __state_dim__))

        for mm in range(__state_dim__):
            for nn in range(__state_dim__):
                cem[mm, nn] = __sx__[i1, i2, :, :][mm, nn] / np.sqrt(__sx__[i1, i2, :, :][mm, mm] *
                                                                     __sx__[i1, i2, :, :][nn, nn])

        __scem__[i1, i2, :, :] = cem

        # relative error matrix
        x_ = res[0]
        rem = np.zeros((__state_dim__, __state_dim__))

        warnings.filterwarnings("ignore")
        for mm in range(__state_dim__):
            for nn in range(__state_dim__):
                rem[mm, nn] = 100 * np.sqrt(__sx__[i1, i2, :, :][mm, nn] / (x_[mm] * x_[nn]))

        __srem__[i1, i2, :, :] = rem

        if __full__:
            __jacobian__[i1, i2, :, :] = res[1]
            __convergence__[i1, i2] = res[2]
            __iterations__[i1, i2] = res[3]
            __gain__[i1, i2, :, :] = res[5]
            __averaging_kernel__[i1, i2, :, :] = res[6]
            __cost_function__[i1, i2] = res[7]
            __dof__[i1, i2] = res[8]
            __information_content__[i1, i2] = res[9]
            __retrieval_noise__[i1, i2, :, :] = res[10]
            __smoothing_error__[i1, i2, :, :] = res[11]
