#!/usr/bin/env python
# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains tools for calculating observation metadata.

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


def varsol(jday, month):
    """Compute solar irradiance variance.

    :param jday:  julian day
    :param month: julian month
    :return:      solar irradiance variance factor
    """
    if 2 < month <= 8:
        j = 31 * (month - 1) - ((month - 1) / 2) - 2 + jday
    elif month <= 2:
        j = 31 * (month - 1) + jday
    else:
        j = 31 * (month - 1) - ((month - 2) / 2) - 2 + jday

    pi = 2 * np.arccos(0)
    om = (0.9856 * (j - 4)) * pi / 180
    dsol = 1 / ((1 - 0.01673 * np.cos(om)) ** 2)
    dsol = 1 / dsol ** 0.5

    return dsol
