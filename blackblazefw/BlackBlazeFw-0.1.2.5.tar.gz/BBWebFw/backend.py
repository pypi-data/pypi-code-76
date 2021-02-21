from webob import Request, Response
#from BBWebFw.FileRenderer import Template
import os, sys, re, datetime
from gunicorn.app.wsgiapp import run as boot

class api:
    """
    docstring
    """

    def __init__(self, name, server):
        self.urls = {}
        self.server = server
        self.name = name
        self.out404 = '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Document</title>\n</head>\n<body>\n    Hello\n</body>\n</html>'
        self.error = {"urlcatcherexists" : "ERR:URL_CATCHER_ALREADY_EXISTS"}
    
    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)
        return response(environ, start_response)

    def getFileType(self, f):
        self.extList={
                    ".png": "image/png",
                    ".jpg": "image/jpg",
                    ".jpeg": "image/jpeg",
                    ".ico": "image/ico",
                    ".txt": "text/txt",
                    ".html": "image/text",
                    ".css": "stylesheet/text",
                }
        self.noDecode={
                    ".png": "image/png",
                    ".jpg": "image/jpg",
                    ".jpeg": "image/jpeg",
                    ".ico": "image/ico",
                }
        return self.extList[os.path.splitext(f)[1]], 

    def handle_request(self, request):
        #user_agent = request.environ.get('HTTP_USER_AGENT')
        response = Response()
        response.status_code = 200
        response.text = "Blank"
        
        handler = self.find_handler(request)

        if handler is not None:
            handler(response)
        else:
            try:
                try:
                    FileType = self.getFileType(request.path)[1]
                    try:
                        response.text = open(os.path.join(self.staticDir,"static"+request.path), "r").read().decode()
                    except:
                        response.text = open(os.path.join(self.staticDir,"static"+request.path), "rb").read().decode()

                    response.content_type = self.getFileType(request.path)[1]
                except Exception as e:
                    print(e)
                    self.err404(response)
            except Exception as e:
                print(e)
                response.text = "Well My Work Was Not Clean Enough, but...<br><b>Thats A Server Problem</b>"
                response.status_code = 500

        with open("access-log.txt", "a") as f:
            f.write("\n")
            f.write((request.remote_addr + ' - - ['+(datetime.date.today().__str__())+' '+(datetime.datetime.now().strftime("%H:%M:%S"))+ ']' + request.method))
            f.write("\n")
            f.write("Request" + ":" + request.path)
            f.write("\n")
            f.write("Response Code" + ":" + response.status_code.__str__())
            f.write("\n")
        return response

    def catchURL(self, path):
        def wrapper(handler):
            if(not(self.urls.__contains__(path))):
                self.urls[path] = handler
                print(self.urls[path])
                return handler
            else:
                print("hi")
                raise AssertionError(self.error["urlcatcherexists"])
                return self.error["urlcatcherexists"]

        return wrapper

    def find_handler(self, request):
        for path, handler in self.urls.items():
            if path == request.path:
                return handler

    def err404(self,response):
        response.status_code = 404
        response.text = self.out404

    def setError(self, code, data):
        if code == 404:
            self.out404 = data
        else:
            raise Exception("Invalid Error Code")

    def setStaticDir(self, dir_):
        self.staticDir = dir_

    def run(self, app, host):
        print("run")

        if (self.name).endswith(".py"):
            self.fname = self.name
            self.name = (self.name).replace(".py", "")
        else:
            self.fname = self.name + ".py"
        
        sys.argv = [re.sub(r'(-script\.pyw|\.exe)?$', '', "env/bin/gunicorn"),self.name+':'+ app, "-b", host]
        print(sys.argv)
        sys.exit(boot())
        
        #key, _hash = crypt("i \u2764\ufe0f you")
        '''
        mode:d
        key>>>PHHdqvF_JLlFW-fUz74wHa2A9M0iY4LFwvJkGfTFZlk=
        hash>>>gAAAAABgCtLb_VGjuqSa46pK6wchnhEPpvBqaTeN12_cRzSyqvkfsMhev5D7i_pblmZVEMQYyir6mrhT6UtSMAcDzA8jZdur9_H34EFzYAStmpP6kf7WyX8=
        '''