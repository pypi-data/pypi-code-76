from pioneer.common import linalg
from pioneer.common.logging_manager import LoggingManager
from pioneer.common.gui import Actors, Geometry, Effect, Transforms, CustomAttribs, Array, CustomEffects, utils

from matplotlib import colors as mpl_colors, cm
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QMatrix4x4, QVector3D, QQuaternion, QColor, QPainterPath, QFont

import collada
import os
import numpy as np
import tqdm

try:
    import pymesh
except:
    LoggingManager.instance().warning("please install pymesh by downloading the right whl at https://github.com/PyMesh/PyMesh/releases")

try:
    import transforms3d
except:
    LoggingManager.instance().warning("please install transform3d - pip install transform3d")

def ensure_Transform(tf):

    if tf is None:
        return ensure_Transform(QMatrix4x4())

    if isinstance(tf, np.ndarray):
        tf = utils.from_numpy(tf.astype('f4'))
    if isinstance(tf, QMatrix4x4):
        return Transforms.MatrixTransform(matrix = tf)
    elif isinstance(tf, Transforms.Transform):
        return tf
    
    raise RuntimeError(f"Unsupported type: {type(tf)}")

def ensure_QColor(color):
    if isinstance(color, QColor):
        return color
    return QColor(color)

def colored_point_cloud(points, colors, matrix = np.eye(4, dtype = 'f4'), name = "pcl"):
    #color = ensure_QColor(color)
    return Actors.Actor(
        geometry = Geometry.Geometry(
            attribs = CustomAttribs.ColorsAttribs( 
                vertices = Array.Array(ndarray = points)
                , colors = Array.Array(ndarray = colors))
            , primitive_type = Geometry.PrimitiveType.POINTS
        ), effect = CustomEffects.point_colors()
        , transform = ensure_Transform(matrix)
        , name = name
    )

def colored_quad_cloud(points, amplitude ,indices, colormap = "viridis", log_scale = False, cm_resolution = 256, matrix = np.eye(4, dtype = 'f4'), color=None,name = "quad"):
    #color = ensure_QColor(color)

    min_amplitude = float(amplitude.min())
    max_amplitude = float(amplitude.max())

    if log_scale:
        norm = mpl_colors.LogNorm(1, cm_resolution)
    else:
        norm = mpl_colors.Normalize(0, cm_resolution)

    colormap_ = getattr(cm, colormap)(norm(np.arange(cm_resolution)))
    cm_array = np.ascontiguousarray(colormap_ * 255, dtype=np.uint8)

    if color is None:
        effect = CustomEffects.color_map(Array.Array(ndarray = cm_array), amplitude.min(), amplitude.max())
    else:
        effect = CustomEffects.material(color=color)
    
    return Actors.Actor(
        geometry = Geometry.Geometry(
            indices = Array.Array(ndarray = indices)
            ,attribs = CustomAttribs.ColorsAttribs( 
                vertices = Array.Array(ndarray = points)
                , colors = Array.Array(ndarray = amplitude))
            , primitive_type = Geometry.PrimitiveType.TRIANGLES
        ), effect = effect
        , transform = ensure_Transform(matrix)
        , name = name
    )
                
def colormap_point_cloud(points, amplitude, min_amplitude = None, max_amplitude = None, colormap = "viridis", log_scale = False, cm_resolution = 256, matrix = np.eye(4, dtype = 'f4'), name = "cmap_pcl"):
    """
    resolution: the color map texture resolution, it affect granularity/precision of the color distribution only
    """

    if min_amplitude is None:
        min_amplitude = float(amplitude.min())

    if max_amplitude is None:
        max_amplitude = float(amplitude.max())

    if log_scale:
        norm = mpl_colors.LogNorm(1, cm_resolution)
    else:
        norm = mpl_colors.Normalize(0, cm_resolution)

    colormap_ = getattr(cm, colormap)(norm(np.arange(cm_resolution)))
    cm_array = np.ascontiguousarray(colormap_ * 255, dtype=np.uint8)

    return Actors.Actor(
        geometry = Geometry.Geometry(
            attribs = CustomAttribs.AmplitudeAttribs( 
                vertices = Array.Array(ndarray = points)
                , amplitude = Array.Array(ndarray = amplitude))
            , primitive_type = Geometry.PrimitiveType.POINTS
        ), effect = CustomEffects.color_map(Array.Array(ndarray = cm_array), min_amplitude, max_amplitude)
        , transform = ensure_Transform(matrix)
        , name = name
    )

