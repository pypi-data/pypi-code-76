#!/usr/bin/python
# -*- coding: utf-8 -*-


#banner / initial information
banner="""

# Blythooon-Test - Copyright & Contact Notice
#############################################
#            Blythooon-Test V0.8            #
#                                           #
#        Created by Dominik Niedenzu        #
#     Copyright (C) 2021 Dominik Niedenzu   #
#          All Rights Reserved              #
#                                           #
#                Contact:                   #
#          blythooon@blackward.de           # 
#             www.blackward.de              #
#############################################

# Blythooon-Test - License
#######################################################################################################################
# Use and redistribution in UNMODIFIED source form is permitted (free of charge) provided that the following          #
# conditions are met (including the disclaimer):                                                                      #
#                                                                                                                     #
# 1. This software (just) is used resp. redistributed as whole and without ANY modification; the name of the file is  #
#    blythooonTest.py . Modifying this software or/and using resp. redistributing just parts of this software resp.   #
#    file is strictly forbidden.                                                                                      #
#                                                                                                                     #
# 2. Neither the name "Dominik Niedenzu", nor the name resp. trademark "Blackward", nor the logo "Blackward"          #
#    may be used to endorse or promote other products without specific prior written permission.                      #
#                                                                                                                     #
# 3. Using or/and redistributing this software in a way or in an environment leading to the infringement (whether     #
#    immediately or indirectly) of one or several third party licenses or other third party rights will automatically #
#    terminate the user's resp. redistributor's rights under this license.                                            #
#                                                                                                                     #
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO   #
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.                            #
#                                                                                                                     #
# IN NO EVENT SHALL DOMINIK NIEDENZU BE LIABLE FOR ANY CLAIM, ANY (DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY   #
# OR CONSEQUENTIAL) DAMAGE OR ANY OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, #
# OUT OF OR IN CONNECTION WITH THIS SOFTWARE OR THE USE OR REDISTRIBUTION OR OTHER DEALINGS IN THIS SOFTWARE.         #
#                                                                                                                     #
# THE USERS RESP. REDISTRIBUTORS OF THIS SOFTWARE ARE SOLELY RESPONSIBLE FOR ENSURING THAT AFOREMENTIONED CONDITIONS  #
# ALL ARE MET AND COMPLIANT WITH THE LAW IN THE RESPECTIVE JURISDICTION - BEFORE (!) THEY USE RESP. REDISTRIBUTE.     #
#######################################################################################################################

"""
print banner


#import common libraries
from sys         import exit                 as Sys_exit
from sys         import argv                 as Sys_argv
from sys         import executable           as Sys_executable
from subprocess  import check_output         as Subprocess_check_output
from ssl         import OPENSSL_VERSION      as Ssl_OPENSSL_VERSION
from ssl         import OPENSSL_VERSION_INFO as Ssl_OPENSSL_VERSION_INFO
from ssl         import PROTOCOL_SSLv23      as Ssl_PROTOCOL_SSLv23
from re          import compile              as Re_compile
from re          import DOTALL               as Re_DOTALL
from platform    import machine              as Platform_machine
from platform    import python_version       as Platform_python_version
from platform    import uname                as Platform_uname
from platform    import system               as Platform_system
from os          import path                 as Os_path


#global error tracker
class ErrorTracker:
      """ Just used to track errors - if any. 'False' means error. """

      sslContextImport = True  
      qtImport         = True      
      pysideImport     = True
      numpy            = True
      pyqtgraph        = True
      matplotlib       = True
      scipy            = True
      pyserial         = True
      pyadaaah         = True
    

#imports which may fail
try:
        from sys     import getwindowsversion as Sys_getwindowsversion
except:
        pass
      

try:
        from ssl     import SSLContext        as Ssl_SSLContext
except:
        ErrorTracker.sslContextImport = False
        print "!! Python/SSL NOT properly installed !!"


try:
        from PySide  import __version__       as PySide___version__
except:
        ErrorTracker.pysideImport = False
        print "!! PySide NOT properly installed !!"
        

try:
        from PySide  import QtCore
        from PySide  import QtGui
        from PySide  import QtXml
        from PySide  import QtSvg
except:
        ErrorTracker.qtImport = False
        print "!! Qt NOT properly installed !!"


try:
        import numpy
        from   numpy        import random
        from   numpy.random import random as random
except:
        ErrorTracker.numpy = False
        print "!! Numpy NOT properly installed !!"         


try:
        import pyqtgraph
except:
        ErrorTracker.pyqtgraph = False
        print "!! PyQtGraph NOT properly installed !!"               


try:
        import matplotlib
        import matplotlib.pyplot
        from   matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg    as MplFigureCanvas
        from   matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as MplNavigationToolbar
        from   matplotlib.figure                  import Figure               as MplFigure        
except:
        ErrorTracker.matplotlib = False
        print "!! Matplotlib NOT properly installed !!"  


try:
        import scipy
        from   scipy             import interpolate
        from   scipy.interpolate import interp1d     as interpol
except:      
        ErrorTracker.scipy = False
        print "!! SciPy NOT properly installed !!" 


try:
        import serial
except:      
        ErrorTracker.pyserial = False
        print "!! pySerial NOT properly installed !!"


try:
        import pyadaaah 
except:      
        ErrorTracker.pyadaaah = False
        print "!! Pyadaaah NOT properly installed !!"         


class Target:
      """ """

      #the machine must be Intel (resp. Intel compatible AMD) based 
      #which means: either "x86", "x86_64" or "AMD64"
      #this SystemTest-Version is for 64-Bit Intels
      machineTypesOk    = ["x86_64", "AMD64"]
      machineTypesMayBe = []
      
      #SystemTest has been developed for "Linux", "macOSX" and "Windows"
      #this SystemTest-Version is for 64-Bit-Windows 
      osTypeOk          = "Windows"
      #osVersionsOK     : hard coded below
      

