from pyWebCamWebServerMonitor import db
from flask import current_app
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    
    #Password encryption
    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)
    
    #Password resolution
    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    def is_pass_admin(self):
        return custom_app_context.verify('admin', self.password)

    #Get token, valid time 24 Hours
    def generate_auth_token(self, expiration = 86400):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    #Resolve the token to confirm the login user identity
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user
    

    def __repr__(self):
        return '<User %r>' % self.username
