"""
Provides supporting functions to generate geometry for support structures
"""

try:
    import triangle

except BaseException as E:
    raise BaseException("Lib Triangle is required to use this Support.geometry submodule")


import subprocess
import numpy as np
import trimesh
from pyslm import pyclipper
import shapely.geometry.polygon

from typing import Optional, Tuple, List

def extrudeFace(extrudeMesh: trimesh.Trimesh, height: Optional[float] = None, heightArray: Optional[np.ndarray] = None) -> trimesh.Trimesh:
    """
    Extrudes a set of connected triangle faces into a prism. This is based on a constant height - or a height array
    for corresponding to extrusions to be added to each triangular facet.

    :param faceMesh: A mesh consisting of *n* triangular faces to extrude
    :param height: A constant height to use for the prism extrusion
    :param heightArray: Optional array consisting of *n* heights to extrude each triangular facet
    :return: The extruded prism mesh
    """
    faceMesh = extrudeMesh.copy()

    # Locate boundary nodes/edges of the support face
    interiorEdges = faceMesh.face_adjacency_edges
    aset = set([tuple(x) for x in faceMesh.edges])
    bset = set([tuple(x) for x in interiorEdges])  # Interior edges
    # cset = aset.difference(bset)
    # boundaryEdges = np.array([x for x in aset.difference(bset)])

    # Deep copy the vertices from the face mesh
    triVertCpy = faceMesh.vertices.copy()

    if height is not None:
        triVertCpy[:, 2] = height
    elif heightArray is not None:
        triVertCpy[:, 2] = heightArray
    else:
        triVertCpy[:, 2] = -0.1

    meshInd = np.array([]).reshape((0, 3))
    meshVerts = np.array([]).reshape((0, 3))

    # Count indicator increases the triangle index upon each loop iteration
    cnt = 0

    # All projected faces are guaranteed to intersect with face
    for i in range(0, faceMesh.faces.shape[0]):
        # extrude the triangle based on the ray length
        fid = faceMesh.faces[i, :]
        tri_verts = np.array(faceMesh.vertices[fid, :])

        # Create a tri from intersections
        meshVerts = np.vstack([meshVerts, tri_verts, triVertCpy[fid, :]])

        # Always create the bottom and top faces
        triInd = np.array([(0, 1, 2),  # Top Face
                           (4, 3, 5)  # Bottom Face
                           ])

        edgeA = {(fid[0], fid[1]), (fid[1], fid[0])}
        edgeB = {(fid[0], fid[2]), (fid[2], fid[0])}
        edgeC = {(fid[1], fid[2]), (fid[2], fid[1])}

        if len(edgeA & bset) == 0:
            triInd = np.vstack([triInd, ((0, 3, 4), (1, 0, 4))])  # Side Face (A)

        if len(edgeB & bset) == 0:
            triInd = np.vstack([triInd, ((0, 5, 3), (0, 2, 5)) ]) # Side Face (B)

        if len(edgeC & bset) == 0:
            triInd = np.vstack([triInd, ((2, 1, 4), (2, 4, 5))])  # Side Face (C)

        triInd += cnt * 6
        cnt += 1

        meshInd = np.vstack((meshInd, triInd))

    # Generate the extrusion
    extMesh = trimesh.Trimesh(vertices=meshVerts, faces=meshInd, validate=True, process=True)
    extMesh.fix_normals()

    return extMesh


def boolUnion(meshA, meshB, CORK_PATH):

    if isinstance(meshA, trimesh.Trimesh):
        meshA.export('a.off')

    if isinstance(meshB, trimesh.Trimesh):
        meshA.export('b.off')

    subprocess.call([CORK_PATH, '-union', 'b.off', 'a.off', 'c.off'])
    return trimesh.load_mesh('c.off')


def boolIntersect(meshA, meshB, CORK_PATH):

    if isinstance(meshA, trimesh.Trimesh):
        meshA.export('a.off')

    if isinstance(meshB, trimesh.Trimesh):
        meshA.export('b.off')

    subprocess.call([CORK_PATH, '-isct', 'a.off', 'b.off', 'c.off'])
    return trimesh.load_mesh('c.off')

def boolDiff(meshA, meshB, CORK_PATH):

    if isinstance(meshA, trimesh.Trimesh):
        meshA.export('a.off')

    if isinstance(meshB, trimesh.Trimesh):
        meshA.export('b.off')

    subprocess.call([CORK_PATH, '-diff', 'a.off', 'b.off', 'c.off'])
    return trimesh.load_mesh('c.off')


def createPath2DfromPaths(paths: List[np.ndarray]) -> trimesh.path.Path2D:
    """
    A static helper function that converts PyClipper Paths into a single :class:`trimesh.path.Path2D` object. This
    function is not used for performance reasons, but provides additional capability if required.

    :param paths: A list of paths generated from ClipperLib paths.
    :return: A Path2D object containing a list of Paths.
    """
    loadedLinePaths = [trimesh.path.exchange.misc.lines_to_path(path) for path in list(paths)]
    loadedPaths = [trimesh.path.Path2D(**path, process=False) for path in loadedLinePaths]

    sectionPath = trimesh.path.util.concatenate(loadedPaths)
    return sectionPath


