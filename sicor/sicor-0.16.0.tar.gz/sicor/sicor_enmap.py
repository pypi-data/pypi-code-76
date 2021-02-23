#!/usr/bin/env python
# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains the Sensor Independent Atmospheric CORrection (SICOR) AC module - EnMAP specific parts.

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
from tqdm import tqdm
import numpy as np
import warnings

from sicor.AC.RtFo_3_phases import Fo, FoFunc, __minimize__
from sicor.Tools.EnMAP.segmentation import empirical_line_solution


def make_ac_enmap(data, enmap_l1b, fo, cwv, pt, surf_res, logger=None):
    """
    Perform atmospheric correction for enmap_l1b product, based on given and retrieved parameters. Instead of returning
    an object, the function adds a 'data_l2a' attribute to each detector. This numpy array holds the retrieved surface
    reflectance map.

    :param data:      array containing measured TOA radiance of VNIR and SWIR
    :param enmap_l1b: EnMAP Level-1B object
    :param fo:        forward operator object
    :param cwv:       CWV retrieval maps for VNIR and SWIR
    :param pt:        forward model parameter vector for VNIR and SWIR
    :param surf_res:  dictionary of retrieved surface parameters ('intercept', 'slope', 'liquid water', 'ice')
    :param logger:    None or logging instance
    :return:          None
    """
    logger = logger or logging.getLogger(__name__)

    for detector_name in enmap_l1b.detector_attrNames:
        logger.info("Calculating surface reflectance for %s detector..." % detector_name)
        detector = getattr(enmap_l1b, detector_name)
        detector.data_l2a = np.full(data[detector_name].shape, np.NaN, dtype=float)

        for icol in tqdm(range(data[detector_name].shape[1]), disable=fo.disable_progressbars):
            for irow in range(data[detector_name].shape[0]):
                detector.data_l2a[irow, icol, :] = fo.surf_ref(dt=data[detector_name][irow, icol, :],
                                                               xx=cwv[detector_name][irow, icol],
                                                               pt=pt[detector_name][irow, icol, :],
                                                               mode=detector_name)
                if detector_name == "swir" and not fo.segmentation:
                    xx = np.array([cwv[detector_name][irow, icol], surf_res["intercept"][irow, icol],
                                   surf_res["slope"][irow, icol], surf_res["liquid"][irow, icol],
                                   surf_res["ice"][irow, icol]])
                    swir_feature = fo.surface_model(xx=xx)
                    detector.data_l2a[irow, icol, fo.fit_wvl] = swir_feature


