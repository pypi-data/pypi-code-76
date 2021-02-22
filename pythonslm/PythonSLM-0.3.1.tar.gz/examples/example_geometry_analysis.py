"""
A simple example showing how to use PySLM for analysising a model for manufacture
"""
import pyslm
from pyslm import hatching as hatching
import numpy as np

# Imports the part and sets the geometry to  an STL file (frameGuide.stl)
solidPart = pyslm.Part('inversePyramid')
solidPart.setGeometry('../models/frameGuide.stl')


solidPart.origin[0] = 5.0
solidPart.origin[1] = 2.5
solidPart.scaleFactor = 1.0
solidPart.rotation = [0, 0.0, 45]
solidPart.dropToPlatform()
print(solidPart.boundingBox)

# Set the layer thickness
layerThickness = 0.04 # [mm]

print('Analysis Beginning')

layers = []

geomSlices = []
for z in np.arange(0, solidPart.boundingBox[5], layerThickness):

    # Typically the hatch angle is globally rotated per layer by usually 66.7 degrees per layer
    # Slice the boundary
    geomSlices.append(solidPart.getVectorSlice(z, False))

print('slices finished')
area = []
for slice in geomSlices:

    areas = sum([poly.area for poly in slice])
    area.append(areas)

print('Slicing Finished')

import matplotlib.pyplot as plt

plt.plot(area)


# Plot the layer geometries using matplotlib
# Note: the use of python slices to get the arrays



