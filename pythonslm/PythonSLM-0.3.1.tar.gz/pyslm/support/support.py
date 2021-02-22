"""
Provides classes  and methods for the creation of support structures in Additive Manufacturing.
"""

import abc
from typing import Any, Optional, List, Tuple, Union
import subprocess
import warnings

from scipy import interpolate
from skimage.measure import approximate_polygon, find_contours
import shapely.geometry
from shapely.geometry import Polygon
import shapely.affinity

import numpy as np
import trimesh

from pyslm import pyclipper

from ..core import Part
from .utils import *
from .geometry import *
from ..hatching import BaseHatcher, utils


class SupportStructure(abc.ABC):
    """
    The Support Structure is the base class representing all definitions of support structures used in PySLM.
    This includes attributes that link to the source part and the original support faces or features of an object and
    shared utility methods for the calculation of useful properties.

    It stores properties that describe the type of support identified during its generation and stores relevant data
    connecting this such as the original support surface (:attr:`supportSurface`) and
    the support object or part (:attr:`supportObject`) and if the suport self-intersects with
    the part (:attr:`supportObject`).
    """
    def __init__(self):
        self._supportSurface = None
        self._supportObject = None
        self._intersectsPart = False

    def __str__(self):
        return 'SupportStructure'

    @abc.abstractmethod
    def geometry(self) -> trimesh.Trimesh:
        """
        Returns the geometry representing the support structure
        """
        raise ValueError('Geometry property is an abstract method')

        return None

    @staticmethod
    def flattenSupportRegion(region):
        """
        The function takes a support surfaces and flattens this as a projected polygon.

        :param region: The support surface as a :class:`trimesh.Trimesh` mesh
        :return: The 2D Polygon of the flattened surface
        """

        supportRegion = region.copy()

        """ Extract the outline of the overhang mesh region"""
        poly = supportRegion.outline()

        """ Convert the line to a 2D polygon"""
        poly.vertices[:, 2] = 0.0

        flattenPath, polygonTransform = poly.to_planar()
        flattenPath.process()

        flattenPath.apply_translation(polygonTransform[:2, 3])  # np.array([polygonTransform[0, 3],
        # polygonTransform[1, 3]]))
        polygon = flattenPath.polygons_full[0]

        return polygon

    def projectedSupportArea(self) -> float:
        """
        Convenience function returns the total projected surface area of the support.

        :return:  The total projected (flattened) surface support area
        """
        if self._supportSurface:
            return self.flattenSupportRegion(self._supportSurface).area
        else:
            return 0.0

    def supportArea(self) -> float:
        """
        Convenience function returns the total surface area  of the support region.

        :return:  The total surface area of the support
        """

        return self._supportSurface.area if self._supportSurface else 0.0

    @property
    def intersectsPart(self) -> bool:
        """ Does the projected support structure intersect with the originating part """
        return self._intersectsPart

    @intersectsPart.setter
    def intersectsPart(self, state : bool):
        self._intersectsPart = state

    @property
    def supportSurface(self) -> trimesh.Trimesh:
        """ The support surface identified on the originating part """
        return self._supportSurface

    @supportSurface.setter
    def supportSurface(self, surface: trimesh.Trimesh):
        self._supportSurface = surface

    @property
    def supportObject(self):
        """ The originating object that the support structure is generated for """
        return self._supportObject

    @supportObject.setter
    def supportObject(self, obj):
        self._supportObject = obj


class BlockSupportBase(SupportStructure):
    """
    The BlockSupport is a base class representing a single block region. This enables different support structures to be
    generated from the core block extrusion.
    """

    def __init__(self):
        super().__init__()

        self._supportVolume = None

    def geometry(self) -> trimesh.Trimesh:
        raise ValueError('Must be re-implemented in a derived class')

    @property
    def supportVolume(self) -> trimesh.Trimesh:
        """
        The support volume stores the 3D mesh geometry representing an extruded geometry projected onto either the
        part surface or build-plate (z=0). This is generated externally in :class:`BlockSupportGenerator` and the
        resultant block 3D geometry is stored in this property.
        """
        return self._supportVolume

    @supportVolume.setter
    def supportVolume(self, supportVolume: trimesh.Trimesh):
        self._supportVolume = supportVolume

    def __str__(self):
        return 'BlockSupport'

    @property
    def supportBoundary(self) -> trimesh.Trimesh:
        """
        The boundary or vertical walls of the support volume.
        """

        blockSupportSides = self._supportVolume.copy()
        sin_theta = getFaceZProjectionWeight(blockSupportSides)

        blockSupportSides.update_faces(sin_theta > (1.0-1e-4))
        blockSupportSides.remove_unreferenced_vertices()

        return blockSupportSides

    @staticmethod
    def triangulateSections(sections) -> trimesh.Trimesh:
        """
        A static method to take a collection of section slice or cross-section and triangulate them into a combined mesh.
        The triangulated meshed are then transformed based on the original transformation generated internally when using
        :meth:`trimesh.Trimesh.section`.

        :param sections: The sections to triangulate into a mesh
        :return: A mesh containing the  concatenated triangulated polygon sections
        """
        sectionMesh = trimesh.Trimesh()

        for section in sections:
            if section is None:
                continue

            v, f = section.triangulate()

            if len(v) == 0:
                continue

            v = np.insert(v, 2, values=0.0, axis=1)
            sec = trimesh.Trimesh(vertices=v, faces=f)
            sec.apply_transform(section.metadata['to_3D'])
            sectionMesh += sec

        return sectionMesh


