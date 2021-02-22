#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 22:45:58 2020

@author: lparry
"""

import re
import os
import struct
import numpy as np


import pyslm
import pyslm.geometry
import pyslm.visualise

def read_uint32(file, count=1):
    return np.fromfile(file, count=count, dtype=np.uint32)

def read_int32(file, count=1):
    return np.fromfile(file, count=count, dtype=np.int32)

def read_int16(file, count=1):
    return np.fromfile(file, count=count, dtype=np.int16)

def read_uint16(file, count=1):
    return np.fromfile(file, count=count, dtype=np.uint16)

def read_uint8(file, count=1):
    return np.fromfile(file, count=count, dtype=np.uint8)

def read_floats(file, count=1):
    return np.fromfile(file, count=count, dtype=np.float32)

# Read the layer
LONG_HATCH_SECTION = 132
SHORT_HATCH_SECTION = 131
LONG_POLYLINE_SECTION = 130
SHORT_POLYLINE_SECTION = 129
SHORT_LAYER_SECTION = 128
LONG_LAYER_SECTION = 127

filename ="cube-10mm_000_s1_vs.cli"

file = open(filename, "rb")

"""
Read the .cli header
"""

header = file.readline().decode("ascii").rstrip("\n")

if header != "$$HEADERSTART":
    raise ValueError("Not .cls file")

fileType  = file.readline().decode("ascii").rstrip("\n")

if fileType != "$$BINARY":
    raise ValueError("not binary file")

line = file.read(11)
params = {}
while line != "$$HEADEREND":

    file.seek(-11, 1)

    # Read the textual line in the header
    line = file.readline()

    if not line:
        break

    line = line.decode("latin-1").rstrip("\n")

    m = re.search("^\${2}(.*)/(.*)", line)

    params[m.group(1)] = m.group(2)

    line = file.read(11).decode("ascii")

id = read_uint16(file)

layers = []

params['UNITS'] = float(params['UNITS'])

while id == SHORT_LAYER_SECTION or id == LONG_LAYER_SECTION:

    layer = pyslm.geometry.Layer()
    layer.z = 0

    if id == LONG_LAYER_SECTION:
        layer.z = read_floats(file,1)
    elif id == SHORT_LAYER_SECTION:
        layer.z = read_uint16(file)

    id  = read_uint16(file)

    while id == SHORT_POLYLINE_SECTION or id == LONG_POLYLINE_SECTION or id == SHORT_HATCH_SECTION or id == LONG_HATCH_SECTION:
        geom = None
        if id == SHORT_POLYLINE_SECTION:
            geom = pyslm.geometry.ContourGeometry()
            geom.bid = read_uint8(file)
            geom.dir = read_uint16(file)
            numPoints = read_uint16(file)

            geom.coods = read_int16(file, 2*int(numPoints)).astype(np.float32).reshape(-1,2) * params['UNITS']

        elif id == LONG_POLYLINE_SECTION:
            geom = pyslm.geometry.ContourGeometry()

            geom.bid = read_uint32(file)
            geom.dir = read_uint32(file)
            numPoints = read_uint32(file)
            geom.coords = read_floats(file, 2 * int(numPoints)).reshape(-1,2)

        elif id == SHORT_HATCH_SECTION:
            geom = pyslm.geometry.HatchGeometry()
            geom.bid = read_uint16(file)
            numPoints = read_uint16(file)

            geom.coords = read_int16(file, 4 * int(numPoints)).astype(np.float32).reshape(-1,2) * params['UNITS']

        elif id == LONG_HATCH_SECTION:
            geom = pyslm.geometry.HatchGeometry()
            geom.bid = read_uint32(file)
            numPoints = read_uint32(file)

            geom.coords = read_floats(file, 4 * int(numPoints)).reshape(-1,2)

        layer.geometry.append(geom)
        id = read_uint16(file)

    print('id', id)
    layers.append(layer)

print('Total Path Distance: {:.1f} mm'.format(pyslm.analysis.getLayerPathLength(layers[0])))

pyslm.visualise.plot(layers[1], plot3D=False, plotOrderLine=True, plotArrows=False)

#pyslm.visualise.plotLayers(layers[0:-1:10])
