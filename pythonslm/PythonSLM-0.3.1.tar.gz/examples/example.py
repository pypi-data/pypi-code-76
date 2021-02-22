"""
A simple example showing how t use PySLM for generating a Stripe Scan Strategy across a single layer.
"""
import numpy as np
import pyslm
import pyslm.analysis.utils as analysis
from pyslm import hatching as hatching

# Imports the part and sets the geometry to  an STL file (frameGuide.stl)
solidPart = pyslm.Part('myFrameGuide')
solidPart.setGeometry('../models/frameGuide.stl')

"""
Transform the part:
Rotate the part 30 degrees about the Z-Axis - given in degrees
Translate by an offset of (5,10) and drop to the platform the z=0 Plate boundary
"""
solidPart.origin = [5.0, 10.0, 0.0]
solidPart.scaleFactor = 1.1
solidPart.rotation = np.array([0, 0, 30])
solidPart.dropToPlatform()

print(solidPart.boundingBox)

#pyslm.visualise.visualiseOverhang(solidPart, 60)

# Create a closed polygon representing the transformed slice geometry

# Martinez et al polygon clipping
# Much faster than both Vatti and Greiner for large samples,
# ...and only barely slower for very small samples
# http://www.cs.ucr.edu/~vbz/cs230papers/martinez_boolean.pdf
# example implementation: https://github.com/akavel/polyclip-go

# STATUS: Mostly implemented but doesnt yet work even for simple cases
# not yet implemented support for overlapping edges or selfintersections

# Classes and helpers

def pairwise(points):
    a = (p for p in points)
    b = (p for p in points)
    next(b)
    for curpoint, nextpoint in zip(a, b):
        yield curpoint, nextpoint


class Sweepline:
    def __init__(self):
        self.edges = []

    def insert(self, edge):
        if len(self.edges) > 0:
            pos = 0
            for v in self.edges:
                if v.y > edge.y or (
                        not edge.vertical and v.y == edge.y):  # nonvertical are placed first for same points, otherwise after
                    break
                pos += 1
            self.edges.insert(pos, edge)
        else:
            self.edges.append(edge)

    def next(self, edge):
        for cur in self.edges:
            if cur.y > edge.y:
                break
        else:
            return None
        return cur

    def prev(self, edge):
        for cur in reversed(self.edges):
            if cur.y < edge.y:
                break
        else:
            return None
        return cur

    def erase(self, edge):
        self.edges.remove(edge)


class Endpoint:  # aka sweepevent
    def __init__(self, xy, polytype):
        self.xy = xy
        self.x, self.y = xy
        self.other = None  # must be set manually as a reference
        self.polytype = polytype
        self.inout = ""
        self.inside = ""
        self.edgetype = ""

    @property
    def vertical(self):
        return self.xy[0] == self.other.xy[0]

    @property
    def left(self):
        if self.vertical:
            return self.xy[1] < self.other.xy[1]  # vertical edge, lower y is considered left
        else:
            return self.xy[0] < self.other.xy[0]

    def __str__(self):
        return ("Left" if self.left else "Right") + "Endpoint(%s, %s)" % self.xy + " --> (%s, %s)" % self.other.xy


def set_inside_flag(endpoint, prevendpoint):
    endpoint1, endpoint2 = endpoint, prevendpoint
    if not endpoint2:
        endpoint1.inside = endpoint1.inout = False
    elif endpoint1.polytype == endpoint2.polytype:
        endpoint1.inside = endpoint2.inside
        endpoint1.inout = endpoint2.inout
    else:
        endpoint1.inside = not endpoint2.inout
        endpoint1.inout = endpoint2.inside


