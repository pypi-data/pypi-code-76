from pioneer.common import times
from pioneer.common.logging_manager import LoggingManager
from pioneer.common.gui import Array
from pioneer.common.gui import utils

from future.utils import viewitems
from inspect import currentframe, getframeinfo
from OpenGL import GL
from operator import attrgetter
from PyQt5.QtQuick import QQuickFramebufferObject
from PyQt5.QtGui import QMatrix4x4, QVector3D, QVector4D, QOpenGLTexture, QOpenGLContext, QOpenGLBuffer, \
QOpenGLFramebufferObject, QOpenGLFramebufferObjectFormat, QOpenGLVersionProfile,\
QOpenGLVertexArrayObject, QSurfaceFormat

import copy
import ctypes
import matplotlib.pyplot as plt
import numpy as np
import traceback

def opengl_error_check(cf, prefix = ""): # pass currentframe()
    error = GL.glGetError()
    if error != GL.GL_NO_ERROR:
        frameinfo = getframeinfo(cf)
        LoggingManager.instance().warning(f"{prefix} @ line {frameinfo.lineno} : OpenGL error {error}")
        return True
    return False

class InFboRenderer( QQuickFramebufferObject.Renderer ):
    def __init__( self ):
        super(InFboRenderer, self).__init__()
        self.vertices_array = None
        self.sorted_actors = []
        self.vertex_array = None
        self.render_to_texture = None
        
        self.render_to_texture_attachment = -1
        self.render_to_texture_array = None
        self.locked_render_to_texture_array = Array.Array(ndarray = np.empty((0,0,4), np.uint8))

        self.draw_buffers = [GL.GL_COLOR_ATTACHMENT0, GL.GL_COLOR_ATTACHMENT1, GL.GL_COLOR_ATTACHMENT2, GL.GL_COLOR_ATTACHMENT3, GL.GL_COLOR_ATTACHMENT4]
        

    def to_texture_target(self, array):
        shape = array.ndarray.shape
        target = None
        if len(shape) == 2 or (len(shape) == 3 and shape[1] == 1):
            target = QOpenGLTexture.Target1D
        elif len(shape) == 3:
            target = QOpenGLTexture.Target2D
        elif len(shape) == 4:
            target = QOpenGLTexture.Target3D
        return target

    def attach_texture_object(self, array):
        if not hasattr(array, "___tex___"):
            target = self.to_texture_target(array)
            if target == None:
                raise RuntimeError('Unable to determine texture  binding target')

            array.___tex___ = QOpenGLTexture(target)
            array.___tex___.setMinificationFilter(QOpenGLTexture.Linear)
            array.___tex___.setMagnificationFilter(QOpenGLTexture.Linear)
            array.___tex___.setWrapMode(QOpenGLTexture.DirectionS, QOpenGLTexture.Repeat)
            if target in [QOpenGLTexture.Target2D, QOpenGLTexture.Target3D]:
                array.___tex___.setWrapMode(QOpenGLTexture.DirectionT, QOpenGLTexture.Repeat)
                if target == QOpenGLTexture.Target3D:
                    array.___tex___.setWrapMode(QOpenGLTexture.DirectionR, QOpenGLTexture.Repeat)
            array.___tex___.dirty = True
            array.productDirty.connect(lambda array=array: setattr(array.___tex___, "dirty", True))


    def attach_buffer_object(self, array, gl_buffer_type):
        if not hasattr(array, "___bo___"):
            array.___bo___ = QOpenGLBuffer(gl_buffer_type)
            array.___bo___.create()
            array.___bo___.setUsagePattern(QOpenGLBuffer.DynamicDraw)
            array.___bo___.dirty = True
            array.productDirty.connect(lambda array=array: setattr(array.___bo___, "dirty", True))

    def map_buffer_object(self, bo, ndarray):
        if bo.dirty:
            bo.allocate(ndarray.size * ndarray.itemsize)
            ibo_addr = bo.map(QOpenGLBuffer.WriteOnly)
            if ibo_addr is not None:
                c_type = None
                if ndarray.dtype == np.dtype(np.float32):
                    c_type = ctypes.c_float
                elif ndarray.dtype == np.dtype(np.float64):
                    c_type = ctypes.c_double
                else:
                    c_type = getattr(ctypes, 'c_' + str(ndarray.dtype))
                assert(c_type is not None)
                ibo_ptr = ctypes.cast(ibo_addr.__int__(), ctypes.POINTER(c_type))
                ibo_np = np.ctypeslib.as_array(ibo_ptr, shape=ndarray.shape)
                ibo_np[:] = ndarray
                bo.unmap()
            bo.shape = ndarray.shape
            bo.dtype = ndarray.dtype
            bo.dirty = False
    
    def goc_output_texture(self, array):

        shape = list(array.ndarray.shape)
        if not len(shape) in (2,3):
            raise RuntimeError("Unexpected shape for output texture, must me 2D, shape was {shape}")
        
        self.attach_texture_object(array)


        shape[0] = int(self.viewport_width)
        shape[1] = int(self.viewport_height)

        if tuple(shape) != tuple(array.ndarray.shape):
            array.set_ndarray(np.empty(shape, array.ndarray.dtype))
            array.___tex___.dirty = True


        if array.___tex___.dirty :
            array.___tex___.destroy()
            array.___tex___.create()
            array.___tex___.setSize(array.ndarray.shape[0], array.ndarray.shape[1])

            dtype_error = RuntimeError(f"Unsupported dtype {array.ndarray.dtype}, you can easily add it yourself")

            if shape[2] == 4:
                if array.ndarray.dtype == np.uint8:
                    array.___tex___.setFormat(QOpenGLTexture.RGBA8_UNorm)
                    array.___tex___.allocateStorage(QOpenGLTexture.RGBA, QOpenGLTexture.UInt32_RGBA8) #GL_RGBA, GL_UNSIGNED_INT_8_8_8_8
                elif array.ndarray.dtype == np.float32:
                    # untested!
                    array.___tex___.setFormat(QOpenGLTexture.RGBA32F)
                    array.___tex___.allocateStorage(QOpenGLTexture.RGBA, QOpenGLTexture.Float32) #GL_RGBA, GL_FLOAT
                else:
                    raise dtype_error
            else:
                raise RuntimeError(f"Unsupported shape {shape}, you can add support yourself")
            
            array.___tex___.shape = array.ndarray.shape
            array.___tex___.dtype = array.ndarray.dtype
            array.___tex___.dirty = False

    def get_texture_attachment(self, loc):
        if loc < 0 or loc > len(self.draw_buffers):
            raise RuntimeError(f"output texture location is {loc} must be between 0 and {len(self.draw_buffers)}")
        return self.draw_buffers[loc]
        
    def del_render_to_texture_attachment(self):
        if hasattr(self.render_to_texture_array, '___tex___'):
            # self.locked_render_to_texture_array.___tex___.destroy()
            self.locked_render_to_texture_array.___tex___.dirty = True

    def synchronize(self, viewport):

        
        
        # This function is called by Qt before calling render()
        # render() will then be called from another thread, which means anything
        # collected here (e.g. sorted_actors) should *not* be accessed during the rendering
        # I should map all buffers during synchronize, and copy all uniforms and whatnot

        viewport.setMirrorVertically(True)

        if self.vertex_array is None:
            # window = viewport.window()
            # gl_context = window.openglContext()
            # profile = QOpenGLVersionProfile()
            # profile.setProfile(QSurfaceFormat.CoreProfile)
            # profile.setVersion( 4, 1 )
            # self.gl = gl_context.versionFunctions(profile)
            
            self.vertex_array = QOpenGLVertexArrayObject()
            self.vertex_array.create()

        self.background_color = viewport._backgroundColor

        self.sorted_actors = []
        self.bo_actors = []
        self.out_textures = {}

        if viewport.actors is None :
            return

        sorted_actors = sorted(list(viewport.actors.get_visible_actors()), key=attrgetter('renderRank'))
        sorted_actors.extend(viewport._debug_actors.get_visible_actors())

        for actor in sorted_actors:
            if not actor.update() :
                if not hasattr(actor, "__error_reported___") or not actor.__error_reported___:
                    LoggingManager.instance().warning("Not rendering actor " + str(actor) + ". It is has error " + str(actor._error )+ ".")
                    actor.__error_reported___ = True
                    actor.productDirty.connect(lambda actor=actor: setattr(actor, "__error_reported___", False))
                continue

            if not hasattr(actor, 'bo_actor'):
                actor.bo_actor = {}
                actor.productDirty.connect(lambda actor=actor: setattr(actor, "bo_actor", {}))
            
            

            if not actor.bo_actor: # actor was dirty or is new
                            
                indices = actor.geometry.indices
                attribs = actor.geometry.attribs.get_attributes()

                bo_actor = {"attribs": {}
                , "textures": {}
                , "out_textures": {}
                , "uniforms": copy.deepcopy(actor.effect.shader0.uniforms)
                , "indices": None
                , "program": actor.effect.shader0._program
                , "point_size": actor.effect.pointSize
                , "line_width": actor.effect.lineWidth
                , "transform" : actor.transform.worldTransform() if actor.transform else QMatrix4x4()
                , "primitiveType": actor.geometry.primitiveType
                , "actor_not_thread_safe": actor}

                for name, value in viewitems(attribs):
                    if value is None:
                        continue
                    self.attach_buffer_object(value, QOpenGLBuffer.VertexBuffer)
                    value.___bo___.bind()

                    self.map_buffer_object(value.___bo___, value.ndarray.astype('f4') if value.ndarray.dtype == np.float64 else value.ndarray)
                    value.___bo___.release()
                    
                    bo_actor["attribs"][name] = value.___bo___

                for name, value in viewitems(actor.effect.shader0.textures):
                    if value is None:
                        LoggingManager.instance().warning('texture {} is null'.format(name))
                        continue
                    self.attach_texture_object(value)
                    if value.___tex___.target() != self.to_texture_target(value):
                        LoggingManager.instance().warning('expected texture target  {}, got  {}'.format(value.___tex___.target(), self.to_texture_target(array)))
                        value.___tex___ = None
                        self.attach_texture_object(value)
                    if value.___tex___.dirty:
                        
                        tex_ndarray = value.ndarray

                        if value.___tex___.target() == QOpenGLTexture.Target1D:
                            value.___tex___.setSize(tex_ndarray.shape[0])
                        if value.___tex___.target() == QOpenGLTexture.Target2D:
                            value.___tex___.setSize(tex_ndarray.shape[0], tex_ndarray.shape[1])
                        if value.___tex___.target() == QOpenGLTexture.Target3D:
                            value.___tex___.setSize(tex_ndarray.shape[0], tex_ndarray.shape[1], tex_ndarray.shape[2])

                        value.___tex___.setFormat(QOpenGLTexture.RGBA8_UNorm)
                        value.___tex___.allocateStorage()
                        value.___tex___.setData(QOpenGLTexture.RGBA, QOpenGLTexture.UInt8, tex_ndarray.data)

                        value.___tex___.shape = value.ndarray.shape
                        value.___tex___.dtype = value.ndarray.dtype

                        value.___tex___.dirty = False

                    
                    bo_actor["textures"][name] = value.___tex___
                
                for name, value in viewitems(actor.effect.shader0.outputTextures):
                    if value is None:
                        LoggingManager.instance().warning(f'output texture {name} is null')
                        continue

                    self.goc_output_texture(value)

                    bo_actor["out_textures"][name] = value.___tex___
                    self.out_textures[value.___tex___] = None

                if indices is not None and indices.size > 0:
                    self.attach_buffer_object(indices, QOpenGLBuffer.IndexBuffer)
                    indices.___bo___.bind()
                    self.map_buffer_object(indices.___bo___, indices.ndarray)
                    indices.___bo___.release()
                    bo_actor["indices"] = indices.___bo___

                actor.bo_actor = bo_actor

            self.sorted_actors.append(actor)
            self.bo_actors.append(actor.bo_actor)
        

        self.view_matrix = viewport.view_matrix()
        self.perspective_matrix = viewport.perspective_matrix()
        self.orthographic_matrix = viewport.orthographic_matrix()


        self.viewport_width = int(viewport.width())
        self.viewport_height = int(viewport.height())

        if viewport.render_to_texture_attachment != -1:

            old = self.render_to_texture_array
            self.render_to_texture_array = self.locked_render_to_texture_array
            self.locked_render_to_texture_array = old if old is not None else Array.Array(ndarray = np.empty((0,0,4), np.uint8))

            if self.render_to_texture_attachment != viewport.render_to_texture_attachment:
                self.del_render_to_texture_attachment()
                self.render_to_texture_attachment = viewport.render_to_texture_attachment
            
            self.goc_output_texture(self.locked_render_to_texture_array)

    def render( self ):
        

        self.framebufferObject().setAttachment(QOpenGLFramebufferObject.CombinedDepthStencil)

        e = GL.glGetError() #clear any pending errors
        
        c = self.background_color
        GL.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF() )
        GL.glClear( GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glEnable( GL.GL_BLEND )
        GL.glBlendFunc( GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA )
        GL.glBlendEquation( GL.GL_FUNC_ADD)
        GL.glEnable(GL.GL_PRIMITIVE_RESTART)
        
        
        GL.glPrimitiveRestartIndex(0xFFFFFFFF)
        GL.glDrawBuffers(len(self.draw_buffers), self.draw_buffers)

        #opengl_error_check(currentframe())

        if self.render_to_texture_attachment != -1:

            GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER
            , self.draw_buffers[self.render_to_texture_attachment]
            , GL.GL_TEXTURE_2D
            , self.locked_render_to_texture_array.___tex___.textureId()
            , 0)

            GL.glClear( GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            if GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER) != GL.GL_FRAMEBUFFER_COMPLETE:
                raise RuntimeError("glCheckFramebufferStatus() problem")
        
        #opengl_error_check(currentframe())

        for actor in self.bo_actors:
            try:
                program = actor['program']
                indices = actor['indices']
                attribs = actor['attribs']
                textures = actor['textures']
                out_textures = actor['out_textures']
                transform = actor['transform']
                uniforms = actor['uniforms']
                primitiveType = actor['primitiveType']
                point_size = actor['point_size']
                line_width = actor['line_width']

                
                program.bind()

                self.vertex_array.bind()
                
                for name, bo in viewitems(attribs):
                    if bo is None:
                        continue
                    bo.bind()
                    loc = program.attributeLocation(name)
                    program.enableAttributeArray(loc)

                    dim = bo.shape[1] if len(bo.shape) > 1 else 1

                    if bo.dtype == np.float32:
                        program.setAttributeBuffer(loc, GL.GL_FLOAT, 0, dim)
                    elif bo.dtype == np.int32:
                        program.setAttributeBuffer(loc, GL.GL_INT, 0, dim)
                    else:
                        raise ValueError(f'Unsupported dtype {bo.dtype} for attrib {name}')
                
                #opengl_error_check(currentframe())

                m = transform
                v = self.view_matrix
                p = self.perspective_matrix

                if program.uniformLocation("matrix") == -1:
                    program.setUniformValue("model_matrix", m)
                    program.setUniformValue("view_matrix", v)
                    program.setUniformValue("projection_matrix", p)
                    program.setUniformValue("normal_matrix", m.normalMatrix())
                    program.setUniformValue("view_matrix_inv", v.inverted()[0])
                else:
                    program.setUniformValue("matrix", p*v*m)
                
                if program.uniformLocation("ortho_matrix") != -1:
                    program.setUniformValue("ortho_matrix", self.orthographic_matrix)

                if program.uniformLocation("aspect_ratio") != -1:
                    program.setUniformValue("aspect_ratio", self.viewport_width/self.viewport_height)

                #opengl_error_check(currentframe())

                if program.uniformLocation("point_size") != -1:
                    GL.glDisable(GL.GL_PROGRAM_POINT_SIZE)
                    program.setUniformValue("point_size", float(point_size))
                elif point_size != 1:
                    try:
                        GL.glEnable(GL.GL_PROGRAM_POINT_SIZE)
                        GL.glPointSize(GL.GLfloat(point_size))
                    except Exception as e:
                        # glPointSize is refused by the driver
                        LoggingManager.instance().warning(f"glPointSize failed with: exception {e}")

                #opengl_error_check(currentframe())

                for name, value in viewitems(uniforms):
                    program.setUniformValue(name, value)
                    #opengl_error_check(currentframe(), f"error with uniform {name}, {value}")

                texture_unit = 0
                for name, tex in viewitems(textures):
                    tex.bind(texture_unit)
                    program.setUniformValue(name, texture_unit)
                    #opengl_error_check(currentframe(), f"error with texture {name}, {value}")
                    texture_unit += 1

                

                for name, tex in viewitems(out_textures):
                    if tex is None:
                        LoggingManager.instance().warning(f'output texture {name} is null')
                        continue

                    # in your fragment shader, you can specify the location via the layout decoration
                    # e.g. layout(location = 1) out vec4 my_output;
                    loc = GL.glGetFragDataLocation(program.programId(), name)
                    
                    GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, self.get_texture_attachment(loc), GL.GL_TEXTURE_2D, tex.textureId(), 0)

                    if GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER) != GL.GL_FRAMEBUFFER_COMPLETE:
                        raise RuntimeError("glCheckFramebufferStatus() problem")            


                #opengl_error_check(currentframe())

                if line_width != 1:
                    try:
                        GL.glEnable(GL.GL_LINE_SMOOTH)
                        #opengl_error_check(currentframe())
                        GL.glLineWidth(GL.GLfloat(line_width))
                    except Exception as e:
                        aliased_r = (GL.GLfloat * 2)()
                        GL.glGetFloatv(GL.GL_ALIASED_LINE_WIDTH_RANGE, aliased_r)
                        smooth_r = (GL.GLfloat * 2)()
                        GL.glGetFloatv(GL.GL_SMOOTH_LINE_WIDTH_RANGE, smooth_r)
                        line_r = (GL.GLfloat * 2)()
                        GL.glGetFloatv(GL.GL_LINE_WIDTH_RANGE, line_r)
                        LoggingManager.instance().warning(f"{e}: yout asked for line_width = {line_width}, line range is {list(line_r)}, aliased range is {list(aliased_r)}, smooth range is {list(smooth_r)}")
                else:
                    GL.glDisable(GL.GL_LINE_SMOOTH)

                #opengl_error_check(currentframe())

                if indices is not None and indices.shape[0] > 0:
                    indices.bind()
                    GL.glDrawElements(primitiveType, indices.shape[0], GL.GL_UNSIGNED_INT, None)
                    indices.release()
                elif attribs["vertices"].shape[0] > 0:
                    GL.glDrawArrays(primitiveType, 0, attribs["vertices"].shape[0])

                for name, bo in viewitems(attribs):
                    if bo is not None:
                        bo.release()
                        program.disableAttributeArray(name)

                for name, tex in viewitems(textures):
                    if tex is not None:
                        tex.release()

                for name, tex in viewitems(out_textures):
                    if tex is not None :
                        tex.release()

                for name, tex in viewitems(out_textures):
                    shape = tex.shape
                    tex.bind()
                    loc = GL.glGetFragDataLocation(program.programId(), name)
                    GL.glReadBuffer(self.get_texture_attachment(loc))

                    if shape[2] == 4:
                        if tex.dtype == np.uint8:
                            pixels = GL.glReadPixels(0,0,shape[0], shape[1], GL.GL_RGBA, GL.GL_UNSIGNED_INT_8_8_8_8)
                            self.out_textures[tex] = pixels.view(np.uint8).reshape(shape[1], shape[0], 4)
                        elif tex.dtype == np.float32:
                            pixels = GL.glReadPixels(0,0,shape[0], shape[1], GL.GL_RGBA, GL.GL_FLOAT)
                            self.out_textures[tex] = pixels

                    tex.release()
                    

            except Exception as e:
                LoggingManager.instance().warning(traceback.format_exc())
            finally:
                self.vertex_array.release()
                program.release()
            

        if self.render_to_texture_attachment != -1:
            shape = self.locked_render_to_texture_array.ndarray.shape
            self.locked_render_to_texture_array.___tex___.bind()
            GL.glReadBuffer(self.draw_buffers[self.render_to_texture_attachment])
            r = GL.glReadPixels(0,0,shape[0], shape[1], GL.GL_RGBA, GL.GL_UNSIGNED_INT_8_8_8_8)
            self.locked_render_to_texture_array.___tex___.release()
            self.locked_render_to_texture_array.ndarray = np.flipud(r.view(np.uint8).reshape(shape[1], shape[0], 4)[...,::-1])

        self.update()

    def createFrameBufferObject( self, size ):
        f = QOpenGLFramebufferObjectFormat()
        f.setAttachment( QOpenGLFramebufferObject.CombinedDepthStencil )
        f.setSamples( 4 )
        return QOpenGLFramebufferObject( size, f )