def lines(indices, vertices, color = QColor("blue"), matrix = np.eye(4, dtype = 'f4'), name = "lines"):
    color = ensure_QColor(color)
    return Actors.Actor(
        geometry = Geometry.Geometry(
            indices = Array.Array(ndarray = indices)
            , attribs = Geometry.Attribs( 
                vertices = Array.Array(ndarray = vertices))
            , primitive_type = Geometry.PrimitiveType.LINES
        ), effect = CustomEffects.emissive(color)
        , transform = ensure_Transform(matrix)
        , name = name
        )

def normals_actor(actor, scale = 0.1, color = QColor("green"), name = "normals", v = None, n = None, matrix = None):
    if actor is not None:
        v = actor.geometry.attribs.vertices.ndarray
        n = actor.geometry.attribs.normals.ndarray
        name = f"{actor.objectName()}_{name}"

    size = v.shape[0]

    vertices = np.vstack((v, v+n*scale))
    indices = np.array(list(zip(range(size), range(size, 2*size))), 'u4').flatten()

    a = lines(indices, vertices, color, name = name)
    a.transform = actor.transform if actor is not None else ensure_Transform(matrix)

    return a

def triangulation_actor(triangles, vertices, color = QColor("blue"), matrix = np.eye(4, dtype = 'f4'), name = "lines"):

    if len(triangles.shape) == 1:
        triangles = triangles.reshape(triangles.shape[0]//3, 3)
    
    l = np.empty((triangles.shape[0], 2, 3), 'u4')

    for i in range(3):
        l[:,0, i] = triangles[:,i]
        l[:,1, (i+1)%3] = triangles[:,(i+1)%3]

    return lines(l.flatten(), vertices, color, name = name, matrix = matrix)


def shallow_copy(actor, effect_f = CustomEffects.material, color = None, matrix = None, name = None, instance_id = None):

    name = actor.objectName() if name is None else name
    instance_id = actor.instance_id if instance_id is None else instance_id

    if isinstance(actor, Actors.Actor):
        return Actors.Actor(
            geometry = actor.geometry
            , effect = actor.effect if color is None else effect_f(color)
            , transform = actor.transform if matrix is None else ensure_Transform(matrix)
            , name = name
            , bbox = actor.bbox
            , type_id = actor.type_id
            , instance_id = instance_id)
    elif isinstance(actor, Actors.Actors):
        tf = ensure_Transform(matrix)
        actors = Actors.Actors(name = name, bbox = actor.bbox, shared_transform = tf, scale = actor.scale
            , all_vertices = actor.all_vertices, type_id = actor.type_id, instance_id = instance_id)
        
        for a in actor.children_actors():
            actors.addActor(shallow_copy(a, effect_f, color, tf, a.objectName(), instance_id))

        return actors



def grid(orientation = 'xy', span = 250, div = 5, color = QColor.fromRgbF(.3,.3,.3,1.0), matrix = np.eye(4, dtype = 'f4'), name = "grid_xz"):
    
    #FIXME optimize (meshgrid?, numba?)
    color = ensure_QColor(color)
    l = []
    n = int(span*2/div)

    for i in range(0, n*n, n):
        l.extend([i, i+n-1])

    for i in range(n):
        l.extend([i, (n-1)*n+i])

    v = [] 
    for x in np.arange(-span, span, div):
        for y in np.arange(-span, span, div):
            v.append([x, y, 0])
    

    vertices = np.array(v, 'f4')
    if orientation == 'xy':
        pass
    elif orientation == 'xz':
        vertices[:,2] = vertices[:,1]
        vertices[:,1] = 0
    
    return lines(np.array(l, 'u4'), vertices, color, matrix, name)

def grid_xz(span = 250, div = 5, color = QColor.fromRgbF(.3,.3,.3,1.0), matrix = np.eye(4, dtype = 'f4'), name = "grid_xz"):
    return grid('xz', span, div, color, matrix, name)

def grid_xy(span = 250, div = 5, color = QColor.fromRgbF(.3,.3,.3,1.0), matrix = np.eye(4, dtype = 'f4'), name = "grid_xy"):
    return grid('xy', span, div, color, matrix, name)

def from_mesh(mesh, color = QColor("blue"), effect_f = CustomEffects.material, scale = 1, matrix = np.eye(4, dtype = 'f4'), name = "mesh"):
    color = ensure_QColor(color)
    mesh.add_attribute("vertex_normal")
    return Actors.Actor(
        geometry = Geometry.Geometry(
            indices = Array.Array(ndarray = mesh.faces.flatten().astype('u4'))
            , attribs = Geometry.Attribs(
                vertices = Array.Array(ndarray = mesh.vertices.astype('f4') * scale)
                , normals = Array.Array(ndarray = mesh.get_vertex_attribute("vertex_normal").astype('f4')))
            , primitive_type = Geometry.PrimitiveType.TRIANGLES
        ), effect = effect_f(color = color)
        , transform = ensure_Transform(matrix)
        , name = name
    )

def cylinder(center0 = [0,0,0], center1 = [0,0,1], radius0 = 1, radius1 = 0.1, num_segments = 42, color = QColor("blue"), effect_f = CustomEffects.material, matrix = np.eye(4, dtype = 'f4'), name = "cylinder"):
    cyl = pymesh.generate_cylinder(center0, center1, radius0, radius1, num_segments=num_segments)
    return from_mesh(cyl, color, effect_f, 1, matrix, name)

def arrow(start = [0,0,0], end = [0,0,1], thickness = 0.1, color = QColor("blue"), effect_f = CustomEffects.material, matrix = np.eye(4, dtype = 'f4'), name = "arrow"):
    start = utils.to_numpy(start)
    end = utils.to_numpy(end)
    direction = end - start
    cyl = pymesh.generate_cylinder(start, start + direction * 0.9, thickness, thickness, 10)
    head = pymesh.generate_cylinder(start + direction * 0.9, end, thickness * 2, thickness * 0.1, 10)
    return from_mesh(pymesh.merge_meshes([cyl, head]), color, effect_f, 1, matrix, name)

def sphere(radius = 0.1, center = [0,0,0], refinement_order = 1, color = QColor("blue"), effect_f = CustomEffects.material, matrix = np.eye(4, dtype = 'f4'), name = "sphere"):
    sph = pymesh.generate_icosphere(radius, center, refinement_order)
    return from_mesh(sph, color, effect_f, 1, matrix, name)

def quad(top_left = [0,0,0], bottom_left = [0,1,0], bottom_right = [1,1,0], top_right = None
, texcoords = [[0,0], [0,1], [1,1], [1,0]]
, filled = False
, color = QColor("blue")
, effect_f = CustomEffects.material
, textures = None
, matrix = np.eye(4, dtype = 'f4'), name = "quad"):

    color = ensure_QColor(color)

    top_left = utils.to_numpy(top_left)
    bottom_left = utils.to_numpy(bottom_left)
    bottom_right = utils.to_numpy(bottom_right)

    v_top = top_left - bottom_left
    v_right = bottom_right - bottom_left
    if top_right is None:
        top_right = bottom_right + v_top
    else:
        top_right = utils.to_numpy(top_right)

    indices = [0,1,2, 3,0,2] if filled else [0,1, 1,2, 2,0, 3,0, 0,2, 2,3]

    vertices = np.vstack((top_left, bottom_left, bottom_right, top_right))

    normals =  np.empty_like(vertices)

    n = np.cross(v_right, v_top)
    normals[:] = n/np.linalg.norm(n)
    
    

    if textures is not None:
        effect = effect_f(textures = textures, color = color)
    else:
        effect = effect_f(color = color)

    return Actors.Actor(
        geometry = Geometry.Geometry(
            indices = Array.Array(ndarray = np.array(indices, 'u4'))
            , attribs = CustomAttribs.TexcoordsAttribs( 
                vertices = Array.Array(ndarray = np.array(vertices, 'f4'))
                , normals = Array.Array(ndarray = np.array(normals, 'f4'))
                , texcoords0 = Array.Array(ndarray = np.array(texcoords, 'f4'))
              ), primitive_type = Geometry.PrimitiveType.TRIANGLES if filled else Geometry.PrimitiveType.LINES
        ), effect = effect
        , transform = ensure_Transform(matrix)
        , name = name
        )

def lane(vertices, color, double=False, dashed=False, width=0.07, matrix = np.eye(4, dtype = 'f4')):

    actors = Actors.Actors()

    offset = width if double else 0
    nb_lanes = 2 if double else 1

    dash_lenght = 1
    lenght_drew = 0
    total_lenght = 0

    for n in range(nb_lanes):

        ddashed = dashed[n] if double else dashed

        if ddashed:
            # For dashed lanes, the distance between vertices needs to be shorter than the dash lenght to be properly displayed
            # So, we upsample if required
            while np.max(((vertices[1:,0] - vertices[:-1,0])**2 + (vertices[1:,1] - vertices[:-1,1])**2)**0.5) > dash_lenght/2:
                new_vertices = (vertices[:-1] + vertices[1:])/2 
                vertices = np.insert(vertices, np.indices(vertices.shape)[0,1:,0], new_vertices, axis=0) 

        for i in range(vertices.shape[0]-1):

            v1x, v1y, v1z = vertices[i,0], vertices[i,1], vertices[i,2]
            v2x, v2y, v2z = vertices[i+1,0], vertices[i+1,1], vertices[i+1,2]

            # Rotate the lane segment so its aspect is preserved in all orientations
            angle = np.arctan(abs(v2y - v1y)/abs(v2x - v1x))
            dx = (width/2)*np.sin(angle)
            dy = (width/2)*np.cos(angle)
            doffx = offset*np.sin(angle)
            doffy = offset*np.cos(angle)

            # Draw half the time only
            if ddashed:
                lenght = ((v2x - v1x)**2 + (v2y - v1y)**2)**0.5
                total_lenght += lenght
                if lenght_drew > total_lenght/2 and int(total_lenght%(2*dash_lenght)):
                    continue
                lenght_drew += lenght
                

            actor = actors.addActor(
                quad(
                    top_left     = [v2x+dx+doffx, v2y+dy+doffy, v2z],
                    bottom_left  = [v1x+dx+doffx, v1y+dy+doffy, v1z],
                    bottom_right = [v1x-dx+doffx, v1y-dy+doffy, v1z],
                    top_right    = [v2x-dx+doffx, v2y-dy+doffy, v2z],
                    filled = True,
                    matrix = matrix,
                    color = color,
                    name = 'lanes',
                    effect_f = CustomEffects.emissive_both_sides
                )
            )

        offset *= -1 #for double lanes, reverse the offset for the second lane

    return actors

def chessboard(nx = 4, ny = 3, dx = 0.1, dy = 0.1, matrix = np.eye(4, dtype = 'f4'), name = "chessboard", color1 = "white", color2 = "black"):

    actors = Actors.Actors()

    actors.chessboard_shared_Transform = ensure_Transform(matrix)
    
    n_squares_x = nx+1
    n_squares_y = ny+1


    for x in range(n_squares_x+2):
        cb_x_i = x-2
        x_even = (cb_x_i)%2 == 0
        x_border = x in (0, n_squares_x+1)
        for y in range(n_squares_y+2):
            cb_y_i = y-2
            y_even = cb_y_i%2 == 0
            y_border = y in (0, n_squares_y+1)
            is_border = x_border or y_border
            color_name = color1 if is_border or (x_even != y_even) else color2
            actor = actors.addActor(quad(
              top_left     = [(x-2)*dx, (y-2)*dy, 0] #we want the (0,0) detected point in (0,0,0)
            , bottom_left  = [(x-2)*dx, (y-1)*dy, 0]
            , bottom_right = [(x-1)*dx, (y-1)*dy, 0]
            , top_right    = [(x-1)*dx, (y-2)*dy, 0]
            , filled = True
            , matrix = actors.chessboard_shared_Transform
            , color = QColor(color_name)
            , name = f"{name}_{color_name}_{x}_{y}"))
            actor.effect.shader0.uniforms['back_color'] = actor.effect.shader0.uniforms['color']
    
    actors.setObjectName(name)

    return actors

def box(min = [0,0,0], max = [1,1,1], filled = False, color = QColor("blue"), effect_f = CustomEffects.material, matrix = np.eye(4, dtype = 'f4'), name = "box"):

    color = ensure_QColor(color)

    indices = [0,1,3, 3,2,0,   7,5,4, 4,6,7,   4,5,1, 1,0,4,   5,7,3, 3,1,5,   6,2,3, 3,7,6,   4,0,2, 2,6,4] if filled else\
              [0,1, 1,3, 3,2, 2,0,       4,5, 5,7, 7,6, 6,4,      0,4, 1,5, 2,6, 3,7]

    vertices = [
                  [min[0], min[1], min[2]] #0
                , [min[0], min[1], max[2]] #1
                , [min[0], max[1], min[2]] #2
                , [min[0], max[1], max[2]] #3
                , [max[0], min[1], min[2]] #4
                , [max[0], min[1], max[2]] #5
                , [max[0], max[1], min[2]] #6
                , [max[0], max[1], max[2]] #7
                ]

    normals =  [
                 [-0.577350269,-0.577350269,-0.577350269] #0
                ,[-0.577350269,-0.577350269, 0.577350269] #1
                ,[-0.577350269, 0.577350269,-0.577350269] #2
                ,[-0.577350269, 0.577350269, 0.577350269] #3
                ,[ 0.577350269,-0.577350269,-0.577350269] #4
                ,[ 0.577350269,-0.577350269, 0.577350269] #5
                ,[ 0.577350269, 0.577350269,-0.577350269] #6
                ,[ 0.577350269, 0.577350269, 0.577350269] #7
                ]
    
    return Actors.Actor(
        geometry = Geometry.Geometry(
            indices = Array.Array(ndarray = np.array(indices, 'u4'))
            , attribs = Geometry.Attribs( 
                vertices = Array.Array(ndarray = np.array(vertices, 'f4'))
                , normals = Array.Array(ndarray = np.array(normals, 'f4'))
              ), primitive_type = Geometry.PrimitiveType.TRIANGLES if filled else Geometry.PrimitiveType.LINES
        ), effect = effect_f(color) if filled else CustomEffects.emissive(color)
        , transform = ensure_Transform(matrix)
        , name = name
        )
    
def axes(size = 1, matrix = np.eye(4, dtype = 'f4'), line_width = 1, name = "axes"):

    indices = [0,1,   2, 3,   4,5]
    vertices = [  [0,0,0] #0
                , [size,0,0] #1
                , [0,0,0] #2
                , [0,size,0] #3
                , [0,0,0] #4
                , [0,0,size] #5
                ]
    colors =   [  [1,0,0] #red
                , [1,0,0] #red
                , [0,1,0] #green
                , [0,1,0] #green
                , [0,0,1] #blue
                , [0,0,1] #blue
               ]
    return Actors.Actor(
        geometry = Geometry.Geometry(
            indices = Array.Array(ndarray = np.array(indices, 'u4'))
            , attribs = CustomAttribs.ColorsAttribs( 
                vertices = Array.Array(ndarray = np.array(vertices, 'f4'))
                , colors = Array.Array(ndarray = np.array(colors, 'f4'))
              )
            , primitive_type = Geometry.PrimitiveType.LINES
        ), effect = CustomEffects.point_colors(line_width = line_width)
        , transform = ensure_Transform(matrix)
        , name = name
        )

def from_file(path, color = QColor("blue"), effect_f = CustomEffects.material, scale = 1, matrix = np.eye(4, dtype = 'f4'), name = "mesh"):
    mesh = pymesh.load_mesh(path)
    return from_mesh(mesh, color, effect_f, scale, matrix, name)

def text(text, font = "Arial", font_size = 6, line_width = 1, color = QColor("blue"), matrix = np.eye(4, dtype = 'f4')
, is_billboard = True, name = "text", scale = 0.1, origin = [0,0,0], u = [1,0,0], v = [0,1,0], w = [0,0,1]):
    '''
        Warning, this function can crash if called before any call to QApplication(sys.argv)
    '''

    color = ensure_QColor(color)

    origin = utils.to_numpy(origin)
    u = utils.to_numpy(u)
    v = utils.to_numpy(v)
    w = utils.to_numpy(w)    

    indices = []
    vertices = []

    path = QPainterPath()
    path.addText(QPointF(0, 0), QFont(font, font_size), text)
    polygons = path.toSubpathPolygons()
    for polygon in polygons:
        for point in polygon:
            indices.append(len(vertices))
            p = utils.to_numpy([point.x(), point.y(), 0]) * scale
            vertices.append(origin + p[0] * u + p[1] * v + p[2] * w)
        indices.append(-1)
    

    return Actors.Actor(
        geometry = Geometry.Geometry(
            indices = Array.Array(ndarray = np.array(indices, 'u4'))
            , attribs = Geometry.Attribs( 
                vertices = Array.Array(ndarray = np.array(vertices, 'f4'))
              )
            , primitive_type = Geometry.PrimitiveType.LINE_LOOP
        ), effect = CustomEffects.emissive(color, line_width = line_width, is_billboard = is_billboard)
        , transform = ensure_Transform(matrix)
        , name = f"{name}_{text}"
        )

def bbox(c = [0,0,0],d = [0,0,0],r=[0,0,0], color = QColor("blue"), effect_f = CustomEffects.material, matrix = np.eye(4, dtype = 'f4'), name = "bbox", return_anchor=False, draw_orientation=True):

    color = ensure_QColor(color)

    indices = [0,1, 1,3, 3,2, 2,0,       4,5, 5,7, 7,6, 6,4,      0,4, 1,5, 2,6, 3,7]
    vertices = linalg.bbox_to_8coordinates(c, d, r)
    vertices = np.vstack([vertices, np.mean(vertices[[5,7]], axis = 0)])
    
    if draw_orientation:
        # add central front point
        # and indices to draw the direction arrow
        indices += [1,8,3,8]

    text_anchor = vertices[np.argmin(np.sum(vertices,axis=1))]
    vertices = vertices.astype('f4')
    
    actor = Actors.Actor(
        geometry = Geometry.Geometry(
            indices = Array.Array(ndarray = np.array(indices, 'u4'))
            , attribs = Geometry.Attribs( 
                vertices = Array.Array(ndarray = vertices)
              ), primitive_type = Geometry.PrimitiveType.LINES
        ), effect = CustomEffects.emissive(color)
        , transform = ensure_Transform(matrix)
        , name = name
        )
  
    if return_anchor:
        return actor, vertices[-1]
    else:
        return actor

def load_collada(filename, scale = 1, matrix = np.eye(4, dtype = 'f4'), name = "collada", bake_matrix = True, merge_actors = True, ignore_non_textured = False, invert_normals = False, type_id = -1, instance_id = -1):

    actors = Actors.Actors(shared_transform = ensure_Transform(np.eye(4, dtype = 'f4')) if bake_matrix else ensure_Transform(matrix), name = name, type_id = type_id, instance_id = instance_id)

    mesh = collada.Collada(filename)

    np_matrix = utils.to_numpy(matrix)
    
    textures_cache = {}

    actors_cache = {}

    bbox = np.full((2,3), np.finfo('f4').max)
    bbox[1,:] = np.finfo('f4').min

    actors.all_vertices = []
    actors.scale = scale

    for coll_geom in tqdm.tqdm(mesh.scene.objects('geometry')):
        for coll_prim in coll_geom.primitives():
            
            #FIXME: stop ignoring colladas transforms

            if isinstance(coll_prim, collada.triangleset.BoundTriangleSet):
                triangles = coll_prim
            elif isinstance(coll_prim, collada.polylist.BoundPolylist):
                triangles = coll_prim.triangleset()
            else:
                LoggingManager.instance().warning(f"{type(coll_prim)} not implementend")
                continue

            textures = {}
            effect_signature = [] #for merging actors
            uniforms = {}
            for effect_name in triangles.material.effect.supported:
                value = getattr(triangles.material.effect, effect_name)
                if isinstance(value, collada.material.Map):

                    texture_image = value.sampler.surface.image
                    effect_signature.append((effect_name, texture_image.id))
                    if texture_image.id in textures_cache:
                        textures[effect_name] = textures_cache[texture_image.id]
                    else:
                        array = textures[effect_name] = textures_cache[texture_image.id] = Array.Array(ndarray = utils.load_texture(texture_image.pilimage))
                elif isinstance(value, tuple):
                    uniforms[effect_name] = QColor.fromRgbF(*value)
                    effect_signature.append((effect_name, value))
                elif isinstance(value, float):
                    uniforms[effect_name] = value
                    effect_signature.append((effect_name, value))
                elif value is not None:
                    LoggingManager.instance().warning(f"Unsupported type {effect_name}: {type(value)}")
                

            if not textures and ignore_non_textured:
                    continue

            effect_signature = frozenset(effect_signature)

            triangles.generateNormals()
            
            vertices = triangles.vertex.astype('f4') * scale

            normals = triangles.normal.astype('f4')

            if invert_normals:
                normals = normals * -1

            if bake_matrix:
                vertices = linalg.map_points(np_matrix, vertices)
                normals = linalg.map_vectors(np_matrix, normals)

            indices = triangles.vertex_index.flatten().astype('u4')
            attributes_ndarrays = {"vertices": vertices, "normals": normals}
            indexed_vertices = vertices[triangles.vertex_index.flatten()]

            for i in range(3):
                bbox[0, i] = min(bbox[0, i], indexed_vertices[:,i].min())
                bbox[1, i] = max(bbox[1, i], indexed_vertices[:,i].max())

            if textures:
                if len(triangles.texcoordset) > 1:
                    LoggingManager.instance().warning(f"warning, {type(coll_prim)} not implementend")
                orig_tc0 = triangles.texcoordset[0].astype('f4')
                tc0_idx = triangles.texcoord_indexset[0].flatten()
                if not np.all(tc0_idx == indices):
                    assert tc0_idx.shape == indices.shape, "texcoord indices must be the same shape as vertex indices"
                    #this will duplicate shared vertices so that we can have a separate texcoords for each triangle sharing vertices
                    attributes_ndarrays['vertices'] = indexed_vertices
                    attributes_ndarrays['normals'] = normals[triangles.normal_index.flatten()]
                    indices = np.arange(indices.shape[0], dtype = indices.dtype)
                    uv = orig_tc0[tc0_idx]
                else:
                    uv = np.empty((vertices.shape[0], 2), 'f4')
                    uv[indices] = orig_tc0[tc0_idx]
                
                attributes_ndarrays['texcoords0'] = uv
                
                attribs = CustomAttribs.TexcoordsAttribs(vertices = Array.Array(ndarray = attributes_ndarrays['vertices'] )
                , normals = Array.Array(ndarray = attributes_ndarrays['normals'] )
                , texcoords0 = Array.Array(ndarray = attributes_ndarrays['texcoords0']))
                #FIXME: bind collada uniforms if present
                effect = CustomEffects.textured_material(textures)
            else:
                attribs = Geometry.Attribs(vertices = Array.Array(ndarray = attributes_ndarrays['vertices'] )
                , normals = Array.Array(ndarray = attributes_ndarrays['normals']))
                #FIXME: bind other uniforms if present
                effect = CustomEffects.material(color = uniforms['diffuse'], back_color = uniforms['diffuse'])

            if invert_normals:
                indices = indices.reshape((indices.shape[0]//3), 3)[:,[0,2,1]].flatten()

            if merge_actors and effect_signature in actors_cache:

                actor = actors_cache[effect_signature]

                actor_attributes = actor.geometry.attribs.get_attributes()
                
                n_vertices_before = actor_attributes['vertices'].shape[0]

                for attr_name, value in actor_attributes.items():
                    value.set_ndarray(np.vstack((value.ndarray, attributes_ndarrays[attr_name])))
                
                actor.geometry.indices.set_ndarray(np.hstack((actor.geometry.indices.ndarray, indices + n_vertices_before)))

            else:
                geometry = Geometry.Geometry(indices = Array.Array(ndarray = indices), attribs = attribs)

                actor = actors.addActor(Actors.Actor(geometry = geometry
                , effect = effect
                , transform = actors.shared_transform
                , name = f"{name}_{coll_geom.original.id}"
                , type_id = type_id
                , instance_id = instance_id))

                actors_cache[effect_signature] = actor
            
                actors.all_vertices.append(actor.geometry.attribs.vertices) #if in merge actor mode, vertices are already there

    actors.bbox = bbox

    return actors
