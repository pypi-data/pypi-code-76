"""
Support generation script - Shows how to generate basic block supports using PySLM
Support Generation currently requires compiling the `Cork library <https://github.com/gilbo/cork> and then providing
the path to the compiled executable`
"""
import os
import subprocess
import random

import trimesh
import numpy as np

from pyslm.core import Part
import pyslm.support

## CONSTANTS ####
CORK_PATH = '/home/lparry/Development/src/external/cork/bin/cork'

pyslm.support.BlockSupportGenerator.CORK_PATH = CORK_PATH

OVERHANG_ANGLE = 55 # deg - Overhang angle

myPart = Part('myPart')
myPart.setGeometry("../models/frameGuide.stl")
myPart.scaleFactor = 1.2
#myPart.rotation = [-70.0, 50.0, -40.0] #[62.0, 50.0, -40.0]
myPart.rotation = [90,5,5] #[76,35,-13]#[62,50,-40.0]
myPart.dropToPlatform(20)

print(myPart.boundingBox)

""" Extract the overhang mesh - don't explicitly split the mesh"""
overhangMesh = pyslm.support.getOverhangMesh(myPart, OVERHANG_ANGLE, False)
overhangMesh.visual.face_colors = [254.0, 0., 0., 254]

"""
Generate the geometry for the supports
"""

# First generate point and edge supports
pointOverhangs = pyslm.support.BaseSupportGenerator.findOverhangPoints(myPart)
overhangEdges = pyslm.support.BaseSupportGenerator.findOverhangEdges(myPart)

"""
Generate block supports for the part.
The BlockSupportGenerator class is initialised and the parameters below are specified
"""
supportGenerator = pyslm.support.BlockSupportGenerator()
supportGenerator.rayProjectionResolution = 0.25 # [mm] - The resolution of the grid used for the ray projection
supportGenerator.innerSupportEdgeGap = 0.25 # [mm] - Inner support offset used between adjacent support distances
supportGenerator.outerSupportEdgeGap = 0.25 # [mm] - Outer support offset used for the boundaries of overhang regions
supportGenerator.simplifyPolygonFactor = 1.5 #  - Factor used for simplifying the overall support shape
supportGenerator.triangulationSpacing = 1.0 # [mm] - Used for triangulatng the extruded polygon for the bloc

# Generate a list of block supports (trimesh objects currently)
blockSupports, supportBlockRegionList = supportGenerator.identifySupportRegions(myPart, OVERHANG_ANGLE)

for block in supportBlockRegionList:
    block.trussWidth = 1.0
"""
Generate the edges for visualisation
"""
edges = myPart.geometry.edges_unique
meshVerts = myPart.geometry.vertices
centroids = myPart.geometry.triangles_center

""" Visualise Edge Supports"""
edgeRays = np.vstack([meshVerts[edge] for edge in overhangEdges])
visualize_support_edges = trimesh.load_path((edgeRays).reshape(-1, 2, 3))
colorCpy = visualize_support_edges.colors.copy()
colorCpy[:] = [254, 0, 0, 254]
visualize_support_edges.colors = colorCpy

edge_supports = []
for edge in overhangEdges:
    coords = np.vstack([meshVerts[edge,:]]*2)
    coords[2:,2] = 0.0

    extrudeFace = np.array([(0, 1, 3), (3, 2, 0)])
    edge_supports.append(trimesh.Trimesh(vertices=coords, faces=extrudeFace))

"""  Visualise Point Supports """
rays = []
for pnt in pointOverhangs:
    coords = np.zeros((2,3))
    coords[:,:] = meshVerts[pnt]
    coords[1,2] = 0.0
    rays.append(coords)


rays = np.hstack([meshVerts[pointOverhangs]]*2).reshape(-1, 2, 3)
rays[:, 1, 2] = 0.0
visualize_support_pnts = trimesh.load_path(rays)

# Make the normal part transparent
myPart.geometry.visual.vertex_colors = [80,80,80, 125]

"""
Visualise all the support geometry
"""

""" Identify the sides of the block extrudes """

