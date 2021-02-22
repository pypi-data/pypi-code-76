'''
A Simple HTTP Server.

Servers:
    AsyncHTTPServer:     Async HTTP server based on asyncio
    ThreadedHTTPServer:  Threaded HTTP Server
Apps:
    App:         A Simple App class with @App.route(route, methods=['GET', 'POST'])
    Application: Same as App
'''
from .app import *
from .srv import *
from .http_support.responses import *

__version__ = "1.7"
