from pioneer.common.gui import Product

from PyQt5.QtGui import QOpenGLShaderProgram, QOpenGLShader

class GLSLProgram( Product.Product ):
    def __init__(self, parent = None, vertex_shader = None, geometry_shader = None, fragment_shader = None, uniforms = {}, textures = {}, outputTextures = {}):
        super(GLSLProgram, self).__init__(parent)
        self._vertexShader = None
        self._geometryShader = None
        self._fragmentShader = None
        self._uniforms = {}
        self._textures = {}
        self._outputTextures = {}
        self._linkDirty = False


        self.vertexShader = vertex_shader
        self.geometryShader = geometry_shader
        self.fragmentShader = fragment_shader
        self.uniforms = uniforms
        self.textures = textures
        self.outputTextures = outputTextures

    def _update(self):

        if self._linkDirty:
            self._program = QOpenGLShaderProgram()
            if self._vertexShader is not None:
                self._program.addShaderFromSourceCode( QOpenGLShader.Vertex, self._vertexShader )
            if self._geometryShader is not None:
                self._program.addShaderFromSourceCode( QOpenGLShader.Geometry, self._geometryShader )
            if self._fragmentShader is not None:
                self._program.addShaderFromSourceCode( QOpenGLShader.Fragment, self._fragmentShader )
            self._program.link()
            self._linkDirty = False

    Product.InputProperty(vars(), 'QVariant', 'uniforms')

    ''' supports dict of Array, subject to the constraints associated with Image.to_QImage() '''
    Product.InputProperty(vars(), 'QVariant', 'textures')

    Product.InputProperty(vars(), 'QVariant', 'outputTextures')


    def relink(self):
        self._linkDirty = True

    Product.InputProperty(vars(), str, 'geometryShader', relink)

    Product.InputProperty(vars(), str, 'vertexShader', relink)

    Product.InputProperty(vars(), str, 'fragmentShader', relink)


class Effect( Product.Product ):
    def __init__(self, parent = None, shader0 = None, point_size = 1, line_width = 1, name = ""):
        super(Effect, self).__init__(parent)
        self._shader0 = None
        self._pointSize = 1
        self._lineWidth = 1
        self.setObjectName(name)

        self.shader0 = shader0
        self.pointSize = point_size
        self.lineWidth = line_width

    Product.InputProperty(vars(), GLSLProgram, 'shader0')

    Product.InputProperty(vars(), int, 'pointSize')

    Product.InputProperty(vars(), int, 'lineWidth')