#bundle of system informations
class SysInfo(object):
      """ """
      
      machineType        = ""
      machineOk          = "KO"
      osType             = ""
      osVersion          = ""
      osOk               = "KO"
      pythonPath         = ""
      pythonVersion      = ""
      pythonOk           = "KO"
      qtVersion          = ""
      qtOk               = "KO"
      pySideVersion      = ""
      pySideOk           = "KO"
      pyQtGraphVersion   = ""
      pyQtGraphOk        = "KO"
      numPyVersion       = ""
      numPyOk            = "KO"
      matplotlibVersion  = ""
      matplotlibOk       = "KO"
      sciPyVersion       = ""
      sciPyOk            = "KO"
      pySerialVersion    = ""
      pySerialOk         = "KO"
      pyadaaahVersion    = ""
      pyadaaahOk         = "KO"      
      
      
      def __init__(self):
          """ """
          
          #machine
          self.machineType   = Platform_machine()

          #os
          self.osType        = self._getOs()
          self.osVersion     = self._getOsVersion(self.osType)
          
          #python executable
          self.pythonPath    = Sys_executable
          self.pythonVersion = Platform_python_version() 
          
          #qt
          try:
                  self.qtVersion = QtCore.__version__
          except:
                  pass
          
          #pyside
          try:
                  self.pySideVersion = PySide___version__
          except:
                  pass

          #pyqtgraph
          try:
                  self.pyQtGraphVersion = pyqtgraph.__version__
          except:
                  pass

          #numpy
          try:
                  self.numPyVersion = numpy.__version__
          except:
                  pass  

          #matplotlib
          try:
                  self.matplotlibVersion = matplotlib.__version__
          except:
                  pass 

          #scipy
          try:
                  self.sciPyVersion = scipy.__version__
          except:
                  pass   

          #pyserial
          try:
                  self.pySerialVersion = serial.__version__
          except:
                  pass  

          #pyadaaah
          try:
                  self.pyadaaahVersion = pyadaaah.getVersion()
          except:
                  pass                                                     
                
          #check versions ('Ok'-s)
          self._checkVersions()                                        

          
      def _getOs(self):
          """ Returns either Linux, macOSX, Windows or ''. """ 
          
          if    Platform_system() == "Linux":
                return 'Linux'
          elif  Platform_system() == "Darwin":
                return 'macOSX'
          elif  Platform_system() == "Windows":
                return 'Windows'
          else:
                return ''
                
                
      def _getOsVersion(self, os):
          """ Returns either the os version or '' (for unknown version). """      

          #default: 'unknown version'
          version = ""
          try:
                  if    os == 'Linux':
                        version += Subprocess_check_output(["lsb_release", "-i", "-s"]).strip()
                        version += " " + Subprocess_check_output(["lsb_release", "-r", "-s"]).strip()                        
                        
                  elif  os == 'macOSX':
                        version = Subprocess_check_output(["sw_vers", "-productVersion"]).strip()
                        
                  elif  os == 'Windows':
                        version = Platform_uname()[2]                                                 
                
          except: 
                  #on error: 'unknown version'
                  pass
                
          #return either the OS version or ''
          return version
          
          
      def _versToInt(self, versionS):
          """ Constructs an int from version strings alike e.g. '4.8.5' (=> 040805) -
              to allow the easy usage of comparison operators.
          """
      
          version = 0
          try:
                  tmp     = map( int, versionS.strip().split('.') )
                  version = "%s%s%s" % ( str(tmp[0]).rjust(2,'0'), \
                                         str(tmp[1]).rjust(2,'0'), \
                                         str(tmp[2]).rjust(2,'0')  )
          
          except:
                  pass
         
          #return an integer standing for the version
          return int(version)
          
          
      def _checkVersions(self):
          """ Fills attributes *Ok. """

          #machine
          if    self.machineType in Target.machineTypesOk:
                self.machineOk    = 'OK'
          elif  self.machineType in Target.machineTypesMayBe:
                self.machineOk    = 'MayBe'
          else: self.machineOk    = 'KO'
                
          #os
          if    self.osType == Target.osTypeOk:
                if    self.osType == 'Windows':
                      if    self.osVersion.startswith("7")      or \
                            self.osVersion.startswith("8")      or \
                            self.osVersion.startswith("10")        :
                            self.osOk = 'OK'
                            
                      elif  self.osVersion.startswith("1")    or \
                            self.osVersion.startswith("2")    or \
                            self.osVersion.startswith("3")    or \
                            self.osVersion.startswith("95")   or \
                            self.osVersion.startswith("98")   or \
                            self.osVersion.startswith("M")    or \
                            self.osVersion.startswith("NT")   or \
                            self.osVersion.startswith("2000")    :
                            self.osOk = 'KO'
                            
                      else:
                            self.osOk = 'MayBe'
                                           
                  
                elif  self.osType == 'macOSX':
                      if    self._versToInt('10.8.0') <= self._versToInt(self.osVersion):
                            self.osOk = 'OK'
                            
                      else:
                            self.osOk = 'MayBe'
                    
                    
                elif  self.osType == 'Linux':
                      self.osOk   = 'OK'
                      
                      
          #python
          if    self._versToInt('2.7.13') <= self._versToInt(self.pythonVersion) <= self._versToInt('2.7.17'):
                self.pythonOk = 'MayBe'

          elif  self._versToInt('2.7.18') <= self._versToInt(self.pythonVersion) <= self._versToInt('2.7.99'):
                self.pythonOk = 'OK'

          else:
                self.pythonOk = 'KO'
                

          #qt
          if    ( self._versToInt('4.8.4') <= self._versToInt(self.qtVersion) <  self._versToInt('4.8.5') ) or \
                ( self._versToInt('4.8.5') <  self._versToInt(self.qtVersion) <  self._versToInt('4.8.7') )    :
                self.qtOk = 'MayBe'

          elif  self._versToInt('4.8.5') == self._versToInt(self.qtVersion):
                self.qtOk = 'OK'

          else:
                self.qtOk = 'KO'
                
                
          #pyside
          if    self._versToInt('1.1.2') <= self._versToInt(self.pySideVersion) < self._versToInt('1.2.2'):
                self.pySideOk = 'MayBe'

          elif  self._versToInt('1.2.2') == self._versToInt(self.pySideVersion):
                self.pySideOk = 'OK'
               
          else:
                self.pySideOk = 'KO'


          #pyqtgraph
          if    self.pyQtGraphVersion == '0.10.0':
                self.pyQtGraphOk = 'OK'

          elif  ( (self.pyQtGraphVersion == '') or self.pyQtGraphVersion.startswith('0.11.0') or self.pyQtGraphVersion.startswith('0.11.1') ):
                self.pyQtGraphOk = 'KO'

          else:
                self.pyQtGraphOk = 'MayBe'

        
          #numpy
          if    self.numPyVersion == '1.16.6':
                self.numPyOk = "OK"

          elif  self._versToInt(self.numPyVersion) >= self._versToInt('1.7.1'):
                self.numPyOk = "MayBe"

          else:
                self.numPyOk = "KO"


          #matplotlib
          if    self.matplotlibVersion == '2.2.5':
                self.matplotlibOk = "OK"

          elif  len(self.matplotlibVersion) > 0:
                self.matplotlibOk = "MayBe"     

          else:
                self.matplotlibOk = "KO"   


          #scipy
          if    self.sciPyVersion == '1.1.0':
                self.sciPyOk = "OK"

          elif  self.sciPyVersion.startswith('1.2'):
                #that is due to an unrefuted virus warning for this version
                self.sciPyOk = "KO"                

          elif  len(self.sciPyVersion) > 0:
                self.sciPyOk = "MayBe"     

          else:
                self.sciPyOk = "KO"    


          #pyserial
          if    self.pySerialVersion == '3.5':
                self.pySerialOk = "OK"

          elif  len(self.pySerialVersion) < 1:
                self.pySerialOk = "KO"

          else:
                self.pySerialOk = "MayBe" 

          #pyadaaah
          if    self._versToInt(self.pyadaaahVersion) >= self._versToInt('0.9'):
                self.pyadaaahOk = "OK"

          else:
                self.pyadaaahOk = "MayBe"                               

        
      def machine(self):
          """ Get machine. """

          return (self.machineType, self.machineOk)           

              
      def os(self):
          """ Get operating system. """

          return ("%s (%s)" % (self.osType, self.osVersion), self.osOk)   
          
          
      def python(self):
          """ Get python. """

          return (self.pythonPath, self.pythonVersion, self.pythonOk)    
          
          
      def qt(self):
          """ Get qt. """

          return (self.qtVersion, self.qtOk) 

      def pyside(self):
          """ Get pyside. """

          return (self.pySideVersion, self.pySideOk)   

      def pyqtgraph(self):
          """ Get pyqtgraph. """

          return (self.pyQtGraphVersion, self.pyQtGraphOk)     

      def numpy(self):
          """ Get numpy. """

          return (self.numPyVersion, self.numPyOk)  

      def matplotlib(self):
          """ Get matplotlib. """

          return (self.matplotlibVersion, self.matplotlibOk)   

      def scipy(self):
          """ Get scipy. """

          return (self.sciPyVersion, self.sciPyOk)  


      def pyserial(self):
          """ Get pyserial. """

          return (self.pySerialVersion, self.pySerialOk)   


      def pyadaaah(self):
          """ Get pyadaaah. """

          return (self.pyadaaahVersion, self.pyadaaahOk)                                                                
          
          
          
          
