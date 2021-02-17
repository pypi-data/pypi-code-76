#     ____        _           
#    / __ \____ _(_)______  __
#   / / / / __ `/ / ___/ / / /
#  / /_/ / /_/ / (__  ) /_/ / 
# /_____/\__,_/_/____/\__, /  
# martin shishkov    /____/   
#
#   Copyright 2020 Martin Shishkov, gulliversoft.com
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from rocket.daisy.utils import types
from rocket.daisy.utils import logger
from rocket.daisy.utils.types import M_JSON, M_PLAIN
from rocket.daisy.utils.version import BOARD_REVISION, VERSION_STRING, MAPPING
from rocket.daisy.devices import manager
from rocket.daisy.devices import instance
from rocket.daisy.devices.bus import BUSLIST

MACROS = {}

class RESTHandler():
    def __init__(self):
        self.device_mapping = True
        self.export = []
        self.routes = {}
        self.macros = {}
        

    def addMacro(self, macro):
        self.macros[macro.__name__] = macro
        
    def addRoute(self, source, destination):
        if source[0] == "/":
            source = source[1:]
        if destination[0] == "/":
            destination = destination[1:]
        self.routes[source] = destination
        logger.info("Added Route /%s => /%s" % (source, destination))
        
    def findRoute(self, path):
        for source in self.routes:
            if path.startswith(source):
                route = path.replace(source, self.routes[source])
                logger.info("Routing /%s => /%s" % (path, route))
                return route
        return path
        
    def extract(self, fmtArray, pathArray, args):
        if len(fmtArray) != len(pathArray):
            return False
        if len(fmtArray) == 0:
            return True
        fmt = fmtArray[0]
        path = pathArray[0]
        if fmt == path:
            return self.extract(fmtArray[1:], pathArray[1:], args)
        if fmt.startswith("%"):
            
            fmt = fmt[1:]
            t = 's'
            if fmt[0] == '(':
                if fmt[-1] == ')':
                    name = fmt[1:-1]
                elif fmt[-2] == ')':                                   
                    name = fmt[1:-2]
                    t = fmt[-1]
                else:
                    raise Exception("Missing closing brace")
            else:
                name = fmt
            
            if t == 's':
                args[name] = path
            elif t == 'b':
                args[name] = types.str2bool(path)
            elif t == 'd':
                args[name] = types.toint(path)
            elif t == 'x':
                args[name] = int(path, 16)
            elif t == 'f':
                args[name] = float(path)
            else:
                raise Exception("Unknown format type : %s" % t)
            
            return self.extract(fmtArray[1:], pathArray[1:], args)
            
        return False

    def getDeviceRoute(self, method, path):
        pathArray = path.split("/")
        deviceName = pathArray[0]
        device = instance.DEVICES[deviceName]
        if device == None:
            return (None, deviceName + " Not Found")
        pathArray = pathArray[1:]
        funcs = device["functions"][method]
        functionName = "/".join(pathArray)
        if functionName in funcs:
            return (funcs[functionName], {})
        
        for fname in funcs:
            func = funcs[fname]
            funcPathArray = func.path.split("/")
            args = {}
            if self.extract(funcPathArray, pathArray, args):
                return (func, args) 
        
        return (None, functionName + " Not Found")
    
    def callDeviceFunction(self, method, path, data=None):
        (func, args) = self.getDeviceRoute(method, path)
        if func == None:
            return (404, args, M_PLAIN)

        if func.data != None:
            args[func.data] = data
        
        result = func(**args)
        response = None
        contentType = None
        if result != None:
            if hasattr(func, "contentType"):
                contentType = func.contentType
                if contentType == M_JSON:
                    response = types.jsonDumps(result)
                else:
                    response = func.format % result
            else:
                response = result
        
        return (200, response, contentType)
        
    def do_GET(self, relativePath, compact=False):
        relativePath = self.findRoute(relativePath)
        
        # JSON full state
        if relativePath == "*":
            return (200, self.getJSON(compact), M_JSON)

        # server version
        elif relativePath == "version":
            return (200, VERSION_STRING, M_PLAIN)

        # board revision
        elif relativePath == "revision":
            revision = "%s" % BOARD_REVISION
            return (200, revision, M_PLAIN)

        
        elif relativePath == "devices/*":
            return (200, manager.getDevicesJSON(compact), M_JSON)
        
        elif relativePath.startswith("devices/"):
            if not self.device_mapping:
                return (404, None, None)
            path = relativePath.replace("devices/", "")
            return self.callDeviceFunction("GET", path)

        else:
            return (0, None, None)

    def do_POST(self, relativePath, data, compact=False):
        relativePath = self.findRoute(relativePath)

                
        if relativePath.startswith("macros/"):
            paths = relativePath.split("/")
            mname = paths[1]
            if len(paths) > 2:
                value = paths[2]
            else:
                value = ""

            if mname in self.macros:
                macro = self.macros[mname]

                if ',' in value:
                    args = value.split(',')
                    result = macro(*args)
                elif len(value) > 0:
                    result = macro(value)
                else:
                    result = macro()
                     
                response = ""
                if result:
                    response = "%s" % result
                return (200, response, M_PLAIN)
                    
            else:
                return (404, mname + " Not Found", M_PLAIN)
                
        elif relativePath.startswith("devices/"):
            if not self.device_mapping:
                return (404, None, None)
            path = relativePath.replace("devices/", "")
            return self.callDeviceFunction("POST", path, data)

        else: # path unknowns
            return (0, None, None)

    def getJSON(self, compact=False):
        if compact:
            f = 'f'
            v = 'v'
        else:
            f = 'function'
            v = 'value'
        
        json = {}
        for (bus, value) in BUSLIST.items():
            json[bus] = int(value["enabled"])
        
        gpios = {}
        json['GPIO'] = gpios
        return types.jsonDumps(json)

