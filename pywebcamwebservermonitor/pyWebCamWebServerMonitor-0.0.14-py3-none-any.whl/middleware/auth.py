from pyWebCamWebServerMonitor import db, auth
from flask import jsonify, request, g
from pyWebCamWebServerMonitor.models.user import User

class Auth:
    
    def __init__(self, app):

        @auth.verify_password
        def verify_password(username_or_token, password):
            if request.path == "/api/login":
                user = User.query.filter_by(username=username_or_token).first()
                if not user or not user.verify_password(password):
                    return False
            else:
                user = User.verify_auth_token(username_or_token)
                if not user:
                    return False    
            g.user = user   
            return True
        
        @auth.error_handler
        def auth_error(status):
            return "Invalid username or password", status



        @app.route('/api/login', methods=['POST'])
        @auth.login_required
        def get_auth_token():
            token = g.user.generate_auth_token()
            return jsonify(token.decode("utf-8"))
        