class SslRating(object):
      """ Used to determine the security rating of the underlying SSL library. """
      
      #regular expression for ssl version string extracting the fork name
      _sslForkRe = Re_compile(r".*(?P<fork>(OpenSSL|LibreSSL)).*", Re_DOTALL)      
      
      
      def _versToNum(self, versionT):
          """ Constructs a long from ssl version tuples alike e.g. (0, 9, 8, 18, 15) -
              to allow the usage of comparison operators.
          """
      
          result = "%s%s%s%s%s" % ( str(versionT[0]).rjust(2,'0'), \
                                    str(versionT[1]).rjust(2,'0'), \
                                    str(versionT[2]).rjust(2,'0'), \
                                    str(versionT[3]).rjust(3,'0'), \
                                    str(versionT[4]).rjust(3,'0')  )
          
          #return an integer standing for the version
          return long(result)    


      def _getVersion(self):
          """
              Note that this already might be outdated - To Be Updated - Do Not Use !!! 
          """
      
          #get openssl version - if any valid
          try:
                  #get complete ssl version string
                  ssl            = {'string' : Ssl_OPENSSL_VERSION}
                  
                  #extract fork: OpenSSL or LibreSSL
                  ssl['fork']    = self._sslForkRe.match(Ssl_OPENSSL_VERSION).groupdict()['fork']            
                  
                  #get version as a list of integers and convert to comparable long
                  ssl['version'] = self._versToNum( Ssl_OPENSSL_VERSION_INFO )            
      
                  if    ssl['fork'] == 'LibreSSL':
                        #rate a libre ssl fork version
                        if    ssl['version'] >= self._versToNum((2,2,7,0,0)):
                              #LibreSSL, at least as up-to-date as 2.2.7, 
                              #is deemed to be
                              #quite secure due and solely to the fact 
                              #that apple uses it in macOSX High Sierra
                              #and that it has been made nearly at the same time 
                              #as OpenSSL 1.0.2h (so it should be at a similar level)
                              ssl['rating']   = 2 #medium
                        else:
                              #earlier versions cannot be trusted on the same basis
                              ssl['rating']   = 3 #min
      
                  elif  ssl['fork'] == 'OpenSSL':
                        #rate an open ssl fork version
                        if    ssl['version']  > self._versToNum((1,1,0,0,0)):
                              #OpenSSL 1.1.0a comes with a severe bug so this is the 
                              #last version with acceptable bugs and which had some
                              #time to prove itself
                              ssl['rating']   = 2 #medium
                          
                        elif  ssl['version']  < self._versToNum((1,0,2,4,0)):
                              #the known bugs of the versions 1.0.2d - 1.0.2f have
                              #been classified thoroughly as 1.0.2d is needed for
                              #32-Bit Windows version - they seem to be acceptable
                              #for the rating of medium security
                              #older versions are not up-to-date anymore
                              ssl['rating']   = 3 #min
                              
                        elif  ssl['version']  < self._versToNum((1,0,2,7,0)):
                              #1.0.2g is the first (already tried-and-tested) version 
                              #with just acceptable bugs; also take the comment concerning
                              #1.0.2d - 1.0.2f above into account
                              ssl['rating']   = 2 #medium
                                                 
                        else:
                              #preferred interval 1.0.2h .. 1.1.0 !!
                              ssl['rating']   = 1 #max
      
                  else:
                        raise Exception("unknown open ssl fork!") 
      
                  #known ssl fork/version found
                  return ssl
      
          except:
                  #unknown ssl fork/version found
                  return {'string' : ssl['string'], 'fork' : None, 'version' : None, 'rating' : None}
                  
                  
      def _getCipher(self):
          """
               Note that this already might be outdated - To Be Updated - Do Not Use !!!  
          """
      
          #check whether one of the two allowed ciphers are available
          cipher = None
          rating = None
          try: 
                    context = Ssl_SSLContext(Ssl_PROTOCOL_SSLv23)    
                    try:
                            context.set_ciphers("ECDHE-RSA-AES256-GCM-SHA384")
                            #no error -> best cipher available
                            cipher = "ECDHE-RSA-AES256-GCM-SHA384"
                            rating = 1
                    except:
                            #exception -> cipher not available
                            try:
                                    #test fallback
                                    context.set_ciphers("AES256-SHA")
                                    #no error -> fallback cipher available
                                    cipher = "AES256-SHA"
                                    rating = 3
                            except:
                                    #fallback not available too, keep cipher/rating None (no suitable cipher available)
                                    pass                  
                    
          except:
                    #keep cipher/rating None (no suitable cipher available)
                    pass
                
          finally:
                   return { 'cipher' : cipher, 'rating' : rating }
                   
                   
      def get(self):
          """ """
          
          result = dict()
      
          #get openssl rating - if any valid
          version = self._getVersion()
          cipher  = self._getCipher()
          
          #forward some information in any case
          result['version'] = version['string']          
          result['cipher']  = cipher['cipher']
          
          rating  = (version['rating'], cipher['rating'])
          if    min(rating) == None:
                result['rating'] = None
             
          else:
                #rating is the worse of the two single ratings... (1 the best, 3 the worst)
                result['rating'] = max(rating)
                
          return result          
                    
          
          
                    