if False:
    blockSupportMesh = blockSupports[11]

    bcurblockSupportSides = blockSupportMesh.copy()
    sin_theta = pyslm.support.getFaceZProjectionWeight(blockSupportSides)

    blockSupportSides.update_faces(sin_theta < 0.99999)
    blockSupportSides.remove_unreferenced_vertices()

    # Split the top and bottom surfaces to a path - guaranteed to be a manifold 2D polygon
    (top, bottom) = blockSupportSides.split(only_watertight=False)

    topPoly3D = top.outline()
    bottomPoly3D = bottom.outline()

    topVerts = topPoly3D.discrete
    topXY = topVerts[0][:,:2]
    topXY2 = np.vstack([topXY, topXY[0,:]])
    delta = np.diff(topXY, prepend =topXY[0,:].reshape(1,-1),  axis=0)
    dist = np.sqrt(delta[:,0]*delta[:,0] + delta[:,1]*delta[:,1])

    topPolyX = np.cumsum(dist)
    topPolyY = topVerts[0][:,2]

    topPolyVerts = np.hstack([topPolyX.reshape(-1,1), topPolyY.reshape(-1,1)])

    """
    Complete the bottom
    """
    bottomVerts = bottomPoly3D.discrete
    bottomXY = bottomVerts[0][:,:2]
    bottomXY2 = np.vstack([bottomXY, bottomXY[0,:]])
    delta = np.diff(bottomXY, prepend =bottomXY[0,:].reshape(1,-1),  axis=0)
    dist = np.sqrt(delta[:,0]*delta[:,0] + delta[:,1]*delta[:,1])

    bottomPolyX = np.cumsum(dist)
    bottomPolyY = bottomVerts[0][:,2]

    bottomPolyVerts = np.hstack([bottomPolyX.reshape(-1,1), bottomPolyY.reshape(-1,1)])

    bottomPolyVerts = np.flipud(bottomPolyVerts)

    myPolyVerts = np.vstack([topPolyVerts, bottomPolyVerts])


    # Convert the shapley polygons to a path list

    def generateMeshGrid(bbox, hatchSpacing: float = 5.0, hatchAngle = 45.0):

        # Hatch angle
        theta_h = np.radians(hatchAngle)  # 'rad'

        # print('bounding box bbox', bbox)
        # Expand the bounding box
        bboxCentre = np.mean(bbox.reshape(2, 2), axis=0)

        # Calculates the diagonal length for which is the longest
        diagonal = bbox[2:] - bboxCentre
        bboxRadius = np.ceil(np.sqrt(diagonal.dot(diagonal)) / hatchSpacing) * hatchSpacing

        # Construct a square which wraps the radius
        x = np.tile(np.arange(-bboxRadius, bboxRadius, hatchSpacing, dtype=np.float32).reshape(-1, 1), (2)).flatten()
        y = np.array([-bboxRadius, bboxRadius])
        y = np.resize(y, x.shape)
        z = np.arange(0, x.shape[0] / 2, 0.5).astype(np.int64)

        coords = np.hstack([x.reshape(-1, 1),
                            y.reshape(-1, 1),
                            z.reshape(-1, 1)])

        # Create the 2D rotation matrix with an additional row, column to preserve the hatch order
        c, s = np.cos(theta_h), np.sin(theta_h)
        R = np.array([(c, -s, 0),
                      (s, c, 0),
                      (0, 0, 1.0)])

        # Apply the rotation matrix and translate to bounding box centre
        coords = np.matmul(R, coords.T)
        coords = coords.T + np.hstack([bboxCentre, 0.0])

        return coords

    from pyslm import pyclipper
    from pyslm.hatching import BaseHatcher
    pc = pyclipper.PyclipperOffset()

    # Offset the outer path to provide a clean boundary to work with

    paths2 = np.hstack([myPolyVerts, np.arange(len(myPolyVerts)).reshape(-1,1)])
    paths2 =list(map(tuple, paths2))
    clipPaths = BaseHatcher.scaleToClipper(paths2)
    pc.AddPath(clipPaths, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDPOLYGON)
    outerPaths = pc.Execute(BaseHatcher.scaleToClipper(1e-6))

    diag = 3 * np.sin(np.deg2rad(60))

    bboxPoly = np.hstack([np.min(myPolyVerts, axis=0), np.max(myPolyVerts, axis=0)])
    # Generate the mesh grid used for the support trusses and merge the lines together
    hatchesA = generateMeshGrid(bboxPoly, hatchAngle=45, hatchSpacing=diag).reshape(-1, 2, 3)
    hatchesB = generateMeshGrid(bboxPoly, hatchAngle=180 - 45, hatchSpacing=diag).reshape(-1, 2, 3)
    hatches = np.vstack([hatchesA, hatchesB])

    pc.Clear()

    for hatch in hatches:
        hatchPath = BaseHatcher.scaleToClipper(hatch)
        pc.AddPath(hatchPath, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDLINE)

    trussPaths = pc.Execute(BaseHatcher.scaleToClipper(1/ 2.0))

    pc2 = pyclipper.Pyclipper()

    """
    Clip or trim the Truss Paths with the exterior of the support slice boundary
    """
    pc2.AddPaths(trussPaths, pyclipper.PT_SUBJECT)
    pc2.AddPaths(outerPaths, pyclipper.PT_CLIP)

    # Use only the truss paths. This simply exports ClipperLib PolyNode Tree

    trimmedTrussPaths = pc2.Execute2(pyclipper.CT_INTERSECTION)

    solution = trimmedTrussPaths

    # Triangulate the polygon
    vy, fy = pyslm.support.geometry.triangulatePolygon(solution)



    from scipy import interpolate

    y1 = topVerts[0][:,0]
    y2 = topVerts[0][:,1]

    x = np.linspace(0.0, np.max(myPolyVerts[:,0]), len(y1))
    f1 = interpolate.interp1d(topPolyX, y1, fill_value="extrapolate")

    x2 = np.linspace(0.0, np.max(myPolyVerts[:,0]), len(y2))
    f2 = interpolate.interp1d(topPolyX, y2, fill_value="extrapolate")

    boundaryX = f1(vy[:,0])
    boundaryY = f2(vy[:,0])
    boundaryZ = vy[:,1]

    verts =  np.hstack([boundaryX.reshape(-1,1), boundaryY.reshape(-1,1), boundaryZ.reshape(-1,1)])
    # Append a z coordinate in order to transform to mesh
    secY = trimesh.Trimesh(vertices=verts, faces=fy)

    secY.show()

    outline = blockSupportSides.outline()