class GridBlockSupport(BlockSupportBase):
    """
    Represents a block support that internally generates a grid truss structure representing the support structure. The
    grid is generated by taking a sequence of cross-sections at a fixed distance (:attr:`~GridBlockSupport.gridSpacing`)
    from the generated support volume (:attr:`BlockSupportBase.supportVolume`).

    The 2D slices along the grid are generated in :meth:`generateSupportSlices` created a 2D grid of
    cross-sections as polygons. These polygon slices can then be designed to include  patterns such as perforation holes
    or a truss network. Potentially the 2D slices may be extruded and offset to increase the support strength,
    if required.

    A truss network is generated to reduce the amount of support material processed, but additionally provides internal
    perforations which aid powder support removal after production. The truss network in 2D is generated
    along with supporting functions for creating a mesh.

    The truss is designed to self-intersect at set distance based on both the :attr:`trussAngle` and
    the :attr:`gridSpacing` so that they combine together as a consistent support mesh. Upon
    generating a polygon for each support slice, this is triangulated via :meth:`triangulatePolygon`
    to create a mesh which may be sliced and hatched later.
    """
    def __init__(self):
        super().__init__()

        self._gridSpacing = [3,3]
        self._gridTemplate = None
        self._generateSupportBorder = True
        self._mergeMesh = False
        self._supportBorderDistance = 3.0
        self._trussWidth = 1.0
        self._trussAngle = 45

    def geometry(self) -> trimesh.Trimesh:
        """
        The geometry for the support structure. This resolve sthe  entire connectivity of the support truss
        meshes used by performing a boolean Union operation on the collection of meshes generated when the
        attribute :attr:`mergeMesh` option is set :code:`True`. Otherwise, the truss structure is mergeed
        as overlapping and non-connected meshes into a single :class:`trimesh.Trimesh` mesh..

        :return: The support geometry mesh
        """
        slicesX, slicesY = self.generateSupportSlices()
        supportBorder = self.generateSupportBorder()

        if self._mergeMesh:
            # print('\t - start intersecting mesh')
            # Intersect the projection of the support face with the original part using the Cork Library
            slicesX.export('secX.off')
            slicesY.export('secY.off')
            subprocess.call([BlockSupportGenerator.CORK_PATH, '-resolve', 'secY.off', 'secX.off', 'merge.off'])
            #print('\t - finished intersecting mesh')
            isectMesh = trimesh.load_mesh('merge.off')

            isectMesh += supportBorder
        else:
            isectMesh =  slicesX + slicesY + supportBorder

        isectMesh.visual.face_colors[:, :3] = np.random.randint(254, size=3)
        return isectMesh

    @property
    def mergeMesh(self) -> bool:
        """
        Determines if the support truss geometry should be merged together into a connected unified mesh"
        """
        return self._mergeMesh

    @mergeMesh.setter
    def mergeMesh(self, state: bool):
        self._mergeMesh = state

    @property
    def trussWidth(self) -> float:
        """
        The width of a strut in the truss network
        """
        return self._trussWidth

    @trussWidth.setter
    def trussWidth(self, width: float):
        self._trussWidth = width

    @property
    def supportBorderDistance(self) -> float:
        """
        The offset used when generating a border or support skin for each truss slice in the support block.
        """
        return self._supportBorderDistance

    @supportBorderDistance.setter
    def supportBorderDistance(self, distance: float):
        self._supportBorderDistance = distance

    @property
    def trussAngle(self) -> float:
        """ The angle (degrees) used for generating the truss structures used in the support structure """
        return self._trussAngle

    @trussAngle.setter
    def trussAngle(self, angle: float):
        self._trussAngle = angle

    @property
    def gridSpacing(self) -> List[float]:
        """ The spacing of the grid truss structure within the block support """
        return self._gridSpacing

    @gridSpacing.setter
    def gridSpacing(self, spacing: List[float]):
        """ The Grid Spacing used for the support structure """
        self._gridSpacing = spacing

    def __str__(self):
        return 'GridBlockSupport'

    @staticmethod
    def holeGeometry():
        return Polygon([[-1.5, 0], [0, 1.], [1.5, 0], [0, -1.0], [-1.5, 0]])

    @staticmethod
    def clipLines(paths: Any, lines: np.ndarray) -> List[np.ndarray]:
        """
        Clips a series of lines (hatches) across a closed polygon or set of paths. It is an overloaded function for
        internally clipping hatches according to a PyClipper supported path.

        :param paths: The set of boundary paths for trimming the lines
        :param lines: The un-trimmed lines to clip from the boundary
        :return: A list of trimmed lines (open paths)
        """

        pc = pyclipper.Pyclipper()

        pc.AddPaths(paths, pyclipper.PT_CLIP, True)

        # Reshape line list to create n lines with 2 coords(x,y,z)
        lineList = lines.reshape(-1, 2, 3)
        lineList = tuple(map(tuple, lineList))
        lineList = BaseHatcher.scaleToClipper(lineList)

        pc.AddPaths(lineList, pyclipper.PT_SUBJECT, False)

        # Note open paths (lines) have to used PyClipper::Execute2 in order to perform trimming
        result = pc.Execute2(pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)

        # Cast from PolyNode Struct from the result into line paths since this is not a list
        lineOutput = pyclipper.PolyTreeToPaths(result)

        return BaseHatcher.scaleFromClipper(lineOutput)

    def generateSliceBoundingBoxPolygon(self, section: trimesh.path.Path2D) -> shapely.geometry.polygon.Polygon:
        """
        Generates an equivalent 2D Polygon bounding box of the support geometry volume transformed correctly into the
        local coordinate system of each grid slice by inversion of the internally stored transformation matrix in
        :class:`trimesh.path.Path2D`. This provides a consistent centroid or local origin for generating the truss
        frame across the entire support volume.

        :param section: A :class:`~trimesh.path.Path2D` cross-section consisting of a 3D transformation matrix
        :return: A 2D polygon representing the bounding box of the support geometry volume.
        """

        supportGeom = self._supportVolume
        bbox = np.dot(np.linalg.inv(section.metadata['to_3D'][:3,:3]), supportGeom.bounds.T).T

        bx = bbox[:, 0]
        by = bbox[:, 1]
        bz = bbox[:, 2]

        a = [np.min(bx), np.max(bx)]
        b = [np.min(by), np.max(by)]

        # Create a closed polygon representing the transformed slice geometry
        bboxPoly = Polygon([[a[0], b[0]],
                            [a[0], b[1]],
                            [a[1], b[1]],
                            [a[1], b[0]],
                            [a[0], b[0]]])

        return bboxPoly

    def generateMeshGrid(self, poly: shapely.geometry.polygon.Polygon,
                         hatchSpacing: Optional[float] = 5.0, hatchAngle: Optional[float] = 45.0) -> np.ndarray:
        """
        Generates a grid mesh i.e. a series of hatches to fill a polygon region in order to generate a truss network
        used as part of a support truss structure. The mesh grid is offset to create the truss.

        The polygon bounding box of the :class:`~shapely.geometry.polygon.Polygon` is generated, and the a hatch grid
        with a separation distance of `hatchSpacing` is generated to guarantee filling this bounding box region at
        any required `hatchAngle`.

        :param poly: A :class:`~shapely.geometry.polygon.Polygon` consisting of a polygon or path to fill with hatches
        :param hatchSpacing: The hatch spacing using to generate the truss network
        :param hatchAngle: The hatch angle to generate truss network with
        :return: The hatch lines that completely fills the geometry
        """

        # Hatch angle
        theta_h = np.radians(hatchAngle)  # 'rad'

        # Get the bounding box of the paths
        bbox = np.array(poly.bounds)

        # print('bounding box bbox', bbox)
        # Expand the bounding box
        bboxCentre = np.mean(bbox.reshape(2, 2), axis=0)

        # Calculates the diagonal length for which is the longest
        diagonal = bbox[2:] - bboxCentre
        bboxRadius = np.ceil(np.sqrt(diagonal.dot(diagonal))/hatchSpacing) * hatchSpacing

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

    def generateSliceGeometry(self, section: trimesh.path.Path2D):
        """
        Generates a truss grid used as a 2D slice used for generating a section as part of a support structures.

        :param section: The polygon section of slice through the geometry
        :return: A Trimesh Path2D object of the truss geometry
        """

        if not section:
            return None

        polys = section.polygons_closed

        if len(polys) == 0:
            return None

        """
        Obtain the bounding box of the geometry and then transform this to local slice coordinate system. This is needed
        to ensure that the X and Y slice grids correctly align when the are eventually put together. It is achieved by
        ensuring the centroid of the support volume is used as a consistent origin in both coordinate systems.
        This transforms the support geometry based on the transformation matrix and the original bounds. 
        """

        bboxPoly = self.generateSliceBoundingBoxPolygon(section)

        """
        In order to improve performance we resort to using PyClipper rather than Shapely library routines, as from
        experience this tends to perform slowly during clipping and offset operations, despite a more convenient
        API.
        """

        # Convert the shapley polygons to a path list

        paths = path2DToPathList(polys)

        import pyslm.visualise


        pc = pyclipper.PyclipperOffset()

        # Offset the outer path to provide a clean boundary to work with
        clipPaths = BaseHatcher.scaleToClipper(paths)
        pc.AddPaths(clipPaths, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDPOLYGON)
        outerPaths = pc.Execute(BaseHatcher.scaleToClipper(1e-6))

        # Offset the outer boundary to make the outside
        pc.Clear()

        pc.AddPaths(clipPaths, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
        offsetPathInner = pc.Execute(BaseHatcher.scaleToClipper(-self._supportBorderDistance))

        if len(offsetPathInner) < 1:
            return None

        diag = self._gridSpacing[0] * np.sin(np.deg2rad(self._trussAngle))

        # Generate the mesh grid used for the support trusses and merge the lines together
        hatchesA = self.generateMeshGrid(bboxPoly, hatchAngle=self._trussAngle, hatchSpacing=diag).reshape(-1,2,3)
        hatchesB = self.generateMeshGrid(bboxPoly, hatchAngle=180-self._trussAngle, hatchSpacing=diag).reshape(-1,2,3)
        hatches = np.vstack([hatchesA, hatchesB])

        """
        We clip the truss hatches to remove any that are outside of the boundary in order to remove any elements which
        are not relevant to the structure in order to improve performance later
        """
        hatches2 = self.clipLines(outerPaths, hatches)

        if False:
            for hatch in hatches:
                 plt.plot(hatch[:,0], hatch[:,1])
            plt.scatter(centroid[0], centroid[1])
            plt.plot(box[:,0], box[:,1])

        """
        Offset the hatches to form a truss structure
        """
        pc.Clear()

        for hatch in hatches2:
            hatchPath = BaseHatcher.scaleToClipper(hatch)
            pc.AddPath(hatchPath, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDLINE)

        trussPaths = pc.Execute(BaseHatcher.scaleToClipper(self._trussWidth / 2.0))

        pc2 = pyclipper.Pyclipper()

        """
        Clip or trim the Truss Paths with the exterior of the support slice boundary
        """
        pc2.AddPaths(trussPaths, pyclipper.PT_SUBJECT)
        pc2.AddPaths(outerPaths, pyclipper.PT_CLIP)

        if self._generateSupportBorder:

            trimmedTrussPaths = pc2.Execute(pyclipper.CT_INTERSECTION)

            """
            Generate the support skin
            """
            pc2.Clear()
            pc2.AddPaths(outerPaths, pyclipper.PT_SUBJECT)
            pc2.AddPaths(offsetPathInner, pyclipper.PT_CLIP)
            skinSolutionPaths = pc2.Execute(pyclipper.CT_DIFFERENCE)

            """
            Merge all the paths together 
            """
            pc2.Clear()
            pc2.AddPaths(trimmedTrussPaths, pyclipper.PT_SUBJECT)
            pc2.AddPaths(skinSolutionPaths, pyclipper.PT_CLIP)
            solution = pc2.Execute2(pyclipper.CT_UNION)
        else:
            # Use only the truss paths. This simply exports ClipperLib PolyNode Tree

            trimmedTrussPaths = pc2.Execute2(pyclipper.CT_INTERSECTION)

            solution = trimmedTrussPaths

        trussPaths = solution
        return trussPaths

    def generateSliceGeometry2(self, section):
        """
        Exists as a reference to how this can be performed using Shapely.Geometry.Polygon Objects

        :param section:
        :return:
        """

        if not section:
            return trimesh.path.Path2D()

        polys = section.polygons_closed

        if len(polys) == 0:
            return trimesh.path.Path2D()

        supportShapes = []

        for poly in polys:

            sliceBBox = poly.bounds

            if True:
                hole = self.holeGeometry()

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
            else:
                section_holes = poly.difference(poly.buffer(-self._supportBorderDistance))

            if self._generateSupportBorder:
                support_border = poly.difference(poly.buffer(-self._supportBorderDistance))
                supportShape = support_border.union(section_holes)
            else:
                supportShape = section_holes

            supportShapes.append(supportShape)

        # Merge the Support Geometry
        #sliceGeometry = shapely.ops.unary_union(supportShapes)

        #print('slice geom', supportShapes)
        loadedPaths = [trimesh.path.exchange.load.load_path(path) for path in list(supportShapes)]
        sectionPath = trimesh.path.util.concatenate(loadedPaths)

        return sectionPath

    def generateSupportBorder(self) -> trimesh.Trimesh:
        """
        Generates the border or boundary wall of a block support structure with a truss structure for perforations for
        material removal.

        :return: A :class:`trimesh.Trimesh` object containing the mesh  of the generated support boundary
        """
        blockSupportMesh = self.supportVolume

        """ 
        Extract the top and bottom surfaces of the mesh that are perpendicular to the z direction
        """
        blockSupportSides = blockSupportMesh.copy()
        sin_theta = getFaceZProjectionWeight(blockSupportSides)

        blockSupportSides.update_faces(sin_theta < 0.99999)
        blockSupportSides.remove_unreferenced_vertices()

        # Split the top and bottom surfaces to a path - guaranteed to be a manifold 2D polygon
        supportSurf = blockSupportSides.split(only_watertight=False)

        if len(supportSurf) > 2:
            # TODO - provide a solution for multiple curves (e.g. holes)
            warnings.warn('Warning: number of isolated curves ')
        (top, bottom) = (supportSurf[0], supportSurf[1])

        """
        Swap the curves based on their overall position in their z-position for the support structure boundary. 
        Semantically this makes no difference to the generation of the support structure.
        """
        if bottom.bounds[0,2] > top.bounds[0,2]:
            top, bottom = bottom, top

        topPoly3D = top.outline()
        topVerts = topPoly3D.discrete
        topPoly3Dcpy = topPoly3D.copy()
        topPoly3Dcpy.vertices[:,2] = 0.0

        topXY = topVerts[0][:, :2]
        topZ = topVerts[0][:,2]

        """ Ensure that the Polygon orientation is consistent in a CW fashion.  """
        if not pyclipper.Orientation(topXY):
            topXY = np.flipud(topXY)
            topZ = np.flip(topZ)

        # Record the start position of the first curve for use later
        topStartPos = topXY[0]

        #topXY2 = np.vstack([topXY, topXY[0, :]])
        delta = np.diff(topXY, prepend=topXY[0, :].reshape(1, -1), axis=0)
        dist = np.sqrt(delta[:, 0] * delta[:, 0] + delta[:, 1] * delta[:, 1])

        topPolyX = np.cumsum(dist)
        topPolyY = topZ

        topPolyVerts = np.hstack([topPolyX.reshape(-1, 1), topPolyY.reshape(-1, 1)])

        """
        Complete the bottom section of the support boundary
        """
        bottomPoly3D = bottom.outline()
        bottomPoly3Dcpy = bottomPoly3D.copy()
        bottomPoly3Dcpy.vertices[:,2] = 0.0
        bottomVerts = bottomPoly3D.discrete
        bottomXY = bottomVerts[0][:, :2]
        bottomZ = bottomVerts[0][:, 2]

        """ 
        The Polygon order or orientation has to be consistent with the top curve, since this is not guaranteed 
        automatically by Trimesh. If the orientations are not consistent between the top and bottom curve both the
        (XY,Z) coordinates are flipped.
        """
        if not(pyclipper.Orientation(topXY) and pyclipper.Orientation(bottomXY)):
            bottomXY = np.flip(bottomXY, axis=0)
            bottomZ = np.flip(bottomZ, axis=0)

        """
        The starting pint of the curves are arbitrary set by Trimesh. We use the start point of the previous curve to 
        identify the point. 
        
        Iterate through all the points in the second curve and  find the closest point to the start index in the 
        previous curve based on the distance. The coordinates (both XY, Z) are moved using numpy.roll to move the
        starting point of the curves as close to each other.
        """
        dist = bottomXY - topStartPos
        dist = np.sqrt(dist[:,0]*dist[:,0] + dist[:,1]*dist[:,1])
        startId = np.argmin(dist)
        bottomXY = np.roll(bottomXY, -startId, axis=0)
        bottomZ = np.roll(bottomZ, -startId, axis=0)

        bottomXY2 = np.vstack([bottomXY, bottomXY[0, :]])
        bottomZ = np.append(bottomZ, bottomZ[0])
        delta = np.diff(bottomXY2, prepend=bottomXY2[0, :].reshape(1, -1), axis=0)
        dist = np.sqrt(delta[:, 0] * delta[:, 0] + delta[:, 1] * delta[:, 1])

        bottomPolyX = np.cumsum(dist)
        bottomPolyY = bottomZ
        bottomPolyVerts = np.hstack([bottomPolyX.reshape(-1, 1), bottomPolyY.reshape(-1, 1)])

        """
        Form the polygon for the support boundary
        """
        bottomPolyVerts = np.flip(bottomPolyVerts, axis=0)
        myPolyVerts = np.vstack([topPolyVerts, bottomPolyVerts])
        pc = pyclipper.PyclipperOffset()

        # Offset the outer path to provide a clean boundary to work with
        paths2 = np.hstack([myPolyVerts, np.arange(len(myPolyVerts)).reshape(-1, 1)])
        paths2 = list(map(tuple, paths2))
        clipPaths = BaseHatcher.scaleToClipper(paths2)

        """ 
        Offset the paths interior
        """
        pc.AddPath(clipPaths, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDPOLYGON)
        outerPaths = pc.Execute(BaseHatcher.scaleToClipper(1e-6))

        if False:
            import trimesh.path.traversal
            for path in outerPathsCpy:
                p = np.array(path)[:,:2]
                print(p.shape)
                pd = trimesh.path.traversal.resample_path(p, step=BaseHatcher.scaleToClipper(0.5))

                print(pd.shape)
                outerPaths.append(pd)
                #outerPaths.append(subdivide_polygon(p, degree=1, preserve_ends=True))

        # Offset the outer boundary to make the outside
        pc.Clear()

        pc.AddPaths(outerPaths, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
        offsetPathInner = pc.Execute(BaseHatcher.scaleToClipper(-self._supportBorderDistance))

        diag = self._gridSpacing[0] * np.sin(np.deg2rad(self._trussAngle))

        a = [np.min(myPolyVerts[:,0]), np.max(myPolyVerts[:,0])]
        b = [np.min(myPolyVerts[:,1]), np.max(myPolyVerts[:,1])]

        # Create a closed polygon representing the transformed slice geometry
        bboxPoly = Polygon([[a[0], b[0]],
                            [a[0], b[1]],
                            [a[1], b[1]],
                            [a[1], b[0]], [a[0], b[0]]])

        """
        Generate the mesh grid used for the support trusses and merge the lines together
        """
        hatchesA = self.generateMeshGrid(bboxPoly, hatchAngle=self._trussAngle, hatchSpacing=diag).reshape(-1, 2, 3)
        hatchesB = self.generateMeshGrid(bboxPoly, hatchAngle=180 - self._trussAngle, hatchSpacing=diag).reshape(-1, 2, 3)
        hatches = np.vstack([hatchesA, hatchesB])

        """
        Generate the truss by expanding the lines accordingly
        """
        pc.Clear()

        for hatch in hatches:
            hatchPath = BaseHatcher.scaleToClipper(hatch)
            pc.AddPath(hatchPath, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDLINE)

        trussPaths = pc.Execute(BaseHatcher.scaleToClipper(self._trussWidth / 2.0))

        """
        Clip or trim the Truss Paths with the exterior of the support slice boundary
        """
        pc2 = pyclipper.Pyclipper()

        if self._generateSupportBorder and len(offsetPathInner) > 0:

            pc2.AddPaths(trussPaths, pyclipper.PT_SUBJECT)
            pc2.AddPaths(outerPaths, pyclipper.PT_CLIP)

            trimmedTrussPaths = pc2.Execute(pyclipper.CT_INTERSECTION)

            """
            Generate the support skin
            """
            pc2.Clear()
            pc2.AddPaths(outerPaths, pyclipper.PT_SUBJECT)
            pc2.AddPaths(offsetPathInner, pyclipper.PT_CLIP)
            skinSolutionPaths = pc2.Execute(pyclipper.CT_DIFFERENCE)

            """
            Merge all the paths together 
            """
            pc2.Clear()
            pc2.AddPaths(trimmedTrussPaths, pyclipper.PT_SUBJECT)
            pc2.AddPaths(skinSolutionPaths, pyclipper.PT_CLIP)
            solution = pc2.Execute2(pyclipper.CT_UNION)
        else:
            # Use only the truss paths. This simply exports ClipperLib PolyNode Tree
            pc2.AddPaths(trussPaths, pyclipper.PT_SUBJECT)
            pc2.AddPaths(outerPaths, pyclipper.PT_CLIP)

            solution = pc2.Execute2(pyclipper.CT_INTERSECTION)

        """
        Create the polygon  and triagulate using the triangle library to provide a precise controlled conformal mesh.
        """
        exterior, interior = sortExteriorInteriorRings(solution, closePolygon=True)
        bufferPoly = createPath2DfromPaths(interior + exterior)

        vy, fy = bufferPoly.triangulate(triangle_args='pa{:.3f}'.format(4.0))

        # Triangulate the polygon - kept as a reference as an alternative
        #vy, fy = triangulatePolygon(solution)

        """
        Create the interpolation or mapping function to go from the 2D polygon to the 3D mesh for the support boundary.
        This is done based on the top most projected curve. 
        """
        y1 = topXY[:, 0]
        y2 = topXY[:, 1]

        x = np.linspace(0.0, np.max(myPolyVerts[:, 0]), len(y1))
        f1 = interpolate.interp1d(topPolyX, y1, bounds_error=False, fill_value=(topXY[0, 0], topXY[-1, 0]))

        x2 = np.linspace(0.0, np.max(myPolyVerts[:, 0]), len(y2))
        f2 = interpolate.interp1d(topPolyX, y2, bounds_error=False, fill_value=(topXY[0, 1], topXY[-1, 1]))

        vy = np.hstack([vy, np.zeros([len(vy),1])])

        import trimesh
        """
        We subdivide and discretise the mesh further in-order to provide sufficient discretisiation of the support mesh.
        This ensures that the mesh correctly conforms to the boundary of the support block volume - especially at sharp
        apexes or corners.
        """
        tmpMesh = trimesh.Trimesh(vertices=vy, faces=fy, process=True, validate=True)
        tmpMesh.merge_vertices()

        vy, fy = trimesh.remesh.subdivide(tmpMesh.vertices, tmpMesh.faces)

        """ 
        Interpolate or map the planar 2D mesh using the existing boundary path to generate the 3D support volume
        """
        boundaryX = f1(vy[:, 0])
        boundaryY = f2(vy[:, 0])
        boundaryZ = vy[:, 1]

        verts = np.hstack([boundaryX.reshape(-1, 1), boundaryY.reshape(-1, 1), boundaryZ.reshape(-1, 1)])
        # Append a z coordinate in order to transform to mesh
        boundaryMesh = trimesh.Trimesh(vertices=verts, faces=fy, process=True)

        return boundaryMesh

    def generateSupportSlices(self):
        """
        Generates support slices

        :return: A tuple of X,Y grid slices
        """
        xSectionMeshList = [trimesh.Trimesh()]
        ySectionMeshList = [trimesh.Trimesh()]

        sectionsX, sectionsY = self.generateGridSlices()

        i = 1
        # Process the Section X
        for sectionX in sectionsX:

            print('X Support generated - {:d}/{:d}'.format(i,len(sectionsX)))
            i+=1
            section = self.generateSliceGeometry(sectionX)

            if section is None:
                continue

            # Triangulate the polygon
            vx, fx  = triangulatePolygon(section)

            if len(vx) == 0:
                continue

            # Append a z coordinate in order to transform to mesh
            vx = np.insert(vx, 2, values=0.0, axis=1)
            secX = trimesh.Trimesh(vertices=vx, faces=fx)

            # Transform using the original transformation matrix generated during slicing
            secX.apply_transform(sectionX.metadata['to_3D'])
            xSectionMeshList.append(secX)

        # Concatenate all the truss meshes for the x-slices together in a single pass
        xSectionMesh = trimesh.util.concatenate(xSectionMeshList)

        i = 1
        # Process the Section Y
        for sectionY in sectionsY:
            print('Y Support generated - {:d}/{:d}'.format(i,len(sectionsY)))
            i+=1
            section = self.generateSliceGeometry(sectionY)

            if section is None:
                continue

            # Triangulate the polygon
            vy, fy = triangulatePolygon(section)

            if len(vy) == 0:
                continue

            # Append a z coordinate in order to transform to mesh
            vy = np.insert(vy, 2, values=0.0, axis=1)
            secY = trimesh.Trimesh(vertices=vy, faces=fy)

            # Transform using the original transformation matrix generated during slicing
            secY.apply_transform(sectionY.metadata['to_3D'])

            ySectionMeshList.append(secY)

        # Concatenate all the truss meshes for the y-slices together in a single pass
        ySectionMesh = trimesh.util.concatenate(ySectionMeshList)

        return xSectionMesh, ySectionMesh

    def generateGridSlices(self):
        """ Identify the sides of the block extrudes """

        # Obtain the bounding box for the support volume
        supportGeom = self._supportVolume

        bx = supportGeom.bounds[:, 0]
        by = supportGeom.bounds[:, 1]
        bz = supportGeom.bounds[:, 2]

        # Specify the spacing of the support grid slices
        spacingX = self._gridSpacing[0]
        spacingY = self._gridSpacing[1]

        # Obtain the section through the STL extension using Trimesh Algorithm (Shapely)
        midX = (bx[0] + bx[1])/2.0
        bottomX =  -1.0 * np.ceil((midX-bx[0])/spacingX)*spacingX
        topX = 1. * np.ceil((bx[1]-midX) / spacingX) * spacingX + 1e-8

        # Generate the support slices of the section
        sectionsX = supportGeom.section_multiplane(plane_origin=[midX, 0.0, 0.0],
                                                   plane_normal=[1.0, 0.0, 0.0],
                                                   heights=np.arange(bottomX, topX, spacingX))
        midY = (by[0] + by[1]) / 2.0
        bottomY = -1.0 * np.ceil((midY-by[0])/spacingY)*spacingY
        topY = 1.0 * np.ceil((by[1]-midY) / spacingY) * spacingY + 1e-8

        sectionsY = supportGeom.section_multiplane(plane_origin=[0.0, midY, 0.0],
                                                   plane_normal=[0.0, 1.0, 0.0],
                                                   heights=np.arange(bottomY, topY, spacingY))

        return sectionsX, sectionsY


class BaseSupportGenerator(abc.ABC):
    """
    The BaseSupportGeneration class provides common methods used for generating the 'support' structures typically used
    in Additive Manufacturing.
    """

    PYCLIPPER_SCALEFACTOR = 1e4
    """ 
    The scaling factor used for polygon clipping and offsetting in `PyClipper <http://pyclipper.com>`_ for the decimal
    component of each polygon coordinate. This should be set to inverse of the required decimal tolerance i.e. 0.01 
    requires a minimum scale factor of 1e2. This scaling factor is used in :meth:`~BaseHatcher.scaleToClipper` 
    and :meth:`~BaseHatcher.scaleFromClipper`. 
    """

    POINT_OVERHANG_TOLERANCE = 0.05

    def __init__(self):
        pass

    def __str__(self):
        return 'BaseGenerator'

    @staticmethod
    def findOverhangPoints(part: Part) -> np.ndarray:

        meshVerts = part.geometry.vertices
        vAdjacency = part.geometry.vertex_neighbors

        pointOverhangs = []
        for i in range(len(vAdjacency)):

            # Find the edge deltas between the points
            v = meshVerts[i]
            neighborVerts = meshVerts[vAdjacency[i], :]
            delta = neighborVerts - v
            # mag = np.sqrt(np.sum(delta * delta, axis=1))
            # theta = np.arcsin(delta[:,2]/mag)
            # theta = np.rad2deg(theta)
            # if np.all(theta > -0.001):
            # pointOverhang.append(i)

            """
            If all neighbouring connected vertices lie above the point, this indicates the vertex lies below and 'may'
            not have underlying connectivity. There are two cases that exist: on upwards or downwards pointing surface.
            """
            if np.all(delta[:, 2] > -BaseSupportGenerator.POINT_OVERHANG_TOLERANCE):

                # Check that the vertex normal is pointing downwards (-ve Z) showing that the no material is underneath
                if part.geometry.vertex_normals[i][2] < 0.0:
                    pointOverhangs.append(i)

        return pointOverhangs

    @staticmethod
    def findOverhangEdges(part: Part, overhangAngle: float = 45.0, edgeOverhangAngle: float = 10.0):
        """
        Identifies edges which requires additional support based on both an support surface and support edge angle.

        :param part:  Part to be analysed
        :param overhangAngle: The support surface overhang angle
        :param edgeOverhangAngle: The edge overhang angle

        :return: A list of edge tuples.
        """
        meshVerts = part.geometry.vertices
        edges = part.geometry.edges_unique
        edgeVerts = meshVerts[edges]

        """ 
        Calculate the face angles with respect to the +z vector  and the inter-face angles
        """
        theta = getSupportAngles(part, np.array([[0., 0., 1.0]]))
        adjacentFaceAngles = np.rad2deg(part.geometry.face_adjacency_angles)

        overhangEdges = []
        # Iterate through all the edges in the model
        for i in range(len(edgeVerts)):

            """
            Calculate the 'vertical' angle of the edge pointing in the z-direction by using the z component.
            First calculate vector, magnitude and the vertical angle of the vector
            """
            edge = edgeVerts[i].reshape(2, 3)
            delta = edge[0] - edge[1]
            mag = np.sqrt(np.sum(delta * delta))
            ang = np.rad2deg(np.arcsin(delta[2] / mag))

            # Identify if the vertical angle of the edge is less than the edgeOverhangAngle irrespective of the actual
            # direction of the vector (bi-directional)
            if np.abs(ang) < edgeOverhangAngle:

                """
                Locate the adjacent faces in the model using the face-adjacency property to identify if the edge 
                belongs to a sharp corner which tends to be susceptible areas. This is done by calculating the angle
                between faces.
                """
                adjacentFaces = part.geometry.face_adjacency[i]
                # triVerts = meshVerts[part.geometry.faces[adjacentFaces]].reshape(-1, 3)

                if adjacentFaceAngles[i] > overhangAngle and np.all(theta[adjacentFaces] > 89):
                    # if np.all(theta[adjacentFaces] > 89) and np.all(triVerts[:,2] - np.min(edge[:,2]) > -0.01):
                    overhangEdges.append(edges[i])

        return overhangEdges

    @staticmethod
    def flattenSupportRegion(region):
        supportRegion = region.copy()

        """ Extract the outline of the overhang mesh region"""
        poly = supportRegion.outline()

        """ Convert the line to a 2D polygon"""
        poly.vertices[:, 2] = 0.0

        flattenPath, polygonTransform = poly.to_planar()
        flattenPath.process()

        flattenPath.apply_translation(polygonTransform[:2, 3]) #np.array([polygonTransform[0, 3],
                                               # polygonTransform[1, 3]]))
        polygon = flattenPath.polygons_full[0]

        return polygon #, polygonTransform


class BlockSupportGenerator(BaseSupportGenerator):
    """
    The BlockSupportGenerator class provides common methods used for generating the 'support' structures typically used
    in Additive Manufacturing for block polygon regions
    """

    CORK_PATH = ''
    """
    The Path to the Cork Boolean Library as a static attribute. This should be specified when initialising the scripts.
    
    :note:
        In future this may be included as a separate Python module for ease of installation. 
    """

    def __init__(self):

        super().__init__()

        self._minimumAreaThreshold = 5.0  # mm2 (default = 10)
        self._rayProjectionResolution = 0.2  # mm (default = 0.5)

        self._lowerProjectionOffset = 0.1
        self._upperProjectionOffset = 0.1

        self._innerSupportEdgeGap = 0.2  # mm (default = 0.1)
        self._outerSupportEdgeGap = 0.5  # mm  - offset between part supports and baseplate supports

        self._triangulationSpacing = 2  # mm (default = 1)
        self._simplifyPolygonFactor = 2.0

        self._overhangAngle = 45.0  # [deg]

    def __str__(self):
        return 'BlockSupportGenerator'

    @staticmethod
    def gradThreshold(rayProjectionDistance: float, overhangAngle: float) -> float:
        """
        A static method which defines the threshold hold to the gradient generated from the support
        generation depth map. This is based on a combination of the ray projection resolution, the overhang angle and
        an arbitrary constant to ensure discrete regions are isolated.

        :param rayProjectionDistance: The ray projection resolution used
        :param overhangAngle: The overhang angle [degrees]
        :return: The gradient threshold used.

        """
        return 5.0 * np.tan(np.deg2rad(overhangAngle)) * rayProjectionDistance

    @property
    def overhangAngle(self) -> float:
        """ The overhang angle, in degrees, used for identifying support surfaces. """
        return self._overhangAngle

    @overhangAngle.setter
    def overhangAngle(self, angle: float):
        self._overhangAngle = angle

    @property
    def upperProjectionOffset(self) -> float:
        """
        The offset applied to the upper projection used to provide a clean intersection when performing the final boolean
        intersection between the original geometry and the extruded support volume geometry
        """
        return self._upperProjectionOffset

    @upperProjectionOffset.setter
    def upperProjectionOffset(self, offset: float) -> None:
        self._upperProjectionOffset = offset

    @property
    def lowerProjectionOffset(self) -> float:
        """
        The offset applied to the lower projection used to provide a clean intersection when performing the final boolean
        intersection between the original geometry and the extruded support volume geometry.
        """
        return self._lowerProjectionOffset

    @lowerProjectionOffset.setter
    def lowerProjectionOffset(self, offset) -> None:
        self._lowerProjectionOffset = offset

    @property
    def outerSupportEdgeGap(self) -> float:
        """ The offset applied to the  boundary of the support volume """
        return self._outerSupportEdgeGap

    @outerSupportEdgeGap.setter
    def outerSupportEdgeGap(self, spacing: float):
        self._outerSupportEdgeGap = spacing

    @property
    def innerSupportEdgeGap(self) -> float:
        return self._innerSupportEdgeGap

    @innerSupportEdgeGap.setter
    def innerSupportEdgeGap(self, spacing: float):
        self._innerSupportEdgeGap = spacing

    @property
    def minimumAreaThreshold(self) -> float:
        """
        The minimum support area threshold used to identify disconnected support regions.
        """
        return self._minimumAreaThreshold

    @minimumAreaThreshold.setter
    def minimumAreaThreshold(self, areaThresholdValue: float):
        self._minimumAreaThreshold = areaThresholdValue

    @property
    def simplifyPolygonFactor(self) -> float:
        """ Simplification factor used on the support structure boundary"""
        return self._simplifyPolygonFactor

    @simplifyPolygonFactor.setter
    def simplifyPolygonFactor(self, value: float) -> None:
        self._simplifyPolygonFactor = value

    @property
    def triangulationSpacing(self) -> float:
        """ The  spacing factor used to to triangulate the support polygon region"""
        return self._triangulationSpacing

    @triangulationSpacing.setter
    def triangulationSpacing(self, spacing: float) -> None:
        self._triangulationSpacing = spacing

    @property
    def rayProjectionResolution(self) -> float:
        """ The Ray Projection resolution used to discretise the projected support region."""
        return self._rayProjectionResolution

    @rayProjectionResolution.setter
    def rayProjectionResolution(self, resolution: float) -> None:
        self._rayProjectionResolution = resolution

    def filterSupportRegion(self, region):
        pass

    def generateIntersectionHeightMap(self):
       raise Exception('Not Implemented')

    def _identifySelfIntersectionHeightMap(self, subregion: trimesh.Trimesh, offsetPoly: trimesh.path.Path2D, cutMesh: trimesh.Trimesh) -> Tuple[np.ndarray]:
        """
        Generates the height map of the upper and lower depths. This is done by projecting rays at a resolution
        (attr:`~BlockSupportGenerator.rayProjectionResolution`) across the entire polygon region (offsetPoly) in both
        vertical directions (+z, -z) and are intersected with the upper and lower support surface. A sequence of
        height maps are generated from these ray intersections.

        :param subregion: The upper surface (typically overhang surface region)
        :param offsetPoly: The polygon region defining the support region
        :param cutMesh: The lower intersecting surfaces which potentially intersect with the polygon region
        :return: A tuple containing various height maps
        """
        # Rasterise the surface of overhang to generate projection points
        supportArea = np.array(offsetPoly.rasterize(self.rayProjectionResolution, offsetPoly.bounds[0, :])).T

        coords = np.argwhere(supportArea).astype(np.float32) * self.rayProjectionResolution
        coords += offsetPoly.bounds[0, :] + 1e-5  # An offset is required due to rounding error

        print('\t - start projecting rays')
        print('\t - number of rays with resolution ({:.3f}): {:d}'.format(self.rayProjectionResolution, len(coords)))

        """
        Project upwards to intersect with the upper surface
        """
        # Set the z-coordinates for the ray origin
        coords = np.insert(coords, 2, values=-1e5, axis=1)
        rays = np.repeat([[0., 0., 1.]], coords.shape[0], axis=0)

        # Find the first location of any triangles which intersect with the part
        hitLoc, index_ray, index_tri = subregion.ray.intersects_location(ray_origins=coords,
                                                                         ray_directions=rays,
                                                                         multiple_hits=False)

        hitLocCpy = hitLoc.copy()
        hitLocCpy[:, :2] -= offsetPoly.bounds[0, :]
        hitLocCpy[:, :2] /= self.rayProjectionResolution

        hitLocIdx = np.ceil(hitLocCpy[:, :2]).astype(np.int32)

        coords2 = coords.copy()

        coords2[index_ray, 2] = 1e7
        rays[:, 2] = -1.0

        # If any verteces in triangle there is an intersection
        # Find the first location of any triangles which intersect with the part
        hitLoc2, index_ray2, index_tri2 = cutMesh.ray.intersects_location(ray_origins=coords2,
                                                                          ray_directions=rays,
                                                                          multiple_hits=False)

        print('\t - finished projecting rays')

        hitLocCpy2 = hitLoc2.copy()
        # Update the xy coordinates
        hitLocCpy2[:, :2] -= offsetPoly.bounds[0, :]
        hitLocCpy2[:, :2] /= self.rayProjectionResolution
        hitLocIdx2 = np.ceil(hitLocCpy2[:, :2]).astype(np.int32)

        # Create a height map of the projection rays
        heightMap = np.ones(supportArea.shape) * -1.0

        heightMapUpper = np.zeros(supportArea.shape)
        heightMapLower = np.zeros(supportArea.shape)

        # Assign the heights
        heightMap[hitLocIdx[:, 0], hitLocIdx[:, 1]] = hitLoc[:, 2]
        heightMapUpper[hitLocIdx[:, 0], hitLocIdx[:, 1]] = hitLoc[:,2]

        # Assign the heights based on the lower projection
        heightMap[hitLocIdx2[:, 0], hitLocIdx2[:, 1]] = hitLoc2[:, 2]
        heightMapLower[hitLocIdx2[:, 0], hitLocIdx2[:, 1]] = hitLoc2[:, 2]

        print('\tgenerated support height map')
        return heightMap, heightMapUpper, heightMapLower

    def identifySupportRegions(self, part: Part, overhangAngle: float,
                               findSelfIntersectingSupport: Optional[bool] = True):
        """
        Extracts the overhang mesh and generates block regions given a part and target overhang angle. The algorithm
        uses a combination of boolean operations and ray intersection/projection to discriminate support regions.
        If :code:`findSelfIntersectingSuppoort` is to set :code:`True` (default), the algorithm will process and
        separate overhang regions that by downward projection self-intersect with the part.
        This provides more refined behavior than simply projected support material downwards into larger support
        block regions and separates an overhang surface between intersecting and non-intersecting regions.

        :param part: The part to generate block supports for
        :param overhangAngle: Overhang angle in degrees
        :param findSelfIntersectingSupport:
        """

        overhangSubregions = getOverhangMesh(part, overhangAngle, True)

        """
        The geometry of the part requires exporting as a '.off' file to be correctly used with the Cork Library
        """
        part.geometry.export('part.off')

        supportBlockRegions = []

        supportBlockRegionList = []

        """ Process sub-regions"""
        for subregion in overhangSubregions:

            print('Processing subregion')
            polygon = self.flattenSupportRegion(subregion)

            # Offset in 2D the support region projection
            offsetShape = polygon.buffer(-self.outerSupportEdgeGap)

            if offsetShape is None or offsetShape.area < self.minimumAreaThreshold:
                print('skipping shape')
                continue

            offsetPoly = trimesh.load_path(offsetShape)

            """
            Create an extrusion at the vertical extent of the part
            """
            extruMesh = extrudeFace(subregion, 0.0)
            extruMesh.vertices[:, 2] = extruMesh.vertices[:, 2] - 0.01

            print('\t - start intersecting mesh')
            # Intersect the projection of the support face with the original part using the Cork Library
            extruMesh.export('downProjExtr.off')
            subprocess.call([self.CORK_PATH, '-isct', 'part.off', 'downProjExtr.off', 'c.off'])
            print('\t - finished intersecting mesh')

            """
            Note the cutMesh is the project down from the support surface with the original mesh
            """
            cutMesh = trimesh.load_mesh('c.off', process=True, validate=True)

            if len(cutMesh.faces) == 0:
                extruMesh.visual.face_colors[:,:3] = np.random.randint(254, size=3)
                supportBlockRegions.append(extruMesh)

                # Create a support block object
                baseSupportBlock = GridBlockSupport()
                baseSupportBlock.supportObject = part
                baseSupportBlock.supportSurface = subregion
                baseSupportBlock.supportVolume = extruMesh

                supportBlockRegionList.append(baseSupportBlock)

                continue  # No intersection had taken place
            elif not findSelfIntersectingSupport:
                continue

            v0 = np.array([[0., 0., 1.0]])

            # Identify Support Angles
            v1 = cutMesh.face_normals
            theta = np.arccos(np.clip(np.dot(v0, v1.T), -1.0, 1.0))
            theta = np.degrees(theta).flatten()

            cutMeshUpper = cutMesh.copy()
            cutMeshUpper.update_faces(theta < 89.95)
            cutMeshUpper.remove_unreferenced_vertices()

            # Toggle to use full intersecting mesh
            # cutMeshUpper = cutMesh

            # Use a ray-tracing approach to identify self-intersections. This provides a method to isolate regions that
            # either are self-intersecting or not.

            heightMap, heightMapUpper, heightMapLower = self._identifySelfIntersectionHeightMap(subregion, offsetPoly, cutMeshUpper)
            vx, vy = np.gradient(heightMap)
            grads = np.sqrt(vx ** 2 + vy ** 2)

            """
            Find the outlines of any regions of the height map which deviate significantly
            This is used to separate both self-intersecting supports and those which are simply connected to the base-plate
            """
            outlines = find_contours(grads, self.gradThreshold(self.rayProjectionResolution, self.overhangAngle))

            polygons = []

            for outline in outlines:

                """
                Process the outline by finding the boundaries
                """
                outline = outline * self.rayProjectionResolution + offsetPoly.bounds[0, :]
                outline = approximate_polygon(outline, tolerance=self.simplifyPolygonFactor* self._rayProjectionResolution)

                if outline.shape[0] < 3:
                    continue

                """
                Process the polygon  by creating a shapley polygon and offseting the boundary
                """
                mergedPoly = trimesh.load_path(outline)

                if not mergedPoly.is_closed or len(mergedPoly.polygons_full) == 0 or mergedPoly.polygons_full[0] is None:
                    continue

                bufferPoly = mergedPoly.polygons_full[0].buffer(-self.innerSupportEdgeGap)

                if isinstance(bufferPoly, shapely.geometry.MultiPolygon):
                    polygons += bufferPoly.geoms
                else:
                    polygons.append(bufferPoly)

            for bufferPoly in polygons:

                if bufferPoly.area < self.minimumAreaThreshold:
                    continue

                """
                Triangulate the polygon into a planar mesh
                """
                poly_tri = trimesh.creation.triangulate_polygon(bufferPoly,
                                                                triangle_args='pa{:.3f}'.format(self.triangulationSpacing))

                """
                Project upwards to intersect with the upper surface
                Project the vertices downward (-z) to intersect with the cutMesh
                """
                coords = np.insert(poly_tri[0], 2, values=-1e-7, axis=1)
                ray_dir = np.repeat([[0., 0., 1.]], coords.shape[0], axis=0)

                # Find the first location of any triangles which intersect with the part
                hitLoc, index_ray, index_tri = subregion.ray.intersects_location(ray_origins=coords,
                                                                                 ray_directions=ray_dir,
                                                                                 multiple_hits=False)

                coords2 = coords.copy()
                coords2[index_ray, 2] = hitLoc[:, 2] + self.upperProjectionOffset

                ray_dir[:, 2] = -1.0

                """
                Intersecting with cutmesh is more efficient when projecting downwards
                """
                hitLoc2, index_ray2, index_tri2 = cutMeshUpper.ray.intersects_location(ray_origins=coords2,
                                                                                       ray_directions=ray_dir,
                                                                                       multiple_hits=False)
                if len(hitLoc) != len(coords) or len(hitLoc2) != len(hitLoc):
                    # The projections up and down do not match indicating that there maybe some flaw
                    print(hitLoc.shape, hitLoc2.shape, coords.shape)

                    if len(hitLoc2) == 0:
                        # Base plate
                        hitLoc2 = coords2.copy()
                        hitLoc2[:, 2] = 0.0

                        print('Creating Base-plate support')
                    else:
                        print('PROJECTIONS NOT MATCHING')
                        raise ValueError('SUPPORT PROJECTIONS NOT MATCHING - Increase the outer edge gap or increase resolution')

                # Create a surface from the Ray intersection
                surf2 = trimesh.Trimesh(vertices=coords2, faces=poly_tri[1])

                # Extrude the surface based on the heights from the second ray cast
                extrudedBlock = extrudeFace(surf2, None, hitLoc2[:, 2] - self.lowerProjectionOffset)
                extrudedBlock.export('b.off')

                """
                Take the near net-shape support and obtain the difference with the original part to get clean 
                boundaries for the support
                """
                subprocess.call([self.CORK_PATH, '-diff', 'b.off', 'part.off', 'c.off'])
                blockSupport = trimesh.load_mesh('c.off', process=True, validate=True)
                blockSupport.fix_normals()
                blockSupport.remove_degenerate_faces()

                # Draw the support structures generated
                blockSupport.visual.face_colors[:,:3] = np.random.randint(254, size=3)

                supportBlockRegions.append(blockSupport)

                # Create a support block object
                baseSupportBlock = GridBlockSupport()
                baseSupportBlock.supportObject = part
                baseSupportBlock.intersectsPart = True
                baseSupportBlock.supportSurface = subregion
                baseSupportBlock.supportVolume = blockSupport

                supportBlockRegionList.append(baseSupportBlock)

            print('processed support face')

        #return supportBlockRegionList
        return supportBlockRegions, supportBlockRegionList
