# -*- coding: utf-8 -*-
'''
  pypos3dviewer intends to be a simple OpenGL viewer for:
  - WaveFront Files (3D geometry files)
  
  Requires : PyOpenGL, PIL, PyGLM, GLFW, pypos3d
'''
import sys
import os
import logging
import argparse

import pypos3d
import pypos3dv
from pypos3dv.Window import View3dWindow, View3dProcess
from pypos3d.wftk.WaveGeom import WFMat


def main(args=None):
  """ The main routine. """
  if args is None:
    args = sys.argv[1:]

  # Logger basic (but detailed) configuration
  logging.basicConfig(format='%(asctime)s %(module)s.%(funcName)s %(message)s')
  
  parser = argparse.ArgumentParser(prog='pypos3dv', formatter_class=argparse.RawDescriptionHelpFormatter,
    description = \
    '''
    pypos3dv is an OpenGL 3d viewer for WaveFront files (*.obj/*.obz).
    
    pypos3dv is distributed under "New BSD License"
    
    pypos3dv opens a graphical GLFW window and display all objects contained in 
    the list of Wavefront files.
    
    Commands (keys for camera management - QWERTY keyboard):
    
    Key                 | Effect
    --------------------+-------------------------------------------------------
    Arrows              | Translate observer position of +/- 0.1 x Right or Up vector
    Shift + Arrows      | In Perspective : Rotate the camera of 0.1 rad
    Ctrl  + Arrows      | In Perspective : Rotate around the observed point of 0.1 rad
    --------------------+-------------------------------------------------------
    PageUp, PageDown    | Translate observer position of +/- 1 x Up vector
    Shift + PageUp/Down | Translate observer position of +/- 1 x Right vector
    --------------------+-------------------------------------------------------
    Wheel (mouse dial)  | Move Forward/Backward of 0.1 x Direction
                        | Ortho: 
                        |   Adapt field width and height to simulate a zoom
    --------------------+-------------------------------------------------------
    + / -               | Perspective: move Forward/Backward of 1 x Direction
    q / a               |   Adapt field width and height to simulate a zoom
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


    Axis colors: Ox in red, Oy in Green, Oz in Blue

    When win1 to win3 arguments are used, pypos3dv creates one subprocess per window.
    
   
    ''', epilog='''Use pip (pypi) to install or update. 
      pypo3dv is also integrated with LibreOffice. Retrieve the application from ''')
  
  parser.add_argument('--background', default='(0.1,0.1,0.1,0.8)', \
                      help='Background color of the window. Format (R,G,B,Alpha) as (float, float, float, float)')

  parser.add_argument('--version', action='version', \
                      version='%(prog)s {:s} using pypos3d {:s}'.format(pypos3dv.__version__, pypos3d.__version__))

  parser.add_argument('--wsize', default='800x600', \
                      help='Window size in pixels')

#   parser.add_argument('--axisgrid', type=str, \
#                       help='''Python Parameters of a customized AxisGrid.
#                       Create by default a 10x10 grid with colored axis
#                       Example:
#                       --axisgrid="(nbStep=5, space=2.0, )"
#                       ''')
  
  parser.add_argument('--verbose', \
                      help='Set log to INFO, else only software errors are reported', action='store_true')

  parser.add_argument('--usemtlfiles', type=bool, default=True, \
                      help='Indicates if material files (*.mtl) shall be loaded')
  
  parser.add_argument('--mtlfile', type=str, \
                      help='''Default mtl file to use.
                      When usemtlfiles is True, the default mtl file is used when
                      a material is not found in the loaded mtl file''')
  
  parser.add_argument('--imgdirpath', type=str, default='.',\
                      help='Ordered set of directories for texture files look-up')
    
  parser.add_argument('files', metavar='wavefront file', type=str, nargs='+', \
                      help='''Window 0 file list
                       Wavefront files to display (*.obj/*.obz) ''')

  parser.add_argument('--win0', metavar='file.obj', type=str, nargs='+', \
                      help='''Window 0 file list
                       Wavefront files to display (*.obj/*.obz) ''')
  
  parser.add_argument('--win1', metavar='file.obj', type=str, nargs='+', \
                      help='''Window 1 file list
                       Wavefront files to display (*.obj/*.obz) ''')
  
  parser.add_argument('--win2', metavar='file.obj', type=str, nargs='+', \
                      help='''Window 2 file list
                       Wavefront files to display (*.obj/*.obz) ''')
  
  parser.add_argument('--win3', metavar='file.obj', type=str, nargs='+', \
                      help='''Window 3 file list
                       Wavefront files to display (*.obj/*.obz) ''')

  args = parser.parse_args()

  #print('Args='+str(args))
  
  try:
    logging.getLogger().setLevel(logging.INFO if args.verbose else logging.ERROR)
    
    w,h = map(int, args.wsize.split('x'))
    
    # Read Default Material File
    defaultDict = None
    if args.mtlfile:
      defaultDict = WFMat.readMtl(args.mtlfile)
  
    dirpath='.'
    if args.imgdirpath:
      dirpath = dirpath.join( [ os.pathsep + os.path.expanduser(p) for p in args.imgdirpath.split(os.pathsep) if p ] )
  
    nbwin = 1 + (args.win1!=None) + (args.win2!=None) + (args.win3!=None)
    
    # Merge files list to win0 file list
    if args.win0:
      args.win0 += args.files if args.files else []
    else:
      args.win0 = args.files 
    
    if nbwin>1:
      # Work in multi process
      lstproc = []
      for winlst in [args.win0, args.win1, args.win2, args.win3]:
        if winlst:
          winproc = View3dProcess(args.verbose, w, h, background=eval(args.background), usemtlfiles=args.usemtlfiles,\
                                  imgdirpath=dirpath)
          for f in winlst:
            winproc.add(f, matDict=defaultDict)
          
          lstproc.append(winproc)
      
      for winproc in lstproc:
        winproc.join()
      
    else:
      win0 = View3dWindow(w,h, background=eval(args.background), usemtlfiles=args.usemtlfiles,\
                          imgdirpath=dirpath)
      for f in args.win0:
        win0.add(f, matDict=defaultDict)
      
      View3dWindow.MainLoop(exitWhenEmpty=True)
    
  except ValueError as e:
    print('Error:'+str(e))
      


if __name__ == "__main__":
    sys.exit(main())
