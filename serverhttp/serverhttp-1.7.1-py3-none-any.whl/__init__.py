'''
A Simple HTTP Server.

Servers:
    HTTPServer : An HTTP Server with details for production
Apps:
    App:         A Simple App class with @App.route(route, methods=['GET', 'POST'])
    Application: Same as App
'''
from .app import *
from .srv import *
from .http_support.responses import *

__version__ = "1.7.1"