def possible_subdivide(ep1, ep2, S, Q):
    """Looks for intersections so that it can subdivide them
    and update the Q and S lists.
    """

    if not (ep1 and ep2):
        # if only one edge, then no intersections
        return

    if ep1.polytype == ep2.polytype:
        # belong to same polytype, stop processing
        return

    intersect = intersect_or_on(ep1, ep2)

    if intersect:
        ipoint, alphaS, alphaC = intersect
        if 0.0 < alphaS < 1.0 or 0.0 < alphaC < 1.0:
            # subdivide so the lines do not intersect...?
            # ie replace the isect point to the end of each edge
            right = ep1.other
            ep1.other = Endpoint(ipoint, ep1.polytype)
            ep1.other.other = ep1
            assert ep1.left
            ep1ext = Endpoint(ipoint, ep1.polytype)
            ep1ext.other = right
            right.other = ep1ext
            assert ep1ext.left
            right = ep2.other
            ep2.other = Endpoint(ipoint, ep2.polytype)
            ep2.other.other = ep2
            assert ep2.left
            ep2ext = Endpoint(ipoint, ep2.polytype)
            ep2ext.other = right
            right.other = ep2ext
            assert ep2ext.left

            # update Q and S
            # TODO: The Q endpoints mut be inserted sorted bottom to top plus more

            ##            cur = Q[1] if len(Q) > 1 else Q[0]
            ##            curpos = 0
            ##            while cur.x == p2.x and cur.y < p2.y and not cur.left:
            ##                curpos += 1
            ##            Q.insert(pos-1,p2)
            ##
            ##            cur = Q[1] if len(Q) > 1 else Q[0]
            ##            curpos = 0
            ##            while cur.x == p4.x and cur.y < p4.y and not cur.left:
            ##                curpos += 1
            ##            Q.insert(pos-1,p4)

            for pos, v in enumerate(Q):
                if v.y > ep1ext.y or v.x != ep1ext.x or (v.xy == ep1ext.xy and not ep1ext.left and v.left):
                    assert pos >= 0
                    while v.xy == ep1ext.xy and ep1ext.left and v.left and S.edges.index(v) < S.edges.index(ep1ext):
                        pos += 1
                    Q.insert(pos, ep1ext)
                    break
            for pos, v in enumerate(Q):
                if v.y > ep2ext.y or v.x != ep2ext.x or (v.xy == ep2ext.xy and not ep2ext.left and v.left):
                    assert pos >= 0
                    while v.xy == ep2ext.xy and ep1ext.left and v.left and S.edges.index(v) < S.edges.index(ep2ext):
                        pos += 1
                    Q.insert(pos, ep2ext)
                    break

            S.insert(ep1ext)
            S.insert(ep2ext)

        else:
            # only intersect at one of their endpoints, stop processing
            return


def intersect_or_on(ep1, ep2):
    """Same as intersect(), except returns
    intersection even if degenerate.
    """
    s1, s2 = ep1, ep1.other
    c1, c2 = ep2, ep2.other
    den = float((c2.y - c1.y) * (s2.x - s1.x) - (c2.x - c1.x) * (s2.y - s1.y))
    if not den:
        return None

    us = ((c2.x - c1.x) * (s1.y - c1.y) - (c2.y - c1.y) * (s1.x - c1.x)) / den
    uc = ((s2.x - s1.x) * (s1.y - c1.y) - (s2.y - s1.y) * (s1.x - c1.x)) / den

    if (0 <= us <= 1) and (0 <= uc <= 1):
        # subj and clip line intersect eachother somewhere in the middle
        # this includes the possibility of degenerates (edge intersections)
        x = s1.x + us * (s2.x - s1.x)
        y = s1.y + us * (s2.y - s1.y)
        return (x, y), us, uc
    else:
        return None


# The algorithm

def clip_polygons(clip, subjects, type):
    # insert all edge endpoints into the priority queue
    Q = []
    for subject in subjects:
        for start, end in pairwise(subject):
            print(start,end)
            ep1 = Endpoint(start, "subject")
            ep2 = Endpoint(end, "subject")
            ep1.other = ep2
            ep2.other = ep1
            Q.append(ep1)
            Q.append(ep2)

    for start, end in pairwise(clip):
        ep1 = Endpoint(start, "clip")
        ep2 = Endpoint(end, "clip")
        ep1.other = ep2
        ep2.other = ep1
        Q.append(ep1)
        Q.append(ep2)

    # sort by x asc, y asc (bottom to top), and right endpoints first

    Q = sorted(Q, key=lambda EP: (EP.x, EP.y, EP.left, EP.other.y))

    # create the sweepline
    S = Sweepline()

    # loop
    raw = []
    while Q:
        endpoint = Q.pop(0)

        if endpoint.left:  # left endpoint
            # some lists
            S.insert(endpoint)
            set_inside_flag(endpoint, S.prev(endpoint))
            # intersections
            possible_subdivide(endpoint, S.next(endpoint), S, Q)
            possible_subdivide(endpoint, S.prev(endpoint), S, Q)

        else:  # right endpoint
            # move forward
            # S.find(endpoint.other)
            next = S.next(endpoint.other)
            prev = S.prev(endpoint.other)
            # print prev,endpoint.other,next
            # some adding
            if endpoint.inside:
                raw.append(endpoint.xy)  # intersection
                raw.append(endpoint.other.xy)
            elif not endpoint.inside:
                raw.append(endpoint.xy)  # union
                raw.append(endpoint.other.xy)
            # some cleanup
            # print "remove",endpoint.other,"from",[str(e) for e in S.edges]
            # S.erase(endpoint) if endpoint in S.edges else S.erase(endpoint.other)
            if endpoint.other in S.edges: S.erase(
                endpoint.other)  # right ends are processed before left, so could be the left hasnt been inserted yet
            possible_subdivide(prev, next, S, Q)

    # connect the final edges
    polys = []
    chains = []
    edges = []
    for edge in pairwise(raw):
        connect = []

        edges.append(edge)

        for chain in chains:
            if chain[0] in edge:
                connect.append(chain)
            elif chain[1] in edge:
                connect.append(chain)

        if len(connect) == 2:
            chain1, chain2 = connect
            chain1.extend(chain2)
            chain1.extend(edge)
            chains.remove(chain2)
            if chain1[0] == chain1[-1]:
                polys.append(chain1)
                chains.remove(chain1)

        elif len(connect) == 1:
            chain = connect[0]
            chain.extend(edge)
            if chain[0] == chain[-1]:
                polys.append(chain)
                chains.remove(chain)

        else:
            chain = list(edge)
            chains.append(chain)

    return [(p, []) for p in polys]


