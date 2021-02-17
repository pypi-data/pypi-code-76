# -*- coding: utf-8 -*-
import sys
import math
import logging
import threading
import multiprocessing as mp

from OpenGL.GL import glDepthFunc, glEnable, glDisable, glBlendFunc, glGetString, glClear, glViewport, glPolygonMode
from OpenGL.GL import GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_RENDERER, GL_SHADING_LANGUAGE_VERSION, \
                      GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_LINE, GL_FRONT_AND_BACK, GL_FILL, GL_CULL_FACE, \
                      GL_LESS, GL_DEPTH_TEST, GL_BLEND
import glm
import glfw

from pypos3d.wftk.WaveGeom import readGeom, WaveGeom
from pypos3dv.Drawable import TextureLoader, RendWaveGeom, Renderable, AxisGrid

    
class View3dWindow:
  ''' Basic GLFW Window (without any popdown menu).
  The class is itself a singleton that manages the list of created (and valid) windows.
  Each View3dWindow instance contains a list of Renderable objects (cf. Module Drawable.py)
  This class executes a single Event Loop (MainLoop() class method)
    
    Camera management:
    
    Key                 | Effect
    --------------------+-------------------------------------------------------
    Arrows              | Translate observer position of +/- 0.1 x Right or Up vector
    PageUp, PageDown    | Translate observer position of +/- 1 x Up vector
    Shift + PageUp/Down | Translate observer position of +/- 1 x Right vector
    --------------------+-------------------------------------------------------
    Wheel (mouse dial)  | Perspective: move Forward/Backward of 0.1 x Direction
                        | Ortho: move Forward/Backward of 0.1 x Direction
                        |   Adapt field width and height to simulate a zoom
    --------------------+-------------------------------------------------------
    + / -               | Perspective: move Forward/Backward of 1 x Direction
    q / a               |   Adapt field width and height to simulate a zoom
    --------------------+-------------------------------------------------------
    Shift + Arrows      | In Perspective : Rotate 0.1 rad
    --------------------+-------------------------------------------------------
    ESC                 | Close the window
    --------------------+-------------------------------------------------------
    l                   | Render in LINE mode
    f                   | Render in Face mode
    c                   | Toggle face culling
    --------------------+-------------------------------------------------------
    x,y,z               | Choose Orthographic project along Axis (+Shift invert)
    --------------------+-------------------------------------------------------
    r                   | Reset to default perspective view
    --------------------+-------------------------------------------------------
    Mouse b1+move       | Rotate of 0.1rad x delta X and delta Y
    --------------------+-------------------------------------------------------
    ESC                 | Close the window 
    --------------------+-------------------------------------------------------
  '''
  
  # Projection types
  PERSPECTIVE, ORTHO, ORTHOX, ORTHOMX, ORTHOY, ORTHOMY, ORTHOZ, ORTHOMZ = range(8)
  
  
  ''' Inserted objects counter '''
  __RIODCNT = 0
  
  __W3DLOCK = threading.Lock()
  
  ''' GLFW library initialization status '''
  __GLFW_STARTED = False
  
  ''' Ask for MainLoop exit '''
  __EXITNOW = False
  
  ''' Number of created (and open) window '''
  __winlst = []

  ''' Indicates if the MainLoop runs '''
  __IN_MAINLOOP = False
  
  
  @classmethod
  def errorMgt(cls, code, description):
    print('GLFW Error[{:d}] : {:s}'.format(code, str(description)))
    
  @classmethod
  def status(cls):
    #print('GLFW Error[{:d}] : {:s}'.format(code, str(description)))
    return (View3dWindow.__GLFW_STARTED, View3dWindow.__EXITNOW, View3dWindow.__IN_MAINLOOP, len(View3dWindow.__winlst))
    
  @classmethod
  def start(cls):
    View3dWindow.__W3DLOCK.acquire()
    if not View3dWindow.__GLFW_STARTED:      
      # Initialize glfw
      View3dWindow.__GLFW_STARTED = glfw.init()
      
      if View3dWindow.__GLFW_STARTED:
        glfw.set_error_callback(View3dWindow.errorMgt)
      else:
        logging.error('GLFW not initialized')        

      # Set Version hints
      #glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
      #glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)
      #glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
      #glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    View3dWindow.__W3DLOCK.release()
      
  @classmethod
  def wakeup(cls):
    ''' Wakeup the MainLoop, if GLFW initialized '''
    # Post an empty event to wake up the Main Loop
    if View3dWindow.__GLFW_STARTED:
      glfw.post_empty_event()
      
  @classmethod
  def stop(cls):
    View3dWindow.__EXITNOW = True
    # Post an empty event to wake up the Main Loop
    View3dWindow.wakeup()


  @classmethod
  def MainLoop(cls, exitWhenEmpty=False, maxDuration=-1.0, pollingPeriod=0.05):
    ''' Run the uniq main loop of the program.
    
    User may start it in a dedicated thread (if needed)
    
    Parameters:
    -----------
    exitWhenEmpty : bool, default False
      Indicate to the main to exit, when the (internal) list of window is empty.
    
    maxDuration : float, default -1.0
      Maximum duration of the main loop in seconds.
      When maxDuration=-1.0, the MainLoop is infinite
      
    pollingPeriod : float, default 0.05
      Polling period of the MainLoop when no more windows are active.
      In a multi-threaded program, it provides the means to monitor
      the MainLoop (and take care of the maxDuration) when no 'MMI' events
      can be received.
      
    '''
    # Ensure GLFW has been started
    View3dWindow.start()
    
    # initializer timer
    glfw.set_time(0.0)
    t = 0.0
    tmax = t + (maxDuration if maxDuration>=0.0 else sys.float_info.max)
    
    runStatus = (t<tmax)
     
    View3dWindow.__IN_MAINLOOP = True

    while runStatus:
      t = glfw.get_time()
      #currT = t

      # Redraw needed windows
      for w3d in View3dWindow.__winlst:        
        if w3d.__verrou.acquire(blocking=False):
          if w3d.win==None: # New window to create
            # The create method makes windows context current
            w3d.__createInternal()
          else:            
            # Make windows context current to perform GL ops
            curCtxt = glfw.get_current_context()
            if curCtxt!=w3d.win:
              glfw.make_context_current(w3d.win)

          if w3d.__resize:
            glViewport(0, 0, w3d.width, w3d.height)
            w3d.calc_MVP(w3d.width, w3d.height)
            w3d.__resize = False
            w3d.__redraw = True
            
          if w3d.__isvalid and w3d.__redraw:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # The window must also set its drawing conditions
            w3d.ogl_draw()
            glfw.swap_buffers(w3d.win)
            w3d.__redraw = False

          elif w3d.__exitNow: # Close this window
            w3d.close()
            View3dWindow.__winlst.remove(w3d)
            
          # Release the lock on the current window
          w3d.__verrou.release()
      #End for w3d
      
      # Wait for events & dispath them      
      if View3dWindow.__winlst:
        # Check if View3dWindow have received any data on their
        # Pipe (cmdQueue)
        rd = False
        for w3d in View3dWindow.__winlst:
          if w3d.cmdQueue:
            rd |= w3d.watchQueue()
        
        if not rd:
          if tmax<sys.float_info.max:
            dt = tmax - glfw.get_time()
            
            if dt>0.0: #  MainLoop waits for dt seconds 
              glfw.wait_events_timeout(dt)
            else:
              View3dWindow.__EXITNOW = True
              
          else: # MainLoop waits indefinitively
            glfw.wait_events()
            
      elif exitWhenEmpty:
        View3dWindow.__EXITNOW = True
        break
      
      else: # When the windows list is empty: Mix polling/event
        glfw.wait_events_timeout(pollingPeriod)
        
      runStatus = not View3dWindow.__EXITNOW and (t<tmax)
    #End of Main Event Loop

    logging.info('MainLoop exits after: {:.3f} s'.format(glfw.get_time()))

    # Safely Delete windows
    View3dWindow.__W3DLOCK.acquire()
    View3dWindow.__IN_MAINLOOP = False

    # All Windows have been closed or Application Exit Required
    for w3d in View3dWindow.__winlst:
      if w3d.__isvalid:
        glfw.make_context_current(w3d.win)
        w3d.close()

    del View3dWindow.__winlst[:]

    View3dWindow.__GLFW_STARTED = False
    View3dWindow.__EXITNOW = False
    View3dWindow.__W3DLOCK.release()
        
    glfw.terminate()
          

  @classmethod
  def getWindow(cls, winIndex=-1):
    ''' Return the window which has the given index in the list.
    Without argument, return the last one.
    '''
    View3dWindow.__W3DLOCK.acquire()
    w = View3dWindow.__winlst[winIndex] if ((winIndex>=0) and (winIndex<len(View3dWindow.__winlst))) or\
       ((winIndex==-1) and View3dWindow.__winlst) else None
    View3dWindow.__W3DLOCK.release()

    return w
      

  def __createInternal(self):
    ''' Internal GLFW and OpenGL creation of the window. 
    Should be called from the MainLoop (GLFW initialized)
    '''
    
    # Create a GLFW window
    self.win = glfw.create_window(self.width, self.height, self.name, None, None)
    
    # Make context current
    glfw.make_context_current(self.win)

    # set window callbacks
    glfw.set_mouse_button_callback(self.win, self.onMouseButton)
    glfw.set_cursor_pos_callback(self.win, self.onMouseMove)
    glfw.set_scroll_callback(self.win, self.onScroll)
    glfw.set_key_callback(self.win, self.onKeyboard)
    glfw.set_window_size_callback(self.win, self.onSize)        
    glfw.set_window_close_callback(self.win, self.onClose)

    # Initialize GL and create default objects (Axis, Grids, ...)
    self.ogl_init()
    logging.info('Window[{:s}] {:d}x{:d} created - GL Context:Renderer:{:s} - Shading Language:{:s}'.format(self.name, self.width, self.height, \
                 str(glGetString(GL_RENDERER)), str(glGetString(GL_SHADING_LANGUAGE_VERSION))))
    
  
  def __init__(self, width=800, height=480, connIn=None, name='pypos3dv.viewer', axisGrid=None, \
               background=(0.1, 0.1, 0.1, 0.8), usemtlfiles=True, defaultmtl=None, imgdirpath='.'):
    ''' Create a new GLFW window and insert it in the list of active windows.
    
    Parameters:
    -----------
    axisGrid: int or AxisGrid
      -1 : No Axis Grid
      None : Use Default AxisGrid (10 x 10 grid with colored axis)
      an AxisGrid : The Renderable you need


    '''
    self.name = name
    self.background = background
    #self.foreground = foreground
    self.culFace = False
    self.polygonMode = GL_FILL
    self.mouse_mode = -1
    self.lastX = 0 
    self.lastY = 0

    # Dictionnary of rendered objects (RIOD:Renderable)
    self.meshes = { }
    self.axisGrid = (axisGrid if isinstance(axisGrid, AxisGrid) else None) if axisGrid else AxisGrid()
    
    # Material management attributes
    self.useMtl = usemtlfiles
    self.defaultMtl = defaultmtl
    self.imgdirpath = imgdirpath

    # Exit flag
    self.__exitNow = False
    
    # Redraw flag
    self.__redraw = True
    
    # Resize to be computed
    self.__resize = True
    
    # Validity status (True when GL buffers are created and operational)
    self.__isvalid = False
    
    # Create a lock to protect GL functions
    self.__verrou = threading.Lock()
    
    # Initialize the communication channel (input with the given mp.Queue)
    self.cmdQueue = connIn    

    # Create the window and Initialize Behavior data
    self.width, self.height = width, height
    self.reset()
    self.aspect = width/float(height)
    self.win = None 
    
    # Add the potential AxisGrid
    if self.axisGrid:
      self.addMesh(self.axisGrid)

    # Safely Record the new Window
    View3dWindow.__W3DLOCK.acquire()
    View3dWindow.__winlst.append(self)
    View3dWindow.__W3DLOCK.release()
    
    # Signal the new window creation (for GL creation and drawing)
    self.signal()
      
    # End Of __init__

  def signal(self, redraw=True, resize=False, close=False):
    self.__redraw = redraw
    self.__resize = resize
    self.__exitNow = close
    View3dWindow.wakeup()

  def addMesh(self, meshWithRender):
    self.__verrou.acquire()
    self.__isvalid = False    
    
    nriod = 'RIOD-{:d}'.format(View3dWindow.__RIODCNT)
    View3dWindow.__RIODCNT+=1
    
    self.meshes[nriod] = meshWithRender

    self.__isvalid = True    
    self.__verrou.release()
    
    self.signal()
    return nriod
  
  def add(self, obj3d, matDict=None, location=None):
    pos = location if location else (0.0,0.0,0.0)
    nroid = None
    
    if isinstance(obj3d, str):
      geomFileName = obj3d 
      wg = readGeom(geomFileName, usemtl=self.useMtl, imgdirpath=self.imgdirpath)
      if wg:
        nroid = self.addMesh( RendWaveGeom(wg, matDict, location=pos) )
      else:
        logging.warn('File not found:%s', obj3d)
        
    elif isinstance(obj3d, WaveGeom):
      nroid = self.addMesh( RendWaveGeom(obj3d, matDict, location=pos) )
    
    return nroid
  
  def show(self, roid):
    try:
      (roid if isinstance(roid, Renderable) else self.meshes[roid]).isVisible = True
      self.signal()
    except KeyError:
      pass
 
  def hide(self, roid):
    try:
      (roid if isinstance(roid, Renderable) else self.meshes[roid]).isVisible = False
      self.signal()
    except KeyError:
      pass

  def moveTo(self, roid, location):
    try:
      robj = roid if isinstance(roid, Renderable) else self.meshes[roid]
      robj.offset = location      
      self.signal()
    except KeyError:
      pass

  def reset(self):
    '''Reset View Data: 
    Observer position: .obs
    Two rotation angles: ax, ay
      where ax is the angle : toward Z, in radian (rot Oy)
      where ay is the elevation angle : in radian (rot Oz)
    The distance to the observed point : distObs

    This set of values provides the means to compute:
      - The direction vector (unitary)
      - The right vector of the observer (unitary)
      - The up vector of the observer (unitary)
      - The Observed point : .lookPos = .obs + distObs x direction
    '''
    
    # Back to a standard perspective
    self.projection = View3dWindow.PERSPECTIVE

    # Initial position:
    self.obs = glm.vec3(5.0, 5.0, 5.0)
    
    # Initialize value so that lookPos is at the origin (0,0,0)
    self.distObs = glm.l2Norm(self.obs)
    
    # Initial horizontal angle : toward Z, in radian (rot Oy)
    self.ax = math.pi + (math.atan(self.obs[0]/self.obs[2]) if self.obs[2] else glm.sign(self.obs[0]) * math.pi/2.0)
    
    # Initial vertical angle in radian
    self.ay = - math.asin(self.obs[1]/self.distObs)

    # Initial Field of View (in °)
    self.Fov = 60.0

    self.w05, self.h05 = 1.0, 1.0
    
    self.computeMatrices()

  def calc_MVP(self, width=0, height=0):        
    if width:
      self.width = width
      self.height = height
      self.computeMatrices()
                  
    self._MVP = self.ProjectionMatrix * self.ViewMatrix 
    
    
  def ogl_init(self):
    ''' OpenGL common drawing conditions of the window. 
    Called once, just after window creation and callback attachment.
    '''
    # glClearColor(*self.background) : Not necessary, because done by the rendering loop(s)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)    
    glEnable(GL_BLEND)
    glEnable(GL_CULL_FACE)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


  def ogl_draw(self):
    ''' OpenGL Window drawing.
    Called by the MainLoop when redraw or resize flags are set.
    '''
         
    self.calc_MVP()
    
    # Clear the window
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set dynamic drawing conditions
    if self.culFace:
      glDisable(GL_CULL_FACE)
    else: 
      glEnable(GL_CULL_FACE)
         
    glPolygonMode(GL_FRONT_AND_BACK, self.polygonMode)

    # Draw visible meshes (Renderable)
    for mesh in self.meshes.values():
      if mesh.isVisible:        
        mesh.rendering(self.win, self._MVP, self.ViewMatrix, self.ProjectionMatrix)
          
  def moveFoward(self, forward):
    self.obs += self.direction*forward

    if self.projection!=View3dWindow.PERSPECTIVE: # Simulate a Zoom (Apply Thales between new and last position)      
      self.w05 *= (self.distObs + forward) / self.distObs
      self.h05 = float(self.height) * self.w05 / float(self.width)
    
    # Update distance to the observed point
    self.distObs += forward

    self.computeMatrices()

  def moveUp(self, up):    
    self.obs += self.up*up
    self.computeMatrices()

  def moveRight(self, right):    
    self.obs += self.right*right
    self.computeMatrices()  

  def cameraLookUpward(self,yaw):
    self.ay += yaw
    self.computeMatrices()  

  def cameraTurn(self,angle):
    self.ax += angle
    self.computeMatrices()  

  def observerYaw(self, da):
    # Change to observed point coord syst and 
    # Rotate along Oy of -ax
    cxa = math.cos(self.ax)
    sxa = math.sin(self.ax)
    p1 = glm.mat3([ [cxa, 0.0, sxa], [0.0, 1.0, 0.0], [-sxa, 0.0, cxa]]) * (self.obs - self.lookPos)
    
    # Rotate of -da along Ox
    cda = math.cos(-da)
    sda = math.sin(-da)
    p2 = glm.mat3([ [1.0, 0.0, 0.0], [0.0, cda, -sda], [0.0, sda, cda]]) * p1
    
    # Rotate along Oy of ax and go back to initial coord system
    self.obs = self.lookPos + glm.mat3([ [cxa, 0.0, -sxa], [0.0, 1.0, 0.0], [sxa, 0.0, cxa]]) * p2 
        
    self.ay -= da
    self.computeMatrices()
  
  def observerTurn(self, da):
    cxa = math.cos(da)
    sxa = math.sin(da)
    # Just Rotate along Oy of da (in observed point coord. syst)
    self.obs = self.lookPos + glm.mat3([ [cxa, 0.0, sxa], [0.0, 1.0, 0.0], [-sxa, 0.0, cxa]]) * (self.obs - self.lookPos)
    self.ax -= da
    self.computeMatrices()  


  # Calc direction right and up
  def computeMatrices(self):
    ''' Must compute ViewMatrix, ProjectionMatrix '''
    
    if self.projection==View3dWindow.PERSPECTIVE:
      self.direction = glm.vec3(math.cos(self.ay) * math.sin(self.ax), 
                                math.sin(self.ay),
                                math.cos(self.ay) * math.cos(self.ax))
      
      self.right = glm.vec3(math.sin(self.ax - math.pi/2.0), 0.0, math.cos(self.ax - math.pi/2.0))
    
      self.ProjectionMatrix = glm.perspective(glm.radians(self.Fov), float(self.width) / float(self.height), 0.01, 1000.0)
      
    #elif self.projection==View3dWindow.ORTHO:
      
    elif self.projection==View3dWindow.ORTHOX:
      self.direction = glm.vec3(-1.0, 0.0, 0.0)
      self.right = glm.vec3(0.0, 0.0, -1.0)

      self.ProjectionMatrix = glm.ortho(-self.w05, self.w05, -self.h05, self.h05, 0.01, 1000.0)

    elif self.projection==View3dWindow.ORTHOY:
      self.direction = glm.vec3(0.0, -1.0, 0.0)
      self.right = glm.vec3(1.0, 0.0, 0.0)

      self.ProjectionMatrix = glm.ortho(-self.w05, self.w05, -self.h05, self.h05, 0.01, 1000.0)
    elif self.projection==View3dWindow.ORTHOZ:
      self.direction = glm.vec3(0.0, 0.0, -1.0)
      self.right = glm.vec3(1.0, 0.0, 0.0)

      self.ProjectionMatrix = glm.ortho(-self.w05, self.w05, -self.h05, self.h05, 0.01, 1000.0)
    else:
      self.reset()

    # Finish with the View matrix
    self.lookPos = self.obs + self.distObs * self.direction       
    self.up = glm.cross(self.right, self.direction)
    self.ViewMatrix = glm.lookAt(self.obs,     # Camera is here
                                 self.lookPos, # and looks here : at the same position, plus "direction"
                                 self.up)      # Head is up (set to 0,-1,0 to look upside-down)
    
    # logging.info('Observer:%s LookAt:%s ', str(self.obs), str(self.lookPos))
    return # computeMatrices
  
  #----------------------------------------------------------------------------
  # Event Management
  #----------------------------------------------------------------------------
  def onKeyboard(self, win, key, scancode, action, mods):
    if action==glfw.PRESS or action==glfw.REPEAT:
      # ESC to quit
      if key==glfw.KEY_ESCAPE: 
        self.signal(close=True)

      elif key==glfw.KEY_PAGE_DOWN: #page down
        if mods & glfw.MOD_SHIFT:
          self.moveRight(1.0)
        else:
          self.moveUp(-1.0) 
        self.signal()

      elif key==glfw.KEY_PAGE_UP:
        if mods & glfw.MOD_SHIFT:
          self.moveRight(-1.0)
        else:
          self.moveUp(1.0) #page up
        self.signal()
        
      elif key==glfw.KEY_UP:#up
        if mods & glfw.MOD_SHIFT:
          self.cameraLookUpward(0.1)
        
        elif mods & glfw.MOD_CONTROL:
          self.observerYaw(0.1)

        else:
          self.moveUp(0.1) #page up
        self.signal()

      elif key==glfw.KEY_DOWN:#down
        if mods & glfw.MOD_SHIFT:
          self.cameraLookUpward(-0.1)

        elif mods & glfw.MOD_CONTROL:
          self.observerYaw(-0.1)
            
        else:
          self.moveUp(-0.1) #page up
        self.signal()

      elif key==glfw.KEY_RIGHT: #right
        if mods & glfw.MOD_SHIFT:
          self.cameraTurn(0.1) 

        elif mods & glfw.MOD_CONTROL:
          self.observerTurn(0.1)
        else:
          self.moveRight(0.5) 

        self.signal()

      elif key==glfw.KEY_LEFT: #left
        if mods & glfw.MOD_SHIFT:
          self.cameraTurn(-0.1) 
        elif mods & glfw.MOD_CONTROL:
          self.observerTurn(-0.1)
        else:
          self.moveRight(-0.5)
          
        self.signal()
        
      elif key==glfw.KEY_KP_ADD or key==glfw.KEY_Q: #KEY_W:
        self.moveFoward(0.5) 
        self.signal()

      elif key==glfw.KEY_KP_SUBTRACT or key==glfw.KEY_A: #KEY_S:
        self.moveFoward(-0.5)
        self.signal()
        
      elif key==glfw.KEY_R: # Reset View 
        self.reset()
        self.signal()

      elif key==glfw.KEY_L: # Set Wireframe
        self.polygonMode = GL_LINE
        self.signal()

      elif key==glfw.KEY_F: # Set Filled face mode
        self.polygonMode = GL_FILL    
        self.signal()

      elif key==glfw.KEY_C: # Toggle cul face
        self.culFace = not self.culFace
        self.signal()
        
      elif key==glfw.KEY_X:
        # Use previous FoV and position to determine w05,h05
        self.w05 = self.distObs / math.tan(glm.radians(self.Fov))
        self.h05 = float(self.height) * self.w05 / float(self.width)
        self.obs = glm.vec3(self.obs[0], 0.0, 0.0)
        self.projection = View3dWindow.ORTHOX
        self.computeMatrices()  
        self.signal()

      elif key==glfw.KEY_Y:
        self.w05 = self.distObs / math.tan(glm.radians(self.Fov))
        self.h05 = float(self.height) * self.w05 / float(self.width)
        self.obs = glm.vec3(0.0, 1.0, 0.0)
        self.projection = View3dWindow.ORTHOY
        self.computeMatrices()  
        self.signal()
        
      elif key==glfw.KEY_W: # Qwerty kb
        self.w05 = self.distObs / math.tan(glm.radians(self.Fov))
        self.h05 = float(self.height) * self.w05 / float(self.width)
        self.obs = glm.vec3(0.0, 0.0, 1.0)
        self.projection = View3dWindow.ORTHOZ
        self.computeMatrices()  
        self.signal()
        
