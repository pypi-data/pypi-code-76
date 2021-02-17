# -*- coding: utf-8 -*-
# package: pypos3dv
import logging
import copy

from OpenGL.GL import glGetError, glCreateProgram, glCreateShader, glCompileShader, glGetShaderiv, glGetShaderInfoLog, \
  glAttachShader, glShaderSource, glLinkProgram, glUseProgram, glGetProgramiv, glGenTextures, glBindTexture, glTexImage2D, \
  glTexParameteri, glGenerateMipmap, glDeleteTextures, glGenBuffers, glBufferData, glBindBuffer, GLfloat, \
  glGetUniformLocation, glUniformMatrix4fv, glUniform4f, glEnableVertexAttribArray, glVertexAttribPointer, \
  glDrawArrays, glDisableVertexAttribArray, glDeleteBuffers, GLushort, glUniform3f, glActiveTexture, glUniform1i, \
  glDrawElements
  
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_NO_ERROR, GL_COMPILE_STATUS, GL_TRUE, GL_FALSE, \
                      GL_LINK_STATUS, GL_TEXTURE_MAG_FILTER, GL_LINEAR, \
                      GL_TEXTURE_2D, GL_RGB, GL_UNSIGNED_BYTE, GL_TEXTURE_WRAP_S, GL_REPEAT, GL_TEXTURE_WRAP_T, \
                      GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR, GL_ELEMENT_ARRAY_BUFFER, GL_STATIC_DRAW, \
                      GL_TEXTURE0, GL_TRIANGLES, GL_UNSIGNED_SHORT, GL_ARRAY_BUFFER, GL_FLOAT, GL_LINES


from OpenGL.GLU import gluErrorString
from PIL import Image
import glm
from langutil.File import File
from pypos3d.wftk.WFBasic import Point3d, TexCoord2f, Vector3d
from pypos3d.wftk.WaveGeom import WFMat

def printOpenGLError():
  err = glGetError() 
  if err!=GL_NO_ERROR:
    print('GLERROR: ', gluErrorString(err))


class Shader:
  ''' Shader class to hold vertex and fragment shaders.
  Initialized with an inlined script.
  '''
 
  def initShader(self, vertex_shader_source_list, fragment_shader_source_list):
    # create program
    self.program = glCreateProgram()
    printOpenGLError()

    # Compile vertex shader
    self.vs = glCreateShader(GL_VERTEX_SHADER) 
    glShaderSource(self.vs, vertex_shader_source_list)
    glCompileShader(self.vs)
    if GL_TRUE!=glGetShaderiv(self.vs, GL_COMPILE_STATUS):
      err =  glGetShaderInfoLog(self.vs) 
      raise Exception(err)
      
    glAttachShader(self.program, self.vs)
    printOpenGLError()

    #  Compile fragment shader
    self.fs = glCreateShader(GL_FRAGMENT_SHADER) 
    glShaderSource(self.fs, fragment_shader_source_list)
    glCompileShader(self.fs)
    if GL_TRUE!=glGetShaderiv(self.fs, GL_COMPILE_STATUS):
      err =  glGetShaderInfoLog(self.fs) 
      raise Exception(err)
           
    glAttachShader(self.program, self.fs)
    printOpenGLError()

    glLinkProgram(self.program)
    if GL_TRUE!=glGetProgramiv(self.program, GL_LINK_STATUS):
      err =  glGetShaderInfoLog(self.vs) 
      raise Exception(err)
              
    printOpenGLError()

  def begin(self):
    if glUseProgram(self.program):
      printOpenGLError()

  def end(self):
    glUseProgram(0)