def sicor_ac_enmap(enmap_l1b, options, unknowns=False, logger=None):
    """
    Atmospheric correction for EnMAP Level-1B products, including a three phases of water retrieval.

    :param enmap_l1b: EnMAP Level-1B object
    :param options:   dictionary with EnMAP specific options
    :param unknowns:  if True, uncertainties due to unknown forward model parameters are added to S_epsilon;
                      default: False
    :param logger:    None or logging instance
    :return:          surface reflectance for EnMAP VNIR and SWIR detectors as well as dictionary containing estimated
                      three phases of water maps and several retrieval uncertainty measures
    """
    logger = logger or logging.getLogger(__name__)

    logger.info("Setting up forward operator...")
    fo_enmap = Fo(enmap_l1b=enmap_l1b, options=options, logger=logger)
    fo_func_enmap = FoFunc(fo=fo_enmap)

    logger.info("Performing 3 phases of water retrieval...")
    res = __minimize__(fo=fo_enmap, opt_func=fo_func_enmap, logger=logger, unknowns=unknowns)

    if fo_enmap.segmentation:
        logger.info("Extrapolating CWV retrieval map to full SWIR data cube...")
        cwv_seg = np.zeros(fo_enmap.data_swir.shape[:2])

        if fo_enmap.land_only:
            for ii, lbl in enumerate(fo_enmap.lbl):
                cwv_seg[fo_enmap.labels == lbl] = res["cwv_model"][:, ii]
        else:
            for i in range(fo_enmap.segs):
                cwv_seg[fo_enmap.labels == i] = res["cwv_model"][:, i]

        logger.info("Transforming CWV retrieval map and segmentation labels to VNIR sensor geometry to enable VNIR "
                    "segmentation...")
        cwv_seg_trans = enmap_l1b.transform_swir_to_vnir_raster(array_swirsensorgeo=cwv_seg,
                                                                resamp_alg=fo_enmap.resamp_alg,
                                                                respect_keystone=False)
        labels_trans = enmap_l1b.transform_swir_to_vnir_raster(array_swirsensorgeo=fo_enmap.labels,
                                                               resamp_alg=fo_enmap.resamp_alg,
                                                               respect_keystone=False)

        logger.info("Segmenting VNIR data cube according to transformed SWIR segmentation labels...")
        vnir_rdn_subset = np.zeros((1, labels_trans.max(), fo_enmap.data_vnir.shape[2]))
        vnir_cwv_subset = np.zeros((1, labels_trans.max()))
        vnir_pt_subset = np.zeros((1, labels_trans.max(), fo_enmap.pt_vnir.shape[2]))

        for ii in range(labels_trans.max()):
            if np.count_nonzero(labels_trans == ii) == 0:
                pass
            else:
                vnir_rdn_subset[:, ii, :] = fo_enmap.data_vnir[labels_trans == ii].mean(axis=0)
                vnir_cwv_subset[:, ii] = cwv_seg_trans[labels_trans == ii].mean(axis=0)
                vnir_pt_subset[:, ii, :] = fo_enmap.pt_vnir[labels_trans == ii].mean(axis=0)

        data_ac = {"vnir": vnir_rdn_subset, "swir": fo_enmap.rdn_subset}
        cwv_ac = {"vnir": vnir_cwv_subset, "swir": res["cwv_model"]}
        pt_ac = {"vnir": vnir_pt_subset, "swir": fo_enmap.pt_subset}

        logger.info("Starting surface reflectance retrieval...")
        warnings.filterwarnings("ignore")
        make_ac_enmap(data=data_ac, enmap_l1b=enmap_l1b, fo=fo_enmap, cwv=cwv_ac, pt=pt_ac, surf_res=None,
                      logger=logger)

        enmap_l2a_vnir = enmap_l1b.vnir.data_l2a
        enmap_l2a_swir = enmap_l1b.swir.data_l2a

        logger.info("Applying empirical line solution to extrapolate L2A data pixelwise...")
        for detector_name in enmap_l1b.detector_attrNames:
            logger.info("Extrapolating L2A spectra for %s detector..." % detector_name)
            if detector_name == "vnir":
                x_vnir = fo_enmap.data_vnir.reshape(fo_enmap.data_vnir.shape[0] * fo_enmap.data_vnir.shape[1],
                                                    fo_enmap.data_vnir.shape[2])
                reflectance = empirical_line_solution(X=x_vnir,
                                                      rdn_subset=vnir_rdn_subset,
                                                      data_l2a_seg=enmap_l2a_vnir,
                                                      rows=fo_enmap.data_vnir.shape[0],
                                                      cols=fo_enmap.data_vnir.shape[1],
                                                      bands=fo_enmap.data_vnir.shape[2],
                                                      segs=labels_trans.max(),
                                                      labels=labels_trans,
                                                      land_only=fo_enmap.land_only,
                                                      processes=fo_enmap.cpu,
                                                      disable_progressbars=fo_enmap.disable_progressbars)
                enmap_l2a_vnir = reflectance.reshape(fo_enmap.data_vnir.shape)
            else:
                reflectance = empirical_line_solution(X=fo_enmap.X,
                                                      rdn_subset=fo_enmap.rdn_subset,
                                                      data_l2a_seg=enmap_l2a_swir,
                                                      rows=fo_enmap.data_swir.shape[0],
                                                      cols=fo_enmap.data_swir.shape[1],
                                                      bands=fo_enmap.data_swir.shape[2],
                                                      segs=fo_enmap.segs,
                                                      labels=fo_enmap.labels,
                                                      land_only=fo_enmap.land_only,
                                                      processes=fo_enmap.cpu,
                                                      disable_progressbars=fo_enmap.disable_progressbars)
                enmap_l2a_swir = reflectance.reshape(fo_enmap.data_swir.shape)

        logger.info("Extrapolating liquid water and ice maps...")
        liq_seg = np.zeros(fo_enmap.data_swir.shape[:2])
        ice_seg = np.zeros(fo_enmap.data_swir.shape[:2])

        if fo_enmap.land_only:
            for ii, lbl in enumerate(fo_enmap.lbl):
                liq_seg[fo_enmap.labels == lbl] = res["liq_model"][:, ii]
                ice_seg[fo_enmap.labels == lbl] = res["ice_model"][:, ii]
        else:
            for i in range(fo_enmap.segs):
                liq_seg[fo_enmap.labels == i] = res["liq_model"][:, i]
                ice_seg[fo_enmap.labels == i] = res["ice_model"][:, i]

        if fo_enmap.land_only:
            enmap_l2a_vnir[fo_enmap.water_mask_vnir != 1] = np.nan
            enmap_l2a_swir[fo_enmap.water_mask_swir != 1] = np.nan

            cwv_seg[fo_enmap.water_mask_swir != 1] = np.nan
            liq_seg[fo_enmap.water_mask_swir != 1] = np.nan
            ice_seg[fo_enmap.water_mask_swir != 1] = np.nan

        res["cwv_model"] = cwv_seg
        res["liq_model"] = liq_seg
        res["ice_model"] = ice_seg
    else:
        logger.info("Transforming CWV retrieval map to VNIR sensor geometry to enable AC of VNIR data...")
        cwv_trans = enmap_l1b.transform_swir_to_vnir_raster(array_swirsensorgeo=res["cwv_model"],
                                                            resamp_alg=fo_enmap.resamp_alg,
                                                            respect_keystone=False)
        cwv_trans[cwv_trans == 0.0] = np.nan

        data_ac = {"vnir": fo_enmap.data_vnir, "swir": fo_enmap.data_swir}
        cwv_ac = {"vnir": cwv_trans, "swir": res["cwv_model"]}
        pt_ac = {"vnir": fo_enmap.pt_vnir, "swir": fo_enmap.pt}
        surf_ac = {"intercept": res["intercept_model"], "slope": res["slope_model"], "liquid": res["liq_model"],
                   "ice": res["ice_model"]}

        logger.info("Starting surface reflectance retrieval...")
        warnings.filterwarnings("ignore")
        make_ac_enmap(data=data_ac, enmap_l1b=enmap_l1b, fo=fo_enmap, cwv=cwv_ac, pt=pt_ac, surf_res=surf_ac,
                      logger=logger)

        enmap_l2a_vnir = enmap_l1b.vnir.data_l2a
        enmap_l2a_swir = enmap_l1b.swir.data_l2a

    # simple validation of L2A data
    if fo_enmap.land_only:
        val_vnir = enmap_l2a_vnir[fo_enmap.water_mask_vnir == 1]
        val_swir = enmap_l2a_swir[fo_enmap.water_mask_swir == 1]
        if np.isnan(val_vnir).any() or np.isnan(val_swir).any():
            logger.warning("The surface reflectance for land only generated by SICOR contains NaN values. Please check "
                           "for errors in the input data, the options file, or the processing code.")
    else:
        if np.isnan(enmap_l2a_vnir).any() or np.isnan(enmap_l2a_swir).any():
            logger.warning("The surface reflectance for land + water generated by SICOR contains NaN values. Please "
                           "check for errors in the input data, the options file, or the processing code.")

    for ii, dl2a in zip(range(2), [enmap_l2a_vnir, enmap_l2a_swir]):
        if dl2a[np.isfinite(dl2a)].shape[0] > 0:
            if ii == 0:
                d_name = "VNIR L2A"
            else:
                d_name = "SWIR L2A"
            if np.min(dl2a[np.isfinite(dl2a)]) < 0:
                logger.warning("%s data contain negative values indicating an overcorrection. Please check for "
                               "errors in the input data, the options file, or the processing code." % d_name)
            if np.max(dl2a[np.isfinite(dl2a)]) > 1:
                logger.warning("%s data contain values exceeding 1 indicating a saturation. Please check for errors "
                               "in the input data, the options file, or the processing code." % d_name)

    del enmap_l1b.vnir.data_l2a
    del enmap_l1b.swir.data_l2a

    logger.info("%s atmospheric correction successfully finished!" % options["sensor"]["name"])

    return enmap_l2a_vnir, enmap_l2a_swir, res