sysInfo = SysInfo()
print "System Test Result:"
print ""
print "************************************************************"
print ("* Architektur:        %s -- %s" % sysInfo.machine()).ljust(59, ' ') + "*"
print ("* Betriebssystem:     %s -- %s" % sysInfo.os()).ljust(59, ' ') + "*"
print ("* Python-Executable:  %s" % sysInfo.python()[0])
print ("* Python-Version:     %s -- %s" % sysInfo.python()[1:]).ljust(59, ' ') + "*"
print ("* Qt-Version:         %s -- %s" % sysInfo.qt()).ljust(59, ' ') + "*"
print ("* PySide-Version:     %s -- %s" % sysInfo.pyside()).ljust(59, ' ') + "*"
print ("* PyQtGraph-Version:  %s -- %s" % sysInfo.pyqtgraph()).ljust(59, ' ') + "*"
print ("* NumPy-Version:      %s -- %s" % sysInfo.numpy()).ljust(59, ' ') + "*"
print ("* Matplotlib-Version: %s -- %s" % sysInfo.matplotlib()).ljust(59, ' ') + "*"
print ("* SciPy-Version:      %s -- %s" % sysInfo.scipy()).ljust(59, ' ') + "*"
print ("* pySerial-Version:   %s -- %s" % sysInfo.pyserial()).ljust(59, ' ') + "*"
print ("* Pyadaaah-Version:   %s -- %s" % sysInfo.pyadaaah()).ljust(59, ' ') + "*"
sslRating = SslRating()
ssl = sslRating.get()
sslOk = 'KO'

if    ssl['rating'] == 1:
      sslOk = 'Maximal (OK)'
elif  ssl['rating'] == 2:
      sslOk = 'Medium (MayBe)'
elif  ssl['rating'] == 3:
      sslOk = 'KO'

print ("* SSL-Version:        %s" % ssl['version']).ljust(59, ' ') + "*"
if    ssl['cipher'] == "ECDHE-RSA-AES256-GCM-SHA384":
      sslCipherMsg = "ECDHE-RSA-AES256-GCM-SHA384 cipher is available"
else:
      sslCipherMsg = "ECDHE-RSA-AES256-GCM-SHA384 cipher is NOT available"
print ("* %s " % sslCipherMsg).ljust(59, ' ') + "*"
#print ("* SSL-Cipher:        %s" % ssl['cipher']).ljust(59, ' ') + "*"
#print ('* SSL-Rating:        %s' % sslOk).ljust(59, ' ') + "*"
print "************************************************************"
print ""


#create the underlying Qt application
mainApplication = QtGui.QApplication(Sys_argv)

#create main window and belonging layout and display it
mainWindow = QtGui.QMainWindow()
std = "rgb(180, 180, 180)"
mainWindow.setStyleSheet("QWidget {background-color: %s;}" % std)
centralWidget = QtGui.QWidget()
mainWindow.setCentralWidget(centralWidget)
layout        = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
centralWidget.setLayout(layout)
mainWindow.setWindowTitle(u'Blackward\u00ae  --  Blythooon-Test V0.8  --  Copyright \u00a9 2021 Dominik Niedenzu')
mainWindow.setGeometry(1, 1, 800, 600)
mainWindow.show()
mainWindow.move(50,50)

#bring main window to front
if    Platform_system() == "Darwin":
      #unfortunately activating does not work under OSX
      #workaround:
      mainWindow.showMinimized()
      mainWindow.showNormal()
else:
      #bring to front / focus
      mainWindow.setWindowState(QtCore.Qt.WindowActive)

