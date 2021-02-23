# Zato extension

import requests as req
from flask import current_app, _app_ctx_stack


class Zato(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    def create_session(self):
        ses = req.Session()
        ses.auth = (
            current_app.config['ZATO_LOGIN'],
            current_app.config['ZATO_PASSWORD']
        )
        ses.verify = current_app.config.get('ZATO_CERT_BUNDLE', False)
        return ses

    def teardown(self, exception):
        pass

    @property
    def session(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'zato_session'):
                ctx.zato_session = self.create_session()
            return ctx.zato_session

    def get(self, path, headers=None, params=None):
        return self.session.get(current_app.config['ZATO_URL'] + path, headers=headers, params=params)

    def post(self, path, payload, headers=None):
        return self.session.post(
            current_app.config['ZATO_URL'] + path,
            json=payload,
            headers=headers
        )