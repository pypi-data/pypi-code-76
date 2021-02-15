# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020-2021, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
"""
"""
from flexsolve import njitable
from math import pi

__all__ = ('cylinder_diameter_from_volume', 
           'cylinder_volume_from_diameter',
           'cylinder_area',
           'circumference')

@njitable(cache=True)
def cylinder_diameter_from_volume(volume, length_to_diameter):
    return (4. * volume / pi / length_to_diameter)**(1./3.)

@njitable(cache=True)
def cylinder_volume_from_diameter(diameter, length_to_diameter):
    return pi * (diameter / 2) ** 2 * diameter * length_to_diameter

@njitable(cache=True)
def cylinder_area(diameter, length):
    return circumference(diameter) * length

@njitable(cache=True)
def circumference(diameter):
    return pi * diameter