if __name__ == "__main__":
    """
    Test and visualize various polygon overlap scenarios.
    Visualization requires the pure-Python PyDraw library from
    https://github.com/karimbahgat/PyDraw
    """

    subjpoly = [(0, 0), (6, 0), (7, 6), (1, 6)]

    # normal intersections
    testpolys_normal = {"simple overlap":
                            [(0 + 4, 0 + 4), (6 + 4, 0 + 4), (7 + 4, 6 + 4), (1 + 4, 6 + 4)],
                        "jigzaw overlap":
                            [(1, 4), (3, 8), (5, 4), (6, 10), (2, 10)],
                        ##                        "smaller, outside":
                        ##                        [(7,7),(7,9),(9,9),(9,7),(7,7)],
                        ##                        "smaller, inside":
                        ##                        [(2,2),(2,4),(4,4),(4,2),(2,2)],
                        ##                        "larger, covering all":
                        ##                        [(-1,-1),(-1,7),(7,7),(7,-1),(-1,-1)],
                        ##                        "larger, outside":
                        ##                        [(-10,-10),(-10,-70),(-70,-70),(-70,-10),(-10,-10)]
                        }




def generateMeshGrid(poly, hatchSpacing: float = 0.1, hatchAngle = 45.0) -> np.ndarray:

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

from shapely.geometry.polygon import *



a = [0,100]
b = [0,100]
bboxPoly = Polygon([[a[0], b[0]],
                    [a[0], b[1]],
                    [a[1], b[1]],
                    [a[1], b[0]], [a[0], b[0]]])

bboxPoly2 = ([a[0], b[0]],
                    [a[0], b[1]],
                    [a[1], b[1]],
                    [a[1], b[0]], [a[0], b[0]])
import shapely

meshGrid = generateMeshGrid(bboxPoly)

meshGrid2 = meshGrid.reshape([-1,2,3])

lines = []
for line in meshGrid2:
    lines.append(([line[0,0], line[0,1]],
                  [line[1,0], line[1,1]]
                  ))

#hatches = shapely.geometry.MultiLineString(lines)

resultpolys = clip_polygons(bboxPoly2, lines[:2], "intersect")

#clippedHatches = hatches.intersection(bboxPoly)

d
import matplotlib.pyplot as plt
for hatch in clippedHatches.geoms:
    coords = np.array(hatch.coords.xy)

    plt.plot(coords[:,0], coords[:,1])

d

