#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pyadaaah - Copyright & Contact Notice
############################################
# Created by Dominik Niedenzu              #      
# Copyright (C) 2020,2021 Dominik Niedenzu #       
#     All Rights Reserved                  #
#                                          #
#           Contact:                       #
#      pyadaaah@blackward.de               #         
#      www.blackward.de                    #         
############################################

# Pyadaaah - Version & Modification Notice
##########################################
# Based on Pyadaaah Version 0.90         #
# Modified by --- (date: ---)            #
##########################################

# Pyadaaah - License
#######################################################################################################################
# Use and redistribution in source and binary forms, without or with modification,                                    #
# are permitted (free of charge) provided that the following conditions are met (including the disclaimer):           #
#                                                                                                                     #
# 1. Redistributions of source code must retain the above copyright & contact notice and                              #
#    this license text (including the permission notice, this list of conditions and the following disclaimer).       #
#                                                                                                                     #
#    a) If said source code is redistributed unmodified, the belonging file name must be pyadaaah.py and              #
#       said file must retain the above version & modification notice too.                                            #
#                                                                                                                     #
#    b) Whereas if said source code is redistributed modified (this includes redistributions of                       #
#       substantial portions of the source code), the belonging file name(s) must be pyadaaah_modified*.py            #
#       (where the asterisk stands for an arbitrary intermediate string) and said files                               #
#       must contain the above version & modification notice too - updated with the name(s) of the change             #
#       maker(s) as well as the date(s) of the modification(s).                                                       #
#                                                                                                                     #
# 2. Redistributions in binary form must reproduce the above copyright & contact notice and                           #
#    this license text (including the permission notice, this list of conditions and the following disclaimer).       #
#    They must also reproduce a version & modification notice similar to the one above - in the                       #
#    sense of 1. a) resp. b).                                                                                         #
#                                                                                                                     #
# 3. Neither the name "Dominik Niedenzu", nor the name resp. trademark "Blackward", nor the names of authors resp.    #
#    contributors resp. change makers may be used to endorse or promote products derived from this software without   #
#    specific prior written permission.                                                                               #
#                                                                                                                     #
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO   # 
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.                            #
#                                                                                                                     #
# IN NO EVENT SHALL DOMINIK NIEDENZU OR AUTHORS OR CONTRIBUTORS OR CHANGE MAKERS BE LIABLE FOR ANY CLAIM, ANY         # 
# (DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY OR CONSEQUENTIAL) DAMAGE OR ANY OTHER LIABILITY, WHETHER IN AN    #
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THIS SOFTWARE (OR PARTS OF THIS   #
# SOFTWARE) OR THE USE OR REDISTRIBUTION OR OTHER DEALINGS IN THIS SOFTWARE (OR PARTS OF THIS SOFTWARE).              #
#                                                                                                                     #
# THE USERS RESP. REDISTRIBUTORS OF THIS SOFTWARE (OR PARTS OF THIS SOFTWARE) ARE SOLELY RESPONSIBLE FOR ENSURING     #
# THAT AFOREMENTIONED CONDITIONS ALL ARE MET AND COMPLIANT WITH THE LAW IN THE RESPECTIVE JURISDICTION - BEFORE (!)   #
# THEY USE RESP. REDISTRIBUTE.                                                                                        #
#######################################################################################################################


#import common libraries resp. parts of such
import sys
from   types    import ModuleType     as Types_ModuleType
from   sys      import stderr         as Sys_stderr
from   sys      import excepthook     as Sys_excepthook
from   sys      import version_info   as Sys_version_info
from   os       import linesep        as Os_linesep
from   re       import compile        as Re_compile
from   re       import DOTALL         as Re_DOTALL
from   argparse import ArgumentParser as Argparse_ArgumentParser


#get pyadaaah version
__version__ = 0.9
def getVersion():
    global __version__
    return __version__


#python version 2 checker
def isPy2():
    """
         Returns True if Python version in use is < 3.0.
    """
    if    Sys_version_info.major < 3.0:
          return True
    else:
          return False
          
          
#python version 3 checker          
def isPy3():
    """
         Returns True if Python version in use is >= 3.0.
    """
    if    Sys_version_info.major >= 3.0:
          return True
    else:
          return False


### take differences between python2 and python3 into account ###
if      isPy2() == True:
        ### python version < 3 ###
        #using the types library for checking for built-in types is (just) python 2(.7) style
        from   types    import StringTypes    as Types_StringTypes
        from   types    import UnicodeType    as Types_UnicodeType
else:
        ### python version >= 3 ###
        #in python3 there are no string types in types library at all
        #in python3 there just is str as a string type (no unicode type)
        Types_StringTypes = (str,)
        Types_UnicodeType = str
        
        #in python3 there is just an int type (no long type)
        long              = int


#if possible, import cythons data types which are used in this module
#if cython is available, set "use cython types" as a default - otherwise not
try:
        import cython
        UseCythonTypes = True
        
except:
        UseCythonTypes = False
      
  
      
      
#STR - accepting (and translating) unicode characters too
class STR(str):
    """
         String class accepting e.g. and in particular unicodes as well; 
         the result is a pure ascii (0-127) string, which is achieved by 
         replacing all non-ascii characters by '?'.
    """
    
    #return the pure ascii string
    def __new__(cls, text):
        """ """   
        
        try:
               #make a str out of text - if not already one (resp. an unicode)
               if    isinstance(text, Types_StringTypes):
                     textS = text
               else:
                     textS = str(text)
              
               #make a unicode out of textS - if not already one
               if not isinstance(textS, Types_UnicodeType):
                  textS = textS.decode("ascii", "replace")
        
               #unicode is str in python 3 - but not in python 2
               #in python 2: encode back to str
               if isPy2() == True:
                  #replace non-ascii characters by '?'
                  textS = textS.encode("ascii", "replace")
                  
               #return
               return textS
              
        except BaseException as ee:
               return "Error in STR: %s!" % str(ee)
               
               
               
               
#helper function
def EVAL(stringS, environmentD=None):
    """
         Return the evaluation of stringS, taking environmentD into account - if not None.
    """
    
    #return the evaluation of stringS
    if    environmentD == None:
          #no environment given (VarDef just comprises built-in and/or cython types)
          return eval(stringS)
          
    else:
          #symbols from environment (e.g. from globals()) are taken into account
          return eval(stringS, environmentD)                 
    



### Exception Handling ###
#exceptions
class PyadaException(BaseException):
      """
           With PyadaExceptions the traceback mechanism is another - see ExceptionHandler.
      """
      
      pass
    
    
    
    
class CtrlException(PyadaException):
      """ 
          Exception which is not catched by a 'logExceptions'-decorator and which 
          correspondingly is not logged. Can e.g. be used for prg flow control. 
      """
      
      pass
    
    
    
    
class Notification(PyadaException):
      """ Something unexpected / unwanted by pyadaaah - but need not be an error. """
      
      pass    
    
    
    
    
class Aberration(PyadaException):
      """ Mild aberration - just requires notification resp. logging. """
      
      pass
    
    
    
    
class LocalError(PyadaException):
      """ Localized error - just requires local measures. """
      
      pass 
    
    
    
    
class FatalError(PyadaException):
      """ Severe error (with potential global impact) - process termination suggested. """
      
      pass
    
    

    
class DocTypesError(FatalError):
      """ 
           Raised in case of an error during parsing the __doc__ string of a
           class inheriting from DocTypes.
      """
      
      pass    
    
    
    
    
class NoAnyRange(CtrlException):
      """ 
           Raised if AnyRange gets a rangeS string parameter which does not fit.
           This error is (just) made to be specifically catchable by 'except's.
      """
      
      pass
    
    
    
    
class TypeMismatch(CtrlException):
      """
          Raised when doc TYPE checking leads to an error.
      """
      
      pass
    
    

    
class RangeMismatch(CtrlException):
      """
          Raised when doc type RANGE checking leads to an error.
      """
      
      pass   
    
    
    
    
class ReadOnly(CtrlException):
      """
          Raised when writing a read only variable.
      """
      
      pass
    
    
    
      
#exception handler comprising logger   
class ExceptionHandler(object):
      """ """
      
      #interface
      __slots__ = ( "stderr", "logTypesT", "_originalHook" )
      
      
      #method used to switch of the standard output of traceback in favour of 
      #an own traceback mechanism on the basis of @logExceptions
      @classmethod
      def hook(cls, exceptionType, exception, traceback):
          """ """

          if    isinstance(exception, PyadaException):
                #(just) give out exception (as pure ascii string)
                cls.stderr.write( STR(exception) )
                
          else:
                #do not change the traceback-mimic for exceptions which are not 
                #inherited from PyadaException
                cls._originalHook(exceptionType, exception, traceback)
      
      
      #constructor
      @classmethod
      def init(cls, stderr=Sys_stderr, exceptHook=Sys_excepthook):
          """ """
          
          #init tuple of types to be logged - beneath strings
          cls.logTypesT = ( Aberration, LocalError, FatalError ) + Types_StringTypes          
          
          #init output channel (with default stderr)
          cls.stderr        = Sys_stderr
          
          #hook in exception handler (exceptHook)
          cls._originalHook = sys.excepthook
          sys.excepthook    = cls.hook
         
                  
      @classmethod
      def log(cls, exception):
          """ If logging should not (just) be done to self.stderr, method should be overwritten. """
          
          if isinstance(exception, cls.logTypesT):
             #enforce pure ascii and enhance readability / beauty
             errMsgS = STR(exception).rstrip() + Os_linesep + Os_linesep
                
             #print out
             cls.stderr.write( errMsgS )
          
        
#init exception handler - which is not an instance (but a somehow 'global' class)
ExceptionHandler.init()         
          



#exception logger - decorator for methods (only !)
def logExceptions(method, logger=ExceptionHandler):
    """ Method wrapper for exception logging (decorator). """

    def decorator(self, *params, **paramDict):
        try:   
                return method(self, *params, **paramDict)

        except  CtrlException:
                raise                
                
        except  BaseException as error: 
                #get class-s name - in a safe manner
                clsNameS = "no class"
                if hasattr(self, "__class__"):
                   if hasattr(self.__class__, "__name__"):
                      clsNameS = self.__class__.__name__
                
                #get method name - in a safe manner
                methodNameS = "no method"
                if hasattr(method, "__name__"):
                   methodNameS = method.__name__
                   
                #get exception type name - in a safe manner
                typeNameS = "Error"
                if   isinstance(error, Aberration):
                     typeNameS = "Aberration"
                elif isinstance(error, LocalError):
                     typeNameS = "Local error"
                elif isinstance(error, FatalError):
                     typeNameS = "Fatal error"
                
                #create message - in a safe manner
                try:
                        errMsgS = "%s in %s.%s: %s" % (typeNameS, clsNameS, methodNameS, STR(error))
                except:
                        errMsgS = "automatic exception message creation failed"
                        
                #enhance readability / beauty
                errMsgS = errMsgS.rstrip() + Os_linesep + Os_linesep
                
                #log error message
                logger.log( type(error)(errMsgS) )
                
                #re-raise exception
                raise type(error)(errMsgS)
                
    #return new (decorator) method
    return decorator
    
    
    
    
#mute exception logger - decorator for methods (only !)
def muteLogging(method, logger=ExceptionHandler):
    """ Useful for decorating self test methods. """
    
    def decorator(self, *params, **paramDict):
        """ Method wrapper for muting exception logging (decorator) temporarily. """
        
        #backup exception list
        bck = logger.logTypesT
        
        #clear exception list - mute logging
        logger.logTypesT = ()
        
        #call method
        retVal = method(self, *params, **paramDict)
        
        #restore exception list - unmute logging again
        logger.logTypesT = bck
        
        #return return value of method
        return retVal
        
    #return new (decorator) method
    return decorator




### Doc Types Classes ###

#base object for ranges
class BaseRange(object):
      """ 
          Just for type checking purposes. Classes inherited from BaseRange must implement
          the __contains__ method!
          
          See descriptions of AnyRange, NumberRange, IntRange and FloatRange.
      """
 
      #constructor     
      @logExceptions
      def __init__(self, *params):
          """ """         
          
          #call parents constructor
          object.__init__(self)
          
      
      @logExceptions
      def __contains__(self, value):
          """ Ensure that method is implemented in class inherited from BaseRange! """
          
          raise FatalError("method __contains__ is not implemented in this class (%s)!" % type(self))
          
          
      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
               Can be called for automatic code testing.
               The code (just) is fine, if no exception is raised.
          """
          
          #test standard subclasses
          print ( "Testing class BaseRange..." )
          AnyRange._selftest()
          NumberRange._selftest()     #calls IntRange._selftest() and FloatRange._selftest()
          ListRange._selftest()       #calls _selftest method of IntListRange, FloatListRange, 
                                      #StrListRange, UniListRange and BaseListRange
          print ( "...class BaseRange tested successfully!" )
 
     
     

#any range checking class
class AnyRange(BaseRange):
      """
           AnyRange is a BaseRange which returns True for ALL 'in'-queries.
      
           examples:
           ---------
           
           5     in AnyRange(       )   ==> True
           "abc" in AnyRange( "[*]" )   ==> True
           float in AnyRange(       )   ==> True
           
           etc., etc..
      """    
          
          
      @logExceptions
      def __init__(self, rangeS="[*]", typee=None):
          """
               The parameters are just dummy parameters.               
               The parameter 'rangeS' must be '[*]' whereas the parameter 'typee' is just ignored -
               otherwise a 'NoAnyRange'-exception is raised, if the list does not contain exactly
               (and only) one '*'.
               
               This mechanism can be used to check the range and type part of a VarDef object (resp. line).
          """
          
          #strip outer whitespaces - if any 
          rangeeS = rangeS.strip()            #ensures that rangeS is a string too
          
          #check brackets
          if    (rangeeS[0], rangeeS[-1]) != ("[", "]"):
                raise FatalError("list brackets ([ and ]) are missing (%s)!" % STR(rangeS))
          
          #check for * - beeing the any placeholder
          if rangeeS[1:-1].strip() != "*":
             raise NoAnyRange("parameter 'rangeS' must be '[*]' (not %s)!" % STR(rangeS))
             
             
      #no exception possible - accordingly no logExceptions here
      def __contains__(self, value):
          """ Returns True. """

          return True   
          
          
      #no exception possible - accordingly no logExceptions here
      def __repr__(self):
          """ Representation of self. """
          
          return "[*]"
          
          
      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
               Can be called for automatic code testing.
               The code (just) is fine, if no exception is raised.
          """
          
          print ( "Testing class AnyRange..." )
          assert 5      in AnyRange() 
          assert 5.1    in AnyRange()
          assert "abc"  in AnyRange()
          assert object in AnyRange()
          
          assert 5      in AnyRange( "[*]" ) 
          assert 5.1    in AnyRange( "[*]" )
          assert "abc"  in AnyRange( "[*]" )
          assert object in AnyRange( "[*]" )

          #check the raising of a NoAnyRange - if no any range
          try:
                  object in AnyRange( "[]" )
                  assert False
                 
          except  NoAnyRange:
                  pass
               
          #check the raising of an exception - if no range string I
          try:
                  object in AnyRange( [] )
                  assert False
                  
          except  AssertionError:
                  #no error from 'in'-request resp. AnyRange constructor
                  raise
                  
          except  BaseException:
                  #no valid any range string given - error expected
                  pass
                     
          #check the raising of an exception - if no range string II
          try:
                  object in AnyRange( "" )
                  assert False
                  
          except  AssertionError:
                  #no error from 'in'-request resp. AnyRange constructor
                  raise
                  
          except  BaseException:
                  #no valid any range string given - error expected
                  pass  
          print ( "...class AnyRange tested successfully!" )                         
          
     
     
     
#class for number range checking  
class NumberRange(BaseRange):
      """
           Belonging instances can be used for range checking via comparator range.
           The comparator range thereby is given either as a tuple, a list or a string by the
           paramter 'rangee'.
           
           If a tuple (with two elements) is given, the belonging range excludes said two elements (bounds).
           If a list (with two elements) is given, the belonging range includes said two elements (bounds).
           If a string is given, the string must comprise the brackets which determine whether the
           two elements (bounds) are included or excluded. The bracket notation for strings
           is the same as in mathematics (at least when using square brackets).
           
           The bounds are type cast to the type given by parameter 'typee'.
           'typee' must either be int or float (type corresponding to vardef type).
           Whitespaces are allowed. 
      
      
           "int" examples:
           ---------------
               
           NumberRange( "[1..3]", int ) <==> NumberRange( [1,3],   int )
           NumberRange( "]1..3]", int )
           NumberRange( "]1..3[", int ) <==> NumberRange( (1,3),   int ) 
           NumberRange( "[1..3[", int ) 
           NumberRange( "]*..3]", int ) 
           NumberRange( "[*..3]", int ) <==> NumberRange( ["*",3], int )
           NumberRange( "[1..*]", int ) <==> NumberRange( [1,"*"], int )
           NumberRange( "[1..*[", int )
               
               
           "float" examples:
           -----------------

           same as integer examples - but with float-bounds and typee=float, for example               
           NumberRange( "]1.1..3.1[", float )
               
           
           "in" operator examples:
           -----------------------
           
           5   in NumberRange( "[1..*]",     int   )   ==> True
           5.5 in NumberRange( "[1.0..5.2]", float )   ==> False
           
           (developers note: could be extended to BoundsRange or similar later?)
      """
      
      #interface
      __slots__ = ("typee", "leftBracket", "lowerBound", "upperBound", "rightBracket")      


      @logExceptions
      def __init__(self, rangee, typee=float):
          """ """
          
          #check typee
          if typee not in [int,float]:
             raise FatalError("parameter 'typee' must either be int or float (not %s)" % typee)
          self.typee = typee          
          
          #ensure that rangee either is a tuple, a list or a string
          if    isinstance(rangee, (tuple,list)):
                #rangee is tuple or list
          
                #take rangee as bounds and type cast bounds to typee
                bounds     = [ elem if elem == "*" else typee(elem) for elem in rangee ]
                
                #check whether type casting the bounds changed them
                if bounds != list(rangee):
                   raise FatalError( "mismatch - bounds of parameter 'rangee' must be of" \
                                     " type %s (not %s)!" % (typee,STR(rangee))               )
                  
                #determine belonging brackets
                if    isinstance(rangee, tuple):
                      #tuple means: excluding the bounds - see mathematical notation e.g. "(1,3]"
                      self.leftBracket  = "]"
                      self.rightBracket = "["
                
                else:
                      #list means: including the bounds
                      self.leftBracket  = "["
                      self.rightBracket = "]"                
                
          elif  isinstance(rangee, Types_StringTypes):
                #rangee is string            
            
                #string: strip outer whitespaces - if any          
                rangeS = rangee.strip()            
                                        
                #round brackets -> square brackets
                rangeS = rangeS.replace("(","]")
                rangeS = rangeS.replace(")","[")
                
                #ensure / parse brackets
                if    not set((rangeS[0], rangeS[-1])).issubset(("[", "]")):
                      raise FatalError( "left and right bracket must either be '[', ']', " \
                                        "'(' or ')' (not %s)!" % STR(rangeS)               )                
                      
                #get bounds and brackets
                bounds            = [ elem.strip() for elem in rangeS[1:-1].split("..") ]                      
                self.leftBracket  = rangeS[0]
                self.rightBracket = rangeS[-1]
                           
          else:
                raise FatalError( "rangee either must be a tuple, a list or a string (not %s)!" % \
                                  STR(rangee)                                                     )
                                
          #ensure that there are (just) two bounds in the tuple, list or string
          if len(bounds) != 2:
             raise FatalError( "range must contain exactly two bounds -"  +             \
                               " namely start and end (but is %s)!"       % STR(rangee) )
                          
          #lower
          self.lowerBound    = bounds[0]
          if self.lowerBound != "*":
             self.lowerBound = typee(self.lowerBound)                   
          
          #upper
          self.upperBound    = bounds[-1]
          if self.upperBound != "*":
             self.upperBound = typee(self.upperBound)                


      @logExceptions
      def __contains__(self, value):
          """ Return True if value is in range of self. False otherwise. """ 
          
          #checks the type (int,float) of value against self.typee
          try:
                  if self.typee(value) != value:
                     raise LocalError("value '%s' has wrong type (not '%s')!" % (STR(value), self.typee))
          except:
                  return False

          val = float(value)
          #check lower bound
          if self.lowerBound != "*":
             if val < self.lowerBound:
                return False
             if (self.leftBracket == "]") and (val == self.lowerBound):
                return False

          #check upper bound
          if self.upperBound != "*":
             if val > self.upperBound:
                return False
             if (self.rightBracket == "[") and (val == self.upperBound):
                return False
                
          #no False up to here means True
          return True
          
          
      @logExceptions
      def __repr__(self):
          """ """
          
          return "%s%s..%s%s" % ( self.leftBracket, self.lowerBound, \
                                  self.upperBound, self.rightBracket )                 

                 
      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
               Can be called for automatic code testing.
               The code (just) is fine, if no exception is raised.
          """
          
          print ( "Testing class NumberRange..." )
          IntRange._selftest()
          FloatRange._selftest()          
          print ( "...class NumberRange tested successfully!" )
                 
                 
                 

#class for number range checking using integer bounds
class IntRange(NumberRange):
      """ 
          IntRange( (3..5) )  <==>  NumberRange("]3..5[", int)    
          IntRange( [3..5] )  <==>  NumberRange("[3..5]", int)
          IntRange("[3..5]")  <==>  NumberRange("[3..5]", int) 
          
          and so on...
      """
                 
      #interface
      __slots__ = ("typee", "leftBracket", "lowerBound", "upperBound", "rightBracket")      


      @logExceptions
      def __init__(self, rangee):
          """ """ 

          NumberRange.__init__(self, rangee, typee=int)

                    
      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
               Can be called for automatic code testing.
               The code (just) is fine, if no exception is raised.
          """
          
          print ( "Testing class IntRange..." )
          #tuple range (excluding bounds)
          assert 5 not in IntRange( ("*", 5) )
          assert 3     in IntRange( ("*", 5) )
          assert 2 not in IntRange( (3, 5)   )
          assert 3 not in IntRange( (3, 5)   ) 
          assert 4     in IntRange( (3, 5)   )
          assert 5 not in IntRange( (3, 5)   )
          assert 6 not in IntRange( (3, 5)   )
          assert 6     in IntRange( (3, "*") )    
          assert 3 not in IntRange( (3, "*") )           
          
          #list range (including bounds)
          assert 6 not in IntRange( ["*", 5] )
          assert 2     in IntRange( ["*", 5] )
          assert 2 not in IntRange( [3, 5]   )
          assert 3     in IntRange( [3, 5]   ) 
          assert 4     in IntRange( [3, 5]   )
          assert 5     in IntRange( [3, 5]   )
          assert 6 not in IntRange( [3, 5]   ) 
          assert 6     in IntRange( [3, "*"] )    
          assert 2 not in IntRange( [3, "*"] )            
          
          #string ranges (some excluding, some including bounds)
          assert 5 not in IntRange( "(*..5)" )
          assert 3     in IntRange( "(*..5)" )          
          assert 2 not in IntRange( "(3..5)" )
          assert 3 not in IntRange( "(3..5)" ) 
          assert 4     in IntRange( "(3..5)" )
          assert 5 not in IntRange( "(3..5)" )
          assert 6 not in IntRange( "(3..5)" )  
          assert 6     in IntRange( "(3..*)" )    
          assert 3 not in IntRange( "(3..*)" )           
          
          assert 6 not in IntRange( "[*..5]" )
          assert 2     in IntRange( "[*..5]" )          
          assert 2 not in IntRange( "[3..5]" )
          assert 3     in IntRange( "[3..5]" ) 
          assert 4     in IntRange( "[3..5]" )
          assert 5     in IntRange( "[3..5]" )
          assert 6 not in IntRange( "[3..5]" )  
          assert 6     in IntRange( "[3..*]" )    
          assert 2 not in IntRange( "[3..*]" )           
          
          assert 6 not in IntRange( "]*..5]" )
          assert 2     in IntRange( "]*..5]" )           
          assert 2 not in IntRange( "]3..5]" )
          assert 3 not in IntRange( "]3..5]" ) 
          assert 4     in IntRange( "]3..5]" )
          assert 5     in IntRange( "]3..5]" )
          assert 6 not in IntRange( "]3..5]" )  
          assert 6     in IntRange( "]3..*]" )    
          assert 2 not in IntRange( "]3..*]" )            
          
          assert 6 not in IntRange( "]*..5[" )
          assert 2     in IntRange( "]*..5[" )           
          assert 2 not in IntRange( "]3..5[" )
          assert 3 not in IntRange( "]3..5[" ) 
          assert 4     in IntRange( "]3..5[" )
          assert 5 not in IntRange( "]3..5[" )
          assert 6 not in IntRange( "]3..5[" )  
          assert 6     in IntRange( "]3..*[" )    
          assert 2 not in IntRange( "]3..*[" )            
          
          assert 6 not in IntRange( "[*..5[" )
          assert 2     in IntRange( "[*..5[" )           
          assert 2 not in IntRange( "[3..5[" )
          assert 3     in IntRange( "[3..5[" ) 
          assert 4     in IntRange( "[3..5[" )
          assert 5 not in IntRange( "[3..5[" )
          assert 6 not in IntRange( "[3..5[" )  
          assert 6     in IntRange( "[3..*[" )    
          assert 2 not in IntRange( "[3..*[" )       
                   
          assert 6 not in IntRange( "(*..5]" )
          assert 2     in IntRange( "(*..5]" )           
          assert 2 not in IntRange( "(3..5]" )
          assert 3 not in IntRange( "(3..5]" ) 
          assert 4     in IntRange( "(3..5]" )
          assert 5     in IntRange( "(3..5]" )
          assert 6 not in IntRange( "(3..5]" )  
          assert 6     in IntRange( "(3..*]" )    
          assert 2 not in IntRange( "(3..*]" )                       
          
          assert 6 not in IntRange( "[*..5)" )
          assert 2     in IntRange( "[*..5)" )           
          assert 2 not in IntRange( "[3..5)" )
          assert 3     in IntRange( "[3..5)" ) 
          assert 4     in IntRange( "[3..5)" )
          assert 5 not in IntRange( "[3..5)" )
          assert 6 not in IntRange( "[3..5)" )  
          assert 6     in IntRange( "[3..*)" )    
          assert 2 not in IntRange( "[3..*)" )                 
          
          
          #whitespaces
          assert 2   not in IntRange( " [ 3 ..   5   ] " )
          assert 3       in IntRange( " [ 3 ..   5   ] " )           
          
          #(wrong) typed numbers/bounds
          assert 3       in IntRange(   [ 3.0,   5.0 ]   ) 
          assert 3.0     in IntRange(   [ 3.0,   5.0 ]   )
          assert 3.1 not in IntRange(   [ 3.0,   5.0 ]   )
          
          #expected exceptions
          try:
                 assert 3     in IntRange(   [ 2.9,   5.1 ]   )  
                 assert False                 
                 
          except FatalError:
                 pass
               
          try:
                 assert 3     in IntRange( " [ 3.0 .. 5.0 ] " ) 
                 assert False                 
                 
          except  AssertionError:
                  #no error from 'in'-request resp. IntRange constructor
                  raise
                  
          except  BaseException:
                  #no valid int range string given (cannot convert bounds to int) - error expected
                  pass
          print ( "...class IntRange tested successfully" )
          
          
          
          
#class for number range checking using float bounds
class FloatRange(NumberRange):
      """ FloatRange("[3..5]")  <==>  NumberRange("[3..5]", float) """
                 
      #interface
      __slots__ = ("typee", "leftBracket", "lowerBound", "upperBound", "rightBracket")      


      @logExceptions
      def __init__(self, rangee):
          """ """                 
          
          NumberRange.__init__(self, rangee, typee=float)          
          
          
      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
               Can be called for automatic code testing.
               The code (just) is fine, if no exception is raised.
          """

          print ( "Testing class FloatRange..." )
          #tuple range (excluding bounds)
          assert 5.1 not in FloatRange( ("*", 5.1) )
          assert 3.1     in FloatRange( ("*", 5.1) )
          assert 2.1 not in FloatRange( (3.1, 5.1)   )
          assert 3.1 not in FloatRange( (3.1, 5.1)   ) 
          assert 4.1     in FloatRange( (3.1, 5.1)   )
          assert 5.1 not in FloatRange( (3.1, 5.1)   )
          assert 6.1 not in FloatRange( (3.1, 5.1)   )
          assert 6.1     in FloatRange( (3.1, "*") )    
          assert 3.1 not in FloatRange( (3.1, "*") )           
          
          #list range (including bounds)
          assert 6.1 not in FloatRange( ["*", 5.1] )
          assert 2.1     in FloatRange( ["*", 5.1] )
          assert 2.1 not in FloatRange( [3.1, 5.1]   )
          assert 3.1     in FloatRange( [3.1, 5.1]   ) 
          assert 4.1     in FloatRange( [3.1, 5.1]   )
          assert 5.1     in FloatRange( [3.1, 5.1]   )
          assert 6.1 not in FloatRange( [3.1, 5.1]   ) 
          assert 6.1     in FloatRange( [3.1, "*"] )    
          assert 2.1 not in FloatRange( [3.1, "*"] )            
          
          #string ranges (some excluding, some including bounds)
          assert 5.1 not in FloatRange( "(*..5.1)" )
          assert 3.1     in FloatRange( "(*..5.1)" )          
          assert 2.1 not in FloatRange( "(3.1..5.1)" )
          assert 3.1 not in FloatRange( "(3.1..5.1)" ) 
          assert 4.1     in FloatRange( "(3.1..5.1)" )
          assert 5.1 not in FloatRange( "(3.1..5.1)" )
          assert 6.1 not in FloatRange( "(3.1..5.1)" )  
          assert 6.1     in FloatRange( "(3.1..*)" )    
          assert 3.1 not in FloatRange( "(3.1..*)" )           
          
          assert 6.1 not in FloatRange( "[*..5.1]" )
          assert 2.1     in FloatRange( "[*..5.1]" )          
          assert 2.1 not in FloatRange( "[3.1..5.1]" )
          assert 3.1     in FloatRange( "[3.1..5.1]" ) 
          assert 4.1     in FloatRange( "[3.1..5.1]" )
          assert 5.1     in FloatRange( "[3.1..5.1]" )
          assert 6.1 not in FloatRange( "[3.1..5.1]" )  
          assert 6.1     in FloatRange( "[3.1..*]" )    
          assert 2.1 not in FloatRange( "[3.1..*]" )           
          
          assert 6.1 not in FloatRange( "]*..5.1]" )
          assert 2.1     in FloatRange( "]*..5.1]" )           
          assert 2.1 not in FloatRange( "]3.1..5.1]" )
          assert 3.1 not in FloatRange( "]3.1..5.1]" ) 
          assert 4.1     in FloatRange( "]3.1..5.1]" )
          assert 5.1     in FloatRange( "]3.1..5.1]" )
          assert 6.1 not in FloatRange( "]3.1..5.1]" )  
          assert 6.1     in FloatRange( "]3.1..*]" )    
          assert 2.1 not in FloatRange( "]3.1..*]" )            
          
          assert 6.1 not in FloatRange( "]*..5.1[" )
          assert 2.1     in FloatRange( "]*..5.1[" )           
          assert 2.1 not in FloatRange( "]3.1..5.1[" )
          assert 3.1 not in FloatRange( "]3.1..5.1[" ) 
          assert 4.1     in FloatRange( "]3.1..5.1[" )
          assert 5.1 not in FloatRange( "]3.1..5.1[" )
          assert 6.1 not in FloatRange( "]3.1..5.1[" )  
          assert 6.1     in FloatRange( "]3.1..*[" )    
          assert 2.1 not in FloatRange( "]3.1..*[" )            
          
          assert 6.1 not in FloatRange( "[*..5.1[" )
          assert 2.1     in FloatRange( "[*..5.1[" )           
          assert 2.1 not in FloatRange( "[3.1..5.1[" )
          assert 3.1     in FloatRange( "[3.1..5.1[" ) 
          assert 4.1     in FloatRange( "[3.1..5.1[" )
          assert 5.1 not in FloatRange( "[3.1..5.1[" )
          assert 6.1 not in FloatRange( "[3.1..5.1[" )  
          assert 6.1     in FloatRange( "[3.1..*[" )    
          assert 2.1 not in FloatRange( "[3.1..*[" )       
                   
          assert 6.1 not in FloatRange( "(*..5.1]" )
          assert 2.1     in FloatRange( "(*..5.1]" )           
          assert 2.1 not in FloatRange( "(3.1..5.1]" )
          assert 3.1 not in FloatRange( "(3.1..5.1]" ) 
          assert 4.1     in FloatRange( "(3.1..5.1]" )
          assert 5.1     in FloatRange( "(3.1..5.1]" )
          assert 6.1 not in FloatRange( "(3.1..5.1]" )  
          assert 6.1     in FloatRange( "(3.1..*]" )    
          assert 2.1 not in FloatRange( "(3.1..*]" )                       
          
          assert 6.1 not in FloatRange( "[*..5.1)" )
          assert 2.1     in FloatRange( "[*..5.1)" )           
          assert 2.1 not in FloatRange( "[3.1..5.1)" )
          assert 3.1     in FloatRange( "[3.1..5.1)" ) 
          assert 4.1     in FloatRange( "[3.1..5.1)" )
          assert 5.1 not in FloatRange( "[3.1..5.1)" )
          assert 6.1 not in FloatRange( "[3.1..5.1)" )  
          assert 6.1     in FloatRange( "[3.1..*)" )    
          assert 2.1 not in FloatRange( "[3.1..*)" )                 
          
          
          #whitespaces
          assert 2.1   not in FloatRange( " [ 3.1 ..   5.1   ] " )
          assert 3.1       in FloatRange( " [ 3.1 ..   5.1   ] " )           
          
          #(wrong) typed numbers/bounds
          assert 3.0     in FloatRange(   [ 3,   5 ]   ) 
          assert 3       in FloatRange(   [ 3,   5 ]   )   
          print ( "...class FloatRange tested successfully!" )
                 
                 
                 
                 
#list range checking class
class ListRange(list, BaseRange):
      """
           Belonging instances can be used for range checking via comparator list.
           
           The comparator list thereby is given either as a list (or tuple) or as a string - 
           namely as the 'rangee' parameter.
           If said 'rangee' is a string, it must evaluate to a list - 
           JUST comprising elements of the type given by the 'typee' parameter.
           
           Said 'typee' can either be bool, int, float, str, BaseRange or a type inherited from BaseRange 
           which has the __contains__ method implemented! 
           
           If an element of the comparator list is not an instance (subclass!) of the type 'typee' 
           an exception is raised. 
           
           If the comparator list (just) comprises bool, int, float or str, the __contains__ method of the parent
           list type is used in case of 'in'-queries.
           
           If on the other hand the comparator list (just) comprises elements of a type inherited from 
           BaseRange then EACH element of said comparator list is queried using 'in' - which means,
           that the __contains__ method of each element is called. So elements of types inherited 
           from BaseRange allows tree like (recursive) queries too.
           
           The 'typee' parameter (and thereby the type of the comparator list-s elements) is stored in
           the slot self.typee.
      
           examples:
           ---------
           
           rangee is a string:
           
           5     in ListRange( '[1, 3, 5]',                                        int         )   ==> True
           5.5   in ListRange( '[1.0, 3.3, 5.2]',                                  float       )   ==> False
           "abc" in ListRange( '["abc", "cde"]',                                   str         )   ==> True 
           5     in ListRange( '[ NumberRange("[1..3]"), NumberRange("[5..7]") ]', NumberRange )   ==> True
           5     in ListRange( '[ IntRange((1,3)), FloatRange([4,6]) ]',           BaseRange   )   ==> True
           
           rangee is a list           
           
           5     in ListRange( [1, 3, 5],                                          int         )   ==> True
           5.5   in ListRange( [1.0, 3.3, 5.2],                                    float       )   ==> False
           "abc" in ListRange( ["abc", "cde"],                                     str         )   ==> True 
           5     in ListRange( [ NumberRange("[1..3]"), NumberRange("[5..7]") ],   NumberRange )   ==> True
           5     in ListRange( [ IntRange((1,3)), FloatRange([4,6]) ],             BaseRange   )   ==> True           
      """
      
      #interface
      __slots__ = ("typee")     #the type of the elements of the (comparator) list 


      #creator - no exception expected here
      def __new__(self, rangee, typee=str):
          """ """
          
          return list.__new__(self)
          
          
      #constructor
      @logExceptions
      def __init__(self, rangee, typee=str):
          """ """          
          
          #check whether parameter is a list or a string
          if    isinstance(rangee, (tuple,list)):
                #parameter is already a list
                listt = rangee
            
          elif  isinstance(rangee, Types_StringTypes):
                #strip outer whitespaces - if any          
                rangeS = rangee.strip()            #also ensures that rangeS is a string
          
                #check (existence of) comparator list brackets - []
                if (rangeS[0], rangeS[-1]) != ("[", "]"):
                   raise FatalError("list brackets ([ and ]) are missing (%s)!" % STR(rangeS))
          
                #get list by evaluating the rangeS string
                listt = EVAL(rangeS)
             
          #check elements (resp. convert to) typee
          if not issubclass(typee, (bool, int, float, BaseRange) + Types_StringTypes):
             raise FatalError( "typee must either be (a subclass of) bool, int, float, str or " \
                               "BaseRange (not %s)!" % typee                                    )
          self.typee = typee
             
          #ensure that all elements are of type typee
          if    typee != BaseRange:
                #typee is not BaseRange
                try:
                        if [ typee(elem) for elem in listt ] != list(listt):
                           raise Exception("wrong type in list")
                except:
                        raise FatalError( "all elements of parameter 'rangee' (%s) must be of type 'typee' (%s)!" % \
                                          (STR(rangee), typee)                                                      )
                                     
          else:
                #typee is BaseRange
                if not all(( isinstance(elem, BaseRange) for elem in listt )):
                   raise FatalError( "all elements of parameter 'rangee' (%s) must be an instance of a subclass " \
                                     "of BaseRange!" % STR(rangee)                                                )
                
          #call list constructor
          list.__init__(self, listt)
          
          
      @logExceptions
      def __contains__(self, value):
          """ Return True if value is in self. False otherwise. """
          
          if    issubclass(self.typee, (bool, int, float) + Types_StringTypes):
                #elements are (inherited from) bools, ints, floats, strs or unis
          
                #checks the type of value against self.typee
                try:
                        if self.typee(value) != value:
                           raise LocalError( "value '%s' has wrong type (not '%s')!" % \
                                             (STR(value), self.typee)                  )
                                             
                        if issubclass(self.typee, bool) and not (self.typee(value) is value):
                           raise LocalError( "value '%s' has wrong type (not '%s')!" %      \
                                             (STR(value), self.typee)                       )
                except:
                        return False
                   
                return list.__contains__(self, self.typee(value))
                
          else:
                #elements are (inherited from) BaseRange
                return any([ (value in elem) for elem in self ])
                

      @logExceptions          
      def __str__(self):
         """ """
         
         #ensure, that also lists containing unicodes can e.g. be printed 
         #(as plain strings) without raising an exception
         return STR( [STR(elem) for elem in self] )
                
                
      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
               Can be called for automatic code testing.
               The code (just) is fine, if no exception is raised.
          """

          print ( "Testing class ListRange..." )
          BoolListRange._selftest()
          IntListRange._selftest()
          FloatListRange._selftest()
          StrListRange._selftest()
          UniListRange._selftest()
          BaseListRange._selftest()  
          print ( "...class ListRange tested successfully!" )
                
                
                
                
#bool list range checking class
class BoolListRange(ListRange):
      """
          The same as ListRange(rangee, typee=bool)
      """  

      #interface
      __slots__ = ("typee")     #the type of the elements of the (comparator) list 


      #creator - no exception expected here
      def __new__(self, rangee):
          """ """
          
          return list.__new__(self)
          
          
      #constructor
      @logExceptions
      def __init__(self, rangee):
          """ """                
          
          ListRange.__init__(self, rangee, bool)
          
          
      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
               Can be called for automatic code testing.
               The code (just) is fine, if no exception is raised.
          """

          print ( "Testing class BoolListRange..." )
          #bool tuples
          assert True not in BoolListRange( (False,) )  
          assert True     in BoolListRange( (True, False) )   

          #bool list
          assert True not in BoolListRange( [False,] )  
          assert True     in BoolListRange( [True, False] )       
          
          #bool string
          assert True not in BoolListRange( "[False]" )  
          assert True     in BoolListRange( "[True, False]" ) 

          #wrong types
          assert 0     not in BoolListRange( [True, False] )
          assert 1     not in BoolListRange( [True, False] )
          assert 2.1   not in BoolListRange( [True, False] )
          assert "abc" not in BoolListRange( [True, False] )
          
          print ( "...class BoolListRange tested successfully!" )              
      
                
#integer list range checking class
class IntListRange(ListRange):
      """ 
          The same as ListRange(rangee, typee=int)        
      """
      
      #interface
      __slots__ = ("typee")     #the type of the elements of the (comparator) list 


      #creator - no exception expected here
      def __new__(self, rangee):
          """ """
          
          return list.__new__(self)
          
          
      #constructor
      @logExceptions
      def __init__(self, rangee):
          """ """                
          
          ListRange.__init__(self, rangee, int)
          
          
      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
               Can be called for automatic code testing.
               The code (just) is fine, if no exception is raised.
          """

          print ( "Testing class IntListRange..." )
          #int tuples
          assert 2 not in IntListRange( (1,3,5) )  
          assert 3     in IntListRange( (1,3,5) )   

          #int list
          assert 2 not in IntListRange( [1,3,5] )  
          assert 3     in IntListRange( [1,3,5] )        
          
          #int string
          assert 2 not in IntListRange( "[1,3,5]" )  
          assert 3     in IntListRange( "[1,3,5]" )  

          #wrong types
          assert 2.0 not in IntListRange( (1,3,5) )  
          assert 3.0     in IntListRange( (1,3,5) ) 
          assert 3.1 not in IntListRange( (1,3,5) )
          
          assert 2.0 not in IntListRange( [1,3,5] )  
          assert 3.0     in IntListRange( [1,3,5] ) 
          assert 3.1 not in IntListRange( [1,3,5] )
          
          assert 2.0 not in IntListRange( "[1,3,5]" ) 
          assert 3.0     in IntListRange( "[1,3,5]" ) 
          assert 3.1 not in IntListRange( "[1,3,5]" ) 
          
          assert 3     in IntListRange( (1,   3.0, 5  ) )    
          assert 3     in IntListRange( (1.0, 3.0, 5.0) )  
          assert "abc" not in IntListRange( (1.0, 3.0, 5.0) ) 
          
          #expected exceptions
          try:
                 assert 3     in IntListRange( (1.0, 3.1, 5.0) )
                 assert False
                 
          except AssertionError:
                 #assertion error not expected
                 raise 
                 
          except BaseException:
                 #list has a member which cannot converted to int without a loss
                 pass
                    
          try:
                 assert 3.1   in IntListRange( (1.0, 3.1, 5.0) )
                 assert False
                 
          except AssertionError:
                 #assertion error not expected
                 raise 
                 
          except BaseException:
                 #list has a member which cannot converted to int without a loss
                 pass 
          print ( "...class IntListRange tested successfully!" )
               
          
   
          
#float list range checking class
class FloatListRange(ListRange):
      """ 
          The same as ListRange(rangee, typee=float)        
      """
      
      #interface
      __slots__ = ("typee")     #the type of the elements of the (comparator) list 


      #creator - no exception expected here
      def __new__(self, rangee):
          """ """
          
          return list.__new__(self)
          
          
      #constructor
      @logExceptions
      def __init__(self, rangee):
          """ """                
          
          ListRange.__init__(self, rangee, float)
          
          
      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
               Can be called for automatic code testing.
               The code (just) is fine, if no exception is raised.
          """

          print ( "Testing class FloatListRange..." )
          #float tuples
          assert 3.0 not in FloatListRange( (1.1, 3.1, 5.1) )  
          assert 3.1     in FloatListRange( (1.1, 3.1, 5.1) )   

          #float list
          assert 3.0 not in FloatListRange( [1.1, 3.1, 5.1] )  
          assert 3.1     in FloatListRange( [1.1, 3.1, 5.1] )        
          
          #float string
          assert 3.0 not in FloatListRange( "[1.1, 3.1, 5.1]" )  
          assert 3.1     in FloatListRange( "[1.1, 3.1, 5.1]" )  

          #wrong types
          assert 1       in FloatListRange( (1.0, 3.1, 5.1) )  
          assert 3   not in FloatListRange( (1.0, 3.1, 5.1) ) 
          
          assert 1       in FloatListRange( [1.0, 3.1, 5.1] )  
          assert 3   not in FloatListRange( [1.0, 3.1, 5.1] ) 
          
          assert 1       in FloatListRange( "[1.0, 3.1, 5.1]" )  
          assert 3   not in FloatListRange( "[1.0, 3.1, 5.1]" )
          
          assert 0 not in FloatListRange( (1.0, 3, 5.0) ) 
          assert 1     in FloatListRange( (1.0, 3, 5.0) )    
          assert 3     in FloatListRange( (1.0, 3, 5.0) )   
          assert 3     in FloatListRange( (1,   3, 5  ) ) 
          
          assert "abc" not in FloatListRange( (1.0, 3.0, 5.0) )    
          print ( "...class FloatListRange tested successfully!" )                 




#string list range checking class
class StrListRange(ListRange):
      """ 
          The same as ListRange(rangee, typee=str)        
      """
      
      #interface
      __slots__ = ("typee")     #the type of the elements of the (comparator) list 


      #creator - no exception expected here
      def __new__(self, rangee):
          """ """
          
          return list.__new__(self)
          
          
      #constructor
      @logExceptions
      def __init__(self, rangee):
          """ """                
          
          ListRange.__init__(self, rangee, str)  
          
          
      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
               Can be called for automatic code testing.
               The code (just) is fine, if no exception is raised.
          """

          print ( "Testing class StrListRange..." )
          #str tuples
          assert "aaa"  not in StrListRange( ("abc", "def", "ghi") )  
          assert "def"      in StrListRange( ("abc", "def", "ghi") )   

          #str list
          assert "aaa"  not in StrListRange( ["abc", "def", "ghi"] )  
          assert "def"      in StrListRange( ["abc", "def", "ghi"] )   
          
          #str string
          assert "aaa"  not in StrListRange( '["abc", "def", "ghi"]' )  
          assert "def"      in StrListRange( '["abc", "def", "ghi"]' ) 

          #wrong types
          assert "aaa"  not in StrListRange( (u"abc", u"def", u"ghi") )  
          assert "def"      in StrListRange( (u"abc", u"def", u"ghi") )  
          
          assert u"aaa" not in StrListRange( ("abc", "def", "ghi") )  
          assert u"def"     in StrListRange( ("abc", "def", "ghi") )          

          assert "aaa"  not in StrListRange( [u"abc", u"def", u"ghi"] )  
          assert "def"      in StrListRange( [u"abc", u"def", u"ghi"] ) 
          
          assert u"aaa" not in StrListRange( ["abc", "def", "ghi"] )  
          assert u"def"     in StrListRange( ["abc", "def", "ghi"] )           
          
          assert "aaa"  not in StrListRange( '[u"abc", u"def", u"ghi"]' )  
          assert "def"      in StrListRange( '[u"abc", u"def", u"ghi"]' ) 
          
          assert u"aaa" not in StrListRange( '["abc", "def", "ghi"]' )  
          assert u"def"     in StrListRange( '["abc", "def", "ghi"]' )           
          
          assert 1      not in StrListRange( ["abc", "def", "ghi"] )  
          assert 1.0    not in StrListRange( ["abc", "def", "ghi"] ) 
          print ( "...class StrListRange tested successfully!" )         
    
          
          
                
#unicode list range checking class
class UniListRange(ListRange):
      """ 
          The same as ListRange(rangee, typee=unicode)        
      """
      
      #interface
      __slots__ = ("typee")     #the type of the elements of the (comparator) list 


      #creator - no exception expected here
      def __new__(self, rangee):
          """ """
          
          return list.__new__(self)
          
          
      #constructor
      @logExceptions
      def __init__(self, rangee):
          """ """                
          
          ListRange.__init__(self, rangee, Types_UnicodeType)  
          
          
      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
               Can be called for automatic code testing.
               The code (just) is fine, if no exception is raised.
          """

          print ( "Testing class UniListRange..." )
          #str tuples
          assert u"aaa"  not in UniListRange( (u"abc", u"def", u"ghi") )  
          assert u"def"      in UniListRange( (u"abc", u"def", u"ghi") )   

          #str list
          assert u"aaa"  not in UniListRange( [u"abc", u"def", u"ghi"] )  
          assert u"def"      in UniListRange( [u"abc", u"def", u"ghi"] )   
          
          #str string
          assert u"aaa"  not in UniListRange( '[u"abc", u"def", u"ghi"]' )  
          assert u"def"      in UniListRange( '[u"abc", u"def", u"ghi"]' ) 

          #wrong types
          assert "aaa"  not in UniListRange( (u"abc", u"def", u"ghi") )  
          assert "def"      in UniListRange( (u"abc", u"def", u"ghi") )  
          
          assert u"aaa" not in UniListRange( ("abc", "def", "ghi") )  
          assert u"def"     in UniListRange( ("abc", "def", "ghi") )          

          assert "aaa"  not in UniListRange( [u"abc", u"def", u"ghi"] )  
          assert "def"      in UniListRange( [u"abc", u"def", u"ghi"] ) 
          
          assert u"aaa" not in UniListRange( ["abc", "def", "ghi"] )  
          assert u"def"     in UniListRange( ["abc", "def", "ghi"] )           
          
          assert "aaa"  not in UniListRange( '[u"abc", u"def", u"ghi"]' )  
          assert "def"      in UniListRange( '[u"abc", u"def", u"ghi"]' ) 
          
          assert u"aaa" not in UniListRange( '["abc", "def", "ghi"]' )  
          assert u"def"     in UniListRange( '["abc", "def", "ghi"]' )           
          
          assert 1      not in UniListRange( [u"abc", u"def", u"ghi"] )  
          assert 1.0    not in UniListRange( [u"abc", u"def", u"ghi"] ) 
          print ( "...class UniListRange tested successfully!" )          
          
          
          
          
#BaseRange list range checking class
class BaseListRange(ListRange):
      """ 
          The same as ListRange(rangee, typee=BaseRange)        
      """
      
      #interface
      __slots__ = ("typee")     #the type of the elements of the (comparator) list 


      #creator - no exception expected here
      def __new__(self, rangee):
          """ """
          
          return ListRange.__new__(self, rangee)
          
          
      #constructor
      @logExceptions
      def __init__(self, rangee):
          """ """                
          
          ListRange.__init__(self, rangee, typee=BaseRange)


      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
               Can be called for automatic code testing.
               The code (just) is fine, if no exception is raised.
          """

          ### the following is just (a poor) sample test ###
          #there are a lot combinations which are not tested here
          print ( "Testing class BaseListRange..." )
          
          #IntListRange-s
          assert 6 not in BaseListRange(( IntListRange((1, 3, 5)), IntListRange((7, 9, 11)) ))
          assert 3     in BaseListRange(( IntListRange((1, 3, 5)), IntListRange((7, 9, 11)) ))
          assert 9     in BaseListRange(( IntListRange((1, 3, 5)), IntListRange((7, 9, 11)) ))
          
          #IntRange-s
          assert 6 not in BaseListRange(( IntRange((1,5)), IntRange((7,11)) ))
          assert 3     in BaseListRange(( IntRange((1,5)), IntRange((7,11)) ))
          assert 9     in BaseListRange(( IntRange((1,5)), IntRange((7,11)) ))          
          
          #mixture of IntRange and IntListRange
          assert 1 not in BaseListRange(( IntRange((1,5)), IntListRange((7, 11)) ))
          assert 8 not in BaseListRange(( IntRange((1,5)), IntListRange((7, 11)) ))
          assert 3     in BaseListRange(( IntRange((1,5)), IntListRange((7, 11)) ))
          assert 7     in BaseListRange(( IntRange((1,5)), IntListRange((7, 11)) ))  
          
          assert 1 not in BaseListRange(( IntListRange((7, 11)), IntRange((1,5)) ))
          assert 8 not in BaseListRange(( IntListRange((7, 11)), IntRange((1,5)) ))
          assert 3     in BaseListRange(( IntListRange((7, 11)), IntRange((1,5)) ))
          assert 7     in BaseListRange(( IntListRange((7, 11)), IntRange((1,5)) ))   
          
          #FloatListRange-s
          assert 6 not in BaseListRange([ FloatListRange((1, 3, 5)), FloatListRange((7, 9, 11)) ])
          assert 3     in BaseListRange([ FloatListRange((1, 3, 5)), FloatListRange((7, 9, 11)) ])
          assert 9     in BaseListRange([ FloatListRange((1, 3, 5)), FloatListRange((7, 9, 11)) ])
          
          #FloatRange-s
          assert 6 not in BaseListRange([ FloatRange((1,5)), FloatRange((7,11)) ])
          assert 3     in BaseListRange([ FloatRange((1,5)), FloatRange((7,11)) ])
          assert 9     in BaseListRange([ FloatRange((1,5)), FloatRange((7,11)) ])          
          
          #mixture of FloatRange and FloatListRange
          assert 1 not in BaseListRange([ FloatRange((1,5)), FloatListRange((7, 11)) ])
          assert 8 not in BaseListRange([ FloatRange((1,5)), FloatListRange((7, 11)) ])
          assert 3     in BaseListRange([ FloatRange((1,5)), FloatListRange((7, 11)) ])
          assert 7     in BaseListRange([ FloatRange((1,5)), FloatListRange((7, 11)) ])  
          
          assert 1 not in BaseListRange([ FloatListRange((7, 11)), FloatRange((1,5)) ])
          assert 8 not in BaseListRange([ FloatListRange((7, 11)), FloatRange((1,5)) ])
          assert 3     in BaseListRange([ FloatListRange((7, 11)), FloatRange((1,5)) ])
          assert 7     in BaseListRange([ FloatListRange((7, 11)), FloatRange((1,5)) ])           
          
          print ( "...class BaseListRange tested successfully!" )
          
          
          

#just necessary for compatibility with python3          
def compare(x, y):
    """ """
    
    if    isPy2():
          return cmp(x,y)
    else:
          #the built in cmp function does not exist in python3 anymore
          if   x < y:
               return -1
          elif x == y:
               return 0
          elif x > y:
               return 1
          
          
          
          
#a simple bool type which does not accept non-boolean initializers
class Bool(int, BaseRange):
      """
          Behaves basically alike a bool - but raises a LocalError when compared
          with values other than True, False, true, false, Bool(True), Bool(False) or
          None.
          
          Examples:
          
          var1B = Bool(True)
          var2B = Bool(False)
      """
      
      #constructor
      @logExceptions
      def __init__(self, valueB):
          """ """        
          
          if not isinstance(valueB, (Bool, bool)):
             raise FatalError("%s is not a bool!" % valueB)
             
             
      #check for equality
      @logExceptions
      def __eq__(self, ohs):
          """ """
          
          if ohs is None:
             return False
          
          if not isinstance(ohs, (bool, Bool)):
             raise TypeMismatch( "instances of the type Bool cannot be compared with " \
                                 "instances of a type which is not Bool, bool or a "   \
                                 "subclass of Bool resp. bool (%s, %s)!" % (self, ohs) )
                              
          #use the comparison method of the built-in bool type
          return (bool(self) == ohs)   
          
          
      #check for un-equality
      @logExceptions
      def __ne__(self, ohs):
          """ """
          
          if ohs is None:
             return True
          
          if not isinstance(ohs, (bool, Bool)):
             raise TypeMismatch( "instances of the type Bool cannot be compared with " \
                                 "instances of a type which is not Bool, bool or a "   \
                                 "subclass of Bool resp. bool (%s, %s)!" % (self, ohs) )
                              
          #use the comparison method of the built-in bool type
          return (bool(self) != ohs)           
          
          
      #comparison
      @logExceptions
      def __cmp__(self, ohs):
          """ """
          
          if ohs is None:
             return -1
          
          if not isinstance(ohs, (bool, Bool)):
             raise TypeMismatch( "instances of the type Bool cannot be compared with " \
                                 "instances of a type which is not Bool, bool or a "   \
                                 "subclass of Bool resp. bool (%s, %s)!" % (self, ohs) )
                              
          #use the comparison method of the built-in bool type
          return compare( bool(self), ohs )
          
          
      #string
      @logExceptions          
      def __str__(self):
          """ """
          
          #do not show the underlying int - show bool instead
          return str(bool(self))          
          

      #representation
      @logExceptions          
      def __repr__(self):
          """ """
          
          #do not show the underlying int - show bool instead
          return str(bool(self))
          
          
      #BaseRange.__cmp__
      @logExceptions
      def __contains__(self, value):
          """
              Necessary, as Bool is inherited from BaseRange
          """
          
          equalB = False
          try:
                 if self.__cmp__(value) == 0:
                    equalB = True                
                 
          except TypeMismatch:
                 pass
                 
          return equalB
          

#true and false are more strict than True and False - in terms of comparison / range checking        
#the following 'defines' cannot be compared to values other than bool or Bool
true  = Bool(True)
false = Bool(False)
            


                 
#helper class for DocParser
class VarDef(object):
      """     
           Object standing for a vardef line 
           of a comment of a class inherited from DocTypes.
           
           example:
           --------
           
           varDef = VarDef('vardef int counter = round(1.23) in [1..3] with rw,check')
      """
      
      ### 'globals' ###
      
      #alike a global define/constant
      #if True, e.g. 'cint' is translated to 'cython.int' (cython type) 
      #otherwise to 'int' (python type)
      useCythonTypes = True
                           
      #!!!TBD!!!             
      typeTransD      = { 
                          "anything"  : dict(cy="object",               py="object"  ), \
                          "bool"      : dict(cy="bool",                 py="bool"    ), \
                          "cbool"     : dict(cy="cython.bint",          py="bool"    ), \
                          "int"       : dict(cy="int",                  py="int"     ), \
                          "cchar"     : dict(cy="cython.char",          py="int"     ), \
                          "cshort"    : dict(cy="cython.short",         py="int"     ), \
                          "cint"      : dict(cy="cython.int",           py="int"     ), \
                          "long"      : dict(cy="long",                 py="long"    ), \
                          "clong"     : dict(cy="cython.long",          py="long"    ), \
                          "clonglong" : dict(cy="cython.longlong",      py="long"    ), \
                          "float"     : dict(cy="float",                py="float"   ), \
                          "cfloat"    : dict(cy="cython.float",         py="float"   ), \
                          "cdouble"   : dict(cy="cython.double",        py="float"   ), \
                          "complex"   : dict(cy="complex",              py="complex" ), \
                          "ccomplex"  : dict(cy="cython.complex",       py="complex" ), \
                          "cdcomplex" : dict(cy="cython.doublecomplex", py="complex" ), \
                          "str"       : dict(cy="str",                  py="str"     ), \
                          "unicode"   : dict(cy="unicode",              py="unicode" ), \
                          "list"      : dict(cy="list",                 py="list"    ), \
                          "tuple"     : dict(cy="tuple",                py="tuple"   ), \
                          "dict"      : dict(cy="dict",                 py="dict"    ), \
                          "class:\w+" : dict(cy="\w+",                  py="\w+"     )  \
                        }   
      if isPy3() ==True:
         #!!!TBD!! check difference between py2 and py3 when using cython
         #and complete the following
         typeTransD["long"]    = dict(cy="int", py="int")
         typeTransD["unicode"] = dict(cy="str", py="str")
                      
      #'built-in atomic types' - !!!TBD!!!check
      rangeAtomTypesL = [bool, int, float] + list(Types_StringTypes)                 
                      
                      
      ### interface ###
      _fullLineS      = None       #full (original) line string - just for error analysis                 
                      
      #first parsing pass results
      _typeS          = None       #type    section string
      nameS           = None       #name    section string
      valueS          = None       #value   section string
      _rangeS         = None       #range   section string
      _accessS        = None       #rw      part of with section string
      _checkS         = None       #check   part of with section string
      _strictS        = None       #strict  part of with section string
      signalMethodS   = None       #signal method name, which is called in the setter (if 'signal' is given) 
      _signalTriggerS = None       #string containing a list of comma separated signal triggers ("write", "change" or/and "mismatch")
      commentS        = None       #comment section string 
      
      #second parsing pass results
      typeS           = None       #self._typeS translated to an evaluatable string using self.typeTransD
                                   #note that in case of "anything" this is "object" -
                                   #which is a special case: "object" cannot be used for casting!
      typeO           = None       #type class - evaluation of self.typeS
      valueO          = None       #value instance - evaluation of self.valueS
      rangeS          = None       #self._rangeS translated to an evaluatable string
      rangeO          = None       #evaluation of self.rangeS - an instance of BaseRange (or its subclasses) - providing the "in" operator      
      readOnlyB       = None       #boolean - whether vardef variable can be modified
      dynCheckB       = None       #boolean - whether vardef variable is dynamically checked (type,range) at all
      strictB         = None       #boolean - whether check is to be done 'strict'ly
      signalTriggersL = None       #list of events triggering the signal, possible values in said list are "write", "change" or/and "mismatch"

      ### internals ###
      _varDefLineD    = None
      _environmentD   = None

      #helper constants - first pass     
      _varTypesS      = r"(?P<_typeS>%s)" % "|".join(typeTransD.keys())
      _varNamesS      = r"(?P<nameS>[a-zA-Z_]+\w*)"
      _valuesS        = r"(?P<valueS>.+?)"
      _rangesS        = r"(?P<_rangeS>[\[\]].+?[\[\]])"
      _signalS       = r"\s*(?P<signalMethodS>[a-zA-Z_]+\w*)\s*(\s+on\s+(?P<_signalTriggerS>([a-zA-Z,]|\s)+)){0,1}"
      _withesS        = r"(?P<_accessS>(r|rw|raw))"
      _withesS       += r"\s*(?P<_checkS>[,]\s*check){0,1}(?P<_strictS>[(]\s*strict\s*[)]){0,1}"
      _withesS       += r"\s*([,]\s*signal[(]%s[)]){0,1}" % _signalS
      _commentsS      = r"(?P<commentS>([#].*?|))"
      
      _varDefLineR    = Re_compile( ( r"^\s*vardef\s+%s\s+%s\s*[=]"             +    \
                                      r"\s*%s\s+in\s+%s\s+with\s+%s\s*%s\s*$" ) %    \
                                    ( _varTypesS, _varNamesS, _valuesS, _rangesS,    \
                                      _withesS, _commentsS                        ), \
                                    Re_DOTALL                                        )
                                    
      #helper constants - second pass
      _rangeR         = Re_compile( r"^(?P<left>[\[\]])\s*"                             + \
                                    r"((?P<range>[0-9*.]+\s*[.][.]\s*[0-9*.]+)"         + \
                                    r"|(?P<list>(\s*.+?\s*[,]*)+))"                     + \
                                    r"\s*(?P<right>[\[\]])$",                             \
                                     Re_DOTALL                                            )
                                   
                                   
      @classmethod
      def getTestStr(cls, typeL, baseNameS, initialL, leftBracketL, rangeL, rightBracketL, withL):
          """
               Used to automatically create syntactic vardef testlines.
          """

          retS = u""
          index = 1
          for typeS in typeL:
              for initialS in initialL:
                  for leftBracketS in leftBracketL:
                      for rangeS in rangeL:
                          for rightBracketS in rightBracketL:
                              for withS in withL:
                                  for spaceS in ["", " ", "\t", " \t "]:
                                      #handle spaces IN range and with string
                                      spcRangeS = rangeS.replace("..", "{0}..{0}".format(spaceS))
                                      spcRangeS = spcRangeS.replace(",", "{0},{0}".format(spaceS))
                                      spcWithS  = withS.replace(",", "{0},{0}".format(spaceS))
                                      spcWithS  = spcWithS.replace("(", "({0}".format(spaceS))
                                      spcWithS  = spcWithS.replace(")", "{0}){0}".format(spaceS))
                                  
                                      retS += u"vardef {8}{0}{8} {8}{1}{2}{8}={8}{3}{8} in {8}{4}{8}{5}{8}{6}{8} with {8}{7}{8}{9}".format(typeS, baseNameS, str(index), initialS, leftBracketS, spcRangeS, rightBracketS, spcWithS, spaceS, Os_linesep)                              
                                      index += 1
                                  
          return retS
                    
                
      @classmethod
      def isCyType(cls, typeS):
          """
               Check whether typeS is a KNOWN cython.* type (see self.typeTransD).
               Returns True if so, False otherwise.
          """
          
          try:   
                 #check type
                 if    cls.typeTransD[typeS]["cy"].startswith("cython."):
                       #known cython.* type
                       return True
             
                 else:
                       #not a known cython.* type
                       return False
                        
          except KeyError:
                 #unknown key means unknown type
                 return False
                
                
      @classmethod
      def isPyType(cls, typeS):
          """
               Check whether typeS is a KNOWN atomic python type (see self.typeTransD).
               Returns True if so, False otherwise.
          """ 
          
          try:
                 #check type
                 if    cls.typeTransD[typeS]["cy"] in ( "bool", "int", "long", "float", "complex", \
                                                        "str", "unicode", "tuple", "list", "dict"  ):
                       #known atomic python type
                       return True
                
                 else:
                       #not a known atomic python type
                       return False
                
          except KeyError:
                 #unknown key means unknown type
                 return False
                 
                 
      @classmethod
      def getSyntaxErrorStr(cls, vardefLineS):
          """
               !!!TBD!!!
          """
          
          ### preparations ###
          lineS  = vardefLineS.strip()
          nameRe = Re_compile( r"^%s$" % cls._varNamesS, Re_DOTALL) 
            
          ### check '#' resp. vardef keyword ###
          if (not lineS.startswith("vardef")) and (not lineS.startswith("#")):
             return "first non-whitespace sequence must either be '#' (for a comment line)" + \
                    " or 'vardef' (for a vardef line)!"
                    
          #as syntax errors in comment lines are not (really) possible, just the vardef lines
          #are handled by the following code          
          lineS = lineS[6:]
          
          ### check whitespace between vardef keyword and type ###
          if len(lineS) == len(lineS.lstrip()):
             return "the whitespace character separating the 'vardef' keyword from " + \
                    "the type keyword is missing!"
                    
          lineS = lineS.lstrip()
          
          #split into non-whitespace sequences
          lineL = lineS.split()
          
          ### check type keyword ###
          curr  = lineL.pop(0) 
          if (curr not in cls.typeTransD.keys()) and (not curr.startswith("class:")):
             return "'%s' is not an allowed type keyword!" % curr
             
          ### check variable name ###
          curr  = lineL.pop(0)        
          
          #if "=" is not surrounded by whitespace, split it manually here
          if "=" in curr:
             index = curr.index("=")
             
             #push the "=" and eventually the value back to list
             if index < (len(curr) - 1):
                #value is also part of curr
                lineL.insert(0, curr[index+1:])
             lineL.insert(0, "=")   
             
             #(just) use the variable name now
             curr = curr[:index]
             
          #check whether variable name matches name convention
          if nameRe.match(curr) == None:
             return "'%s' does not match the naming convention of vardef variable names!" % curr
          if curr.startswith("__"):
             return "vardef variable name must not start with '__'!"
             
          ### check the "=" ###
          curr = lineL.pop(0)
          if curr != "=":
             return "the first non-whitespace character behind the variable name must be a '='!"
             
          ### value is not checked ###
             
          ### find/check "in" ###
          if "in" not in lineL:
             "no 'in' found!"
             
          index = lineL.index("in")
          lineL = lineL[(index+1):]

          ### range is not checked ###

          ### find/check "with" ###
          if "with" not in lineL:
             return "no 'with' found!"
             
          index = lineL.index("with")
          lineL = lineL[(index+1):]

          ### check with section ###
          curr  = "".join(lineL)
          
          #strip comment section off - if any
          if "#" in curr:     
             #comment section found
             index = curr.index("#")
             curr  = curr[:index]
             
          #split into with section keyphrases
          lineL = curr.split(",")
          
          #check for 'r', 'rw'
          curr = lineL.pop(0)
          if curr not in ("r","rw", "raw"):
             return "the 'with' section must either start with 'r', 'rw' or 'raw'!"
             
          #check for 'check'
          try:
                 curr = lineL.pop(0)
          
                 if curr == "check":
                    curr = lineL.pop(0)
                    
          except IndexError:
                 curr = None
                 
          #check for 'signal'
          if (curr != None):
             if (not curr.startswith("signal(")) or (not curr.endswith(")")):
                return "'signal(...)' expected but %s found (in with section)!" % curr
                
             curr = curr[7:-1]
             if nameRe.match( curr ) == None:
                return "'%s' does not match the naming convention of vardef signal method names!" % curr
             if curr.startswith("__"):
                return "signal method names must not start with '__'!"
               
          #check for keywords behing r,rw,raw and check and signal
          try:
                 curr = lineL.pop(0)
                 return "unexpected keyword '%s' in with section!" % curr
                    
          except IndexError:
                 pass
             
          #no errro found - so error must be in the sections, which are not checked in this
          #method at all (range and with sections)
          return "syntax error either in section behind '='"                            + \
                 " (initial value section), 'in' (range section) or 'with' (with section)!"               
               
                             
      @logExceptions
      def __processTypeSection(self):
          """
              Internal helper method - determining second pass properties 
              self.typeS and self.typeO
          """

          #temporary variable
          typeS = self._typeS      
               
          #ensure that self._typeS is a string (and in particular not None)
          if isinstance(typeS, Types_StringTypes):
             
             #'class:ExampleName' is treated specially: 'class:' is stripped
             if typeS.startswith("class:"):
                typeS = typeS[6:]
                
             #### determine self.typeS and self.typeO ###
             try: 
                     #check whether to use cython type
                     if    (self.useCythonTypes  == True) and \
                           (self.isCyType(typeS) == True):
                           #cython type - use known cython type string
                           self.typeS = self.typeTransD[typeS]["cy"]
                           
                     elif  typeS in self.typeTransD.keys():
                           #python type or "anything" - use known python type string
                           self.typeS = self.typeTransD[typeS]["py"]
                           
                     elif  typeS != self._typeS:
                           #"class:..."
                           self.typeS = typeS
                     
                     else:
                           #wrong type declaration
                           raise FatalError("unknown type identifier (%s)!" % self._typeS)                                                     
                           
                     #create belonging type obj                           
                     self.typeO = EVAL(self.typeS, self._environmentD)
                     
             except  FatalError:
                     raise 
                     
             except  BaseException as ee:
                     raise FatalError( "evaluating type section '%s' failed (%s)!" % (self._typeS, ee) )
                     
                     
      @logExceptions
      def __processNameSection(self):
          """
              Internal helper method - checking whether name is fine.
          """                      
          
          if self.nameS.startswith("__"):
             raise FatalError("a vardef variable name must not start with '__' (%s)!" % self.nameS)
                              
                                                                                    
      @logExceptions
      def __processValueSection(self):
          """
              Internal helper method - stripping self.valueS and 
              determining second pass property self.valueO
          """           

          try:
                 #ensure that self.valueS is a string (and in particular not None)
                 if isinstance(self.valueS, Types_StringTypes):                   
                   
                    #a value of '*' means: no initial value
                    if self.valueS != "*":
                      
                       #ensure, that the mode is not raw mode
                       if "raw" in self._accessS:
                          raise FatalError("in raw mode, assigning an initial value is not possible (use '*' instead)!")                       
                          
                       self.valueO = EVAL(self.valueS, self._environmentD)
                       
                       #type check of value is not done if type is 'anything' or "class:*"
                       if (self._typeS != "anything") and (not self._typeS.startswith("class:")):
                          #ensure, that self.valueO is cast-able to self.typeO without loss
                          cast = self.typeO(self.valueO)
                          if cast != self.valueO:
                             raise FatalError( "'%s' is not of type '%s' (casting leads to a loss of" \
                                               " information)!" % (self.valueO, self.typeO)           )
                              
                          #cast value to type
                          self.valueO = cast                           
                 
          except FatalError:
                 raise 
                 
          except BaseException:
                 raise Exception( "evaluating value section '%s' failed (must be a valid value " \
                                  "of type '%s')!" % (STR(self.valueS), self._typeS)             )
                                  
                                  
      @logExceptions
      def __processRangeSection(self, typee):
          """ 
              Internal helper method - determining second pass property self.rangeO by 
              analyzing first pass property self._rangeS.
              
              Self.rangeO after that either is a NumberRange, an AnyRange or a ListRange
              with type 'typee'.
              
              'typee' can (just) be int, float, str, unicode or subclass of BaseRange!
          """  
          
          #check typee
          if (typee not in self.rangeAtomTypesL) and not issubclass(typee, BaseRange):
             raise FatalError( "parameter 'typee' must either be bool, int, float, str " \
                               "or unicode (not %s)!" % typee                            )
          
          #ensure that self._rangeS is a string (and not e.g. None)
          if isinstance(self._rangeS, Types_StringTypes):
             match = self._rangeR.match( self._rangeS )
             if match != None:
                groupDict = match.groupdict()
                if    isinstance(groupDict["range"], Types_StringTypes):
                      ### number range detected ###
                
                      #create evaluatable range string
                      if   typee == int:
                           self.rangeS = 'IntRange("""%s""")' % self._rangeS
                      elif typee == float:
                           self.rangeS = 'FloatRange("""%s""")' % self._rangeS
                           
                      #create belonging BaseRange instance
                      self.rangeO = EVAL(self.rangeS, self._environmentD)
                                  
                elif  isinstance(groupDict["list"], Types_StringTypes):
                      ### list range detected ###                                     
                
                      try:
                             #(check for) AnyRange (just "[*]" found)
                             #try to create BaseRange instance
                             tmp         = u'AnyRange(u"""'+self._rangeS+'""")'
                             self.rangeO = EVAL(tmp, self._environmentD) 
                             
                             ### any range detected ###
                             #no exception means valid any range
                             #create evaluatable range string
                             self.rangeS = tmp
                                                   
                      except NoAnyRange:
                             ### list range detected ###
                      
                             #neither a number range, nor an any range - must be a list range
                             #create evaluatable range string
                             if   typee == bool:
                                  self.rangeS = 'BoolListRange("""%s""")' % self._rangeS
                             elif typee == int:
                                  self.rangeS = 'IntListRange("""%s""")' % self._rangeS
                             elif typee == float:
                                  self.rangeS = 'FloatListRange("""%s""")' % self._rangeS
                             elif typee == str:
                                  self.rangeS = 'StrListRange("""%s""")' % self._rangeS
                             elif typee == Types_UnicodeType:
                                  self.rangeS = u'UniListRange(u"""'+self._rangeS+'""")' 
                             elif issubclass(typee, BaseRange):
                                  self.rangeS = u'BaseListRange(u"""'+self._rangeS+'""")'
                             
                             #create belonging BaseRange instance
                             self.rangeO = EVAL(self.rangeS, self._environmentD)
                    
                else:
                      raise FatalError( "range description (%s) does neither contain a NumberRange, " \
                                        "an AnyRange or a ListRange part!" % self._rangeS             ) 
                      
             else:
                   raise FatalError("range description is invalid (%s)!" % STR(self._rangeS))                                  
          
                                              
      @logExceptions
      def __processWithSection(self):
          """
              Internal helper method - determining second pass properties 
              self.readOnly and self.dynCheck by analyzing first pass properties
              self._access and self._checkS.
          """
          
          #ensure that self._accessS is a string (and not e.g. None) 
          if isinstance(self._accessS, Types_StringTypes):               
             #check whether read only or not
             if    self._accessS  == "r":
                   self.readOnlyB = True
                         
             elif  self._accessS  == "rw":
                   self.readOnlyB = False 

             elif  self._accessS  == "raw":
                   self.readOnlyB = None                   
                     
             else:
                   raise FatalError( "unexpected accessS string ('%s')!" % \
                                     self._varDefLineD["_accessS"]         )
                                           
             #check whether assignments are (dynamically) type and range checked or not
             if    self._checkS   == None:
                   self.dynCheckB = False
                   self.strictB   = False
                         
             elif  self._checkS.split(",")[-1].strip() == "check":
                   self.dynCheckB = True
                   if self._accessS == "raw":
                      raise FatalError( "dynamical (type and range) checking is not " + \
                                        "possible in 'raw' mode!"                       )
                          
                   #check whether type checking is to be done strictly
                   if    isinstance(self._strictS, Types_StringTypes) and \
                         ("strict" in self._strictS)                      :
                         self.strictB = True
                   else:
                         self.strictB = False
                         
             else:
                   raise FatalError( "unexpected checkS string ('%s')!" % \
                                     self._varDefLineD["_checkS"]          )                                               
                      
          #check is just valid with rw, as dynamic checking is just done when writing
          if (self.readOnlyB != False) and (self.dynCheckB == True):
             raise FatalError( "dynamical (type and range) checking " +      \
                               "just is possible for write access --> 'rw'!" )
                        
          #signal is just valid with rw, as signal is triggered (just) in setter          
          if isinstance(self.signalMethodS, Types_StringTypes):
             if    (self.readOnlyB != False):
                   raise FatalError( "signals are just possible for write access ('rw')!" )
                               
             else:
                   #create list of events triggering the signal
                   if    not isinstance(self._signalTriggerS, Types_StringTypes):
                         #if no event is given, (just) the default event "write" triggers the signal
                         self.signalTriggersL = ["write"]

                   else:
                         try:
                                 #convert string to list
                                 self.signalTriggersL = [ trigger.strip() for trigger in self._signalTriggerS.split(",") ]

                                 #ensure, that list JUST contains "write", "change" or/and "mismatch"
                                 validTriggerSet = set(["write","change","mismatch"])
                                 if (set(self.signalTriggersL) | validTriggerSet) != validTriggerSet:
                                    print (set(self.signalTriggersL) | validTriggerSet), validTriggerSet
                                    raise Exception()

                         except:
                                 raise FatalError( "list of events to trigger signal '%s' is not valid (valid triggers: 'write','change','mismatch')!" % self._signalTriggerS )

                         #write already includes change - give a hint
                         if ("write" in self.signalTriggersL) and ("change" in self.signalTriggersL):
                            raise Notification("the signal trigger 'write' already comprises the signal trigger 'change' (just use 'write' here)!")
     
      
      @logExceptions
      def __init__(self, commentLineS, environmentD=None):
          """ 
               commentLineS is comment line (of a class inherited from DocTypes).
               It either must be a vardef or a pure comment line or an empty line.
               
               environmentD normally is globals().
          """
          
          #store full line string for error analysis in case of a syntax error
          self._fullLineS = commentLineS
          
          #globals
          self._environmentD = environmentD
      
          #parse commentLineS resp. check whether it matches a vardef line
          match      = self._varDefLineR.match( commentLineS )
          if match  != None:
                #is vardef line - get belonging line dictionary
                self._varDefLineD = match.groupdict()
                
                #copy values belonging to keys to attributes with same name - if any
                for key in self._varDefLineD.keys():
                    if hasattr(self, key):
                       setattr(self, key, self._varDefLineD[key])
                       
          else:
                #line is no vardef line - but it might be an empty one or a comment
                self._varDefLineD = None
                
                #check for empty line resp. comment
                comment = commentLineS.strip()
                if    (len(comment) == 0) or comment.startswith("#"):
                      #is an empty line or a comment
                      self.commentS = comment
                      
                else:
                      #comment line structure is invalid
                      raise FatalError( "line is neither a proper vardef nor"  + \
                                        " an empty nor a comment line!"          )
                                    
          #if there is no valid vardef line (but e.g. a valid pure-comment line instead) 
          #there also need not be a valid type section, value section, ...
          if self._varDefLineD != None:
                          
             #evaluate the type section
             self.__processTypeSection() 
             
             #evaluate the name section
             self.__processNameSection()

             #evaluate the value section
             self.__processValueSection()   
   
             #evaluate the values belonging to keys 'access' and 'check'
             self.__processWithSection()
          
             ### evaluate the range section ###          
             #get known python type belonging to self._typeS - if any
             if    isinstance(self._typeS, Types_StringTypes) and \
                   self._typeS in self.typeTransD.keys()          :
                   pyType = EVAL(self.typeTransD[self._typeS]["py"], self._environmentD)
             else:
                   pyType = None

             #check type and call self.__processRangeSection accordingly
             if    pyType in self.rangeAtomTypesL:
                   #cython or "atomic" python type
                   self.__processRangeSection(typee=pyType)                   
                   
             elif  (type(self.typeO) == type) and issubclass(self.typeO, BaseRange):
                   #type inherited from BaseRange
                   self.__processRangeSection(typee=self.typeO)
                   
             else:
                   #any range or error
                   try:
                           #check whether self._rangeS is an any range (no range checking at all)
                           AnyRange(self._rangeS)
                           
                   except:
                           if (self.dynCheckB == True):
                              raise FatalError( "attributes of type '%s' cannot be range checked" \
                                                " yet (use '[*]' instead)!" % self._typeS         )                                                  
             
             #just do range check for initial value, if "check" has been chosen
             if self.dynCheckB == True:                                                          
                #check whether (initial/default) value is in range - if any given; 
                #* is always in range (initial None)
                if (self.valueS != "*") and (self.rangeO != None) and \
                   (self.valueO not in self.rangeO)                   :
                   raise FatalError( "initial value '%s' is not in range '%s'!" \
                                     % (self.valueO, self.rangeO)               )             

                              
      @logExceptions
      def __str__(self):
          """ """
          
          #check whether line is a proper vardef line
          if self._varDefLineD == None:
             #no proper vardef line
             if    isinstance(self.commentS, Types_StringTypes):
                   #but an empty line resp. comment line
                   return self.commentS
             else:
                   return "!!! line is neither a proper vardef nor an empty nor a comment line !!!"
          
          #line is a proper vardef line, return it-s representational string
          withS = "rw"
          if self.readOnlyB == True:
             withS = "r"
          if self.dynCheckB == True:
             withS = (withS + ",").ljust(3) + " check"
             
          return "%s %s = %s in %s with %s %s" %                                      \
                 ( str(self._typeS).ljust(10), str(self.nameS).ljust(15),             \
                   STR(self.valueS).ljust(10), STR(self._rangeS).ljust(15),           \
                   str(withS).ljust(15), self.commentS                                )
                   
                   
      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
               Can be called for automatic code testing.
               The code (just) is fine, if no exception is raised.
          """
          
          print ( "Testing class VarDef..." )

          ### test type ###
          #test all known alphanumeric type strings
          for typee in self.typeTransD.keys():
              if   typee.startswith("c") and (typee[:5] not in ["comple", "class:"]) and \
                   (('cython' not in globals()) or (type(cython) != Types_ModuleType))   :
                   #typee is a cython type but cython module has not been loaded (successfully)
                   pass
               
              elif typee.isalpha() == True:            #excludes 'class:...'
                   print ( "testing %s" % typee )
                 
                   vardef = VarDef( "vardef %s var1 = * in [*] with rw,check" % typee )                  
                   assert vardef._typeS == typee
                 
          #test an example for 'class:...' type strings
          vardef = VarDef( "vardef class:BaseRange var1 = * in [*] with rw,check" )                  
          assert vardef._typeS == "class:BaseRange"
           
          #test an example with an unknown type
          try:
                 vardef = VarDef( "vardef unknown var1 = * in [*] with rw,check" )                  
                 assert False
                     
          except FatalError:
                 pass
               
          #unknown class:type
          try:
                 vardef = VarDef( "vardef class:Unknown var1 = * in [*] with rw,check" )                  
                 assert False
                     
          except FatalError:
                 pass
               
          ### test (initial) value ### 
          #test anything
          for val in (False, 1, 1.1, complex(1,2), "'abc'", u"u'uabc'", (1,2,3), [1,2,3], dict()):
              vardef = VarDef( "vardef anything var1 = %s in [*] with rw,check" % str(val) )              
              #test value
              if    not isinstance(val, Types_StringTypes):
                    assert vardef.valueO == val
              else:
                    assert vardef.valueO == val.strip("u").strip("'")
                             
          #test bool
          for typeS in ["bool", "cbool"]:
              vardef = VarDef( "vardef %s var1 = True in [*] with rw,check" % typeS )
              assert isinstance( vardef.typeO(vardef.valueO), bool )
              assert vardef.valueO == True
               
          #test integers
          for typeS in (key for key in self.typeTransD.keys() if self.typeTransD[key]["py"] == "int"):
              vardef = VarDef( "vardef %s var1 = 3 in [1..5] with rw,check" % typeS )
              assert isinstance( vardef.typeO(vardef.valueO), (int,long) )
              assert vardef.valueO == 3
              
          #test floats
          for typeS in (key for key in self.typeTransD.keys() if self.typeTransD[key]["py"] == "float"):
              vardef = VarDef( "vardef %s var1 = 1.23 in [1.1..5.1] with rw,check" % typeS )
              assert isinstance( vardef.typeO(vardef.valueO), float )
              assert vardef.valueO == 1.23
              
          #test complex
          for typeS in (key for key in self.typeTransD.keys() if self.typeTransD[key]["py"] == "complex"):
              vardef = VarDef( "vardef %s var1 = complex(1.1,1.2) in [*] with rw,check" % typeS )
              assert isinstance( vardef.typeO(vardef.valueO), complex )
              assert vardef.valueO == complex(1.1,1.2)
              
          #test str
          vardef = VarDef( "vardef str var1 = 'abc' in ['abc', 'cde'] with rw,check" )
          assert isinstance( vardef.typeO(vardef.valueO), str )
          assert vardef.valueO == "abc"          
          
          #test unicode
          vardef = VarDef( "vardef unicode var1 = u'\u1234 abc' in [u'\u1234 abc', u'cde'] with rw,check" )   
          assert isinstance( vardef.typeO(vardef.valueO), Types_UnicodeType )
          assert vardef.valueO == u"\u1234 abc"  
          
          #test list
          vardef = VarDef( "vardef list var1 = [1,3,5] in [*] with rw,check" )  
          assert isinstance( vardef.typeO(vardef.valueO), list )
          assert vardef.valueO == [1,3,5]        
          
          #test tuple
          vardef = VarDef( "vardef tuple var1 = (1,3,5) in [*] with rw,check" ) 
          assert isinstance( vardef.typeO(vardef.valueO), tuple )
          assert vardef.valueO == (1,3,5)          
          
          #test dict
          vardef = VarDef( "vardef dict var1 = dict(a=1, c=3) in [*] with rw,check" )
          assert isinstance( vardef.typeO(vardef.valueO), dict )
          assert vardef.valueO == dict(a=1, c=3)           

          #test mismatch: type and initial-value-type
          tuplee = ( ("bool",False), ("int",1), ("float", 1.1), ("complex", complex(1,2)), \
                     ("str", "'abc'"), ("tuple", (1,2,3)), ("list", [1,2,3]),              \
                     ("dict", dict())                                                      )
          if isPy2() == True: 
             tuplee += (("unicode", u"u'uabc'"),)
             
          for tuple1 in tuplee:
              for tuple2 in tuplee:
                  if tuple1 != tuple2:
                     try:
                            vardef = VarDef( "vardef {0} var1 = {1} in [*] with rw,check".format( \
                                             tuple1[0], str(tuple2[1])                          ) )                                   
                                
                     except BaseException as fe:
                            if (not str(fe).startswith( "Fatal error in VarDef.__init__: Fatal "      \
                                                        "error in VarDef.__processValueSection:")) and \
                               (not str(fe).startswith( "Error in VarDef.__init__: Error "            \
                                                        "in VarDef.__processValueSection:"))           :                                                       
                               raise
                     
          print ( "...class VarDef tested successfully!" )
                   
                   
                   
                   
#type for self.docStruct of classes inheriting from DocType
class DocStructTuples(object):
      """ 
           Struct for containing the parts of __doc__ as (list of strings) attributes.
      """
      
      
      #interface
      __slots__ = ("interface", "description", "internals", "examples")
 
       
      #constructor
      @logExceptions
      def __init__(self, docDict=None):
          """ 
              Copies content of docDict to attributes self.interface, ..., self.examples
              if docDict != None.
          """
          
          #init in any case
          self.interface   = None
          self.description = None
          self.internals   = None
          self.examples    = None
          
          #init contents of docDict - if any
          if isinstance(docDict, dict):
             for key in ("interface", "description", "internals", "examples"):
                 if key in docDict.keys():
                    setattr(self, key, docDict[key])
                    
                    
      #helper method for __str__
      @logExceptions
      def _linesToStr(self, linesL):
          """ Returns a pretty str of linesL. """
          
          text  = "" + Os_linesep
          for line in linesL:
              text += line + Os_linesep
          
          return text
                    
                    
      #conversion to str
      @logExceptions
      def __str__(self):
          """
               Returns a string pretty printing the contents.
          """
          
          retS  = "interface   : %s%s" % (self._linesToStr(self.interface),   Os_linesep)
          retS += "description : %s%s" % (self._linesToStr(self.description), Os_linesep)
          retS += "internals   : %s%s" % (self._linesToStr(self.internals),   Os_linesep)
          retS += "examples    : %s%s" % (self._linesToStr(self.examples),    Os_linesep)
           
          return retS  
          
          
          
          
#string with representation method
class ReprUni(Types_UnicodeType):
      """ 
          A string which provides a nicer output in some shells - due to __repr__ method. 
      """
      
      #necessary due to inheritance from built-in class
      def __new__(self, text):
          """ """
          
          #if empty, return str initialised by emptyS
          return Types_UnicodeType.__new__(self, text)
          
          
      #representation
      def __repr__(self):
          """ """
          
          return self
          
          
          
          
#structure like class with setup by exec and representation abilities
class SourcesStructStrings(object):
      """
          Class used to store the 'sources' strings.
      """


      #for executable setup string 
      def toExecStr(self):
          """
               Returns a string which, if executed, creates this
               SourcesStructStrings object named 'sources'.
          """

          #create (temporary) target object
          execS = u"sources = SourcesStructStrings()%s" % Os_linesep

          #add attributes and belonging values
          for attrNameS in dir(self):
              if (not attrNameS.startswith("__")) and \
                 (attrNameS != "toExecStr"      )     :
                 execS += u"sources.%s = ReprUni(u'''%s''')%s" %                                           \
           ( attrNameS,                                                                                    \
             Types_UnicodeType(getattr(self, attrNameS)).replace("'''", '***triple***single***quotes***'), \
             Os_linesep                                                                                    )
                          
          #return string to be excecuted
          return ReprUni(execS)  
          
          
      #representation
      def __repr__(self):
          """ """
          
          retS = ""
          
          #add attributes and start of belonging values
          for attrNameS in dir(self):
              if (not attrNameS.startswith("__")) and \
                 (attrNameS != "toExecStr"      )     :
                 retS += "%s%s" % ( attrNameS, Os_linesep )
                 
          #return representation string
          return ReprUni(retS)




#just for 'doc' attributes of classes inherited from DocTypes
class DocStructStrings(object):
      """ 
           Struct for containing the parts of __doc__ as (string) attributes.
           Used to extend classes by .doc and its attributes:
           *.doc.interface
           *.doc.description
           *.doc.internals
           *.doc.examples
           providing a nice output in shells.
      """
      
      
      #interface
      __slots__ = ("interface", "description", "internals", "examples")               
      

      #constructor
      def __init__(self):
          """ """

          self.interface   = ReprUni("")
          self.description = ReprUni("")
          self.internals   = ReprUni("")
          self.examples    = ReprUni("")  
          
          
      #representation
      def __repr__(self):
          """ """
          
          retS  = \
"""----------
Interface:
----------

"""
          retS += self.interface
          
          retS += \
"""
------------
Description:
------------

"""   
          retS += self.description
          
          retS += \
"""
----------
Internals:
----------

"""           

          retS += self.internals
          
          retS += \
"""
---------
Examples:
---------

"""        

          return retS    
          
          
         

#helper class used to put DocTypes-types in place 
class DocParser(object):
      """
          Provides (infrastructure and) CLASSMETHODS for parsing the __doc__ of an(other)
          class and to extract type infos from it for adding corresponding
          (typed) attributes to said class.
          
          The latter is done via executing a string provided by self.docTypesExecStr().
          
          ---------
          Examples:
          ---------
          
          class Example(object):
                ...
                
                #must be executed in classes 'header'
                exec( DocParser.docTypesExecStr("Example", __doc__) )
                
                def __init__(self):
                
                ...
      """  
      
      #if True, the auto-generated code is stored under the attribute 'sources'
      _storeSourcesB = True
      #if True, the auto-generated code is printed before executed (for debugging)
      _printSourcesB = False

      ### just creates __sectionsL and __sectionReL automatically ###
      __sectionsL     = ["interface", "description", "internals", "examples"]
      sectionsT       = ( "[%s%s]%s" % (elem[0].upper(), elem[0], elem[1:]) for elem in __sectionsL )
      sectionsT       = tuple(sectionsT)
      sectionS        = "(%s)" % ("|".join(tuple(sectionsT)))
      separatorAbcS   = "(?P<frame>[-#])[-#]{2,}[ \t\r\n]+Abc\s*[:][ \t\r\n]+[-#]{2,}(?P=frame)"
      anySeparatorS   = separatorAbcS.replace("Abc", sectionS).replace("frame", "emarf")     #renaming to 'emarf' is necessary as separatorAbcS and anySeparatorS both are used at the same time in a later regex
      
      __sectionReL    = []
      for section in tuple(sectionsT):
          sectionName = section[2] + section[4:]

          sectionSepS = separatorAbcS.replace("Abc", section)
          sectionRe   = Re_compile( r".*?%s(?P<content>.*?)(%s|$)"        % \
                                    (sectionSepS, anySeparatorS), Re_DOTALL )
                           
          #here one can see, what __sectionReL contains !!!
          __sectionReL.append( (sectionName, sectionRe) )
          
      _emptyHeaderRe  = Re_compile(r"[ \t\v\f\r\n]*[\r\n]+")
          
      #delete all temporary variables
      del sectionsT, sectionS, separatorAbcS, anySeparatorS
      del section, sectionName, sectionSepS, sectionRe 
      ### creation of __sectionsL and __sectionReL finished ###
      
      ### internal helpers ###
      _setterFctHeadS = \
u"""@logExceptions
def _set_%s(self, value):
    
"""
  
      _roExceptionS   = \
u"""    raise ReadOnly("access error in _set_{0}: '%s.{0} = %s' is not allowed as '%s.{0}' is read only!" % (self.__class__.__name__, STR(value), self.__class__.__name__))
    
"""

      _tryS           = \
u"""  try:

"""

      _strictCheckS   = \
u"""    if not isinstance(val, {0}):
       raise TypeMismatch("type mismatch in _set_{1}: '%s.{1} = %s' is not allowed as '%s.{1}' is of type '{0}'!%s" % (self.__class__.__name__, STR(value), self.__class__.__name__, Os_linesep))

"""

      _typeCheckS     = \
u"""    try:
           val = {0}(value)
    except BaseException:
           raise TypeMismatch("type mismatch in _set_{1}: '%s.{1} = %s' is not allowed as '%s.{1}' is of type '{0}'!%s" % (self.__class__.__name__, STR(value), self.__class__.__name__, Os_linesep))

    if val != value:
       raise TypeMismatch("type mismatch in _set_{1}: '%s.{1} = %s' is not allowed as '%s.{1}' is of type '{0}'!%s" % (self.__class__.__name__, STR(value), self.__class__.__name__, Os_linesep))
       
"""

      _rangeCheckS    = \
u"""    if val not in self._shadow_{1}_range:
       raise RangeMismatch("range mismatch in _set_{1}: '%s.{1} = %s' is not allowed as '%s.{1}' has range '{0}'!%s" % (self.__class__.__name__, STR(value), self.__class__.__name__, Os_linesep))
       
"""

      _checkChangeS   =\
u"""    valueChangedB    = False
    if val != self._shadow_{0}:
       valueChangedB = True

"""

      _setValueS      = \
u"""    self._shadow_{0} = val
    
"""

      _writeSignalS    = \
u"""    self.{0}("{1}", val, None)
    
"""

      _changeSignalS    = \
u"""    if valueChangedB == True:
       self.{0}("{1}", val, None)
    
"""

      _classCheckS    = \
u"""    if not isinstance(val,{0}):
       raise TypeMismatch("type mismatch in _set_{1}: '%s.{1} = %s' is not allowed as '%s.{1}' is of type '{0}'!" % (self.__class__.__name__, STR(value), self.__class__.__name__))
          
"""

      _exceptS        = \
u"""  except (TypeMismatch, RangeMismatch) as ee:
    self.{0}("{1}", val, ee)
    return None

"""

      _docS = \
u"""doc = DocStructStrings()
doc.interface   = ReprUni('''{interface}''')
doc.description = ReprUni('''{description}''')
doc.internals   = ReprUni('''{internals}''')
doc.examples    = ReprUni('''{examples}''')

"""

      _propertiesS = \
u"""properties = {0}
      
"""

      _initialsS = \
u"""
def {0}__init__(self):   
{1}
    for attrNameS in dir(self.sources):
        if (not attrNameS.startswith("__")) and (attrNameS != "toExecStr"):      
           setattr( self.sources, attrNameS, ReprUni( getattr( self.sources, attrNameS ).replace("***triple***single***quotes***", "'''") ) )
    
"""

        

      #helper method for __splitDoc     
      @classmethod
      def __stripEmptyFrame(cls, textS):
          """ 
              Returns textS stripped of its leading empty lines and trailing whitespaces. 
              Does not destroy the indent of first non-empty line.
          """
          
          #strip trailing whitespaces
          strippedS = textS.rstrip()
          
          #strip leading empty lines
          match = cls._emptyHeaderRe.match(strippedS)
          if (match != None) and (match.span()[0] == 0):
             strippedS = strippedS[match.span()[1]:]
                       
          #return result
          return strippedS
                            
          
      #helper method parsing __doc__ string
      @classmethod
      def __splitDoc(cls, classesDoc, sectionType=tuple):
          """ Returns a dictionary with keys from cls.__sectionsL (e.g. 'interface') 
              and values: belonging regular expression (e.g. matching '--interface:-- content --description:--')
          """

          sectionDict = {'interface':'', 'description':'', 'internals':'', 'examples':''}
          for (sectionName, sectionRe) in cls.__sectionReL:
              match = sectionRe.match(classesDoc)
              if match != None:
                 lines = match.groupdict()["content"]
                 if    sectionType == tuple:
                       lines = lines.strip().splitlines()
                       sectionDict[sectionName] = tuple(( line.strip() for line in lines ))
                       
                 elif  sectionType == str:
                       #enforce an ascii representation
                       lines = STR(lines)
                       
                       #strip empty frame without destroying the indent of first non-empty line
                       lines = cls.__stripEmptyFrame(lines) + Os_linesep
                                                       
                       #assign result
                       sectionDict[sectionName] = lines
                       
                 else:
                       raise FatalError("unexpected branch!")                 
          
          return sectionDict
          
          
      @classmethod
      def _getTypeCastS(cls, varDef):
          """ 
               Helper method for getInitStr and getSetterStr
          """
          
          #get default str for typecast (no typecast at all)
          typeS = ""
                
          #just explicitly typecast value if type "check" is chosen 
          #and type is not "anything" or "class:*"
          #Note that unknown types may not have the typecast functionality at all
          if    (varDef.dynCheckB == True) and isinstance(varDef.typeS, Types_StringTypes):
                if   varDef._typeS.startswith("class:"):
                     pass
                         
                elif (varDef.typeO != object):
                     #known type - key of VarDef.typeTransD, but "anything" or "class:*"
                     typeS = varDef.typeS
                     
          return typeS
          
          
      @classmethod
      def getInitLineStr(cls, preS, varDef):
          """
              Intermediate helper method.
          """
          
          if    ( (varDef.valueO    != None)   or \
                  (varDef.valueS    == "None")    ) and \
                ( varDef.readOnlyB  != None       )     : #varDef.readOnlyB == None <=> 'raw'
                #get str for typecast
                typeS = cls._getTypeCastS(varDef)

                #create type comment hint - if type is an atomic python type
                commentS = ""
                if varDef.isPyType( typeS ) == True:
                   commentS = "# type: %s" % typeS
                      
                #set shadow variable to initial value
                return """%s%s = %s(%s) %s%s""" % (preS, varDef.nameS, typeS, varDef.valueS, commentS, Os_linesep)
          else:
                #initial value None - independently from the variable type
                return """%s%s = None%s""" % (preS, varDef.nameS, Os_linesep)
                
                
      @classmethod
      def getInitStr(cls, classNameS, initLinesS):
          """
              Returns the string (to be executed) which sets the shadow variables
              of the property belonging to varDef to the initial value - if any.
          """
          
          return cls._initialsS.format(classNameS, initLinesS)                
                
                
      @classmethod
      def getGetterStr(cls, varDef):
          """
              Returns the string (to be executed) which defines the getter method
              of the property belonging to varDef - if any.
          """
          if    (varDef.nameS != None):
                #define getter
                return "@logExceptions{1}def _get_{0}(self):{1}" \
                       "    return self._shadow_{0}{1}{1}".format(varDef.nameS, Os_linesep) 
          else:
                #no (valid) property at all - no getter
                return ""


      @classmethod
      def getSetterStr(cls, varDef):
          """
              Returns the string (to be executed) which defines the setter method
              of the property belonging to varDef - if any.
          """
          
          if    (varDef.nameS != None): 
                ### define setter (str) ###
          
                #method base
                setterS = cls._setterFctHeadS % varDef.nameS

                #if read only: just return exception raising string
                if varDef.readOnlyB == True:
                   setterS += cls._roExceptionS.format( varDef.nameS )
                   return setterS

                #add a try...except frame if signal trigger "mismatch" has been given
                if isinstance(varDef.signalTriggersL, list) and ("mismatch" in varDef.signalTriggersL):
                   #catching mismatch exceptions just does make sense if mismatch exceptions can happen at all
                   if    (varDef.readOnlyB == False) and (varDef.dynCheckB == True):
                         setterS += cls._tryS
                   else:
                         raise FatalError("the signal trigger 'mismatch' is just possible when 'rw' as well as 'check' is given!")

                #belongs to the method base - had to be delayed a little due to the unindentation of the previous try...except clause belonging to "mismatch"
                setterS += "    val = value{0}{0}".format(Os_linesep)

                #type check
                typeS = cls._getTypeCastS(varDef)
                if    len(typeS) > 0:
                      #just type resp. range check known, castable types of VarDef.typeTransD.keys()
                      #which means: neither "anything" nor "class:*"
                      
                      #type cast and check
                      if    varDef.strictB == True:
                            setterS += cls._strictCheckS.format( typeS, varDef.nameS )
                      else:
                            setterS += cls._typeCheckS.format( typeS, varDef.nameS )

                      #range check
                      if (not isinstance(varDef.rangeO, AnyRange)) and \
                         (varDef.rangeO != None)                       :
                         #note that 'AnyRange' means 'no range check'
                         setterS += cls._rangeCheckS.format( STR(varDef.rangeO), varDef.nameS )
                         
                elif  varDef._typeS.startswith("class:"):
                      if    varDef.typeS == "Bool":
                            #Bool is made a special case ("extended built-in type")
                            setterS += cls._classCheckS.format("(Bool, bool)", varDef.nameS)                 
                      
                      else:
                            #check 'type'
                            setterS += cls._classCheckS.format(varDef.typeS, varDef.nameS)
                            
                      #check 'range'
                      if isinstance(varDef.rangeO, BaseListRange):
                         #just do a range check, if all list elements are of type BaseRange
                         #and therefore has the __contains__ method implemented
                         setterS += cls._rangeCheckS.format( STR(varDef.rangeO), varDef.nameS )

                #check whether value has been changed - if the on "change" signal trigger has been chosen
                if isinstance(varDef.signalTriggersL, list) and ("change" in varDef.signalTriggersL):
                   setterS += cls._checkChangeS.format( varDef.nameS )
                
                #set value
                setterS += cls._setValueS.format( varDef.nameS )
                
                #add signal method call if signal given
                if isinstance(varDef.signalMethodS, Types_StringTypes):
                   if varDef.signalMethodS.startswith("__"):
                      FatalError( "a vardef signal method name must not start with '__' (%s)!" \
                                  % varDef.signalMethodS                                       )

                   #check whether "write" OR "change" signal trigger has been chosen
                   if isinstance(varDef.signalTriggersL, list):
                      if   "write" in varDef.signalTriggersL:
                           setterS += cls._writeSignalS.format( varDef.signalMethodS, varDef.nameS )

                      elif "change" in varDef.signalTriggersL:
                           setterS += cls._changeSignalS.format( varDef.signalMethodS, varDef.nameS )                       
                
                #ensure that the automatic return of the last expression is suppressed
                setterS += "    return None{0}{0}".format(Os_linesep)

                #add a try...except frame if signal trigger "mismatch" has been given
                if isinstance(varDef.signalTriggersL, list) and ("mismatch" in varDef.signalTriggersL):
                   #catching mismatch exceptions just does make sense if mismatch exceptions can happen at all
                   if    (varDef.readOnlyB == False) and (varDef.dynCheckB == True):
                         setterS += cls._exceptS.format( varDef.signalMethodS, varDef.nameS )               

                #return str to be executed to define the setter method    
                return setterS

          else:
                #no (valid) property at all - no setter
                return ""


      @classmethod
      def getPropertyStr(cls, varDef):
          """
              Returns the string (to be executed) which sets the property
              belonging to varDef - if any.
          """
          
          if    (varDef.nameS != None): 
                #set property
                return """{0} = property(_get_{0}, _set_{0}, doc='''{1}'''){2}""".format(                     \
                                varDef.nameS, " ".join( [ elem for elem in STR(varDef).split(" ")             \
                                                          if len(elem) > 0]                     ), Os_linesep )
          else:
                #no (valid) property at all
                return ""


      @classmethod
      def getPropertiesStr(cls, propertiesL):
          """ 
              Returns the string (to be executed) which sets the attribute
              'properties'.
          """
              
          return cls._propertiesS.format( str(set(propertiesL)) )
          
          
      #method parsing docStruct and transforming cls to a real DocTypes
      @classmethod
      @muteLogging
      def docTypesExecStr(cls, classNameS, docS, envD=None):
          """ 
               As this method is called before __new__ and __init__ during the creation
               of another class, this method must be a classmethod (inheriting did not
               happen then).
               
               For further details see the description of DocTypesApi.execStr.
          """
          
          #get doc struct of doc
          try:
                 docStruct = DocStructTuples( cls.__splitDoc(docS) )
                 
                 if not isinstance(docStruct.interface, tuple):
                    raise FatalError("section 'interface' does not exist or does not comply with the DocTypes format (%s)!" % docStruct.interface)
                 
                 if not isinstance(docStruct.internals, tuple):
                    raise FatalError("section 'internals' does not exist or does not comply with the DocTypes format (%s)!" % docStruct.internals)
                 
          except BaseException as ee:
                 Sys_stderr.write( STR(docS) + Os_linesep )
                 raise DocTypesError("__doc__ string format does not comply with the DocTypes format (%s)!%s" % (STR(ee), Os_linesep))
                 
          
          ### create return string to be executed ###
          #create self.doc attribute
          docDict            = cls.__splitDoc(docS, sectionType=str)
          setupS             = cls._docS.format( **docDict )
          
          #find and parse all lines in __doc__ (resp. docStruct) containing vardef-s
          propertiesL   = []          #list of all vardef variable names
          initialsS     = ""          #executable string defining the self.*__init__() method 
          sourcesStruct = SourcesStructStrings() #to contain all parts of the exec-string 
          for lineS in (docStruct.interface + docStruct.internals):       
              try:                     
                     #parse vardef line
                     varDef  = VarDef(lineS, envD)                     
                     oneDefS = u""
                     if (varDef.nameS != None):
                        #initial value - part 1 (for raw mode only - otherwise overwritten below)
                        #in raw mode there is no shadow variable (==> "")
                        oneDefS = u"{0}{1}".format( cls.getInitLineStr("", varDef), Os_linesep )                       
                              
                        if    (varDef.readOnlyB != None):
                              #no empty resp. comment line AND no 'raw' mode line
                              #note that varDef.readOnlyB == None means varDef._accessS == "raw" (or any unexpected error in the code...)
                        
                              #initial value - part 2
                              #overwrite oneDefS and hereby init (just) the shadow variable ("_shadow_") 
                              oneDefS    = u"{0}{1}".format( cls.getInitLineStr("_shadow_", varDef), Os_linesep )
                              #add the belonging part in self.*__init__()
                              if (varDef.valueS != "*") and (varDef.readOnlyB != True):
                                 #calling the setter with None might lead to an exception
                                 initialsS += u"    %s" % cls.getInitLineStr("self.", varDef)

                              #range for range checking              
                              if (varDef.dynCheckB == True)                and \
                                 (varDef.typeO     != object)              and \
                                 (not isinstance(varDef.rangeO, AnyRange)) and \
                                 (varDef.rangeS != None)                       :
                                 oneDefS += u"_shadow_%s_range = %s%s%s" % ( varDef.nameS, varDef.rangeS, \
                                                                            Os_linesep, Os_linesep       )
                               
                              #getter method
                              oneDefS += cls.getGetterStr(varDef)
              
                              #setter method
                              oneDefS += cls.getSetterStr(varDef) 
                 
                              #property
                              oneDefS += cls.getPropertyStr(varDef)
                              oneDefS += Os_linesep
              
                        #add this def to setup str
                        if len(oneDefS) > 0:
                           setupS += oneDefS
                        
                        #add name of current attribute to properties list
                        propertiesL.append(str(varDef.nameS))
              
                        if cls._storeSourcesB == True:
                           setattr(sourcesStruct, str(varDef.nameS), oneDefS)
                           
                        if cls._printSourcesB == True:
                           print (oneDefS)
              
              except BaseException as ee:
                     #error in vardef line
              
                     excS  = "Error during parsing the following line:{0}{0}".format(Os_linesep)
                     excS += "{0}{1}{1}".format(STR(lineS), Os_linesep)
                     excS += STR(ee)

                     #in python 3 there is no 'message' attribute in exceptions anymore                     
                     if    isPy2():
                           message = ee.message
                     else:
                           message = str(ee)                    
                     
                     try:
                             if ( "line is neither a proper vardef nor an empty " + \
                                  "nor a comment line!"                             ) in \
                                message                                               :
                                #more detailed error desciption
                                excS += "(Potential reason: {0}){1}".format(         \
                                         VarDef.getSyntaxErrorStr(lineS), Os_linesep )
                     except:
                             print ( ">>>>>>>>>", message )
                             pass
                     
                     #enhance readability / beauty
                     excS = excS.rstrip() + Os_linesep + Os_linesep
                     
                     #log and raise exception
                     Sys_stderr.write( STR(docS).rstrip() + Os_linesep + Os_linesep )
                     raise DocTypesError(excS)
          

          #add 'properties' attribute
          propertiesLinesS          = cls.getPropertiesStr(propertiesL) 
          setupS                   += propertiesLinesS        
          if cls._storeSourcesB   == True:
             setattr( sourcesStruct, "properties", propertiesLinesS )
           
          #add init() method
          initialsLinesS            = cls.getInitStr(classNameS, initialsS)
          setupS                   += initialsLinesS
          if cls._storeSourcesB   == True:
             setattr(sourcesStruct, "init_ials", initialsLinesS)
             setattr(sourcesStruct, "all", setupS)
             setupS += sourcesStruct.toExecStr()
             
          #return string to be executed - containing all necessary definitions 
          #(in particular getters and setters)
          return setupS 
          
          
          
          
#api class
class DocTypesApi(object):
      """
           API for DocTypes (means for handling classes inherited from DocTypes).
           It just contains class methods - so that this API can be used anywhere -
           alike a global.
           
      """ 

      #interface method
      @classmethod
      def execStr(cls, classNameS, docS, envD=None):
          """ 
              Just a wrapper for the 'global' classmethod DocParser.docTypesExecStr(). 
              As this method is called before __new__ and __init__ during the creation
              of another class, this method must be a classmethod (inheriting did not
              happen then).
              
              The parameter 'classNameS' must contain the (exact) name of the class
              being processed by this method; this is the very same name used in
              self.*__init__() method which is automatically created by this method too
              (whereby said name replaces the '*' here).
              
              The parameter 'docS' must be __doc__.
              
              The parameter 'envD' can e.g. be globals() and stands for the environment
              in which the exec is done.
          """  
          
          return DocParser.docTypesExecStr(classNameS, docS, envD)
       
       
      #interface method
      @classmethod       
      def useCythonTypes(cls):
          """
               Toggle method. 
               
               After this method has been called, the setter methods (automatically generated
               by execStr) always cast to cython types when used, e.g.: 'cython.int(value)' 
               when cint is used in the belonging vardef line.
          """
          
          VarDef.useCythonTypes = True
          
          
      #interface method
      @classmethod       
      def dontUseCythonTypes(cls):
          """  
               Toggle method. 
               
               After this method has been called, the setter methods (automatically generated
               by execStr) always cast to python types, e.g.: 'int(value)' - also when e.g. 
               cint (cython type) is used in the belonging vardef line.          
          """
          
          VarDef.useCythonTypes = False
          
          
      #debug on
      @classmethod
      def sourcesOn(cls):
          """
              After this method has been called, the auto-generated code 
              (automatically generated by execStr) always is stored under
              the class attribute 'sources'.
          """
          
          DocParser._storeSourcesB = True
          
          
      #debug on
      @classmethod
      def printSourcesOn(cls):
          """
              After this method has been called, the auto-generated code 
              (automatically generated by execStr) always is printed before
              execStr executes it.
          """
          
          DocParser._printSourcesB = True          
          
          
      #debug off
      @classmethod
      def sourcesOff(cls):
          """
              After this method has been called, the auto-generated code 
              (automatically generated by execStr) is NEVER stored under
              the class attribute 'sources'.
          """
          
          DocParser._storeSourcesB = False   


      #debug on
      @classmethod
      def printSourcesOff(cls):
          """
              After this method has been called, the auto-generated code 
              (automatically generated by execStr) is NOT printed before
              execStr executes it.
          """
          
          DocParser._printSourcesB = False           
          
          
  
        
#base class
class DocTypes(object):
      """
           Base class for all classes with __doc__ types (to be used). __doc__ types are types 
           defined in the __doc__ of said classes (using vardef-s).
           
           Belonging getter-s, setter-s and property-s are automatically created/added by
           the DocTypesApi.execStr() method
           
           Minimal example (with no vardef at all):  
           class ClassName(DocTypes):
                 ''' '''
                 exec( DocTypesApi.execStr("ClassName", __doc__) )
           
           For details/examples have a look at the TestClass-es and the pyadaaah_example.py
      """ 
      
      #whether to inhibit the dynamic addition of attributes (alike __slots__)
      enforceStaticAttrList = True
      
      
      #constructor
      @logExceptions
      def __init__(self, staticB = True):
          """
              If staticB is True, the dynamic addition of attributes is inhibited
              (somehow similar to the __slots__ mechanism).
          """
          
          self.enforceStaticAttrList = True
            
            
      @logExceptions
      def __setattr__(self, nameS, value):
          """ 
              If self.enforceStaticAttrList is True,
              the dynamic addition of attributes (alike __slots__) is blocked. 
          """
          
          if    (self.enforceStaticAttrList == True) and \
                not hasattr(self, nameS)                 :
                  
                #inhibit dynamic attribute addition
                raise LocalError( ("class %s has no property '%s' (resp. '_shadow_%s')" + \
                                   " - note that attribute 'enforceStaticAttrList' is " + \
                                   "True!"                                                ) % \
                                  (self.__class__.__name__, nameS, nameS)                     )
                
          else:
                #set the attribute name as wished to value
                object.__setattr__(self, nameS, value)
                
                
                
                
#type checking for the type of this list comes with range checking for it-s white list too
class ConstrainedList(list):
      """
           Base class for a list type, which provides range checking with payadas type checking feature.
           Lists inherited from 'ConstrainedList' just can be one (in terms of content) of the 
           lists in the white list 'self._whiteListL'. 
           
           The difference to e.g. ListRange is, that
           the list type at the same time is the list itself - which leads to the fact, that
           checking for the type of lists inherited from 'ConstrainedList' automatically leads to
           range checking their contents (and the range checked for is the white list).
           
           For a better understanding have a lokk at the ConstrExampleL example and the belonging test
           in the method selftest of SemanticTestClass.
      """
      
      #the white list contains the valid range - 
      #just lists contained therein can be the constructors parameter (and hereby ConstrainedLists)
      __slots__ = ["_whiteListL"]
      
      #constructor
      @logExceptions
      def __init__(self, listL):
          """ """        
          
          #ensure, that constructor just works with values being of type list (type check)
          if not isinstance(listL, list):
             raise TypeMismatch("%s is not a list!" % listL)                 
             
          #ensure, that classes inherited from ConstrainedList are setup correctly
          if not hasattr(self, "_whiteListL"):
             raise FatalError( "'ConstrainedList' just is a ('virtual') base class. Classes "  \
                               "inheriting from 'ConstrainedList' must implement an __init__ " \
                               "method comprising the assignment of self._whiteListL!"         )
                               
          #ensure, that constructor just works with values being in the white list (range check)
          if listL not in self._whiteListL:
             raise RangeMismatch("%s is not in range (%s)!" % (listL, self._whiteListL))
             
             
             
             
#example for a list, which just can take some given value-sets as content
class ConstrExampleL(ConstrainedList):
      """
           List, which just can be [1,3,5] or [2,4,6]. Trying to call the constructor 
           (resp. __init__) with other lists lead to a RangeMismatch.
           
           This means: checking for the type of ConstrExampleL at the same time does
           a range check (whereby the range is [[1,3,5], [2,4,6]] - given with it-s white list).
      """
      
      __slots__ = ["whiteListL"]

      def __init__(self, listL):
          """ """

          #determine the range of value-sets this list class
          self._whiteListL = [[1,3,5], [2,4,6]]

          #call the parent-s init
          ConstrainedList.__init__(self, listL)
                
  
  
  
#switch on automatic source debug mode and use cython types mode             
DocTypesApi.sourcesOn()
#DocTypesApi.printSourcesOn()             
DocTypesApi.useCythonTypes() 



  
                
         

      
if __name__ == "__main__":
  
   #parse command line arguments
   argParser = Argparse_ArgumentParser()
   argParser.add_argument("--test", action="store_true", help="run code testing this library for errors using test cases.")
   argParser.add_argument("--all",  action="store_true", help="run syntax testing code too (needs some additional ressources, in particular time!).")  
   
   args      = argParser.parse_args()

   #run tests if '--test' is given in command line
   if    args.test == True:
     
         #check whether cython is available - else do not use cython types
         if    UseCythonTypes == True:
               DocTypesApi.useCythonTypes()
         else:
               DocTypesApi.dontUseCythonTypes()
     
         #call basic selftest routines
         def selftest():
             """ Automatic selftest of this module - if no exception is raised, modules code works as expected. """
         
             BaseRange._selftest()
             VarDef._selftest()  
             
         #run selftest             
         selftest()     
         
         
         if    args.all == True:         
               #dummy helper class
               class Dummy(object):
                     def __init__(self, *args):
                         pass
     
     
               #dummy class for testing syntax resp. parser
               print ( "Creating test cases for testing syntax rules resp. the parser-s syntax module..." )
               class SyntaxTestClass(DocTypes):
                     __doc__ =  """
                         ----------
                         Interface:
                         ----------
                          
                     """
               
                     #anything
                     __doc__ += VarDef.getTestStr(["anything"], "attriba", ["1", "'a'", "dict()", "*"], ["["], ["*"], ["]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])
                     __doc__ += VarDef.getTestStr(["anything"], "attriba", ["1", "'a'", "dict()", "*"], ["["], ["1,'a',dict()", "*"], ["]"], ["r", "rw", "rw,signal(sigMethod)"]                          )
               
                     #bool
                     __doc__ += VarDef.getTestStr(["bool", "cbool"], "togglea", ["True", "False", "*"], ["["], ["*"], ["]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])
                            
                     #integers
                     __doc__ += VarDef.getTestStr(["int","cchar","cshort","cint"], "counta", ["2","*"], ["[", "]"], ["1..3", "*..3", "1..*", "*..*"], ["[", "]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])
                     __doc__ += VarDef.getTestStr(["int","cchar","cshort","cint"], "countb", ["2","*"], ["["],      ["*"],                            ["]"],      ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])
                     __doc__ += VarDef.getTestStr(["long","clong","clonglong"],    "countc", ["2","*"], ["[", "]"], ["1..3", "*..3", "1..*", "*..*"], ["[", "]"], ["r", "rw", "rw,signal(sigMethod)"]                                          )
                     __doc__ += VarDef.getTestStr(["long","clong","clonglong"],    "countd", ["2","*"], ["["],      ["*"],                            ["]"],      ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])
                
                     #floats
                     __doc__ += VarDef.getTestStr(["float","cfloat","cdouble"], "limita", ["2.0","*"], ["[", "]"], ["1.0..3.0", "*..3.0", "1.0..*", "*..*"], ["[", "]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])
                     __doc__ += VarDef.getTestStr(["float","cfloat","cdouble"], "limitb", ["2.0","*"], ["["],      ["*"],                                    ["]"],      ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])
               
                     #complex-s
                     __doc__ += VarDef.getTestStr(["complex","ccomplex","cdcomplex"], "vectora", ["complex(1.0, 2.0)","*"], ["["], ["*"], ["]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])
               
                     #str-s
                     __doc__ += VarDef.getTestStr(["str"], "namea", ["'a'", '"b"', "r'a'", 'r"b"', "*"], ["["], ["'a', 'b'", '"a", "b"', "*"], ["]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])
                     if isPy2() == True:
                        __doc__ += VarDef.getTestStr(["unicode"], "namea", ["'a'", '"b"', "r'a'", 'r"b"', "*"], ["["], ["'a', 'b'", '"a", "b"', "*"], ["]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])
                     
                              
                     #unicodes
                     if isPy2() == True:
                        __doc__ += VarDef.getTestStr(["unicode"], "nameb", [u"u'§'", u'u"§"', u"u'\u00a7'", u'u"\U000000a7"'], ["["], [u"u'a', u'§'", u"u'a', u'\u00a7'", u"u'a', u'\U000000a7'" , "*"], ["]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])               
               
                     #lists
                     __doc__ += VarDef.getTestStr(["list"], "primesa", ['[3, 5, 7]'], ["["], ["*"], ["]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])               
                     __doc__ += VarDef.getTestStr(["list"], "pricesa", ['[11.1, 22.2, 33.3]'], ["["], ["*"], ["]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])                              
                     __doc__ += VarDef.getTestStr(["list"], "fruitsa", ['["banana", "apple"]'], ["["], ["*"], ["]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])
               
                     #tuples
                     __doc__ += VarDef.getTestStr(["tuple"], "primesb", ['(3, 5, 7)'], ["["], ["*"], ["]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])               
                     __doc__ += VarDef.getTestStr(["tuple"], "pricesb", ['(11.1, 22.2, 33.3)'], ["["], ["*"], ["]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])                              
                     __doc__ += VarDef.getTestStr(["tuple"], "fruitsb", ['("banana", "apple")'], ["["], ["*"], ["]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])
                            
                     #dicts
                     __doc__ += VarDef.getTestStr(["dict"], "collection", ['{"a":1, "b":2, "c":"c"}', 'dict(a=1, b=2, c="c")'], ["["], ["*"], ["]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])               
                            
                     #class:-es
                     __doc__ += VarDef.getTestStr(["class:Dummy"], "ownThing", ['Dummy(5)'], ["["], ["*"], ["]"], ["r", "rw", "rw,check", "rw,signal(sigMethod)", "rw,check,signal(sigMethod)"])
               
                     __doc__ += """
                         ----------
                         Internals:
                         ----------
                   
                     """
                          
                     exec(DocTypesApi.execStr("SyntaxTestClass", __doc__))
               
               del SyntaxTestClass
               print ( "...tested syntax rules resp. the parser-s syntax module successfully!" )
              
                                                 
         #dummy class for testing semantics resp. the functionality of the automatic output
         print ( "Creating test cases for testing semantics resp. the functionality of the automatic output..." )
         class SemanticTestClass(DocTypes):
               u""" 
                   ----------
                   Interface:
                   ----------
         
                   ### raw mode ###
                   vardef anything    toggled   = *             in [*]                with raw                               #the variable 'toggled' just is 'registered' (in terms of 'enforceStaticAttrList') - nothing else
                   vardef bool        toggled2  = *             in [True, False]      with raw                               #the type (bool) and range ([True, False]) has no effect (but documentation) here
                   
                   #the raw mode can be used to 'circumvent' DocTypes (and manage the belonging variable manually instead)
                   #the raw mode means: everything (besides 'registering the variable name') is resp. has to be done manually!
                   #'registering' comes with initialization of the belonging class property (SemanticTestClass.toggled resp. ...toggled2) with 'None' - 
                   #the belonging instance property is neither created nor initialized (automatically) - both has to be taken care of manually instead
                   #an initial value (e.g. '= True') is not allowed with raw variables, neither are
                   #'check' or 'signal' allowed here
                   #in raw mode no shadow variable is created/used (automatically)
                   
                   ### bool ###                   
                   vardef bool        toggled3  = True          in [True]             with r                                 #a bool constant (due to read only mode 'r')
                   #note that just the belonging class shadow variable is initialized (not the instance-s shadow variable!)
                   #note that in read-only mode checking ('check') is not possible (as well as 'signal(...)')
                                      
                   vardef bool        toggled4  = *             in [*]                with rw, check                         #a bool (True or False - OR 0 or 1 !!) 
                   vardef bool        toggled5  = True          in [True, False]      with rw, check, signal( sigMethod )    #a bool (just True or False) - if toggled5 is assigned, method sigMethod is called afterwards
                   #keep in mind that using uninitialized variables ('= *') is a little dangerous - use that with care!
                   #(you have to understand the pyadaaah relations between class attributes, instance attributes, shadow variables and properties to be sure)
                   #checking for the bool type is equivalent to range checking for [True, False, 1, 0] 
                   #if one wants JUST the range [True, False] that has to be done via range checking (for initial/default value) resp. using the type class:Bool (for setter)
                   #note that the range checking of the initial/default value is more strict than that of the setter:
                   #in the setter, the value to be set FIRST is converted to the target type (if possible) and AFTER THAT range checked
                   #(whereas that is not true for the range check of the initial/default value)
                   #unfortunately e.g. bool("abc") evaluates to bool too - so, if you do not like this, have a look at the payada-class 'Bool'
                   
                   vardef class:Bool  toggledC  = true          in [*]                with rw, check                         #a bool with inherent range check [true, True, false, False] (but 0 and 1 are not in range resp. valid here!)
                   vardef class:Bool  toggledD  = false         in [false]            with rw, check                         #either False or false
                   #note the lower case 'true' - which is defined as Bool(True) in payada

                   vardef bool        toggled6  = False         in [True, False]      with rw                                #unchecked - can be anything; just documentation
                   vardef cbool       toggled7  = True          in [true, false]      with rw, check, signal( sigMethod )    #if cython is available, the type cython.bint is used
                   #one can connect a signal to a setter method by adding the signal keyword followed by the method name (method of same class)
                   #to be connected with the setter of the belonging variable
                   #in aforementioned example, the sigMethod is always called, when the variable toggled7 has set successfully 
                   
                   vardef bool        toggled8  = False         in [True, False]      with rw, check( strict )               #just a bool, either True or False
                   #the keyword strict is explained below in detail
                   
                   ### int ###
                   vardef int         looper    = 6             in [5..7]             with rw, check                         #5, 6 or 7
                   vardef int         counter   = 5             in [3,5,7]            with rw, check                         #3, 5 or 7
                   vardef int         value     = 1             in [*]                with rw, check                         #any integer
                   vardef int         latch     = *             in [*]                with rw, check                         #any integer with initial value None
          
                   vardef long        starCnt   = 3             in [*]                with rw, check                         #any long integer
                   vardef clonglong   starCnt2  = 3             in [*]                with rw, check                         #any cython.longlong
                   
                   ### float ###
                   vardef float       rangee    = 6.1           in [5.1..6.9]         with rw, check( strict )               #JUST (due to strict) floats with 5.1 <= float <= 6.9
                   vardef float       hit       = 1.3           in [1.3, 1.7]         with rw, check( strict )               #JUST (due to strict) floats with 1.3 or 1.7
                   #'check' without '(strict)' does not do a strict type check - instead it
                   #tries to convert to the type and checks whether the converted value is equal to the original
                   #example: 
                   #rangee = 6 means: 
                   #val = float(6); if val != 6: raise TypeMismatch...
                   
                   #'check(strict)' instead does a real type check
                   #example:
                   #rangee = 6 means:
                   #val = 6; if not isinstance(val, float): raise TypeMismatch
                   
                   vardef float       lower     = 1.4           in [*..2.1[           with rw, check                         #float < 2.1
                   vardef float       upper     = 1.5           in ]1.4..*]           with rw, check                         #float > 1.4
                         
                   ### mixed ###                         
                   vardef int         value2    = 9             in [3,5,7]            with rw                                #neither type nor range check - line is just a pure info
                   vardef float       upper2    = 1.5           in [1.5]              with r                                 #constant, raises Exception when changed
                   
                   vardef cint        cloop     = 6             in [5..7]             with rw, check                         #cython integer 5, 6 or 7
                   vardef cfloat      chit      = 1.3           in [1.3, 1.7]         with rw, check                         #cython float 1.3 or 1.7
                   
                   ### complex ###
                   vardef complex     vector    = complex(1,2)  in [*]                with rw, check( strict )               #any complex number
                   vardef ccomplex    vector2   = complex(1,2)  in [*]                with rw, check                         #any cython.complex
                    
                   ### anything ###
                   vardef anything    arbitr1   = 1             in [*]                with rw                                #any object; initially 1   
                   vardef anything    arbitr2   = "lala"        in [*]                with rw, check                         #check has no effect here
                           
                   ### str ###
                   vardef str         text      = "abc"         in [*]                with rw, check( strict )               #any string
                   vardef str         text2     = "abc"         in ["abc", "def"]     with rw, check                         #"abc" or "def"
                   vardef str         text3     = 'abc'         in ['abc', 'def']     with rw, check                         #"abc" or "def"                 
                           
                   ### unicode ###
                   vardef unicode     uni       = u"a\u00a7bc"  in [u"a§bc", u"def"]  with rw, check                         #u"a§bc" or u"def"
                   vardef unicode     uni2      = u"a§bc"       in [u"a§bc"]          with rw, check                         #u#"a§bc"
                                
                   ### strict / signal ###
                   vardef int         primes    = 3             in [3,5,7]            with rw, check( strict ), signal( sigMethod )  #comment
                 
                   ### tuple / list ###
                   vardef tuple       xyz       = (6,4,2)       in [*]                with rw, check                         #any tuple
                   vardef list        xyz2      = [6,4,2]       in [*]                with rw, check( strict )               #any list
                   
                   ### dict ###
                   vardef dict        summary   = dict(a=1,b=2) in [*]                with rw, check                         #any dictionary
                   
                   ### own classes / extensions of payadas type & range checking ###
                   vardef class:ConstrExampleL selection = ConstrExampleL([1,3,5]) in [*] with rw, check( strict )           #either [1,3,5] or [2,4,6]
                 
                   ------------
                   Description:
                   ------------          
                   
                   Description text.          
                   
                   ----------
                   Internals:
                   ----------
                   
                   vardef int         _counterb = 2             in [1..3]             with rw,check                          #comment counterb
                   
                   ---------
                   Examples:
                   ---------
                   
                   Text with examples.
               
               """
               
               signalCnt = 0
                
               exec(DocTypesApi.execStr("SemanticTestClass", __doc__))
                
                
               def __init__(self):
                   DocTypes.__init__(self)
                   self.SemanticTestClass__init__()
                
                
               #method connected to the signal sent by setting variables
               def sigMethod(self, key, value, error):
                   #print ( "Signal triggered by: %s = %s" % (key, value) )
                   self.signalCnt += 1
                   
                   
               #helper method for selftest
               def _fineAssigns( self, attributeNameS, valuesL, alreadyAssigned=False ):
                   """ Method for testing assign-s, which are expected to work. """
                   
                   #loop over all values to be assigned
                   for value in valuesL:
                       if alreadyAssigned == False:
                          #'check' whether setting raises exception
                          setattr(self, attributeNameS, value)
                       
                       #check whether setting was successful                       
                       assert getattr(self, attributeNameS) == value, "Assigning %s to %s failed!" % (value, attributeNameS)
                       
                   return None
                       
                       
               #helper method for selftest
               def _typeMismatchAssigns( self, attributeNameS, valuesL ):
                   """ Method for testing assign-s, which are expected to raise an TypeMismatch. """
                   
                   #loop over all values to be assigned
                   acceptedL = []
                   tm        = 0
                   for value in valuesL:
                       try:
                              setattr(self, attributeNameS, value)
                              acceptedL.append(value)
                              
                       except TypeMismatch:
                              tm += 1
                   
                   if tm != len(valuesL):
                      raise FatalError("the type checking of %s unexpectedly accepts %s" % (attributeNameS, acceptedL))
                      
                   return None
                      
                      
               #helper method for selftest
               def _rangeMismatchAssigns( self, attributeNameS, valuesL ):
                   """ Method for testing assign-s, which are expected to raise an RangeMismatch. """
                   
                   #loop over all values to be assigned
                   acceptedL = []
                   rm        = 0
                   for value in valuesL:
                       try:
                              setattr( self, attributeNameS, value)
                              acceptedL.append(value)
                              
                       except RangeMismatch:
                              rm += 1
                   
                   if rm != len(valuesL):
                      raise FatalError("the range checking of %s unexpectedly accepts %s" % (attributeNameS, acceptedL))
                      
                   return None                  
                   
                   
               #self test
               def selftest(self):
                   """ """
                   
                   print ("Selftesting SemanticTestClass...")
                   
                   ### raw mode ###
                   try:
                          print ("Checking raw mode...")                     
                     
                          #raw initializes (just) the class property
                          assert SemanticTestClass.toggled  == None, "variable SemanticTestClass.toggled  not created/initialized properly"
                          assert SemanticTestClass.toggled2 == None, "variable SemanticTestClass.toggled2 not created/initialized properly"
                          
                          #this just changes the instance-s property
                          self._fineAssigns( "toggled", [True] )
                          self._fineAssigns( "toggled2", [True] )
                          
                          #the classe-s property is unchanged
                          assert SemanticTestClass.toggled  == None, "SemanticTestClass.toggled  changed unexpectedly"
                          assert SemanticTestClass.toggled2 == None, "SemanticTestClass.toggled2 changed unexpectedly"
                          
                          #neither type nor value/range is checked at all
                          self._fineAssigns( "toggled", (123, "abc") )
                          self._fineAssigns( "toggled2", (123, "abc") )
                          
                          print ("...raw mode checked successfully!")
                         
                   except BaseException as ee:
                          raise FatalError("error during 'raw mode' check (%s)!" % STR(ee))
                          
                   ### bool ###
                   try:
                          print ("Checking bool...")

                          #read only initializes (just) the class property
                          assert self._shadow_toggled3              == True, "shadow variable SemanticTestClass._shadow_toggled3 not created/initialized properly"
                          self._fineAssigns( "toggled3", [True], True )

                          #writing should raise a ReadOnly exception                          
                          ro = False
                          try:
                                 self.toggled3                       = False
                                 assert self.toggled3               == True, "property self.toggled3 unexpectedly changed"
                                                               
                          except ReadOnly:
                                 #as toggled3 is read only, the ReadOnly exception is expected here
                                 ro = True
                          assert ro                                 == True, "no ReadOnly despite write attempt"
                          
                          #just the classe-s shadow variable is initialized
                          SemanticTestClass._shadow_toggled3         = 123
                          assert self.toggled3                      == 123,   "self.toggled3 is unexpectedly not connected to SemanticTestClass._shadow_toggled3"                          
                          
                          #circumventing the read only protection by accessing the shadow should still work
                          self._shadow_toggled3                      = "abc"
                          assert self.toggled3                      == "abc", "writing the shadow variable self.toggled3 failed unexpectedly"
                          
                          #check relations between class shadow, instance shadow and variable itself
                          assert self.toggled4                      == None, "unexpected initial value of self.toggled4"
                          SemanticTestClass._shadow_toggled4         = False
                          assert self.toggled4                      == False, "self.toggled4 is unexpectedly not connected to SemanticTestClass._shadow_toggled4"
                          self._shadow_toggled4                      = True
                          assert self.toggled4                      == True, "self.toggled4 is unexpectedly not connected to self._shadow_toggled4"                          
                          
                          #in range of bool
                          self._fineAssigns( "toggled4", (True, False, 0, 1) )
                          
                          #not in range of bool
                          self._typeMismatchAssigns("toggled4", (2, "True", 1.1))                             
                             
                          #check expected relations between class-, instance- variables, properties and shadows
                          assert self.toggled5                       == True, "init of self.toggled5 failed"
                          assert self._shadow_toggled5               == True, "init of self._shadow_toggled5 failed"
                          assert SemanticTestClass._shadow_toggled5  == True, "init of SemanticTestClass._shadow_toggled5 failed"
                          assert type(SemanticTestClass.toggled5)    == property, "SemanticTestClass.toggled5 unexpectedly is not a property"
                          
                          #check whether signal method is triggered
                          sc = self.signalCnt
                          self.toggled5 = False
                          assert (sc + 1) == self.signalCnt, "setting self.toggled5 unexpectedly did not trigger sigMethod" 
                          
                          #toggled6 is unckecked - an error must not occur with the following
                          assert self.toggled6                       == False, "init of toggled6 failed unexpectedly" 
                          self.toggled6 = 123
                          self.toggled6 = "abc"
                          assert self.toggled6                       == "abc", "setting toggled6 to 'abc' failed unexpectedly"
                          
                          #check init/setting and signaling of toggled7
                          assert self.toggled7                       == True, "init of toggled7 failed unexpectedly"
                          before = self.signalCnt
                          self.toggled7 = False
                          assert self.toggled7                       == False, "setting toggled7 to False failed unexpectedly"
                          assert self.signalCnt == (before + 1),               "signal belonging to toggled7 is unexpectedly not triggered"
                          
                          #not in range of bool
                          self._typeMismatchAssigns("toggled7", (2, "True", 1.1)) 
                          
                          #toggledC - a Bool (not bool!)
                          assert self.toggledC                       == True, "init of toggledC failed unexpectedly"
                          self._fineAssigns("toggledC", (False, True, false, true)) 
                          self._typeMismatchAssigns("toggledC", (0, 1, 2, "abc", 3.3))
                          
                          #toggledD - a Bool (not bool!)
                          self._fineAssigns("toggledD", (False, false)) 
                          self._rangeMismatchAssigns("toggledD", (True, true))
                          self._typeMismatchAssigns("toggledD", (0, 1, 2, "abc", 1.1))
                          
                          #toggled8 - a bool (strict)
                          self._fineAssigns("toggled8", [False], True)
                          self._fineAssigns("toggled8", (False, True))
                          self._typeMismatchAssigns("toggled8", (0, 1, 2, 3.3, "abc", false, true))

                          print ("...bool checked successfully!")                   
                   
                   except BaseException as ee:
                          raise FatalError("error during 'bool' check (%s)!" % STR(ee))
                          
                          
                   ### integer ###
                   try:
                          print ("Checking integer...")
                          
                          #looper
                          self._fineAssigns("looper", [6], True)
                          self._fineAssigns("looper", (5,6,7))
                          self._rangeMismatchAssigns("looper", (4,8))
                          self._typeMismatchAssigns("looper", ("abc", 1.1, false))
                          
                          #counter
                          self._fineAssigns("counter", [5], True)
                          self._fineAssigns("counter", (3,5,7))
                          self._rangeMismatchAssigns("counter", (2,4,6,8))
                          self._typeMismatchAssigns("counter", ("abc", 1.1, false))
                          
                          #value
                          self._fineAssigns("value", [1], True)
                          self._fineAssigns("value", (-10000,-1,0,1,2,3,10000))
                          self._typeMismatchAssigns("value", ("abc", 1.1, false)) 
                          
                          #latch
                          self._fineAssigns("latch", [None], True)
                          self._fineAssigns("latch", (-10000,-1,0,1,2,3,10000, 10000000000000000000000000000000000000000000000000000000000000))
                          self._typeMismatchAssigns("latch", ("abc", 1.1, false))
                          self.latch = 1.0
                          assert type(self.latch) == int, "latch unexpectedly does not contain an integer!" 
                          
                          #starCnt
                          self._fineAssigns("starCnt", [3], True)
                          self._fineAssigns("starCnt", (-10000,-1,0,1,2,3,10000, 10000000000000000000000000000000000000000000000000000000000000))
                          self._typeMismatchAssigns("starCnt", ("abc", 1.1, false))
                          self.starCnt = 1.0
                          if     isPy2() == True:
                                 #long just exists with Python 2.*
                                 assert type(self.starCnt) == long, "starCnt unexpectedly does not contain a long!" 
                          else:
                                 #not with Python 3.*
                                 assert type(self.starCnt) == int, "starCnt unexpectedly does not contain an int!"
                          
                          #starCnt2
                          self._fineAssigns("starCnt2", [3], True)
                          self._fineAssigns("starCnt2", (-10000,-1,0,1,2,3,10000, 10000000000000000000000000000000000000000000000000000000000000))
                          self._typeMismatchAssigns("starCnt2", ("abc", 1.1, false))
                          self.starCnt2 = 10000000000000000000000000000000000000000000000000000000.0
                          if     isPy2() == True:
                                 #long just exists with Python 2.*
                                 assert type(self.starCnt2) == long, "starCnt unexpectedly does not contain a long!" 
                          else:
                                 #not with Python 3.*
                                 assert type(self.starCnt2) == int, "starCnt unexpectedly does not contain an int!"
                                 
                          #cloop
                          self._fineAssigns("cloop", [6], True)
                          self._fineAssigns("cloop", (5, 6.0, 7))
                          self._rangeMismatchAssigns("cloop", (4,8))                          
                          self._typeMismatchAssigns("cloop", ("abc", 5.1, 6.1, false))
                          self.cloop = 6.0
                          assert type(self.cloop) == int, "cloop unexpectedly does not contain an int!"                           
                          
                          #primes
                          tmp = self.signalCnt
                          self._fineAssigns("primes", [3], True)
                          self._fineAssigns("primes", (3,5,7))
                          self._rangeMismatchAssigns("primes", (2,4,6,8))
                          self._typeMismatchAssigns("primes", (1.0, 2.2, "abc"))
                          assert (self.signalCnt - tmp) == 3, "signal connected to primes failed!"  
                          
                          print ("...integer checked sucessfully!")
                     
                   except BaseException as ee:
                          raise FatalError("error during 'integer' check (%s)!" % STR(ee))
                          
              ### float ###
                   try:
                          print ("Checking float...")                     
                     
                          #rangee
                          self._fineAssigns("rangee", [6.1], True)
                          self._fineAssigns("rangee", (5.1, 6.0, 6.4123, 6.9))
                          self._rangeMismatchAssigns("rangee", (5.09,6.91))
                          self._typeMismatchAssigns("rangee", ["abc", false])
                          
                          #hit
                          self._fineAssigns("hit", [1.3], True)
                          self._fineAssigns("hit", (1.3, 1.7))
                          self._rangeMismatchAssigns("hit", (1.2, 1.4, 1.6, 1.8, 2.0))
                          self._typeMismatchAssigns("hit", ["abc", false])                          
                          
                          #lower
                          self._fineAssigns("lower", [1.4], True)
                          self._fineAssigns("lower", (-1111.11, 0, 1.1, 2.09999))
                          self._rangeMismatchAssigns("lower", (2.1, 3, 11111.11))
                          self._typeMismatchAssigns("lower", ["abc"])  
                          
                          #upper
                          self._fineAssigns("upper", [1.5], True)
                          self._fineAssigns("upper", (1.400001, 1.5, 2, 111111.123))
                          self._rangeMismatchAssigns("upper", (-1.1, 1.4))
                          self._typeMismatchAssigns("upper", ["abc"])  

                          #value2
                          self._fineAssigns("value2", [9], True)
                          self._fineAssigns("value2", [-111.111, 0, "abc", "None"])
                          
                          #upper2
                          self._fineAssigns("upper2", [1.5], True)
                          try:
                                 self.upper2 = 1.5
                                 raise FatalError("upper2 is read only, but excepted writing!")                                 
                                 
                          except ReadOnly:
                                 pass
                               
                          #chit
                          self._fineAssigns("chit", [1.3], True)
                          self._fineAssigns("chit", (1.3,1.7))
                          self._rangeMismatchAssigns("chit", (1,1.2,1.4,1.6,1.8))                          
                          self._typeMismatchAssigns("chit", ["abc"])
                          self.chit = 1.7
                          assert type(self.chit) == float, "chit unexpectedly does not contain an int!"                           
                          
                          print ("...float checked successfully!")
                                                 
                   except BaseException as ee:
                          raise FatalError("error during 'float' check (%s)!" % STR(ee))                          
                          
                   ### complex ###
                   try:
                          print ("Checking complex...")
                          
                          #vector
                          self._fineAssigns("vector", [complex(1,2)], True)
                          self._fineAssigns("vector", (complex(-1.1,-2.2), complex(3,4)))
                          self._typeMismatchAssigns("vector", (1, 2.2, "abc", True))
                             
                          #vector2
                          self._fineAssigns("vector2", [complex(1,2)], True)
                          self._fineAssigns("vector2", (complex(-1.1,-2.2), complex(3,4)))
                          self.vector2 = 1
                          if type(self.vector2) != complex:
                             raise FatalError("setting vector2 to 1 leads to an unexpected type!")                             
                             
                          print ("...complex checked successfully!")
                                                 
                   except BaseException as ee:
                          raise FatalError("error during 'complex' check (%s)!" % STR(ee))                          
                                                 
                   ### anything ###
                   try:
                          print ("Checking anything...")
                          
                          #arbitr1
                          self._fineAssigns("arbitr1", [1], True)
                          self._fineAssigns("arbitr1", (2, 3.1, "abc"))    
                          
                          #arbitr2
                          self._fineAssigns("arbitr2", ["lala"], True)
                          self._fineAssigns("arbitr2", (2, 3.1, "abc")) 
                          
                          print ("...anything checked sucessfully!")
                                                 
                   except BaseException as ee:
                          raise FatalError("error during 'anything' check (%s)!" % STR(ee))  
                          
                   ### string ###
                   try:
                          print ("Checking string...")
                          
                          #text
                          self._fineAssigns("text", ["abc"], True)
                          self._fineAssigns("text", ("", "abc", "sdhcgjhd"))                          
                          self._typeMismatchAssigns("text", [1, 2.2, false])
                          
                          #text2
                          self._fineAssigns("text2", ["abc"], True)
                          self._fineAssigns("text2", ("abc", "def"))                          
                          self._typeMismatchAssigns("text2", (1, 2.2, false))
                          self._rangeMismatchAssigns("text2", ("", "aaa"))    
                          
                          #text3
                          self._fineAssigns("text3", ["abc"], True)
                          self._fineAssigns("text3", ("abc", "def"))                          
                          self._typeMismatchAssigns("text3", (1, 2.2, false))
                          self._rangeMismatchAssigns("text3", ("", "aaa"))  

                          print ("...string checked successfully!")                          
                                                 
                   except BaseException as ee:
                          raise FatalError("error during 'string' check (%s)!" % STR(ee))   
                          
                   ### unicode ###
                   try:
                          print ("Checking unicode...")                          
                          
                          #uni
                          self._fineAssigns("uni", [u"a§bc"], True)
                          self._fineAssigns("uni", (u"a§bc", "def"))                          
                          self._typeMismatchAssigns("uni", (1, 2.2, false))
                          self._rangeMismatchAssigns("uni", ("", "aaa"))    
                          
                          #uni2
                          self._fineAssigns("uni2", [u"a§bc"], True)
                          self._fineAssigns("uni2", [u"a§bc"])                          
                          self._typeMismatchAssigns("uni2", (1, 2.2, false))
                          self._rangeMismatchAssigns("uni2", ("", "aaa", "def"))     
                          
                          print ("...unicode checked successfully!")
                                                 
                   except BaseException as ee:
                          raise FatalError("error during 'unicode' check (%s)!" % STR(ee)) 
                          
                   ### non-atomics ###
                   try:
                          print ("Checking non-atomics...")                          
                          
                          #xyz
                          self._fineAssigns("xyz", [(6,4,2)], True)
                          self._fineAssigns("xyz", ((6,4,2), (1,2,3)))                          
                          self._typeMismatchAssigns("xyz", (1, 2.2, "abc", [6,4,2], false))       
                          
                          #xyz2
                          self._fineAssigns("xyz2", [[6,4,2]], True)
                          self._fineAssigns("xyz2", ([6,4,2], [1,2,3]))                          
                          self._typeMismatchAssigns("xyz2", (1, 2.2, "abc", (6,4,2), false)) 

                          #summary
                          self._fineAssigns("summary", [dict(a=1,b=2)], True)
                          self._fineAssigns("summary", (dict(a=1,b=2), dict(c=3,d=4)))                          
                          self._typeMismatchAssigns("summary", (1, 2.2, "abc", (6,4,2), false))  
                          
                          #selection
                          self._fineAssigns("selection", [ConstrExampleL([1,3,5])], True)
                          self._fineAssigns("selection", [ConstrExampleL([1,3,5]), ConstrExampleL([2,4,6])])                          
                          self._typeMismatchAssigns("selection", (1, 2.2, "abc", (1,3,5), [1,3,5], false))
                          try:
                                 self._rangeMismatchAssigns("selection", [ConstrExampleL([1,2,3,4,5])])                                                     
                                 raise FatalError("range check failed for 'selection' resp. 'ConstrExampleL'!")
                                 
                          except RangeMismatch:
                                 pass
                          
                          print ("...non-atomics checked successfully!")
                                                 
                   except BaseException as ee:
                          raise FatalError("error during 'non-atomics' check (%s)!" % STR(ee))  
                          
                   #test whether internals section is taken into account to
                   assert self._counterb == 2, "initializing _counterb failed unexpectedly!"
                     
                   print ("...selftesting SemanticTestClass successful!")
                   
         #test semantics
         semTest = SemanticTestClass()
         semTest.selftest()
                   
         #del SemanticTestClass
         print ( "...tested semantics resp. the functionality of the automatic output successfully!" )
          
          

### TBD ###
# complete and check cython part
# complete and check range checking with (recursively used) subclasses of BaseRange
# think about introducing checked methods too
# add 'raw' and 'strict' to syntactic selftest
# rescue the world
      

          
          

                  
                   
          
          
          
             
           