class TextureLoader:
  ''' Manage Texture Loading by searching a set of directories (imgdirpath).
  imgdirpath shall be separated by the os.pathsep.
  Keep a cach of loaded textures for each GL Context [ ( GLContext, { filename --> Texture GLID } ), ]
  Note: GLContext is not hashable and can not be used as dictionary key
  '''
  glTexCach = [ ]
  
  def __init__(self, fname, mode="RGB", imgdirpath=''):
    ''' Create a GL Texture from an image file.
    Texture is identified by attribute textureGLID
    '''
    fn = File.finder(fname, imgdirpath)
    self.loadByPIL(fn, mode)

  def loadByPIL(self, fname, mode):
    logging.info('Loading Image (%s)', fname)
    image = Image.open(fname)
    converted = image.convert(mode)        
    self.buffer = converted.transpose( Image.FLIP_TOP_BOTTOM ).tobytes()
    self.height = image.height
    self.width = image.width
    self.format = mode
    image.close()
    
    self.textureGLID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, self.textureGLID)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.buffer)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glGenerateMipmap(GL_TEXTURE_2D)
    logging.info('Image (%s) loaded', fname)

  @classmethod
  def LoadTexture(cls, w3dctxt, fname, imgdirpath=''):
    # Protect from FileNotFound
    try:
      ctxtcach = None
     
      for tpl in TextureLoader.glTexCach:
        if tpl[0]==w3dctxt:
          ctxtcach = tpl[1]
          break
      
      if not ctxtcach:
        ctxtcach = { }
        TextureLoader.glTexCach.append( (w3dctxt, ctxtcach) )
        
      try:
        tl = ctxtcach[fname]      
      except KeyError:
        tl = TextureLoader(fname, imgdirpath=imgdirpath)
        ctxtcach[fname] = tl
  
    except FileNotFoundError:
      logging.info('Image (%s) not found', fname)
      tl = None
 
    return tl
  
  @classmethod
  def DeleteBuffers(cls, w3dctxt):
    ''' Delete GL resources and clean cach of the given GL context (ie. FLGW window ID). '''
    for tpl in TextureLoader.glTexCach:
      if tpl[0]==w3dctxt:
        ctxtcach = tpl[1]
        glDeleteTextures( [ tl.textureGLID  for tl in ctxtcach.values() ] )
        ctxtcach.clear()
        break

class Renderable:
  ''' Abstract class of OpenGL renderable 3d objects. '''
  def __init__(self, offset=(0.0,0.0,0.0)):
    self.isVisible = True
    self.offset = offset
    
    # Indicate if the GL objects have been created
    # with the FLGW windoow ID
    self.win3d = None

  def makeContext(self, win3d:'FLGW window'):
    self.win3d = win3d
    self.loadShader()
    self.loadObject()
    self.loadTexture()
    return self

  def loadShader(self):
    self.shader = Shader()
        
  def loadObject(self):
    #self.mesh = None
    #print("Make and fill OPENGL buffers,vertex,uv,normal,trangent,indices")
    return NotImplemented

  def loadTexture(self):
    self.texture = None
    
  def rendering(self, win3d, MVPptr, ViewPtr, ProjectionPtr):
    if not self.win3d:
      self.makeContext(win3d)
  
  def DeleteBuffers(self):
    return NotImplemented
  
  @classmethod
  def toArrayBuffer(cls, t):
    buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(t)*4, (GLfloat * len(t))(*t), GL_STATIC_DRAW)   
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    return buffer
 
  