def path2DToPathList(shapes: List[shapely.geometry.polygon.Polygon]) -> List[np.ndarray]:
    """
    Returns the list of paths and coordinates from a cross-section (i.e. :class:`Trimesh.path.Path2D` objects).
    This is required to be done for performing boolean operations and offsetting with the internal PyClipper package.

    :param shapes: A list of :class:`shapely.geometry.polygon.Polygon` representing a cross-section or container of
                    closed polygons
    :return: A list of paths (Numpy Coordinate Arrays) describing fully closed and oriented paths.
    """

    paths = []

    for poly in shapes:
        coords = np.array(poly.exterior.coords)
        paths.append(coords)

        for path in poly.interiors:
            coords = np.array(path.coords)
            paths.append(coords)

    return paths


def sortExteriorInteriorRings(polyNode,
                              closePolygon: Optional[bool] = False) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """
    A recursive function that sorts interior and exterior rings or paths from PyClipper :class:`pyclipper.PyPolyNode`
    objects.

    :param closePolygon: If `True`, the contours are closed
    :param polyNode: The PyPolyNode tree defining the polygons and interior holes
    :return: A tuple consisting of exterior and interior rings
    """

    import pyslm.hatching

    exteriorRings = []
    interiorRings = []

    if polyNode.Contour:

        contour = pyslm.hatching.BaseHatcher.scaleFromClipper(polyNode.Contour)

        if closePolygon:
            contour.append(contour[0])

        contour = np.array(contour)[:, :2]

        if polyNode.IsHole:
            interiorRings.append(contour)
        else:
            exteriorRings.append(contour)

    for node in polyNode.Childs:

        exteriorChildRings, interiorChildRings = sortExteriorInteriorRings(node, closePolygon)

        exteriorRings += exteriorChildRings
        interiorRings += interiorChildRings

    return exteriorRings, interiorRings

def triangulatePolygon(section) -> Tuple[np.ndarray, np.ndarray]:
    """
    Function triangulates polygons generated natively by PyClipper, from :class:`pyclipper.PyPolyNode` objects.
    This is specifically used to optimally generate the polygon triangulations using an external triangulation
    library Mapbox using the Ear Clipping algorithm - see :link:`Mapbox <https://github.com/mapbox/earcut.hpp>`_ and
    the :link:`Ear-Cut <https://pypi.org/project/mapbox-earcut/>`_ PyPi package .

    By using the PyPolyNode object, ClipperLib automatically generates a polygon hierarchy tree for separating both
    external contours and internal holes, which can be passed directly to the earcut algorithm. Otherwise, this
    requires passing all paths and sorting these to identify interior holes.

    :param section: A :class:`pyclipper.PyPolyNode` oject containing a collection of polygons
    :return: A tuple of vertices and faces generated from the triangulation
    """

    try:
        from mapbox_earcut import triangulate_float32
    except BaseException as E:
        raise Exception("Ensure mapbox-earcut package has been installed in order to use the support module")

    vertIdx = 0
    meshFaces = []
    meshVerts = []

    meshes = []

    """
    For multiple polygons, we know the exteriors must not overlap therefore they can be treat as independent meshes
    when they sorted    
    """
    for polygon in section.Childs:

        exterior, interior = sortExteriorInteriorRings(polygon)

        exteriorPath2D = np.array(exterior[0])[:, :2]

        interiorPath2D = []
        for path in interior:
            coords = np.array(path)[:, :2]
            interiorPath2D.append(coords)

        # get vertices as sequence where exterior is the first value
        vertices = [np.array(exteriorPath2D)]
        vertices.extend(np.array(i) for i in interiorPath2D)
        # record the index from the length of each vertex array
        rings = np.cumsum([len(v) for v in vertices])
        # stack vertices into (n, 2) float array

        triVerts = np.vstack(vertices)

        # run triangulation
        triangFaces = triangulate_float32(triVerts, rings).reshape( (-1, 3)).astype(np.int64).reshape((-1, 3))
        triFaces = triangFaces + vertIdx

        meshFaces.append(triFaces)
        meshVerts.append(triVerts)
        vertIdx += len(triVerts)

        # Save below as a reference in the future if required
        #vy = np.insert(triVerts, 2, values=0.0, axis=1)
        #meshes.append(trimesh.Trimesh(vertices=vy, faces=triangFaces))


    meshFaces = np.vstack(meshFaces)
    meshVerts = np.vstack(meshVerts)

    #mesh = trimesh.util.concatenate(meshes)
    return meshVerts, meshFaces


def generatePolygonBoundingBox(bbox: np.ndarray) -> shapely.geometry.polygon.Polygon:
    """
    Generates a shapely Polygon bounding box based on the bounding box of an object

    :param bbox: The bounding Box of the Polygon
    :return: A 2D polygon representing the bounding box
    """

    bx = bbox[:, 0]
    by = bbox[:, 1]
    bz = bbox[:, 2]

    a = [np.min(bx), np.max(bx)]
    b = [np.min(by), np.max(by)]

    # Create a closed polygon representing the transformed slice geometry
    bboxPoly = shapely.geometry.polygon.Polygon([[a[0], b[0]],
                                                 [a[0], b[1]],
                                                 [a[1], b[1]],
                                                 [a[1], b[0]],
                                                 [a[0], b[0]]])

    return bboxPoly