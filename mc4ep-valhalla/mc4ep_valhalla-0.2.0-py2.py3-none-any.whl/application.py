import os

from flask import Flask
from flask_redis import FlaskRedis
from flask_uuid import FlaskUUID
from nidhoggr.core.repository import BaseTextureRepo, BaseUserRepo
from werkzeug.exceptions import InternalServerError, BadRequest, Unauthorized, NotFound, Forbidden

from valhalla import utils
from valhalla.views import auth, texture
from valhalla.converter import FlaskTextureType


def configure_error_handlers(app: Flask):
    app.register_error_handler(InternalServerError, utils.error_handler)
    app.register_error_handler(BadRequest, utils.error_handler)
    app.register_error_handler(Unauthorized, utils.error_handler)
    app.register_error_handler(NotFound, utils.error_handler)
    app.register_error_handler(Forbidden, utils.error_handler)


def configure_views(app: Flask):
    app.add_url_rule('/api/v1/auth/handshake', 'auth_handshake', auth.handshake, methods=['POST'])
    app.add_url_rule('/api/v1/auth/response', 'auth_response', auth.response, methods=['POST'])
    app.add_url_rule('/api/v1/user/<uuid(strict=False):uuid>', 'texture_fetch', texture.fetch, methods=['GET'])
    app.add_url_rule('/api/v1/user/<uuid(strict=False):uuid>/<kind:kind>', 'texture_post', texture.post, methods=['POST'])
    app.add_url_rule('/api/v1/user/<uuid(strict=False):uuid>/<kind:kind>', 'texture_put', texture.put, methods=['PUT'])
    app.add_url_rule('/api/v1/user/<uuid(strict=False):uuid>/<kind:kind>', 'texture_delete', texture.delete, methods=['DELETE'])


def configure_redis(app: Flask, redis: FlaskRedis):
    app.config["REDIS_URL"] = os.getenv("REDIS_URL")
    redis.init_app(app)
    app.redis = redis


def create_app(textures: BaseTextureRepo, users: BaseUserRepo, redis: FlaskRedis) -> Flask:
    app = Flask(__package__, root_path=os.path.dirname(__file__))
    FlaskUUID(app)
    FlaskTextureType(app)
    app.users = users
    app.textures = textures
    configure_error_handlers(app)
    configure_views(app)
    configure_redis(app, redis)
    return app