#
# Draw a 10x10 grey grid "on the ground" and the coordinate system axis
# Ox in red, Oy in Green, Oz in Blue
class AxisGrid(Renderable):
  ''' Defines a 3D Coordinate system. '''

  def __init__(self, space=1.0, nbStep=10, center=(0.0,0.0,0.0), \
               withGrid=True, gridColor=(0.2,0.2,0.2,1.0),
               withAxis=True, oxColor=(1.0,0.2,0.2,1.0), oyColor=(0.2,1.0,0.2,1.0), ozColor=(0.2,0.2,1.0,1.0)):
    super(AxisGrid, self).__init__(offset=center)
    
    self.oxColor = oxColor
    self.oyColor = oyColor
    self.ozColor = ozColor
    self.gridColor  = gridColor
    
    self.withGrid = withGrid
    self.withAxis = withAxis
    
    # Spacing between lines
    self.space = space
    
    # Number of step in each direction
    self.nbStep = nbStep

  def loadShader(self):
    ''' Create colored Shaders. '''
    super(AxisGrid, self).loadShader()

    self.shader.initShader(
      ['''#version 300 es
      uniform mat4 MVP;
      layout(location = 0) in vec3 vertexPosition_modelspace;
 
      void main(void)
        {
        gl_Position = MVP *vec4(vertexPosition_modelspace,1);
        }
      ''',  ],\
      ['''#version 300 es
      // This Fragment returns a constant color
      uniform mediump vec4 fragmentColor;

      // Ouput data
      out mediump vec4 color;

      void main()
        {
        // Output color = color specified in the uniform constant 
        color = fragmentColor;
        }''', ])
      
    self.MVP_ID = glGetUniformLocation(self.shader.program,"MVP")
    self.shader.Color_ID = glGetUniformLocation(self.shader.program, "fragmentColor")

  def loadObject(self):
    maxVal = self.space * self.nbStep
    
    Ox, Oy, Oz = self.offset[0], self.offset[1], self.offset[2] 
    
    # Prepare Axis Buffers    
    axisX = [Ox-maxVal, Oy,        Oz] +        [Ox+maxVal, Oy,        Oz]
    axisY = [Ox,        Oy-maxVal, Oz] +        [Ox,        Oy+maxVal, Oz]
    axisZ = [Ox,        Oy,        Oz-maxVal] + [Ox,        Oy,        Oz+maxVal]

    self.axisXBuffer = Renderable.toArrayBuffer(axisX)
    self.axisYBuffer = Renderable.toArrayBuffer(axisY)
    self.axisZBuffer = Renderable.toArrayBuffer(axisZ)
    
    if self.withGrid:
      gridLines = []
      
      # Prepare Grid Buffer (one the grid)
      for noStep in range(self.withAxis, self.nbStep+1):
        pos = noStep * self.space
        gridLines.extend( [Ox-maxVal, Oy, Oz+pos] +    [Ox+maxVal, Oy, Oz+pos] )
        gridLines.extend( [Ox-maxVal, Oy, Oz-pos] +    [Ox+maxVal, Oy, Oz-pos] )
        gridLines.extend( [Ox-pos,    Oy, Oz-maxVal] + [Ox-pos,    Oy, Oz+maxVal] )
        gridLines.extend( [Ox+pos,    Oy, Oz-maxVal] + [Ox+pos,    Oy, Oz+maxVal] )
                          
      self.gridBuffer = Renderable.toArrayBuffer(gridLines)
    else:
      self.gridBuffer = None
      
  def rendering(self, win3d, MVP, View, Projection):
    super(AxisGrid, self).rendering(win3d, MVP, View, Projection)

    self.shader.begin()
    
    glUniformMatrix4fv(self.MVP_ID, 1, GL_FALSE, glm.value_ptr(MVP))

    if self.withGrid:
      glUniform4f(self.shader.Color_ID, self.gridColor[0], self.gridColor[1], self.gridColor[2], self.gridColor[3] )
      
      glEnableVertexAttribArray(0)
      glBindBuffer(GL_ARRAY_BUFFER, self.gridBuffer)
      glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
      
      glDrawArrays(GL_LINES, 0, 2*2*2*(self.nbStep+1-self.withAxis))
      glBindBuffer(GL_ARRAY_BUFFER, 0)  
      glDisableVertexAttribArray(0)

    if self.withAxis:
      for buf,col in [(self.axisXBuffer, self.oxColor), (self.axisYBuffer, self.oyColor), (self.axisZBuffer, self.ozColor), ]:
        glUniform4f(self.shader.Color_ID, col[0], col[1], col[2], col[3])
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, buf)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glDrawArrays(GL_LINES, 0, 2)
        glBindBuffer(GL_ARRAY_BUFFER, 0)  
        glDisableVertexAttribArray(0)
    
    self.shader.end()
    
  def DeleteBuffers(self):
    glDeleteBuffers(4, [self.gridBuffer, self.axisXBuffer, self.axisYBuffer, self.axisZBuffer] )