#helper function
def getColor(ok):
    """ """
    global green, yellow, red
    
    if    ok == 'OK':
          return "rgb(0,200,0)"
    elif  ok == 'KO':
          return "rgb(250,0,0)"
    else:
          return "rgb(210,210,0)"


#helper function
def lineEdit(text, color):
    """ """

    widget           = QtGui.QLineEdit()
    widget.setReadOnly(True)
    widget.setAlignment(QtCore.Qt.AlignCenter)
    widget.setText(text)
    widget.setStyleSheet("background-color: %s;" % color)
    
    return widget  


### blackward logo ###
#load svg part from the end of this file
scriptPathS      = Os_path.abspath( Os_path.realpath(__file__) )
with open(scriptPathS, "r") as fileHandle:
     #ignore everything before said svg part
     while not fileHandle.readline().startswith('blackwardLogoSvgStringS = """'):
           pass

     #create string containing logo SVG
     blackwardLogoSvgS = ""
     currLineS         = fileHandle.readline()
     while not currLineS.startswith('""" #end of Blackward logo SVG'):
           blackwardLogoSvgS += currLineS
           currLineS          = fileHandle.readline()

#put it into a SVG widget
blackwardWidget = QtSvg.QSvgWidget()
blackwardWidget.load( QtCore.QByteArray( blackwardLogoSvgS ) ) 

#set up Blackward logo SVG widget  
blackwardWidget.setMinimumWidth(181)
blackwardWidget.setMinimumHeight(30)
blackwardWidget.setMaximumWidth(181)
blackwardWidget.setMaximumHeight(30)
layout.addWidget(blackwardWidget)


#architecture
text         = "Architektur:        %s" % sysInfo.machine()[0]
color        = getColor(sysInfo.machine()[1])
archWidget   = lineEdit(text, color)
archWidget.setFrame(False)
layout.addWidget(archWidget)

#operating system
text         = "Betriebssystem:     %s" % sysInfo.os()[0]
color        = getColor(sysInfo.os()[1])
osWidget     = lineEdit(text, color)
osWidget.setFrame(False)
layout.addWidget(osWidget)

#python
pathText     = Os_path.split(sysInfo.python()[0])[0]
fileText     = Os_path.split(sysInfo.python()[0])[1]
text         = "Python-Executable:  %s" % (pathText[:80]+"   "+fileText)
pythonWidget = lineEdit(text, std)
pythonWidget.setFrame(False)
layout.addWidget(pythonWidget)
text         = "Python-Version:     %s" % sysInfo.python()[1]
color        = getColor(sysInfo.python()[2])
python2Widget = lineEdit(text, color)
python2Widget.setFrame(False)
layout.addWidget(python2Widget)

#qt
text         = "Qt-Version:         %s" % sysInfo.qt()[0]
color        = getColor(sysInfo.qt()[1])
qtWidget     = lineEdit(text, color)
qtWidget.setFrame(False)
layout.addWidget(qtWidget)

#pyside
text         = "PySide-Version:     %s" % sysInfo.pyside()[0]
color        = getColor(sysInfo.pyside()[1])
psWidget     = lineEdit(text, color)
psWidget.setFrame(False)
layout.addWidget(psWidget)

#pyqtgraph
text         = "PyQtGraph-Version:  %s" % sysInfo.pyqtgraph()[0]
color        = getColor(sysInfo.pyqtgraph()[1])
pqgWidget     = lineEdit(text, color)
pqgWidget.setFrame(False)
layout.addWidget(pqgWidget)

#numpy
text         = "NumPy-Version:      %s" % sysInfo.numpy()[0]
color        = getColor(sysInfo.numpy()[1])
npWidget     = lineEdit(text, color)
npWidget.setFrame(False)
layout.addWidget(npWidget)

#matplotlib
text         = "Matplotlib-Version: %s" % sysInfo.matplotlib()[0]
color        = getColor(sysInfo.matplotlib()[1])
mplWidget     = lineEdit(text, color)
mplWidget.setFrame(False)
layout.addWidget(mplWidget)

#scipy
text         = "SciPy-Version:      %s" % sysInfo.scipy()[0]
color        = getColor(sysInfo.scipy()[1])
spWidget     = lineEdit(text, color)
spWidget.setFrame(False)
layout.addWidget(spWidget)

#ssl
text         = "SSL-Version:        %s" % ssl['version']
sslVers      = sslRating._getVersion()['rating']
#color         = getColor('KO')
#if    sslVers == 1:
#      color   = getColor('OK')
#elif  sslVers == 2:
#      color   = getColor('MayBe')
      
sslWidget     = lineEdit(text, std)
sslWidget.setFrame(False)
layout.addWidget(sslWidget)

#sslCiph       = sslRating._getCipher()['rating']
#color         = getColor('KO')
#if    sslCiph == 1:
#      color   = getColor('OK')
#elif  sslCiph == 2:
#      color   = getColor('MayBe')

text          = sslCipherMsg
ssl2Widget    = lineEdit(text, std)
ssl2Widget.setFrame(False)
layout.addWidget(ssl2Widget)

#text         = 'SSL-Rating' 
#color        = getColor('KO')
#if    sslOk == 'Maximal (OK)':
#      color  = getColor('OK')
#elif  sslOk == 'Medium (MayBe)':
#      color  = getColor('MayBe')
      
#ssl3Widget    = lineEdit(text, color)
#ssl3Widget.setFrame(False)
#layout.addWidget(ssl3Widget)


#pyserial
text          = "pySerial-Version:   %s" % sysInfo.pyserial()[0]
color         = getColor(sysInfo.pyserial()[1])
pslWidget     = lineEdit(text, color)
pslWidget.setFrame(False)
layout.addWidget(pslWidget)


#pyadaaah
text          = "Pyadaaah-Version:   %s" % sysInfo.pyadaaah()[0]
color         = getColor(sysInfo.pyadaaah()[1])
pyhWidget     = lineEdit(text, color)
pyhWidget.setFrame(False)
layout.addWidget(pyhWidget)


