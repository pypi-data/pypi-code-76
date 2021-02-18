
#   Ti Sitara/Maxwell implementation 2020 Martin Shishkov - gulliversoft.com

import os
import socket
import threading
import codecs
import mimetypes as mime
import logging

from rocket.daisy.utils.version import VERSION_STRING, PYTHON_MAJOR
from rocket.daisy.utils.logger import info, exception, debug
from rocket.daisy.utils.crypto import encrypt
from rocket.daisy.utils.types import str2bool

if PYTHON_MAJOR >= 3:
    import http.server as BaseHTTPServer
else:
    import BaseHTTPServer


DAISY_DOCROOT = "/usr/share/daisy/htdocs"

class HTTPServer(BaseHTTPServer.HTTPServer, threading.Thread):
    if socket.has_ipv6:
        address_family = socket.AF_INET6

    def __init__(self, host, port, handler, context, docroot, index, auth=None, realm=None):
        try:
            BaseHTTPServer.HTTPServer.__init__(self, ("", port), HTTPHandler)
        except:
            self.address_family = socket.AF_INET
            BaseHTTPServer.HTTPServer.__init__(self, ("", port), HTTPHandler)

        threading.Thread.__init__(self, name="HTTPThread")
        self.host = host
        self.port = port

        if context:
            self.context = context
            if not self.context.startswith("/"):
                self.context = "/" + self.context
            if not self.context.endswith("/"):
                self.context += "/"
        else:
            self.context = "/"

        self.docroot = docroot

        if index:
            self.index = index
        else:
            self.index = "index.html"
            
        self.handler = handler
        self.auth = auth
        if (realm == None):
            self.authenticateHeader = "Basic realm=daisy"
        else:
            self.authenticateHeader = "Basic realm=%s" % realm

        self.running = True
        self.start()
            
    def get_request(self):
        sock, addr = self.socket.accept()
        sock.settimeout(10.0)
        return (sock, addr)

    def run(self):
        info("HTTP Server binded on http://%s:%s%s" % (self.host, self.port, self.context))
        try:
            self.serve_forever()
        except Exception as e:
            if self.running == True:
                exception(e)
        info("HTTP Server stopped")

    def stop(self):
        self.running = False
        self.server_close()

class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    logger = logging.getLogger("HTTP")

    def log_message(self, fmt, *args):
        pass
    
    def log_error(self, fmt, *args):
        pass
        
    def version_string(self):
        return VERSION_STRING
    
    def checkAuthentication(self):
        if self.server.auth == None or len(self.server.auth) == 0:
            return True
        
        authHeader = self.headers.get('Authorization')
        if authHeader == None:
            return False
        
        if not authHeader.startswith("Basic "):
            return False
        
        auth = authHeader.replace("Basic ", "")
        if PYTHON_MAJOR >= 3:
            auth_hash = encrypt(auth.encode())
        else:
            auth_hash = encrypt(auth)
            
        if auth_hash == self.server.auth:
            return True
        return False

    def requestAuthentication(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", self.server.authenticateHeader)
        self.end_headers();
        
    
    def logRequest(self, code):
        debug('### daisy gulliversoft "%s %s %s" - %s %s (Client: %s <%s>)' % (self.command, self.path, self.request_version, code, self.responses[code][0], self.client_address[0], self.headers["User-Agent"]))
    
    def sendResponse(self, code, body=None, contentType="text/plain"):
        if code >= 400:
            if body != None:
                self.send_error(code, body)
            else:
                self.send_error(code)
        else:
            self.send_response(code)
            self.send_header("Cache-Control", "no-cache")
            if body != None:
                self.send_header("Content-Type", contentType);
                self.send_header("Content-Length", len(body));
                self.end_headers();
                self.wfile.write(body)
        self.logRequest(code)

    def findFile(self, filepath):
        if os.path.exists(filepath):
            if os.path.isdir(filepath):
                filepath += "/" + self.server.index
                if os.path.exists(filepath):
                    return filepath
            else:
                return filepath
        return None
        
                
    def serveFile(self, relativePath):
        if self.server.docroot != None:
            path = self.findFile(self.server.docroot + "/" + relativePath)
            if path == None:
                path = self.findFile("./" + relativePath)

        else:
            path = self.findFile("./" + relativePath)                
            if path == None:
                path = self.findFile(DAISY_DOCROOT + "/" + relativePath)

        if path == None and (relativePath.startswith("daisy.") or relativePath.startswith("jquery")):
            path = self.findFile(DAISY_DOCROOT + "/" + relativePath)

        if path == None:
            return self.sendResponse(404, "Not Found")

        realPath = os.path.realpath(path)
        
        if realPath.endswith(".py"):
            return self.sendResponse(403, "Not Authorized")
        
        if not (realPath.startswith(os.getcwd()) 
                or (self.server.docroot and realPath.startswith(self.server.docroot))
                or realPath.startswith(DAISY_DOCROOT)):
            return self.sendResponse(403, "Not Authorized")
        
        (contentType, encoding) = mime.guess_type(path)
        f = codecs.open(path, encoding=encoding)
        data = f.read().encode('utf-8')
        f.close()
        self.send_response(200)
        self.send_header("Content-Type", contentType);
        self.send_header("Content-Length", len(data))
        self.end_headers()
        debug("### daisy gulliversoft: data: %s serveFile: %s" % (data, realPath))
        self.wfile.write(data)
        self.logRequest(200)
        
    def processRequest(self):
        self.request.settimeout(None)
        if not self.checkAuthentication():
            return self.requestAuthentication()
        
        request = self.path.replace(self.server.context, "/").split('?')
        relativePath = request[0]
        if relativePath[0] == "/":
            relativePath = relativePath[1:]
            
        if relativePath == "daisy" or relativePath == "daisy/":
            self.send_response(301)
            self.send_header("Location", "/")
            self.end_headers()
            return

        params = {}
        if len(request) > 1:
            for s in request[1].split('&'):
                if s.find('=') > 0:
                    (name, value) = s.split('=')
                    params[name] = value
                else:
                    params[s] = None
        
        compact = False
        if 'compact' in params:
            compact = str2bool(params['compact'])

        try:
            result = (None, None, None)
            if self.command == "GET":
                result = self.server.handler.do_GET(relativePath, compact)
            elif self.command == "POST":
                length = 0
                length_header = 'content-length'
                if length_header in self.headers:
                    length = int(self.headers[length_header])
                result = self.server.handler.do_POST(relativePath, self.rfile.read(length), compact)
            else:
                result = (405, None, None)
                
            (code, body, contentType) = result
            
            if code > 0:
                self.sendResponse(code, body.encode('utf-8'), contentType)
            else:
                if self.command == "GET":
                    debug("### daisy gulliversoft: GET on on http://%s:%s%s file:%s" % (self.server.host, self.server.port, self.server.context, relativePath))
                    self.serveFile(relativePath)
                else:
                    self.sendResponse(404)

        except ValueError as e:
            self.sendResponse(403, "%s" % e)
        except Exception as e:
            self.sendResponse(500)
            raise e
            
    def do_GET(self):
        self.processRequest()

    def do_POST(self):
        self.processRequest()
