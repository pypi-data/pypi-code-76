"""
A simple example showing the basic structure and layout required for generating a machine build file for a SLM System.
This is automatically built into the hatching classes, but for simple experiments or simulations it can be useful to
create these structures manually.

The following example demonstrate the overall structure required for creating the border of a square region.
"""

import pyslm
import numpy as np
import copy

staticmethod

"""
The structures necessary for creating a machine build file should be imported from the geometry submodule. 
Fallback python classes that are equivalent to those in libSLM are provided to ensure prototyping can take place.
"""
from pyslm import geometry as slm

"""
A header is needed to include an internal filename. This is used as a descriptor internally for the Machine Build File. 
The translator Writer in libSLM will specify the actual filename.
"""
header = slm.Header()
header.filename = "MachineBuildFile"

# Depending on the file format the version should be provided as a tuple
header.version = (1,2)

# The zUnit is the uniform layer thickness as an integer unit in microns
header.zUnit = 1000 # [μm]

"""
Create the model:
A model represents a container with a unique ID (.mid) which has a set of BuildStyles. The combination of both the
Model and BuildStyle are assigned to various LayerGeometry features within the build file. 
 
:note:
    For each model, the top layer ID that contains a child buildstyle must be included. 
"""
model = slm.Model()
model.mid = 1
model.name = "Point Exposure Test"
model.topLayerId = 0

"""
Generate a set of exposure points
"""

exposurePointDistance = 100e-3 # [Point Distance]

y = np.arange(0,15.0, exposurePointDistance).reshape(-1,1)
x = np.ones(y.shape)
coords = np.hstack([x,y])

"""
Generate a list of point geometries corresponding to each point exposure. Each point geometry has a unique build style 
(bid)
"""
pointsGeom = [slm.PointsGeometry(mid=1, bid=i+1) for i in range(len(coords))]

# Assign the points
for i in range(len(coords)):
    pointsGeom[i].coords = coords[i].reshape(1,-1)

bstyles = [slm.BuildStyle() for i in range(len(coords))]

for i in range(len(bstyles)):
    bstyles[i].setStyle(bid=i+1,
                        focus=0, power=200.0,
                        pointExposureTime=80, pointExposureDistance=50,
                        laserMode=slm.LaserMode.PULSE)

# Eg. set every 2nd exosure point to half the power
for bstyle in bstyles[1:-1:2]:
    bstyle.laserPower = 100

model.buildStyles = bstyles
"""
Create the layers
"""
layerThickness = 30 # [mu m]

layers = [slm.Layer(id=i, z=i*layerThickness) for i in range(len(coords))]

for layer in layers:
    # Assign the geometry to the file
    layer.geometry = pointsGeom
    #layer.geometry = copy.deepcopy(pointsGeom) # Note: deep copy is needed to create copies of the layer geometry

# Locate the height (layer.z) for the last layer in the build. Note: must be set!
model.topLayerId = layers[-1].layerId
models = [model]

""" Validate the .mtt file to check for any inconsistencies in the definition of model or layers"""
slm.utils.ModelValidator.validateBuild(models, layers)

"""
Import the MTT (Renishaw SLM) Exporter
"""
from libSLM import mtt

"Create the initial object"
mttWriter = mtt.Writer()
mttWriter.setFilePath("build.mtt")
mttWriter.write(header, models, layers)

"""
Read the MTT file
"""

mttReader = mtt.Reader()
mttReader.setFilePath("build.mtt")
mttReader.parse()

readLayers = mttReader.layers

""" 
Plot the laser id used for each hatch vector used. A lambda function is used to plot this. 
"""
def plotLaserBid(models, pointGeom):
    buildStyle = pyslm.analysis.getBuildStyleById(models, pointGeom.mid, pointGeom.bid)
    return np.tile(buildStyle.bid, [int(len(pointGeom.coords)),1])

def plotLaserPower(models, pointGeom):
    buildStyle = pyslm.analysis.getBuildStyleById(models, pointGeom.mid, pointGeom.bid)
    return np.tile(buildStyle.laserPower, [int(len(pointGeom.coords)),1])

(fig, ax) = pyslm.visualise.plot(readLayers[0], plot3D=False, plotOrderLine=True, plotPoints=True,
                                            index=lambda pointGeom :plotLaserPower(models, pointGeom))

ax.grid(which="both")

