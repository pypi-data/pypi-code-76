from pyWebCamWebServerMonitor.api.user import user
from pyWebCamWebServerMonitor.api.webcam import webcam
# ...

def init_app(app):
    app.register_blueprint(user)
    app.register_blueprint(webcam)    
