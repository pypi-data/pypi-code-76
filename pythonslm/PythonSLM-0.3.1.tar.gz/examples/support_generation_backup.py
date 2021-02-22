""" Support generation script - 01/08/2020"""
import os
import subprocess
import random

import trimesh
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import skimage.measure

import shapely.geometry
import shapely.affinity
from shapely.ops import unary_union

from pyslm.core import Part
import pyslm.support


def extrudeFace(supportFaceMesh, height=None, heightArray=None):
    # Locate boundary nodes/edges of the support face
    interiorEdges = supportFaceMesh.face_adjacency_edges
    aset = set([tuple(x) for x in supportFaceMesh.edges])
    bset = set([tuple(x) for x in interiorEdges])  # Interior edges
    # cset = aset.difference(bset)
    # boundaryEdges = np.array([x for x in aset.difference(bset)])

    meshInd = np.array([]).reshape((0, 3))
    meshVerts = np.array([]).reshape((0, 3))
    cnt = 0

    triHitLocCpy = supportFaceMesh.vertices.copy()

    if height is not None:
        triHitLocCpy[:, 2] = height
    elif heightArray is not None:
        triHitLocCpy[:, 2] = heightArray
    else:
        triHitLocCpy[:, 2] = -0.1

    # All projected faces are guaranteed to intersect with face
    for i in range(0, supportFaceMesh.faces.shape[0]):
        # extrude the triangle based on the ray length
        fid = supportFaceMesh.faces[i, :]
        tri_verts = np.array(supportFaceMesh.vertices[fid, :])

        # Create a tri from intersections
        meshVerts = np.vstack([meshVerts, tri_verts, triHitLocCpy[fid, :]])

        # Always create the bottom and top faces
        triInd = np.array([(0, 1, 2),  # Top Face
                           (4, 3, 5)  # Bottom Face
                           ])

        edgeA = set([(fid[0], fid[1]),
                     (fid[1], fid[0])])

        if len(edgeA & bset) == 0:
            triInd = np.vstack([triInd,
                                np.array([(0, 3, 4), (1, 0, 4)])  # Side Face (A)
                                ])

        edgeB = set([(fid[0], fid[2]),
                     (fid[2], fid[0])])

        if len(edgeB & bset) == 0:
            triInd = np.vstack([triInd,
                                np.array([
                                    (0, 5, 3), (0, 2, 5)])  # Side Face (B)
                                ])

        edgeC = set([(fid[1], fid[2]),
                     (fid[2], fid[1])])

        if len(edgeC & bset) == 0:
            triInd = np.vstack([triInd,
                                np.array([
                                    (2, 1, 4), (2, 4, 5)])  # Side Face (C)
                                ])

        triInd += cnt * 6
        cnt += 1

        meshInd = np.vstack((meshInd, triInd))

    extMesh = trimesh.Trimesh(vertices=meshVerts,
                              faces=meshInd,
                              validate=True,
                              process=True)

    extMesh.fix_normals()
    return extMesh


## CONSTANTS ####
CORK_PATH = '/home/lparry/Development/src/external/cork/bin/cork'
MIN_SUPPORT_AREA = 10  # mm2
SUPPORT_EDGE_GAP = 1  # mm  - offset between part supports and baseplate supports
PART_SUPPORT_OFFSET_GAP = 1  # mm  - offset between part supports and baseplate supports
BASE_PLATE_SUPPORT_DISTANCE = 5  # mm  - Distance between lowest point of part and baseplate
OVERHANG_ANGLE = 45  # deg - Overhang angle
RAY_RES = 1  # mm

myPart = Part('myPart')
myPart.setGeometry("../models/frameGuide.stl")
myPart.rotation = [-60.0, 20.0, -10.0]
myPart.dropToPlatform()

""" Extract the overhang mesh - don't explicitly split the mesh"""
overhangMesh = pyslm.support.getOverhangMesh(myPart, OVERHANG_ANGLE, False)
overhangMesh.visual.face_colors = [1.0, 0., 0., 1.0]

# split the mesh
overhangSubregions = overhangMesh.split(only_watertight=False)

