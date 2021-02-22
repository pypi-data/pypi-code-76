#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 22:45:58 2020

@author: lparry
"""

import os
import struct
import zlib 
import numpy as np
import matplotlib.pyplot as plt
import binascii

import pyslm
import pyslm.visualise

def CRC32_from_file(file, endpos):
    file.seek(0)
    buf = file.read(endpos)
    buf = (binascii.crc32(buf) & 0xFFFFFFFF)
    return buf# "%08X" % buf

    
def read_uint8(file):
    return np.fromfile(file, count=1, dtype=np.uint8)

def read_floats(file, count=1):
    return np.fromfile(file, count=count, dtype=np.float32)

[0x22,0x60]

def read_number_test(bits):

    size = (bits[0] & 0xE0) >> 5    
    remBits = bits[0] & 0x1F # mask 0001 1111   
    #print(bits, size)
    # Reset the file position pointer (second argument is relative (1))
    
    if size == 0:
        return remBits
    
    bits[0] = remBits # override the first array
    
    
    # Read the bytes backwards
    val  =  int.from_bytes(bytes(bits[size::-1]), byteorder='little')

    return val

def read_number(file):
    bits = list(file.read(8))
    file.seek(-8,1)
    size = (bits[0] & 0xE0) >> 5    
    remBits = bits[0] & 0x1F # mask 0001 1111   
    #print(bits, size)
    # Reset the file position pointer (second argument is relative (1))
    file.seek(size+1,1)

    if size == 0:
        return remBits
    
    bits[0] = remBits # override the first array

    # Read the bytes backwards
    val  =  int.from_bytes(bytes(bits[size::-1]), byteorder='little')
    #print(bits, 'size', size, 'val', val)
    return val


HEADER         = 1
FILEIDENT      = 2 # Filename
VERSION        = 3
LSEEKPOS       = 4  # Position  of the layer section
MODELINFO      = 5  # Model information
MODELID        = 6  # Unique ID for each model
MODELNAME      = 7  # Name of the Model in UTF-16
LAYERSEEKTBL   = 8  # Layer Seek Table
LAYERTBLENTRY  = 9  # Layer Table Entry
LAYER          = 10 # The layer section  containing geometric data for each layer
POLYGON        = 11 # Describes a polygon
HATCH          = 12 # Describes a hatch section
MODELBSTYLE    = 13 # Model Build Style - one for ever build style in each model
BUILDSTYLEID   = 14 # Build Style of the ID
LASERSPEED     = 15 # Laser Speed in mm/s
LASERPOWER     = 16 # Laser Power in Watts
LASERFOCUS     = 17 # Laser Focus offset in mm
MODELREF       = 18 # Build style chosen for the model
POLYCOORDS     = 19 # Polygon Coordinates [x1,y1,x2,y2,....,xn,yn]
HCOORDS        = 20 # Hatch Coordinates [xStart, yStart, xEnd, yEnd]
CRC            = 21
MODELTOPSLICE  = 22 # The highest layer slice of each model
LAYERSEEKPOS   = 23 # File position of the layer section
LAYERZPOS      = 24
PNTDISTANCE    = 25 # Point distance value for low level exposure control
PNTEXPTIME     = 26
ZUNIT          = 27
PNTSEQ         = 28 # Point sequences exposed one by one [x1,y1,x2,y2,....,xn,yn]
PNTCOORDS      = 29
UNKNOWN        = 34 # Unknown BuildStyle Section ID (float value)
BUILDPROCESSORINFO    = 35 # Build-Processors Paramter Information (UTF16 key-value store)
MODELBUILDSTYLENAME = 37 # Model Build Style Family Name
MODELBUILDSTYLEDESC = 39 # Model Build Style Family Description
BUILDSTYLEDESC = 40 # Build style description (UTF16)
BUILDINFO = 41 #General Build-Processors Paramter Information Section on Hatch Parameters
BUILDINFOUNKNOWN = 43 # Unknwon section feature a single number
MODELSECTUNKNOWN = 48 # Unknown Model Section consisting of a single number

def readModel(file):
        
    model = dict()            
    modelIdSect = read_number(file)
    modelIdlLen = read_number(file)
    model['id'] = read_number(file)
    
    modelNameSect = read_number(file)
    modelNameLen = read_number(file)
    
    print(modelIdSect, modelIdlLen, modelNameSect, modelNameLen)
    model['name'] = (file.read(modelNameLen))
    
        
    modelTopSliceSect = read_number(file)
    modelTopSliceLen = read_number(file)
    model['topSlice'] = read_number(file)
    d
    
    return model
    

   

def readLayerGeom(file):
    file.seek(-1, 1)
    layerGeomType = read_uint8(file)
    layerGeomSectLen = read_number(file)
    
    layerGeom = dict()
    #print('layerGeomType', layerGeomType)
    if layerGeomType == HATCH:
        layerGeom = pyslm.HatchGeometry()
    elif layerGeomType == POLYGON:
        layerGeom = pyslm.ContourGeometry()
        layerGeom.subType = 'inner'
    elif layerGeomType == PNTSEQ:
        layerGeom = pyslm.PointsGeometry()

    modelRefSect = read_uint8(file)
    modelRefSectLen = read_number(file)
    layerGeom.mid =  read_number(file)
    layerGeom.bid =  read_number(file)

    geomSectId = read_uint8(file)
    numCoords = read_number(file)    

    #print('geom sect id', modelRefSect, modelRefSectLen, layerGeom, numCoords, file.tell())
    if geomSectId == HCOORDS:           
        coords = np.fromfile(file, count=int(numCoords/4), dtype=np.float32).reshape(-1,2)
        layerGeom.coords = coords
    elif geomSectId == POLYCOORDS:
        coords = np.fromfile(file, count=int(numCoords/4), dtype=np.float32).reshape(-1,2)
        layerGeom.coords = coords
    elif geomSectId == PNTCOORDS:
        coords = np.fromfile(file, count=int(numCoords/4), dtype=np.float32).reshape(-1,2)
        layerGeom.coords = coords
    return layerGeom

filename = "cube-10mm.slm"

file = open(filename, "rb")

# Read header
headerSectId = read_number(file)
headerLen = read_number(file)

nameSectId = read_number(file)
nameLen = read_number(file)
name = (file.read(nameLen)).decode('ascii')

versionSectId = read_number(file)
versionLen = read_number(file)
version = (read_number(file),read_number(file))

headerUidSectId = read_number(file) # Header Section ID  - Assuming UUID [42]
headerUidLen = read_number(file)
headerUid = (file.read(headerUidLen)).decode('ascii')

zUnitSectId = read_number(file)
zUnitSectLen = read_number(file)
zUnit = read_number(file)

layerSeekTableSectId =  read_number(file)
layerSeekTableSectLen = read_number(file)
layerSeekTableFilePos = read_number(file)

""" Section provides build processor information [44]"""
sectHeaderId = read_number(file) # Header build processor info [44]
sectHeaderLen = read_number(file)

""" Read the build processor name  [45] """
sectHeaderAId = read_number(file) # Header build processor id [45]
sectHeaderALen = read_number(file)
sectHeaderAContent = (file.read(sectHeaderALen)).decode('utf16')

""" Read the build processor version [46] """
sectHeaderBId = read_number(file)
sectHeaderBLen = read_number(file)
sectHeaderBContent = (file.read(sectHeaderBLen)).decode('utf16')

""" Read the timestamp of the file generation [47]"""
sectHeaderCId = read_number(file)
sectHeaderCLen = read_number(file)
sectHeaderCContent = (file.read(sectHeaderCLen)).decode('ascii')

sectHeaderDId = read_number(file)
sectHeaderDLen = read_number(file)
sectHeaderDContent1 =  read_uint8(file)
sectHeaderDContent2 =  read_uint8(file)

sectHeaderEId = read_number(file) # Build Processor Material Style [36]

sectHeaderELen = read_number(file)

sectHeaderEContent =  (file.read(sectHeaderELen)).decode("utf16")


modelSect = read_number(file) # [5]
modelSectLen = read_number(file)

models = []
sectId = read_uint8(file)

while sectId == MODELID:
    
    model = dict()            
    modelIdlLen = read_number(file)
    model['id'] = read_number(file)
    
    modelNameSect = read_number(file) # Model Name Section [7]
    modelNameLen = read_number(file)
    model['name'] = (file.read(modelNameLen)).decode('utf16')

    modelTopSliceSect = read_number(file) # Model Top Slice Section [22]
    modelTopSliceLen = read_number(file)
    model['topSlice'] = read_number(file)

    #models.append(readModel(file))
    
    # Read the build style
    
    bstyleSectId = read_number(file) # Model Build Style Section [37]
    bstyleSectLen = read_number(file)
    model['buildStyleName'] = (file.read(bstyleSectLen)).decode("utf16")
    
    bstyleDescId = read_number(file) # Model Build Style Description [39]
    bstyleDescLen = read_number(file)
    model['buildStyleDescription'] = (file.read(bstyleDescLen)).decode("utf16")
    
    # Unsure what this region is
    sectId8= read_number(file)
    sectLen8 = read_number(file)

     = read_number(file)
    print('bstyle unknwon', sectId8, sectLen8, sectContent8)

    """ Read the build styles """
    sectId = read_number(file) # MODELBSTYLE

    buildStyles = []
    
    while sectId == MODELBSTYLE:
        
        bstyleLen = read_number(file)
        
        sectId1 = read_number(file) # BUILDSTYLEID  [14]
        sectLen1 = read_number(file)
        bstyleId = read_number(file)
        
        laserSpeedId = read_uint8(file) # LASERSPEED [15]
        laserSpeedLen = read_number(file)
        laserSpeed = read_floats(file, 1)
        
        laserPowerId = read_uint8(file) # LASERPOWER [16]
        laserPowerLen = read_number(file)
        laserPower = read_floats(file, 1)	
        
        laserFocusId = read_number(file)  #LASERFOCUS [17]
        laserFocusLen = read_number(file)
        laserFocus = read_floats(file, 1)	
        
        pointDistanceId = read_number(file)  #PNTDISTANCE [25]
        pointDistanceLen = read_number(file)
        pointDistance = read_number(file)       
        
        pointExposureTimeid = read_number(file)  #POINTEXPOSURETIME [26]
        pointExposureTimeLen = read_number(file)
        pointExposureTime = read_number(file)

        buildStyleuUnknownId = read_number(file) # Length is 4 but unknown this value
        buildStyleUnknownLen = read_number(file)
        #buildStyleNum = read_number(file)
        #buildStyleNum2 = read_number(file)
        #buildStyleNum3 = read_number(file)


        buildStyleNum = read_floats(file, 1)
 
        
        buildStyleDescId = read_number(file) # Build style description [40]
        buildStyleDescLen = read_number(file)
        buildStyleDescription =  (file.read(buildStyleDescLen)).decode("utf16")
        
        buildStyles.append(dict({'id': bstyleId,
                                 'description': buildStyleDescription,
                         'speed': laserSpeed,
                         'power': laserPower,
                         'focus': laserFocus,
                         'unknown': (buildStyleuUnknownId, buildStyleNum),
                         'pointExposureTime': pointExposureTime,
                         'pointExposureDistance': pointDistance}))


        sectId = read_number(file) # ?????
    
    
    models.append(model)

print('Bstyle info', sectId) # General info section [41]
sectIdLen = read_number(file)
sectGId = read_number(file) #  Unknown Section [43]
sectGLen = read_number(file) # [1]
sectGContent = read_number(file) # [3]

infos = []
infoIds = []


sectId = read_number(file) # ?????
while sectId == 35: # unknown

    sectInfoLen = read_number(file)
    information = (file.read(sectInfoLen)).decode("utf16")
    infos.append(information)
    infoIds.append((sectId, sectInfoLen))
    sectId = read_number(file) # ?????

infoIds2 = []
infos2 = []
while sectId == 41: # unknown

    sectLen = read_number(file) # 500
    sectId3 = read_number(file) # [43]
    sectLen3 =  read_number(file)
    sectCont3 =  read_number(file)
    
    sectId = read_number(file)
    
    while sectId == 35: # unknown

        sectLen = read_number(file)
        information = (file.read(sectLen)).decode("utf16")
        infos2.append(information)
        infoIds2.append(sectId)
        sectId = read_number(file) # ?????
       


# Read file string at 11 
# approximate length of header section
print(file.tell())
# Skip to the start of the layers section
#file.seek(17840)

# Read the layer section
layers= []

#sectId = read_uint8(file)

layerId = 0

while sectId == LAYER:
    
    #print("new layer")
    layer = pyslm.geometry.Layer()
    layer.z = layerId

    layerLength = read_number(file) 
    sectId = read_uint8(file)
    while sectId == HATCH or sectId == POLYGON or sectId == PNTSEQ:
        layer.geometry.append(readLayerGeom(file))
        sectId = read_uint8(file)
        	
    #print("filepos", file.tell())
    sectId = sectId
    #print("section id", sectId)
    layers.append(layer)
    layerId += 1



# Read layer sect id
layerSeekTableSectId = sectId
layerSeekTableLen = read_number(file)
 
seekTable = [] 
sectId = read_uint8(file)  

layerId = 0
while sectId == LAYERTBLENTRY:
    
    sectLen = read_number(file)
    sectId = read_uint8(file)  
    sectLen = read_number(file)
    seekPos = read_number(file)
    sectId = read_uint8(file)  
    sectLen = read_number(file)
    zLevel = read_number(file)
    
    seekTable.append([layerId, zLevel, seekPos])
    
    layerId += 1    
    sectId = read_uint8(file)  
    
        
print(file.tell())
"""
READ THE CHECKSUM SECTION
"""
crc32 = CRC32_from_file(file,file.tell()+1)
print('crc', crc32, "%08X" % crc32)
print('end', file.tell())
#file.close()

print('Total Path Distance: {:.1f} mm'.format(pyslm.analysis.getLayerPathLength(layers[0])))

pyslm.visualise.plot(layers[0], plot3D=False, plotOrderLine=True, plotArrows=False)

#pyslm.visualise.plotLayers(layers[0:-1:10])
