import pyslm

from pyslm import hatching as hat
import pyslm.pyclipper as pyclipper
import numpy as np
import matplotlib.pyplot as plt

solidPart = pyslm.Part('myFrameGuide')
solidPart.setGeometry('../models/frameGuide.stl')

z = 23

sliceRes = 0.04

sliceA = solidPart.getVectorSlice(z-sliceRes*4, returnCoordPaths=True)
sliceB = solidPart.getVectorSlice(z, returnCoordPaths=True)
sliceC = solidPart.getVectorSlice(z+sliceRes*4, returnCoordPaths=True)

pc = pyclipper.Pyclipper()

for path in sliceA:
    path = np.hstack([path, np.ones([path.shape[0],1])])
    pc.AddPath(pyclipper.scale_to_clipper(path,1000), pyclipper.PT_CLIP, True)

for path in sliceB:
    path = np.hstack([path, np.ones([path.shape[0],1])])

    pc.AddPath(pyclipper.scale_to_clipper(path,1000), pyclipper.PT_SUBJECT, True)

result = pc.Execute(pyclipper.CT_DIFFERENCE, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)

result = pyclipper.scale_from_clipper(result,1000)


myHatcher = hat.StripeHatcher()
myHatcher.stripeWidth = 5.0

myHatcher.hatchAngle = 10
myHatcher.volumeOffsetHatch = 0.08
myHatcher.spotCompensation = 0.06
myHatcher.numInnerContours = 2
myHatcher.numOuterContours = 1

print('hatching')
geomSlice2 = []
geomSlice = solidPart.getVectorSlice(z, returnCoordPaths = True)
for geom in geomSlice:
    geomSlice2.append(geom*4)
layer = myHatcher.hatch(geomSlice2)

if False:
    greedySort = hat.GreedySort()
    greedySort.sortY = False
    greedySort.hatchAngle = myHatcher.hatchAngle

#linearSort = hat.LinearSort()
#linearSort.hatchAngle = myHatcher.hatchAngle
#layer.hatches[0].coords = linearSort.sort(layer.hatches[0].coords)
print('done')
hat.Hatcher.plot(layer, plot3D=False)# plotArrows=True)

for poly in result:
    poly = np.array(poly)
    plt.plot(poly[:,0], poly[:,1])