#       else:
#         print('Unmanaged Key:'+str(key))  
    return #onKeyboard

  def onSize(self, win, width, height):
    # Just store new window dimensions and ask for a resize (in the Main Loop)
    self.width = width
    self.height = height
    self.aspect = width/float(height)
    self.signal(resize=True)
    
  def onClose(self, win):
    # Just ask to exit (deletion will be performed by the Main Loop)
    self.signal(close=True)

  def onMouseButton(self, win, button, action, mods):
    ''' Callback for mouse button management. '''
    if (button==glfw.MOUSE_BUTTON_LEFT) and (action==glfw.PRESS):
      self.lastX, self.lastY = glfw.get_cursor_pos(win)
      self.mouse_mode = 1

    elif (button==glfw.MOUSE_BUTTON_MIDDLE) and (action==glfw.PRESS):
      self.lastX, self.lastY = glfw.get_cursor_pos(win)
      self.mouse_mode = 2  

    else:
      self.lastX = -1
      self.lastY = -1    
      self.mouse_mode = -1           
          
  def onMouseMove(self, win, x, y):
    ''' Track mouse displacements. '''
    deltaX = self.lastX - x
    deltaY = self.lastY - y
    if self.mouse_mode==1:
      self.lastX, self.lastY = x, y
      self.cameraLookUpward(deltaY*0.01)
      self.cameraTurn(deltaX*0.01)
      self.signal()
      
    elif self.mouse_mode==2:
      self.lastX, self.lastY = x, y
      self.moveUp(-0.1*deltaY)
      self.moveRight(-0.1*deltaX) 
      self.signal()

  def onScroll(self, win, dx, dy):
    ''' Callback for mouse dial or touchpad swift. '''
    self.moveFoward(0.1 if dy>0.0 else -0.1) 
    self.signal()

  def isValid(self):
    return self.__isvalid
  
  def close(self):
    # Manage End of Window's life: Delete All GL allocated resources
    self.__isvalid = False
    
    # glfw.make_context_current(self.win) : Made by the caller
    for mesh in self.meshes.values():
      mesh.DeleteBuffers() 

    # Delete Texture buffers
    TextureLoader.DeleteBuffers(self)

    # Destroy the closed window
    glfw.destroy_window(self.win)

  
  #
  # Communication Management callback
  #   
  def watchQueue(self):
    ''' This callback lookup for any entry in the command Queue.
    The check of the input pipe is non blocking.
    Commands are either a single string or a tuple of any kind of object    
    Some command may acquire the lock of the View3dWindow.
    
    return the redraw status of the window
    
    '''
    while self.cmdQueue.poll():
      inputVal = self.cmdQueue.recv()
      
      if isinstance(inputVal, str):
        cmd = inputVal.lower()
        args = None
      else:
        cmd = inputVal[0].lower()
        args = inputVal[1:]
        
      logging.info('Recieved Command:%s (%s)', cmd, str(args))
      if cmd=='readgeom':
        geomFileName = args[0] 
        matDict = args[1]
        pos = args[2] if len(args)>1 and args[2] else (0.0,0.0,0.0)
        wg = readGeom(geomFileName, usemtl=self.useMtl, imgdirpath=self.imgdirpath)
        if wg:
          nriod = self.addMesh( RendWaveGeom(wg, matDict, location=pos) )
          self.cmdQueue.send(nriod)
        else:
          self.cmdQueue.send('READ_ERROR')
          
      elif cmd=='loadgeom':
        wg = args[0]
        matDict = args[1]
        pos = args[2] if len(args)>1 and args[2] else (0.0,0.0,0.0)
        nriod = self.addMesh( RendWaveGeom(wg, matDict, location=pos) )
        self.cmdQueue.send(nriod)
        
      elif cmd=='hide': # Use RIOD
        self.hide(args[0])
        
      elif cmd=='show': # Use RIOD
        self.show(args[0])
        
      elif cmd=='exit': 
        self.signal(close=True)
        
      elif cmd=='moveto': # Use RIOD
        self.moveTo(args[0], args[1])

      else:
        logging.warning('Viewer[%s] recieved unknown command:%s', self.name, cmd)
    
    return self.__redraw
    
    