#two plot layout
plotWidget    = QtGui.QWidget()
plotLayout    = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
plotWidget.setLayout(plotLayout)
layout.addWidget(plotWidget)

#(just) initial data for plots
x = [1,2,3,4,5,6,7,8]
y = [1,2,3,4,5,6,7,8]

### pyqtgraph ###
try:
         pyqtgraph.setConfigOption('foreground', 'w')
         pyqtgraphWidget = pyqtgraph.PlotWidget(title="PyQtGraph test plot")
         pyqtgraphWidget.setLabel('left',   "y axis label [unit]")
         pyqtgraphWidget.setLabel('bottom', "x axis label [unit]")
         pyqtgraphWidget.plot(x, y, pen=None, symbolPen=None, symbol="o", symbolBrush="b")

except   BaseException as ee:
         print ee
         #show a red area where the pyqtgraph should be - indicating an error
         pyqtgraphWidget = QtGui.QWidget()
         pyqtgraphWidget.setAttribute(QtCore.Qt.WA_StyledBackground, True)
         pyqtgraphWidget.setStyleSheet( "QWidget {background-color: %s;}" % getColor("KO") )

plotLayout.addWidget(pyqtgraphWidget)

### matplotlib ###
try:
         #create matplotlib widget with layout
         mplWidget = QtGui.QWidget()
         mplWidget.setAttribute(QtCore.Qt.WA_StyledBackground, True)
         mplWidget.setAutoFillBackground(True)
         mplWidget.setStyleSheet( "QWidget {color: white; background-color: black;}" )

         mplLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)

         #create plot widgets
         mplFigure, mplPlot  = matplotlib.pyplot.subplots()
         mplFigure.tight_layout(pad=4)

         mplCanvas  = MplFigureCanvas(mplFigure)

         mplToolbar = MplNavigationToolbar(mplCanvas, mplWidget)
         mplToolbar.setStyleSheet( "QWidget {color: black; background-color: white;}" )

         #set background to black
         mplFigure.set_facecolor("black")

         #plot data
         mplPlot.set_facecolor("black")
         mplPlot.title.set_color('white')
         mplPlot.set_title("Matplotlib test plot")
         mplPlot.tick_params(axis='both', colors='white')
         mplPlot.spines['left'].set_color('white')
         mplPlot.spines['bottom'].set_color('white')
         mplPlot.xaxis.label.set_color('white')
         mplPlot.set_xlabel("x axis label [unit]")
         mplPlot.yaxis.label.set_color('white')
         mplPlot.set_ylabel("y axis label [unit]")

         #plot data
         mplPlot.scatter(x, y, color="b")

         #compose plot widgets
         mplLayout.addWidget(mplToolbar)
         mplLayout.addWidget(mplCanvas)

         #delayed set layout - to be sure, that no error occured up to that
         mplWidget.setLayout(mplLayout)

except   BaseException as ee:
         print ee
         #show a red area where the pyqtgraph should be - indicating an error
         mplWidget.setStyleSheet( "QWidget {color: white; background-color: red;}" )

#add/show matplotlib widget
plotLayout.addWidget(mplWidget)

#create a button and add it to the main window
buttonWidget = QtGui.QPushButton('OK')
layout.addWidget(buttonWidget)

#connect button and window-close-event with exitLoop()
appOk = "KO"
def exitLoop(*params, **paramDict):
    global appOk
    appOk = "OK"
    mainWindow.close()
QtCore.QObject.connect(buttonWidget, QtCore.SIGNAL('clicked()'), exitLoop)
mainWindow.closeEvent = exitLoop




class SlidingDataBox(object):
      """ """

      ### internal attributes ###
      #just use interface methods!
      _abscissaeL         = []          #x coordinates 
      _ordinatesL         = []          #y coordinates

      _directionSignI     = 1           #the sign of the current 'data direction': 1<=>upwards, -1<=>downwards
      _continueDirectionI = 5           #continue in the current direction for further 'number of points' given here
      _changeDirectionInI = 5           #change direction every 'number of points'

      _boxWidthI          = 8           #number of points in sliding box           
      _frameWidthI        = 2           #frame width (additional, unseen points) - around sliding box (helpful for e.g. cubic interpolation)
      _effectiveBoxWidthI = 8 + (2*2)   #_boxWidthI + 2 * _frameWidthI


      #constructor
      def __init__(self):
          """ Initialises the classes attributes. """

          self._abscissaeL         = [ x for x in range(self._effectiveBoxWidthI) ]

          self._effectiveBoxWidthI = self._boxWidthI + 2 * self._frameWidthI 
          self._ordinatesL         = [ y for y in self._abscissaeL ]


      #interface method
      def currentXes(self):
          """ Returns the x values of the current (visible) box. """

          return self._abscissaeL[ self._frameWidthI : -self._frameWidthI ]


      #interface method
      def currentYes(self):
          """ Returns the y values of the current (visible) box. """

          return self._ordinatesL[ self._frameWidthI : -self._frameWidthI ]      


      #interface method
      def interpolFct(self):
          """ Returns function interpolating the currrent (visible and invisible) box. """

          return interpol(numpy.array(self._abscissaeL), numpy.array(self._ordinatesL), kind="cubic")


      #interface method
      def shiftBox(self):
          """ Shifts the box by one point to the right (adds a new random point). """

          #if a new graph direction is necessary, assign it randomly
          if self._continueDirectionI <= 0:
             self._continueDirectionI = round(self._changeDirectionInI * random())
             if    ( random() >= 0.5 ):
                   #upwards
                   self._directionSignI = 1
             else:
                   #downwards
                   self._directionSignI = -1

          #shift box
          self._abscissaeL.pop(0)
          self._abscissaeL.append( self._abscissaeL[-1] + 1 )

          self._ordinatesL.pop(0)
          self._ordinatesL.append( self._ordinatesL[-1] + (self._directionSignI * random()) )

          self._continueDirectionI -= 1