rays = []
myExtrusions = []

myPart.geometry.export('part.off')

numcnt = 10

""" Process sub-regions"""
for subregion in overhangSubregions:
    print('processed subregion')

    supportRegion = subregion.copy()

    poly = subregion.outline()

    minHeight = float(np.min(poly.vertices[:, 2]))
    avgHeight = float(np.mean(poly.vertices[:, 2]))
    maxHeight = float(np.max(poly.vertices[:, 2]))
    poly.vertices[:, 2] = minHeight - 0.5

    flattenPath, bd = poly.to_planar()
    flattenPath.process()

    polygon = flattenPath.polygons_full[0]

    offsetShape = polygon.buffer(-SUPPORT_EDGE_GAP)

    if offsetShape is None or offsetShape.area < 1e-4:
        continue

    offsetPoly = trimesh.load_path(offsetShape)
    offsetPoly.apply_translation(np.array([bd[0, 3], bd[1, 3]]))

    verts, tris = offsetPoly.triangulate()

    verts3d = np.hstack((verts, np.tile(0, [verts.shape[0], 1])))
    anchorFaceMesh = trimesh.Trimesh(vertices=verts3d,
                                     faces=tris)

    # Create an extrusion at the vertical extent of the part
    extruMesh = extrudeFace(supportRegion.copy(), 0.0)
    extruMesh.vertices[:, 2] = extruMesh.vertices[:, 2] - 0.01

    # extruMesh.apply_transform(bd) # Inverse transform needed to return polygon to

    # Intersect the projection of the support face with the original part using the Cork Library
    extruMesh.export('downProjExtr.off')
    subprocess.call([CORK_PATH, '-isct', 'part.off', 'downProjExtr.off', 'c.off'])

    """
    Note the cutMesh is the project down from the support surface with the original mesh
    """
    cutMesh = trimesh.load_mesh('c.off')

    if len(cutMesh.faces) == 0:
        myExtrusions.append(extruMesh)
        continue  # No intersection had taken place

    res = 0.2

    # Rasterise the surface of overhang to generate projection points
    supportArea = np.array(offsetPoly.rasterize(res, offsetPoly.bounds[0, :])).T

    coords = np.argwhere(supportArea).astype(np.float32) * res
    coords += offsetPoly.bounds[0, :] + 0.0001  # An offset is required due to rounding error

    """
    Project upwards to intersect with the upper surface
    """

    # Set the z-coordinates for the ray origin
    coords = np.hstack([coords, np.tile(-1e5, [coords.shape[0], 1])])
    rays = np.tile(np.array([[0., 0., 1.0]]), (coords.shape[0], 1))

    # Find the first location of any triangles which intersect with the part
    hitLoc, index_ray, index_tri = supportRegion.ray.intersects_location(ray_origins=coords,
                                                                         ray_directions=rays,
                                                                         multiple_hits=False)

    hitLocCpy = hitLoc.copy()
    hitLocCpy[:, :2] -= offsetPoly.bounds[0, :]
    hitLocCpy[:, :2] /= res

    hitLocIdx = np.ceil(hitLocCpy[:, :2]).astype(np.int32)

    coords2 = coords.copy()

    coords2[index_ray, 2] = 1e7
    rays[:, 2] = -1.0

    # If any verteces in triangle there is an intersection
    # Find the first location of any triangles which intersect with the part
    hitLoc2, index_ray2, index_tri2 = cutMesh.ray.intersects_location(ray_origins=coords2,
                                                                      ray_directions=rays,
                                                                      multiple_hits=False)

    hitLocCpy2 = hitLoc2.copy()
    # Update the xy coordinates
    hitLocCpy2[:, :2] -= offsetPoly.bounds[0, :]
    hitLocCpy2[:, :2] /= res
    hitLocIdx2 = np.ceil(hitLocCpy2[:, :2]).astype(np.int32)

    # Create a height map of the projection rays
    heightMap = np.ones(supportArea.shape) * -1.0
    heightMap2 = np.ones(supportArea.shape) * -1.0
    # Assign the heights
    heightMap[hitLocIdx[:, 0], hitLocIdx[:, 1]] = hitLoc[:, 2]

    # Assign the heights based on the lower projection
    heightMap[hitLocIdx2[:, 0], hitLocIdx2[:, 1]] = hitLoc2[:, 2]

    vx, vy = np.gradient(heightMap)
    grads = np.sqrt(vx ** 2 + vy ** 2)

    """
    Find the outlines of any regions of the height map which deviate significantly
    This is used to seperate both self-intersecting supports and those which are simply connected to the base-plate
    """
    outlines = skimage.measure.find_contours(grads, 0.5)

    if numcnt < 1000:
        pass
    else:
        plt.figure()
        plt.imshow(grads)
        plt.contour(grads, 0.5, linewidths=2.0, colors='white')
        plt.figure()
        plt.imshow(heightMap.T)
        plt.figure()
        plt.imshow(grads.T)

        for outline in outlines:
            plt.plot(outline[:, 0], outline[:, 1])

    numcnt += 1

    for outline in outlines:

        """
        Process the outline by finding the boundaries
        """
        outline = outline * res + offsetPoly.bounds[0, :]
        outline = skimage.measure.approximate_polygon(outline, tolerance=res)

        if outline.shape[0] < 3:
            continue

        """
        Process the polygon
        ---------------------
        Create a shapley polygon  and offset the boundary
        """
        mergedPoly = trimesh.load_path(outline)

        if not mergedPoly.is_closed or len(mergedPoly.polygons_full) == 0:
            continue

        if mergedPoly.polygons_full[0] is None:
            continue

        bufferPoly = mergedPoly.polygons_full[0].buffer(-0.1)

        if bufferPoly.area < 0.1:
            continue

        arg = trimesh.creation._polygon_to_kwargs(bufferPoly)

        """
        Triangulate the polygon into a planar mesh
        """
        from triangle import triangulate

        # arg['vertices'] = np.vstack([arg['vertices'], points])
        result = triangulate(arg, 'pa{:.3f}'.format(1))

        # Project the vertices downward (-z) to intersect with the cutMesh
        coords = np.hstack([result['vertices'], np.tile(0.0, (result['vertices'].shape[0], 1))])

        """
        Project upwards to intersect with the upper surface
        """
        ray_dir = np.tile(np.array([[0., 0., 1.0]]), (coords.shape[0], 1))

        # Find the first location of any triangles which intersect with the part
        hitLoc, index_ray, index_tri = supportRegion.ray.intersects_location(ray_origins=coords,
                                                                             ray_directions=ray_dir,
                                                                             multiple_hits=False)

        coords2 = coords.copy()
        coords2[index_ray, 2] = hitLoc[:, 2] + 0.1

        ray_dir[:, 2] = -1.0

        """
        Intersecting with cutmesh is more efficient when projecting downwards
        """
        hitLoc2, index_ray2, index_tri2 = cutMesh.ray.intersects_location(ray_origins=coords2,
                                                                          ray_directions=ray_dir,
                                                                          multiple_hits=False)
        if len(hitLoc) != len(coords) or len(hitLoc2) != len(hitLoc):
            # The projections up and down do not match indiciating some flaw
            print(hitLoc.shape, hitLoc2.shape, coords.shape)

            if len(hitLoc2) == 0:
                # Base plate
                hitLoc2 = coords2.copy()
                hitLoc2[:, 2] = 0.0

                print('CREATING BASE-PLATE SUPPORT')
            else:
                raise ValueError('Projections do not match')

        # Create a surface from the Ray intersection
        surf2 = trimesh.Trimesh(vertices=coords2, faces=result['triangles'])

        # Extrude the surface based on the heights from the second ray cast
        newShapes = extrudeFace(surf2, None, hitLoc2[:, 2] + 0.05)

        """
        Take the near net-shape support and obtain the difference with the original part to get clean boundaries for the support
        """

        newShapes.export('b.off')
        subprocess.call([CORK_PATH, '-diff', 'b.off', 'part.off', 'c.off'])
        cutMesh2 = trimesh.load_mesh('c.off')

        # Draw the support structures generated
        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255]
        cutMesh2.visual.face_colors = color
        myExtrusions.append(cutMesh2)

    print('processed support face')

    continue

    # Process any baseplate supports - offsetting any previous connected support regions
    offsetShape2 = shapely.affinity.translate(offsetShape, bd[0, 3], bd[1, 3])

    if outline is None:
        basePlateExtrOutlineGeoms = offsetShape2
    else:
        basePlateExtrOutlineGeoms = offsetShape2.difference(outline.buffer(PART_SUPPORT_OFFSET_GAP))

    geoms = []
    if isinstance(basePlateExtrOutlineGeoms, shapely.geometry.polygon.Polygon):
        geoms.append(basePlateExtrOutlineGeoms)

    else:
        geoms = basePlateExtrOutlineGeoms.geoms

    print('Generating  base supports', len(geoms))

    for basePlateExtrOutline in geoms:
        if basePlateExtrOutline.area < MIN_SUPPORT_AREA:
            continue

        basePlateExtrPoly = trimesh.load_path(basePlateExtrOutline)
        # Extrude the polygon to intersect with the support surface
        # TODO check if distance is suitable
        newShape = basePlateExtrPoly.extrude(maxHeight + 5)

        # Calculate the difference bteween the bodies
        newShape.export('b.off')
        subprocess.call([CORK_PATH, '-diff', 'b.off', 'part.off', 'c.off'])
        cutMesh2 = trimesh.load_mesh('c.off')

        bodies = cutMesh2.split()

        print('len bodies', len(bodies))
        dist = np.inf
        supBody2 = None

        # For all bodies, the one with the closest maximum distance is most likely to be connected to the support face
        # TODO use projection method to determine the distance
        for body in bodies:
            distance = np.abs(np.max(body.vertices[:, 2]) - avgHeight)
            if distance < dist:
                supBody2 = body
                dist = distance

        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255]

        supBody2.visual.face_colors = color
        myExtrusions.append(supBody2)
    #    except:
    #        print('exception 2')
    #        continue

    # plt.plot(coord[:,0], coord[:,1])

    # Create bodies for supports extending to the baseplate

    origins = anchorFaceMesh.triangles_center
    # origins = shape3D.vertices
    # origins =  trimesh.sample.sample_surface_even(subregion, 100)[0]

    origins[:, 2] -= 0.05
    ray_dir = np.tile(np.array([[0., 0., -1.0]]), [origins.shape[0], 1])

    # Find the first location of any triangles which intersect with the part
    locations, index_ray, index_tri = myPart.geometry.ray.intersects_location(ray_origins=origins,
                                                                              ray_directions=ray_dir,
                                                                              multiple_hits=False)

    # Support face mesh is the triangulated surface to be projected below
    supportFaceMesh = trimesh.Trimesh(vertices=anchorFaceMesh.vertices,
                                      faces=anchorFaceMesh.faces[index_ray, :],
                                      process=False)

    # myExtrusions.append(cutMesh)

    # myPart.geometry.visual.face_colors[index_tri,:] = 255.0 *np.array([0.0 ,0.0 , 1.0, 1.0])

    ia = np.indices(origins.shape)

    anchorFaceMesh = trimesh.Trimesh(vertices=myPart.geometry.vertices,
                                     faces=myPart.geometry.faces[index_tri, :],
                                     process=False)

    subMeshes = anchorFaceMesh.split(only_watertight=False)

    print('num anchor meshes {:d}', anchorFaceMesh.body_count)

    if len(index_ray) > 0:
        rays.append(np.hstack((origins[index_ray], locations)))

# rays = np.vstack(rays)
# baseplateRays = np.vstack(baseplateRays)
# ray_visualize = trimesh.load_path((rays).reshape(-1, 2, 3))
# basePlateRays_visualize = trimesh.load_path((baseplateRays).reshape(-1, 2, 3))


s = trimesh.Scene([overhangMesh, myPart.geometry] + myExtrusions)
# open the scene viewer and move a ball around
s.show(viewer='gl')

overhangMesh.export('testSupport.ply');
# myPart.draw()
