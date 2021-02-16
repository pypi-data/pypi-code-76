from pyWebCamWebServerMonitor.middleware.auth import Auth

def init_app(app):
    Auth(app)