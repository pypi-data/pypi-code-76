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

from sicor.AC.RtFo_3_phases import FoGen, FoFunc, __minimize__


def make_ac_generic(data_l1b, fo, xx, logger=None):
    """Perform atmospheric correction for sensor-independent hyperspectral L1 products, based on given and retrieved
       parameters.

    :arg data_l1b:
         Level-1B data object
    :arg fo:
         Forward operator
    :arg xx:
         Solution state vector, must be in the order [cwv, cwc, ice, lai, dasf, p_max, k, b]
    :arg logger:
         None or logging instance
    :return:
         Level-2A data object
    """
    logger = logger or logging.getLogger(__name__)
    data_l2a = np.full(data_l1b.shape, np.NaN, dtype=float)

    ncols, nrows = (data_l1b.shape[1], data_l1b.shape[0])
    logger.info("Performing columnwise ac...")
    warnings.filterwarnings("ignore")
    for icol in tqdm(range(ncols)):
        for irow in range(nrows):
            data_l2a[irow, icol, :] = fo.surf_ref(dt=data_l1b[irow, icol, :], xx=[xx["cwv_model"][irow, icol]],
                                                  pt=fo.pt[irow, icol, :], mode="full")
            swir_feature = fo.surface_model(xx=[xx["cwv_model"][irow, icol], xx["intercept_model"][irow, icol],
                                                xx["slope_model"][irow, icol], xx["liq_model"][irow, icol],
                                                xx["ice_model"][irow, icol]])
            data_l2a[irow, icol, fo.fit_wvl] = swir_feature

    return data_l2a


def sicor_ac_generic(data_l1b, options, dem=None, unknowns=False, logger=None):
    """Atmospheric correction for sensor-independent imaging spectroscopy L1 products, including a three phases of water
       retrieval.

    :arg data_l1b:
         Level-1B data object in units of TOA radiance
    :arg options:
         Dictionary with pre-defined specific instrument options
    :arg dem:
         Digital elevation model to be provided in advance ; default: None
    :arg unknowns:
         If True, uncertainties due to unknown forward model parameters are added to S_epsilon; default: False
    :arg logger:
         None or logging instance
    :return:
         Surface reflectance, water vapor, liquid water and ice maps, as well as fitted TOA radiances and retrieval
         uncertainties
    """
    logger = logger or logging.getLogger(__name__)

    logger.info("Setting up forward operator...")
    fo_gen = FoGen(data=data_l1b, options=options, dem=dem, logger=logger)
    fo_func_gen = FoFunc(fo=fo_gen)

    logger.info("Starting 3 phases of water retrieval...")
    res = __minimize__(fo=fo_gen, opt_func=fo_func_gen,  unknowns=unknowns, logger=logger)

    logger.info("Starting surface reflectance retrieval...")
    data_l2a = make_ac_generic(data_l1b=data_l1b, fo=fo_gen, xx=res, logger=logger)

    logger.info("%s atmospheric correction successfully finished!" % options["sensor"]["name"])

    return data_l2a, res