#called cyclically
def nextPlot():
    """ """

    global commonOnce, pyQtGraphOnce, matplotlibOnce, data, pyqtgraphWidget, mplPlot 

    #common block
    try:
            #shift data box one point to the right (add another random point on the right)
            data.shiftBox()

            #get current box
            xesL     = data.currentXes()
            yesL     = data.currentYes()
            moreXesL = numpy.linspace( xesL[0], xesL[-1], len(xesL) * 10 )
            moreYesL = data.interpolFct()(moreXesL)

    except  BaseException as ee:
            #avoid cyclically printing errors 
            if    commonOnce == False:
                  commonOnce = True
                  print "Error in function nextPlot (common block):"
                  print ee
            else:
                  pass            

    #pyqtgraph block
    try:
            #update pyqtgraph plot
            pyqtgraphWidget.clear()
            pyqtgraphWidget.plot(xesL, yesL,         pen=None, symbolPen=None, symbol="o",  symbolBrush="b")
            pyqtgraphWidget.plot(moreXesL, moreYesL, pen="r",  symbolPen=None, symbol=None, symbolBrush=None)

    except  BaseException as ee:
            #avoid cyclically printing errors 
            if    pyQtGraphOnce == False:
                  pyQtGraphOnce = True
                  print "Error in function nextPlot (pyqtgraph block):"
                  print ee
            else:
                  pass            

    #matplotlib block     
    try:
            mplPlot.clear()
            mplPlot.title.set_color('white')
            mplPlot.set_title("Matplotlib test plot")
            mplPlot.scatter(xesL, yesL, color="b")
            mplPlot.plot(moreXesL, moreYesL, color="r")
            mplPlot.set_xlabel("x axis label [unit]")
            mplPlot.set_ylabel("y axis label [unit]")
            mplCanvas.draw()  

    except  BaseException as ee:
            #avoid cyclically printing errors 
            if    matplotlibOnce == False:
                  matplotlibOnce = True
                  print "Error in function nextPlot (matplotlib block):"
                  print ee
            else:
                  pass   




#start Qt application main loop
commonOnce     = False
pyQtGraphOnce  = False
matplotlibOnce = False
data = SlidingDataBox()
timer = QtCore.QTimer()
QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), nextPlot)
timer.start(200) 
mainApplication.exec_()


### after closing window ###
#check whether installation was successful and return belonging value
results = []
results.append(sysInfo.machineOk)
results.append(sysInfo.osOk)
results.append(sysInfo.pythonOk)
results.append(sysInfo.qtOk)
results.append(sysInfo.pySideOk)
results.append(sysInfo.pyQtGraphOk)
results.append(sysInfo.numPyOk)
results.append(sysInfo.matplotlibOk)
results.append(sysInfo.sciPyOk)
results.append(sysInfo.pySerialOk)
results.append(sslVers)
results.append(appOk)

#return
if    ("KO" in results)                        or \
      (ErrorTracker.qtImport         == False) or \
      (ErrorTracker.pysideImport     == False) or \
      (ErrorTracker.pyqtgraph        == False) or \
      (ErrorTracker.numpy            == False) or \
      (ErrorTracker.matplotlib       == False) or \
      (ErrorTracker.scipy            == False) or \
      (ErrorTracker.sslContextImport == False) or \
      (ErrorTracker.pyserial         == False)    :
      #notify installation error
      Sys_exit(1)
else:
      #notify successful installation
      Sys_exit(0)