#------------------------------------------------------------------------------
# Subprocess management part   
def _procQueueEntry(connIn, verbose=False, width=800, height=480, name='pypos3dv.viewer Process', axisGrid=None, \
                   background=(0.1, 0.1, 0.1, 0.8), usemtlfiles=True, defaultmtl=None, imgdirpath='.'):
  ''' Subprocess entry procedure. '''
  logging.basicConfig(format='%(asctime)s %(module)s.%(funcName)s %(message)s')
  
  logging.getLogger().setLevel(logging.INFO if verbose else logging.ERROR)

  dummy = View3dWindow(width, height, connIn, name=name, axisGrid=axisGrid, \
                     background=background, usemtlfiles=usemtlfiles, \
                     defaultmtl=defaultmtl, imgdirpath=imgdirpath)
  
  logging.info("Starting draw")
  View3dWindow.MainLoop(exitWhenEmpty=True)
  logging.info("Application Exits")

    
    
class View3dProcess(mp.Process):
  ''' Functional interface to subprocess viewer.
  Maintain consistency between sent/displayed objects and usuable user ids (RIOD).
  Manage communications aspects (queue and messages format).
  
  '''

  def __init__(self, verbose=False, width=800, height=480, connIn=None, name='Pypos3d.viewer Process', axisGrid=None, \
               background=(0.1, 0.1, 0.1, 0.8), usemtlfiles=True, defaultmtl=None, imgdirpath='.'):
    
    self.__pparent, self.__pchild = mp.Pipe() 
    
    super(View3dProcess, self).__init__(target=_procQueueEntry, args=(self.__pchild, verbose, width, height, name, \
                                                                     axisGrid, background, usemtlfiles, \
                                                                     defaultmtl, imgdirpath)) 

    self.start()

    

  def show(self, roid):
    ''' Show the Renderable object identified by its 'RIOD' '''
    self.__pparent.send( ('show', roid) )

  def hide(self, roid):
    ''' Hide the Renderable object identified by its 'RIOD' '''
    self.__pparent.send( ('hide', roid) )

  def moveTo(self, roid, location:'tuple'):
    ''' Move the Renderable object identified by its 'RIOD' to the given absolute position '''
    self.__pparent.send( ('moveto', roid, location) )


#   def translate(self, roid, v:'Vector3d'):
#     ''' Translate the Renderable object identified by its 'RIOD' of the given vector
#     '''
#     pass

#   def rotate(self, roid, rotv:'Vector3d'):
#     ''' Rotate the Renderable object identified by its 'RIOD' of the given vector
#     '''
#     pass
# 
#   def scale(self, roid, scalev:'Vector3d'):
#     ''' Scale the Renderable object identified by its 'RIOD' of the given vector
#     '''
#     pass


  def add(self, obj3d:'filename or WaveGeom', matDict=None, location=None):
    ''' Add and display the given object. '''
    
    if isinstance(obj3d, str):
      self.__pparent.send( ('readgeom', obj3d, matDict, location) )
    elif isinstance(obj3d, WaveGeom):
      self.__pparent.send( ('loadgeom', obj3d, matDict, location) )
    else:
      return None
    
    nriod = self.__pparent.recv()
        
    return nriod
  
  def end(self):
    ''' Stop the child process. '''
    self.__pparent.send('exit')
    
    self.join(0.01)
    
    if self.is_alive():
      self.terminate()











  
  
  