s1 = trimesh.Scene([myPart.geometry,
                    blockSupports[3]]) # , overhangMesh] + supportExtrudes)

s1.show()

s1a = trimesh.Scene([myPart.geometry,
                    blockSupports[4]])

with open('overhangSupport.glb', 'wb') as f:
    f.write(trimesh.exchange.gltf.export_glb(s1, include_normals=True))

s2 = trimesh.Scene([myPart.geometry, overhangMesh,
                    visualize_support_edges, edge_supports,
                    visualize_support_pnts,
                    blockSupports]) # , overhangMesh] + supportExtrudes)
#s2.show()

#
"""
Merge the support geometry together into a single mesh
"""

if True:


    meshSupports = []

    for supportBlock in supportBlockRegionList:
        meshSupports.append(supportBlock.geometry())


    #isectMesh.visual.face_colors = [0, 155, 255, 255]
    #blockSupportSides.visual.face_colors = [0, 155, 255, 200]

    #blockSupportMesh = sum(meshSupports, trimesh.Trimesh())

    #blockSupportMesh.visual.face_colors = [0.3, 0.3, 0.3, 1.0]
    s2 = trimesh.Scene([overhangMesh, myPart.geometry
                       # visualize_support_edges, edge_supports,
                       # visualize_support_pnts,
                       ] + meshSupports)



    s2.show()
    nau

sliceMesh = trimesh.util.concatenate(meshSupports +[myPart.geometry])
supportMesh = trimesh.util.concatenate(meshSupports)
sections = sliceMesh.section(plane_origin=[0.0, 0, 50.0], plane_normal=[0, 0, 1])

lineSegs = trimesh.intersections.mesh_plane(supportMesh, plane_origin=[0.0, 0, 136.0], plane_normal=[0, 0, -1.0])

for seg in lineSegs:
    plt.plot(seg[:,0], seg[:,1])






supportGeom = sum(blockSupports)
bx = supportGeom.bounds[:,0]
by = supportGeom.bounds[:,1]

spacingX = 3.0
spacingY = 3.0

# Obtain the section through the STL extension using Trimesh Algorithm (Shapely)
sectionsX = supportGeom.section_multiplane(plane_origin=[0.0, 0, 0],
                                           plane_normal=[1, 0, 0],
                                           heights = np.arange(bx[0], bx[1], spacingX))

sectionsY = supportGeom.section_multiplane(plane_origin=[0, 0.0, 0],
                                           plane_normal=[0.0, 1.0, 0],
                                           heights = np.arange(by[0], by[1], spacingY))



import matplotlib .pyplot as plt

from shapely.geometry import Polygon, MultiPolygon
import shapely.affinity