class RendGroupMat:
  ''' Contains the GL buffers and attributes required to render the part
  of a GeomGroup that share a same Material (Texture or Color)
  '''
  DEFAULT_SIG = set()  
  
  def __init__(self, grp, material:'WFMat', hasTexture, hasNormal, coords, texs, norms):    
    self.vertexs   = []
    self.texcoords = []
    self.normals   = []
    self.indices   = []
    self.hasTexture = hasTexture
    self.hasNormal  = hasNormal
    self.wg = grp.geom

    # Give a default texture color
    self.textureColor = (0.9, 0.9, 0.9, 1.0)
    
    # Temporary attributes
    self.coords = coords
    self.texs = texs
    self.norms = norms
    self.combination = { } # Dictionnary of (Vertex No, TexCoord No, Normal No): indice

    self.material = material
    self.texture = None
        
    self.vertexbuffer, self.indicesbufferSizeself, self.indicesbuffer = 0,0,0            

    if not material:
      # Use default texture Color
      self.material = WFMat('default')
      self.material.kd = self.textureColor
      gg = grp.geom.getName()+'.'+grp.getName()
      if not gg in RendGroupMat.DEFAULT_SIG:
        logging.warning('Group[%s.%s] will use default Color', grp.geom.getName(), grp.getName())
        RendGroupMat.DEFAULT_SIG.add(gg)
    
  def addGLPoint(self, vno, vtno, nno):
    ''' Add a GL point based on known coordinates.'''
    vtnpoint = (vno, vtno, nno)

    try:
      newindex = self.combination[vtnpoint]
      
    except KeyError:      
      # Add a new combination of Vertex, Texture Coords and Normal
      p = self.coords[vno]                  
      self.vertexs.extend( p )
      
      if vtno>=0 and self.hasTexture:
        t = self.texs[vtno]
        self.texcoords.extend( t )

      if nno>=0 and self.hasNormal:      
        n = self.norms[nno]                  
        self.normals.extend( n )
      
      newindex = len(self.combination)      
      self.combination[vtnpoint] = newindex
        
    self.indices.append(newindex)


  def addExtraGLPoint(self, ptab, ttab, ntab):
    ''' Add a GL point based on new coordinates.'''
    vno = len(self.coords)
    self.coords.append( ptab )

    if self.hasTexture:
      vtno = len(self.texs)
      self.texs.append( ttab )
    else:
      vtno = -1
    
    if self.hasNormal:
      nno = len(self.norms)
      self.norms.append(ntab)
    else:
      nno = -1
      
    self.addGLPoint(vno, vtno, nno)


  def checkClear(self):
    ''' Shall be called at the end of a RendGroupMat creation. '''
    del self.combination
    self.coords = None
    self.texs = None
    self.norms = None
    return len(self.indices)


