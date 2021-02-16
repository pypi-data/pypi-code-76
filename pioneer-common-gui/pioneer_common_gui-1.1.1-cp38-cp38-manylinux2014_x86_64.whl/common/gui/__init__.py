from pioneer.common import linalg
from pioneer.leddar_utils_cpp import BVH, PointsBVH

import numpy as np
import traceback

from PyQt5.QtQml import qmlRegisterType

#generic non-leddar-related modules

from . import Viewport, Camera, Actors, Geometry, Effect, Array, Transforms, Product, CustomAttribs, MPLFigures

qmlRegisterType(Product.Product, "Leddar", 1, 0, "Product" )
qmlRegisterType(Product.VariantProduct, "Leddar", 1, 0, "VariantProduct" )

qmlRegisterType(Viewport.Viewport, "Leddar", 1, 0, "Viewport" )

qmlRegisterType(Camera.Camera, "Leddar", 1, 0, "Camera" )

qmlRegisterType(Actors.Renderable, "Leddar", 1, 0, "Renderable" )
qmlRegisterType(Actors.Actor, "Leddar", 1, 0, "Actor" )
qmlRegisterType(Actors.Actors, "Leddar", 1, 0, "Actors" )
#
qmlRegisterType(Transforms.Transform, "Leddar", 1, 0, "Transform" )
qmlRegisterType(Transforms.Translation, "Leddar", 1, 0, "Translation" )
qmlRegisterType(Transforms.Rotation, "Leddar", 1, 0, "Rotation" )
qmlRegisterType(Transforms.MatrixTransform, "Leddar", 1, 0, "MatrixTransform" )
#
qmlRegisterType(Geometry.Geometry, "Leddar", 1, 0, "Geometry" )
qmlRegisterType(Geometry.Attribs, "Leddar", 1, 0, "Attribs" )
qmlRegisterType(CustomAttribs.AmplitudeAttribs, "Leddar", 1, 0, "AmplitudeAttribs" )
qmlRegisterType(CustomAttribs.ColorsAttribs, "Leddar", 1, 0, "ColorsAttribs" )
# qmlRegisterType(CustomAttribs.SegmentationLabelsAttribs, "Leddar", 1, 0, "SegmentationLabelsAttribs" )
#
qmlRegisterType(Array.Array, "Leddar", 1, 0, "Array")
qmlRegisterType(Array.ArrayFloat1, "Leddar", 1, 0, "ArrayFloat1" )
qmlRegisterType(Array.ArrayFloat2, "Leddar", 1, 0, "ArrayFloat2" )
qmlRegisterType(Array.ArrayFloat3, "Leddar", 1, 0, "ArrayFloat3" )
qmlRegisterType(Array.ArrayFloat4, "Leddar", 1, 0, "ArrayFloat4" )
qmlRegisterType(Array.ArrayShort512, "Leddar", 1, 0, "ArrayShort512")
qmlRegisterType(Array.ArrayUShort1, "Leddar", 1, 0, "ArrayUShort1")

qmlRegisterType(Array.ArrayUInt1, "Leddar", 1, 0, "ArrayUInt1" )
qmlRegisterType(Array.ArrayUByte3, "Leddar", 1, 0, "ArrayUByte3" )
qmlRegisterType(Array.ArrayUByte4, "Leddar", 1, 0, "ArrayUByte4" )

qmlRegisterType(Array.ArrayInt1, "Leddar", 1, 0, "ArrayInt1" )

qmlRegisterType(Effect.GLSLProgram, "Leddar", 1, 0, "GLSLProgram" )
qmlRegisterType(Effect.Effect, "Leddar", 1, 0, "Effect" )


qmlRegisterType(MPLFigures.EchoesMPLFigureProvider, "Leddar", 1, 0, "EchoesMPLFigureProvider" )

#optional modules

try:
    from . import Clouds, Traces, Image, Sensor, SensorFilters
    qmlRegisterType(Clouds.ImageArray, "Leddar", 1, 0, "ImageArray")
    qmlRegisterType(Clouds.PointCloud, "Leddar", 1, 0, "PointCloud")
    qmlRegisterType(Clouds.SurfaceCloud, "Leddar", 1, 0, "SurfaceCloud")
    qmlRegisterType(Clouds.SensorReferential, "Leddar", 1, 0, "SensorReferential")

    qmlRegisterType(Traces.TracesGeometry, "Leddar", 1, 0, "TracesGeometry")
    qmlRegisterType(Traces.TracesDataSource, "Leddar", 1, 0, "TracesDataSource")

    qmlRegisterType(Sensor.SensorCapture, "Leddar", 1, 0, "SensorCapture")#, "SensorCapture is an abstract type, use a derivation" )
    qmlRegisterType(Sensor.LiveCapture, "Leddar", 1, 0, "LiveCapture" )

    qmlRegisterType(SensorFilters.PackageFilter, "Leddar", 1, 0, "PackageFilter")

    qmlRegisterType(Image.QImagePainter, "Leddar", 1, 0, "QImagePainter")
    qmlRegisterType(Image.ImageFilter, "Leddar", 1, 0, "ImageFilter")
    qmlRegisterType(Image.BGRToRGBFilter, "Leddar", 1, 0, "BGRToRGBFilter")
    qmlRegisterType(Image.ColorMapFliter, "Leddar", 1, 0, "ColorMapFliter")
    qmlRegisterType(Image.ColorMapArray, "Leddar", 1, 0, "ColorMapArray")
except:
    print(traceback.format_exc())

# try:
#     from . import PySpinCamera
#     qmlRegisterType(PySpinCamera.PySpinCamera, "Leddar", 1, 0, "PySpinCamera")
# except:
#     print(traceback.format_exc())

# try:
#     from . import V4LCamera
#     qmlRegisterType(V4LCamera.V4LCamera, "Leddar", 1, 0, "V4LCamera")
# except:
#     print(traceback.format_exc())


def merge_bvhs(bvhs, matrices = None):

    vertices_list  = []
    triangles_list = []
    
    vertex_offsets = [0]
    for i, bvh in enumerate(bvhs):
        if bvh is None:
            triangles_list.append(np.empty((0,3), 'u4'))
            vertices_list.append(np.empty((0,3), 'f4'))
            continue

        if matrices is not None and matrices[i] is not None:
            vertices_list.append(linalg.map_points(matrices[i], bvh.vertices))
        else:
            vertices_list.append(bvh.vertices)
        offset = vertex_offsets[-1]
        triangles_list.append(bvh.triangles + offset)
        offset += bvh.vertices.shape[0]
        vertex_offsets.append(offset)

    vertices = np.vstack(vertices_list)
    triangles = np.vstack(triangles_list)
    triangles_mapping = np.empty((triangles.shape[0]), 'u4')

    triangle_offsets = [0]
    offset_from = 0
    for i, t in enumerate(triangles_list):
        t_size = 0 if t is None else t.shape[0]
        triangles_mapping[offset_from:offset_from+t_size] = i
        offset_from += t_size
        triangle_offsets.append(offset_from)


    return BVH(triangles, vertices), triangles_mapping, triangle_offsets, vertex_offsets

BVH.merge_bvhs = staticmethod(merge_bvhs)