if False:
    poly = shapely.ops.unary_union(sectionsX[5].polygons_closed)

    sliceBBox = poly.bounds

    hole = Polygon([[-1.5, 0], [0,1.], [1.5,0], [0, -1.0], [-1.5,0]])

    holes = []
    i = 1
    for x in np.arange(sliceBBox[0],sliceBBox[2],2.25):
        i += 1
        for y in np.arange(sliceBBox[1], sliceBBox[3], 3):
            y2 = y
            if i % 2:
                holes.append(shapely.affinity.translate(hole, x,y2))
            else:
                holes.append(shapely.affinity.translate(hole, x, y2 + 1.5))

    union_holes = shapely.ops.unary_union(holes)

    section_holes = poly.difference(union_holes)
    support_boundary = poly.difference(poly.buffer(-1.0))
    #trimesh.path.polygons.plot_polygon(support_boundary)
    trimesh.path.polygons.plot_polygon(support_boundary.union(section_holes))
else:
    polys = sectionsX[5].polygons_closed

    supportShapes = []

    for poly in polys:
        sliceBBox = poly.bounds

        hole = Polygon([[-1.5, 0], [0, 1.], [1.5, 0], [0, -1.0], [-1.5, 0]])

        holes = []
        i = 1
        for x in np.arange(sliceBBox[0], sliceBBox[2], 2.25):
            i += 1
            for y in np.arange(sliceBBox[1], sliceBBox[3], 3):
                y2 = y
                if i % 2:
                    holes.append(shapely.affinity.translate(hole, x, y2))
                else:
                    holes.append(shapely.affinity.translate(hole, x, y2 + 1.5))

        union_holes = shapely.ops.unary_union(holes)

        section_holes = poly.difference(union_holes)
        support_boundary = poly.difference(poly.buffer(-1.0))

        supportShapes.append(support_boundary.union(section_holes))

    out = shapely.ops.unary_union(supportShapes)

    trimesh.path.polygons.plot_polygon(out)
s
xSectionMesh = trimesh.Trimesh()
ySectionMesh = trimesh.Trimesh()


#loadedPaths = [trimesh.path.exchange.load.load_path(path) for path in list(out)]
#sectionPath = trimesh.path.util.concatenate(loadedPaths)


for section in sectionsX:
    if section is None:
        continue

    vx,fx = section.triangulate()

    if(len(vx)  == 0):
        continue

    vx = np.insert(vx, 2, values=0.0, axis=1)
    secX = trimesh.Trimesh(vertices=vx, faces=fx)
    secX.apply_transform(section.metadata['to_3D'])
    xSectionMesh += secX

for section in sectionsY:

    if section is None:
        continue


    vy,fy = section.triangulate()

    if (len(vy) == 0):
        continue

    vy = np.insert(vy, 2, values=0.0, axis=1)
    secY = trimesh.Trimesh(vertices=vy, faces=fy)
    secY.apply_transform(section.metadata['to_3D'])
    ySectionMesh += secY

xSectionMesh

print('\t - start intersecting mesh')
# Intersect the projection of the support face with the original part using the Cork Library
xSectionMesh.export('secX.off')
ySectionMesh.export('secY.off')
subprocess.call([CORK_PATH, '-resolve', 'secY.off', 'secX.off', 'merge.off'])
print('\t - finished intersecting mesh')
isectMesh = trimesh.load_mesh('merge.off')
#sectionsX[0].show()
#sectionsY[0].show()

supportGeom.visual.face_colors = [0.0, 1., 0., 0.3]
isectMesh.visual.face_colors = [0, 155, 255, 255]
blockSupportSides.visual.face_colors = [0, 155, 255, 200]

s2 = trimesh.Scene([myPart.geometry, overhangMesh,
                    visualize_support_edges, edge_supports,
                    visualize_support_pnts,
                    blockSupportSides, isectMesh]) # , overhangMesh] + supportExtrudes)
#s2.show()

s2.show()

isectMesh += blockSupportSides

isectMesh = blockSupportMesh + myPart.geometry

# Obtain the 2D Planar Section at this Z-position
sections = isectMesh.section(plane_origin=[0.0, 0, 10.0], plane_normal=[0, 0, 1])
blockSupportMesh
transformMat = np.array(([1.0, 0.0, 0.0, 0.0],
                         [0.0, 1.0, 0.0, 0.0],
                         [0.0, 0.0, 1.0, 0.0],
                         [0.0, 0.0, 0.0, 1.0]), dtype=np.float32)

planarSection, transform = sections.to_planar(transformMat, normal=[1,0,0])
sections.show()

