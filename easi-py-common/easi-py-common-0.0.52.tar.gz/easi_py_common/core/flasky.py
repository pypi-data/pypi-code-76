import decimal
import json

import orjson
import logging
import os

from flask import Flask, Blueprint, render_template, request, current_app

from flask.logging import default_handler
from flask_sqlalchemy import get_debug_queries
from flaskerk import Flaskerk
from flaskerk.view import APIview
from pydantic import BaseModel, ValidationError

from easi_py_common.core.env import EnvHelper
from werkzeug.utils import find_modules, import_string

from easi_py_common.core.error import ServiceException, intercept_service_exception
from easi_py_common.core.redis import redis_store, redis_ro_store
from easi_py_common.core.sql_alchemy import db
from easi_py_common.core.monkey_doc import validate
from easi_py_common.sqs.producer import producer


class ORJSONDecoder:

    def __init__(self, **kwargs):
        self.options = kwargs

    @staticmethod
    def decode(obj):
        return orjson.loads(obj)


class ORJSONEncoder:

    def __init__(self, **kwargs):
        self.options = kwargs

    @classmethod
    def encode(cls, obj):
        return json.dumps(obj, default=cls.default)
        # try:
        #     return orjson.dumps(obj, default=cls.default)
        # except TypeError:
        #     return json.dumps(obj, default=cls.default)

    @classmethod
    def default(cls, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        raise TypeError


router_notes = {}
menu_map = {}


def wrap_route(self, rule=None, menu=None, **options):
    if rule is not None:
        url_path = rule
        if self.url_prefix:
            url_path = '{0}{1}'.format(self.url_prefix, rule if rule.startswith('/') else '/{0}'.format(rule))

        url_path = url_path.replace("//", "/")
        methods = options.get('methods', None)
        router_notes[url_path] = methods

        methods = options.get('methods', None)
        if methods is None or ('get' in methods or 'GET' in methods):
            if '<' not in url_path and menu:
                menu_data = list(menu)
                if len(menu_data) == 2:
                    menu_key = menu_data[0]
                    menu_name = menu_data[1]

                    menu_map[url_path] = dict(
                        url_prefix=self.url_prefix,
                        menu_name=menu_name,
                        menu_icon='',
                        url_path=url_path,
                        menu_key=menu_key,
                        is_front_router=0,
                        blue_name=self.name if self.name else ''
                    )
    else:
        if menu:
            menu_data = list(menu)
            if len(menu_data) == 3:
                menu_key = menu_data[0]
                menu_name = menu_data[1]
                menu_url = menu_data[2]

                menu_map[menu_key] = dict(
                    url_prefix=self.url_prefix,
                    menu_name=menu_name,
                    menu_icon='',
                    url_path=menu_url,
                    menu_key=menu_key,
                    is_front_router=1,
                    blue_name=self.name if self.name else ''
                )

    def decorator(f):
        if rule is None:
            return f
        endpoint = options.pop("endpoint", f.__name__)
        self.add_url_rule(rule, endpoint, f, **options)
        return f

    return decorator


def custom_api_doc_view(self):
    assert self.config.ui in self.config._support_ui
    mode = request.args.get('mode')
    ui_file = 'redoc.html'
    if mode == 'swagger':
        ui_file = 'swagger.html'
    return render_template(ui_file, spec_url=self.config.filename)


class AppHelper:
    @staticmethod
    def get_menu():
        return dict(**menu_map)


old_bypass = Flaskerk.bypass


def new_bypass(self, func):
    if not hasattr(func, 'tags'):
        return True
    if 'ignore' in func.tags:
        return True

    return old_bypass(self, func)


class AppWrapper:

    def __init__(self, name: str):
        self.app = self._create_app(name)

    def get_app(self) -> Flask:
        return self.app

    def ctx(self):
        return self.app.app_context()

    def _create_app(self, name: str) -> Flask:
        APIview.get = custom_api_doc_view
        Blueprint.route = wrap_route
        Flaskerk.validate = validate
        Flaskerk.bypass = new_bypass

        app = Flask(name)

        app.config.from_object("config.default")
        env = os.environ.get("ENV")
        if env is not None:
            app.config.from_object("config.{}".format(env))
        else:
            app.config.from_object("config.dev")

        app.json_encoder = ORJSONEncoder
        app.json_decoder = ORJSONDecoder

        db.init_app(app)
        redis_store.init_app(app)
        redis_ro_store.init_app(app)

        self._install_pydantic()

        @app.errorhandler(ServiceException)
        @intercept_service_exception
        def intercept_service_error(e):
            raise e

        @app.errorhandler(ValidationError)
        @intercept_service_exception
        def validation_error(e):
            raise e

        @app.after_request
        def after_request(response):
            if not EnvHelper.is_prod() and 'FLASKY_SLOW_DB_QUERY_TIME' in current_app.config:
                for query in get_debug_queries():
                    if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
                        current_app.logger.warning(
                            'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' %
                            (query.statement, query.parameters, query.duration,
                             query.context))
            return response

        _format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=_format)
        logger = logging.getLogger()
        app.logger.removeHandler(default_handler)
        if app.config['ENV'] == 'production':
            logger.setLevel(logging.ERROR)
        return app

    def start_producer(self, log_app_name='delivery'):
        producer.start(self.app, log_app_name=log_app_name)

    def register_blueprints(self, path: str = None):
        path = path if path else self.app.import_name
        path = path.replace("-", "_")
        for name in find_modules(path, recursive=True, include_packages=False):
            if 'wsgi' in name:
                continue
            module = import_string(name)
            if hasattr(module, "mod") and isinstance(module.mod, Blueprint):
                self.app.register_blueprint(module.mod)

    def register_blueprint(self, mod: Blueprint):
        for name in find_modules(mod.import_name, recursive=True, include_packages=False):
            import_string(name)
        self.app.register_blueprint(mod)

    def auto_import(self, path: str = None):
        path = path if path else self.app.import_name
        path = path.replace("-", "_")
        for name in find_modules(path, recursive=True, include_packages=False):
            import_string(name)

    def print_router(self):
        for path, methods in router_notes.items():
            self.app.logger.info('{}, {}'.format(path, methods))

    def _install_pydantic(self):
        def orjson_dumps(v, *, default):
            return orjson.dumps(v, default=default).decode()

        BaseModel.Config.orm_mode = True
        BaseModel.Config.json_loads = orjson.loads
        BaseModel.Config.json_dumps = orjson_dumps

    def install_doc(self, doc: Flaskerk):
        doc.register(self.app)