if False:
    import trimesh.remesh
    import trimesh.sample

    origMesh = solidPart.geometry

    surfaceResolution = 1.0 # [mm]
    surfaceArea = origMesh.area

    numSamplePoints = int(surfaceArea / (surfaceResolution*surfaceResolution))

    # Generate sample points across the mesh
    origin, originFaces = trimesh.sample.sample_surface_even(origMesh, numSamplePoints,surfaceResolution/2)

    #sort the origins
    sortIds = np.argsort(originFaces)
    faceIds = originFaces[sortIds]

    # Collect the normals associated from the face normals the sample points are generated on
    normals = origMesh.face_normals[originFaces]

    # Offset the surface to prevent any self intersections
    origin = origin -1.0e-3 * normals

    # Find the first location of any triangles which intersect with the part
    hitLoc, index_ray, index_tri = origMesh.ray.intersects_location(ray_origins=origin,
                                                                   ray_directions=normals*-1.0,
                                                                   multiple_hits=False)
    v = np.zeros(origin.shape)
    v[index_ray] = hitLoc
    delta = v - origin
    distance = np.linalg.norm(delta, axis=1)

    faceDist = np.zeros((len(origMesh.faces)))
    for i in np.arange(len(originFaces)):
        idx = originFaces[i]
        faceDist[idx] = (faceDist[idx] + distance[i])/2

    import matplotlib
    bounds = (np.min(faceDist), np.max(faceDist))
    colors = matplotlib.cm.jet((faceDist - bounds[0]) / (bounds[1] - bounds[0]))



    #colors = subMesh.visual.face_colors.copy()

    #subMesh.visual.faces_colors = colors*255
    #colors[:, 3] = 0.1

    rays = []
    dist2 = []
    entities = []
    for i in np.arange(len(origin)):
        coords = np.zeros((2,3))
        coords[:,:] = origin[i]
        coords[1,:] += 0.5* normals[i]#v[i]
        entities.append(trimesh.path.entities.Line((2*i,2*i+1)))
        dist2.append(np.linalg.norm(v[i]-origin[i]))
        rays.append(coords)

    dist2 = np.array(dist2)
    vertexColors = matplotlib.cm.jet((dist2 - bounds[0]) / (np.max(dist2)- bounds[0]))

    import trimesh.path
    visualize_support_pnts = trimesh.path.Path3D(entities=entities, vertices=np.vstack(rays), process=False)

    for i in np.arange(len(visualize_support_pnts.entities)):

        visualize_support_pnts.entities[i].color = vertexColors[i]

    import trimesh.visual
    origMesh.visual.vertex_colors = trimesh.visual.color.face_to_vertex_color(origMesh, colors)

    s2 = trimesh.Scene([origMesh,
                        visualize_support_pnts]) # , overhangMesh] + supportExtrudes)
    s2.show()



# Set te slice layer position
z = 1.0

# Create a BasicIslandHatcher object for performing any hatching operations (
myHatcher = hatching.Hatcher()
myHatcher.islandWidth = 3.0
myHatcher.stripeWidth = 5.0

# Set the base hatching parameters which are generated within Hatcher
myHatcher.hatchAngle = 90.0 # [°] The angle used for the islands
myHatcher.volumeOffsetHatch = 0.08 # [mm] Offset between internal and external boundary
myHatcher.spotCompensation = 0.06 # [mm] Additional offset to account for laser spot size
myHatcher.numInnerContours = 2
myHatcher.numOuterContours = 1
myHatcher.hatchSortMethod = hatching.AlternateSort()

"""
Perform the slicing. Return coords paths should be set so they are formatted internally.
This is internally performed using Trimesh to obtain a closed set of polygons.
The boundaries of the slice can be automatically simplified if desired. 
"""
geomSlice = solidPart.getVectorSlice(z, simplificationFactor=0.1)
layer = myHatcher.hatch(geomSlice)

"""
Note the hatches are ordered sequentially across the stripe. Additional sorting may be required to ensure that the
the scan vectors are processed generally in one-direction from left to right.
The stripes scan strategy will tend to provide the correct order per isolated region.
"""

"""
Plot the layer geometries using matplotlib
The order of scanning for the hatch region can be displayed by setting the parameter (plotOrderLine=True)
Arrows can be enables by setting the parameter plotArrows to True
"""

pyslm.visualise.plot(layer, plot3D=False, plotOrderLine=True, plotArrows=False)

"""
Before exporting or analysing the scan vectors, a model and build style need to be created and assigned to the 
LaserGeometry groups.

The user has to assign a model (mid)  and build style id (bid) to the layer geometry
"""

for layerGeom in layer.geometry:
    layerGeom.mid = 1
    layerGeom.bid = 1

bstyle = pyslm.geometry.BuildStyle()
bstyle.bid = 1
bstyle.laserSpeed = 200 # [mm/s]
bstyle.laserPower = 200 # [W]

model = pyslm.geometry.Model()
model.mid = 1
model.buildStyles.append(bstyle)

"""
Analyse the layers using the analysis module. The path distance and the estimate time taken to scan the layer can be
predicted.
"""
print('Total Path Distance: {:.1f} mm'.format(analysis.getLayerPathLength(layer)))
print('Total jump distance {:.1f} mm'.format(analysis.getLayerJumpLength(layer)))
print('Time taken {:.1f} s'.format(analysis.getLayerTime(layer, [model])) )