### the following is an embedded SVG file containing the Blackward logo ###
### note that using said, following Blackward logo outside of this program is strictly forbidden ###
blackwardLogoSvgStringS = """
<?xml version="1.0" standalone="no"?>
<?xml-stylesheet type="text/css" href="./style.css" ?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" >

<svg preserveAspectRatio="xMinYMin meet" viewBox="0 0 283.7 47.0" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<desc> BlackwardLogo-RTM - Copyright 2014-2021 by Dominik Niedenzu, All Rights Reserved </desc>


   <!-- definition of R of (R)-->
   <defs>
      <symbol>
         <path id="R" horiz-adv-x="555" d="M381 620c-68 0 -85 -17 -90 -46l-49 -249h48c93 0 171 28 195 153c3.10001 16.1 4.60001 30.5 4.60001 43.3c0 80.8 -57.7 98.7 -108.6 98.7zM387 654c60 0 119 -5 156 -50c20.6 -25.1 31 -53.9 31 -87.4c0 -11.9 -1.40002 -24.4 -4 -37.6c-21 -105 -117 -157 -161 -171
l80 -210c17 -43 34 -77 77 -77l-3 -24c-11 -5 -28 -7 -42 -7c-58 0 -91 42 -110 89l-68 174c-10 23 -27 38 -107 38l-43 -219c-1 -4.8 -1.5 -9.2 -1.5 -13c0 -20.1 13.6 -27.5 45.5 -30l25 -2c4 0 7 -3 6 -8l-3 -19l-3 -2c-45 1 -84 2 -122 2s-77 -1 -122 -2l-2 2l4 19
c1 5 4 8 9 8l25 2c41 3 56 15 61 43l98 502c0.600006 3.40002 0.899994 6.59998 0.899994 9.5c0 24.3 -20.6 31.6 -34.9 32.5l-37 2c-4 0 -6 2 -5 6l4 21l3 2c45 -1 83 -2 121 -2s98 9 122 9z" />
      </symbol>
   </defs>


   <!-- "(R)" -->
   <g transform="translate(267.5,2.5) scale(0.015)">
      <circle cx="310" cy="440" r="500" fill="#c0c0c0" opacity="0.35" stroke="none"/>
      <use xlink:href="#R" transform="matrix(1,0,0,-1,0,754)"/>

      <circle cx="310" cy="440" r="500" fill="none" stroke="black" stroke-width="80"/>
      <!-- desktop version hyperlink connection-->
      <a xlink:href="https://register.dpma.de/DPMAregister/marke/register/3020130315073/DE" target="homepage">
         <circle class="button" cx="310" cy="440" r="500" stroke="none" stroke-width="80" fill="white" opacity="0.0"/>
      </a>
   </g>


   <a xlink:href="https://www.blackward.de" target="homepage">
     <g class="logo" transform="skewX(-12)">
         <desc> character B </desc>
         <g>
           <path d="M 12.5,46 q -2.5,0 -2.5,-2.5 l 0,-40 q 0,-2.5 2.5,-2.5 l 12.5,0 l 4,0 q 7,0 7,7 l 0,6 q 0,7 -7,7 l 4,0 q 7,0 7,7 l 0,11 q 0,7 -7,7 z M 22.5,37 q -2.5,0 -2.5,-2.5 l 0,-23 q 0,-2.5 2.5,-2.5 l 1,0 q 2.5,0 2.5,2.5 l 0,1 q 0,2.5 -2.5,2.5 q -2.5,0 -2.5,2.5 l 0,8 q 0,2.5 2.5,2.5 l 4,0 q 2.5,0 2.5,2.5 l 0,4 q 0,2.5 -2.5,2.5 z" fill-rule="evenodd" />
         </g>

         <desc> character l </desc>
         <g>
           <path d="M 44.5,3.5 q 0,-2.5 2.5,-2.5 l 5,0 q 2.5,0 2.5,2.5 l 0,40 q 0,2.5 -2.5,2.5 l -5,0 q -2.5,0 -2.5,-2.5 z"/>
         </g>

         <desc> character a </desc>
         <g>
           <path d="M 59.5,18 q 0,-7 7,-7 q 7,0 7,7 l 0,-4.5 q 0,-2.5 2.5,-2.5 l 5,0 q 2.5,0 2.5,2.5 l 0,30 q 0,2.5 -2.5,2.5 l -5,0 q -2.5,0 -2.5,-2.5 l 0,-4.5 q 0,7 -7,7 q -7,0 -7,-7 z M 73.5,28.5 l 0,6 q 0,2.5 -2.5,2.5 q -2.5,0 -2.5,-2.5 l 0,-12 q 0,-2.5 2.5,-2.5 q 2.5,0 2.5,2.5 z" fill-rule="evenodd" />
         </g>

         <desc> character c </desc>
         <g>
           <path d="M 95.5,46 q -7,0 -7,-7 l 0,-21 q 0,-7 7,-7 l 8.5,0 q 2.5,0 2.5,2.5 l 0,4 q 0,2.5 -2.5,2.5 l -3,0 q -2.5,0 -2.5,2.5 l 0,12 q 0,2.5 2.5,2.5 l 3,0 q 2.5,0 2.5,2.5 l 0,4 q 0,2.5 -2.5,2.5 l -8.5,0 z" />
         </g>

         <desc> character k </desc>
         <g>
           <path d="M 128.5,46 q -2.5,0 -2.5,-2.5 l 0,-3 q 0,-7 -7,-7 l 2,0 l 0,10 q 0,2.5 -2.5,2.5 l -5,0 q -2.5,0 -2.5,-2.5 l 0,-40 q 0,-2.5 2.5,-2.5 l 5,0 q 2.5,0 2.5,2.5 l 0,22 l -2,0 q 7,0 7,-7 l 0,-5 q 0,-2.5 2.5,-2.5 l 5,0 q 2.5,0 2.5,2.5 l 0,9 q 0,7 -7,7 q 7,0 7,7 l 0,7 q 0,2.5 -2.5,2.5 z" />
         </g>

         <desc> character w </desc>
         <g>
           <path d="M 141,13.5 q 0,-2.5 2.5,-2.5 l 5,0 q 2.5,0 2.5,2.5 l 0,21 q 0,2.5 2.5,2.5 q 2.5,0 2.5,-2.5 l 0,-21 q 0,-2.5 2.5,-2.5 l 5,0 q 2.5,0 2.5,2.5 l 0,21 q 0,2.5 2.5,2.5 q 2.5,0 2.5,-2.5 l 0,-21 q 0,-2.5 2.5,-2.5 l 5,0 q 2.5,0 2.5,2.5 l 0,25.5 q 0,7 -7,7 l -6,0 q -7,0 -7,-7 q 0,7 -7,7 l -6,0 q -7,0 -7,-7 z" />
         </g>

         <desc> character a </desc>
         <g>
           <path d="M 186,18 q 0,-7 7,-7 q 7,0 7,7 l 0,-4.5 q 0,-2.5 2.5,-2.5 l 5,0 q 2.5,0 2.5,2.5 l 0,30 q 0,2.5 -2.5,2.5 l -5,0 q -2.5,0 -2.5,-2.5 l 0,-4.5 q 0,7 -7,7 q -7,0 -7,-7 z M 200,28.5 l 0,6 q 0,2.5 -2.5,2.5 q -2.5,0 -2.5,-2.5 l 0,-12 q 0,-2.5 2.5,-2.5 q 2.5,0 2.5,2.5 z" fill-rule="evenodd" />
         </g>

         <desc> character r </desc>
         <g>
           <path d="M 217.5,46 q -2.5,0 -2.5,-2.5 l 0,-30 q 0,-2.5 2.5,-2.5 l 5,0 q 2.5,0 2.5,2.5 l 0,4.5 q 0,-7 7,-7 q 2.5,0 2.5,2.5 l 0,7 q 0,2.5 -2.5,2.5 q -7,0 -7,7 l 0,13.5 q 0,2.5 -2.5,2.5 z" />
         </g>

         <desc> character d </desc>
         <g>
           <path d="M 237.5,18 q 0,-7 7,-7 q 7,0 7,7 l 0,-14.5 q 0,-2.5 2.5,-2.5 l 5,0 q 2.5,0 2.5,2.5 l 0,40 q 0,2.5 -2.5,2.5 l -5,0 q -2.5,0 -2.5,-2.5 l 0,-4.5 q 0,7 -7,7 q -7,0 -7,-7 z M 251.5,28.5 l 0,6 q 0,2.5 -2.5,2.5 q -2.5,0 -2.5,-2.5 l 0,-12 q 0,-2.5 2.5,-2.5 q 2.5,0 2.5,2.5 z" fill-rule="evenodd" />
         </g>
     </g>
   </a>
</svg>
""" #end of Blackward logo SVG