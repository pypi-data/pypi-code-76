import os

from flask import Flask
from werkzeug.exceptions import NotFound, MethodNotAllowed, InternalServerError

from nidhoggr.core.config import BLConfig
from nidhoggr.core.repository import BaseTextureRepo, BaseUserRepo
from nidhoggr.views import auth, session, core


def configure_error_handlers(app: Flask):
    app.register_error_handler(NotFound, core.not_found)
    app.register_error_handler(MethodNotAllowed, core.method_not_allowed)
    app.register_error_handler(InternalServerError, core.internal_server_error)


def configure_views(app: Flask):
    for func in auth.__all__:
        app.add_url_rule(f"/{func}", func, getattr(auth, func), methods=["POST"])
    for func in session.__all__:
        app.add_url_rule(f"/{func}", func, getattr(session, func), methods=["POST"])


def create_app(users: BaseUserRepo, config: BLConfig, textures: BaseTextureRepo) -> Flask:
    app = Flask(__package__, root_path=os.path.dirname(__file__))
    app.bl = {
        BaseUserRepo: users,
        BLConfig: config,
        BaseTextureRepo: textures
    }
    configure_error_handlers(app)
    configure_views(app)
    return app