class RendWaveGeom(Renderable):
  ''' Rendering of a WaveGeom with a several textures.
  Keeps data on a WaveGeom to render it in a GL Window.
  Uses RendGroupMat.
  '''

  def __init__(self, wg, defaultLibMat:'Dict of Materials (WFMat)'=None, location=(0.0,0.0,0.0)):
    super(RendWaveGeom, self).__init__(offset=location)

    self.meshName = wg.getName()
    self.wg = wg
    # Merge Matrials libraries
    self.libMat = copy.copy(self.wg.libMat)
    
    if defaultLibMat:
      self.libMat.update(defaultLibMat)
      
    self._models = None
    self.hasNormal = (wg.normList!=None) and (len(wg.normList)>0)
    self.hasTexture = (wg.texList!=None) and (len(wg.texList)>0)
    self.to_single_index_style()


  def loadShader(self):
    ''' Create the shaders for the materials:
    .shader for textured material
    .shaderC for colored ones
    '''
   
    # Create Textured Shaders 
    self.shader = Shader()
    self.shader.initShader( \
      ['''#version 300 es
      // Input vertex data, different for all executions of this shader.
      layout(location = 0) in vec3 vertexPosition_modelspace;
      layout(location = 1) in vec2 vertexUV;

      // Output data ; will be interpolated for each fragment.
      out vec2 UV;

      // Values that stay constant for the whole mesh.
      uniform mat4 MVP;
      uniform vec3 OFFSET;
      
      void main()
        {
        vec3 position_offset = vertexPosition_modelspace.xyz + OFFSET.xyz;
        // Output position of the vertex, in clip space : MVP * position
        gl_Position =  MVP * vec4(position_offset,1);
  
        // UV of the vertex. No special space for this one.
        UV = vertexUV;
        }
      ''', ], \
      ['''#version 300 es
      // Interpolated values from the vertex shaders
      in mediump vec2 UV;
      
      // Diffuse color to combine (blending --> multiply)
      uniform mediump vec4 fragmentColor;
      
      // Ouput data
      out mediump vec4 color;

      // Values that stay constant for the whole mesh.
      uniform sampler2D myTextureSampler;

      void main()
        {
        // Output color = color of the texture at the specified UV
        // I want to preserve the alpha channel of the underlying color
        color.rgb = texture( myTextureSampler, UV ).rgb * fragmentColor.rgb;
        color.a = fragmentColor.a;        
        }      
      ''', ])


    self.shader.MVP_ID = glGetUniformLocation(self.shader.program, "MVP")
    self.shader.OFFSET_ID = glGetUniformLocation(self.shader.program, "OFFSET")
    self.shader.Texture_ID =  glGetUniformLocation(self.shader.program, "myTextureSampler")
    self.shader.Color_ID = glGetUniformLocation(self.shader.program, "fragmentColor")
    
    # Create Colored Shaders 
    self.shaderC = Shader()
    self.shaderC.initShader( \
      [ '''#version 300 es
      // Input vertex data, different for all executions of this shader.
      layout(location = 0) in vec3 vertexPosition_modelspace;
      //layout(location = 1) in vec3 vertexColor;

      // Output data ; will be interpolated for each fragment.
      out mediump vec3 fragmentColor;
      
      // Values that stay constant for the whole mesh.
      uniform mat4 MVP;
      uniform vec3 OFFSET;

      void main()
        {  
        // Output position of the vertex, in clip space : MVP * position
        // gl_Position =  MVP * vec4(vertexPosition_modelspace,1);
        
        vec3 position_offset = vertexPosition_modelspace.xyz + OFFSET.xyz;
        // Output position of the vertex, in clip space : MVP * position
        gl_Position =  MVP * vec4(position_offset,1);        
        }
       ''', ],
      ['''#version 300 es
      // This Fragment returns a constant color
      uniform mediump vec4 fragmentColor;

      // Ouput data
      out mediump vec4 color;

      void main()
        {
        // Output color = color specified in the uniform constant 
        color = fragmentColor;
        }
       ''', ])
    
    self.shaderC.MVP_ID = glGetUniformLocation(self.shaderC.program, "MVP")
    self.shaderC.OFFSET_ID = glGetUniformLocation(self.shaderC.program, "OFFSET")
    self.shaderC.Color_ID = glGetUniformLocation(self.shaderC.program, "fragmentColor")


  def to_single_index_style(self):
    ''' Convert a WaveGeom to a GL compliant 'model' for rendering. '''
    geom = self.wg
    logging.info("Geom[%s] with %d polygons OpenGL conversions", geom.getName(), geom.getNbFace())

    # Prepare a copy of vertex, tex coords and normals
    coords = [ (p.x, p.y, p.z) for p in geom.coordList ]
    texs = [ (t.x, t.y) for t in geom.texList ] if self.hasTexture else None
    norms = [ (n.x, n.y, n.z) for n in geom.normList ] if self.hasNormal else None

    # Inspect the WaveGeom to Prepare Groupe x Material dictionnary
    nbMat = len(geom.lstMat)
      
    # self._models = list[0..NbGrp] of Dictionnary of MatName--> RendGroupMat
    self._models = [ ]

    nbtri = 0

    # Write the face of each group
    for grp in geom.getGroups():
      vertIdxTbl = grp.vertIdx
      tvertIdxTbl = grp.tvertIdx if (self.hasTexture and grp.tvertIdx) else [-1]*len(vertIdxTbl)
      normIdxTbl = grp.normIdx if (self.hasNormal and grp.normIdx) else [-1]*len(vertIdxTbl)
      
      grpModels = [ RendGroupMat(grp, self.libMat.get(geom.lstMat[i]), self.hasTexture, self.hasNormal, coords, texs, norms) \
                    for i in range(nbMat) ] if self.libMat else \
                  [ RendGroupMat(grp, None, self.hasTexture, self.hasNormal, coords, texs, norms) for i in range(nbMat) ]
     
      for noface in range(0, grp.getNbFace()):
        startIdx = grp.getFaceStartIdx(noface)
        lastIdx = grp.getFaceLastIdx(noface)
        argc = lastIdx - startIdx
        matIdx = grp.getMatIdx(noface)
        glcont = grpModels[matIdx]

        v0 = vertIdxTbl[startIdx]
        v1 = vertIdxTbl[startIdx+1]
        v2 = vertIdxTbl[startIdx+2]

        if argc==3:
          # self.add_face(v0, v1, v2, isprotected, matIdx, grpNo)
          glcont.addGLPoint(v0, tvertIdxTbl[startIdx], normIdxTbl[startIdx])
          glcont.addGLPoint(v1, tvertIdxTbl[startIdx+1], normIdxTbl[startIdx+1])
          glcont.addGLPoint(v2, tvertIdxTbl[startIdx+2], normIdxTbl[startIdx+2])
          
        elif argc==4:
          v3 = vertIdxTbl[startIdx+3]          

          e0 = Point3d(geom.coordList[v1]).sub(geom.coordList[v0]).normalize()
          e1 = Point3d(geom.coordList[v2]).sub(geom.coordList[v1]).normalize()
          e2 = Point3d(geom.coordList[v3]).sub(geom.coordList[v2]).normalize()
          e3 = Point3d(geom.coordList[v0]).sub(geom.coordList[v3]).normalize()

          a_02 = (1 - e0.dot(e3)) + (1.0 - e1.dot(e2))
          a_13 = (1 - e1.dot(e0)) + (1.0 - e3.dot(e2))
          # Comparison with Java Algo : Accuracy changes
          if a_02 <= a_13:
            glcont.addGLPoint(v0, tvertIdxTbl[startIdx], normIdxTbl[startIdx])
            glcont.addGLPoint(v1, tvertIdxTbl[startIdx+1], normIdxTbl[startIdx+1])
            glcont.addGLPoint(v2, tvertIdxTbl[startIdx+2], normIdxTbl[startIdx+2])

            glcont.addGLPoint(v0, tvertIdxTbl[startIdx], normIdxTbl[startIdx])
            glcont.addGLPoint(v2, tvertIdxTbl[startIdx+2], normIdxTbl[startIdx+2])
            glcont.addGLPoint(v3, tvertIdxTbl[startIdx+3], normIdxTbl[startIdx+3])
            
          else:
            glcont.addGLPoint(v0, tvertIdxTbl[startIdx], normIdxTbl[startIdx])
            glcont.addGLPoint(v1, tvertIdxTbl[startIdx+1], normIdxTbl[startIdx+1])
            glcont.addGLPoint(v3, tvertIdxTbl[startIdx+3], normIdxTbl[startIdx+3])

            glcont.addGLPoint(v1, tvertIdxTbl[startIdx+1], normIdxTbl[startIdx+1])
            glcont.addGLPoint(v2, tvertIdxTbl[startIdx+2], normIdxTbl[startIdx+2])
            glcont.addGLPoint(v3, tvertIdxTbl[startIdx+3], normIdxTbl[startIdx+3])
            
        else:
          # Input polygon many sides (>4). Triangularize it.
          # Compute the isobarycentre
          isoG = Point3d()
          t = TexCoord2f()
          n = Vector3d()
          for i,vno in enumerate(vertIdxTbl[startIdx:lastIdx]):
            isoG.add(geom.coordList[vno])
            if self.hasNormal:
              n.add(geom.normList[grp.normIdx[i+startIdx]])
                
            if self.hasTexture:
              t.add(geom.texList[tvertIdxTbl[i+startIdx]])
              
          factor = 1.0/float(argc)                           
          isoG.scale(factor)
          t.scale(factor)
          n.scale(factor)
          
          for i in range(startIdx, lastIdx-1):
            #self.add_face(gno, , , isprotected, matIdx, grpNo)
            glcont.addExtraGLPoint((isoG.x, isoG.y, isoG.z), (t.x, t.y), (n.x, n.y, n.z))
            glcont.addGLPoint(vertIdxTbl[i], tvertIdxTbl[i], normIdxTbl[i])
            glcont.addGLPoint(vertIdxTbl[i+1], tvertIdxTbl[i+1], normIdxTbl[i+1])

          #self.add_face(gno, vertIdxTbl[lastIdx-1], vertIdxTbl[startIdx], isprotected, matIdx, grpNo)
          glcont.addExtraGLPoint((isoG.x, isoG.y, isoG.z), (t.x, t.y), (n.x, n.y, n.z))
          glcont.addGLPoint(vertIdxTbl[lastIdx-1], tvertIdxTbl[lastIdx-1], normIdxTbl[lastIdx-1])
          glcont.addGLPoint(vertIdxTbl[startIdx], tvertIdxTbl[startIdx], normIdxTbl[startIdx])

      # Finish the Renderable group creation
      nbtri += len(glcont.indices)
      grpDict = { geom.lstMat[i]:glcont for i,glcont in enumerate(grpModels) if glcont.checkClear() }
      self._models.append( grpDict )

    logging.info("Geom[%s] with %d polygons has %d triangles", geom.getName(), geom.getNbFace(), nbtri//3)
    



  def loadObject(self):
    for model in [ d for lstMDict in self._models for d in lstMDict.values()  ]:
      model.vertexbuffer = glGenBuffers(1)
      glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, model.vertexbuffer)
      glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(model.vertexs)*4, (GLfloat * len(model.vertexs))(*model.vertexs), GL_STATIC_DRAW)

      model.indicesbufferSize = len(model.indices)
  
      model.indicesbuffer  = glGenBuffers(1)            
      glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, model.indicesbuffer)
      glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(model.indices)*2, (GLushort * len(model.indices))(*model.indices), GL_STATIC_DRAW)
      
  def loadTexture(self):
    for glcont in [ d for grpDict in self._models for d in grpDict.values()  ]:
      if glcont.material.map_kd:
        
        # Use cached version
        glcont.texture = TextureLoader.LoadTexture(self.win3d, glcont.material.map_kd, self.wg.imgdirpath)
        # glcont.texture = TextureLoader(glcont.material.map_kd, imgdirpath=self.wg.imgdirpath)
        
        if glcont.texture:
          glcont.texturebuffer = glcont.texture.textureGLID
          glcont.uvbuffer = glGenBuffers(1)
          glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, glcont.uvbuffer)
          glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(glcont.texcoords)*4, (GLfloat * len(glcont.texcoords))(*glcont.texcoords), GL_STATIC_DRAW)
          #else: # In case of error (load error), go back to color mode

  def rendering(self, win3d, MVP, View, Projection):
    super(RendWaveGeom, self).rendering(win3d, MVP, View, Projection)
    
    for glcont in [ d for grpDict in self._models for d in grpDict.values()  ]:
      
      # Use the right program : Texture or Color
      shader = self.shader if glcont.texture else self.shaderC
      
      shader.begin()
      
      glUniformMatrix4fv(shader.MVP_ID,1,GL_FALSE, glm.value_ptr(MVP))
      glUniform3f(shader.OFFSET_ID, self.offset[0], self.offset[1], self.offset[2])

      glEnableVertexAttribArray(0)
      glBindBuffer(GL_ARRAY_BUFFER, glcont.vertexbuffer)
      glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)
      
      if glcont.texture:
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, glcont.texturebuffer)
        glUniform1i(shader.Texture_ID, 0)
  
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, glcont.uvbuffer)
        glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,0,None)
      
      # Diffuse color is for every case
      glUniform4f(shader.Color_ID, glcont.material.kd[0], glcont.material.kd[1], glcont.material.kd[2], glcont.material.kd[3] )
      
      glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, glcont.indicesbuffer)
      
      glDrawElements(GL_TRIANGLES, glcont.indicesbufferSize, GL_UNSIGNED_SHORT, None )    
      glDisableVertexAttribArray(0)
      glDisableVertexAttribArray(1)
      shader.end()        

  def DeleteBuffers(self):
    lm = [ model for model in [ d for lstMDict in self._models for d in lstMDict.values() ] ]
    nb = len(lm)
    glDeleteBuffers(nb, [ model.vertexbuffer for model in lm ] )
    glDeleteBuffers(nb, [ model.indicesbuffer for model in lm ] )
    # Texture buffers are delete at window level
    # glDeleteBuffers(nb, [ model.texture.textureGLID for model in lm if model.material.map_kd ] )
      
