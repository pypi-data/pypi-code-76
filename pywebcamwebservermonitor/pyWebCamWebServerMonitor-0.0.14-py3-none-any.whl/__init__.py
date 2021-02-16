
import os

#/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, make_response
from flask_httpauth import HTTPBasicAuth
from types import MethodType
from flask import send_from_directory
#from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time
import pathlib
import builtins
from functools import wraps

main_dir = os.path.dirname(os.path.abspath(__file__))

dir_needed = ("{}{}".format(main_dir, "/db"), "{}{}".format(main_dir,
                                                            "/videos"), "{}{}".format(main_dir, "/stream"))

for app_dir in dir_needed:
    if os.path.isdir(app_dir) is False:
        os.mkdir(app_dir)

database_file = "{}{}".format(main_dir, "/db/_appdb.db")
database_URI = "sqlite:///{}".format(database_file)
dbExists = pathlib.Path(database_file).exists()
static_path = main_dir + '/web/static'

db = SQLAlchemy()

basicAuth = HTTPBasicAuth()


def overwrite_auth_error_handler(self, f):
    @wraps(f)
    def decorated(*args, **kwargs):
        res = f(*args, **kwargs)
        res = make_response(res)
        return res
    self.auth_error_callback = decorated
    return decorated


basicAuth.error_handler = MethodType(overwrite_auth_error_handler, basicAuth)

auth = basicAuth


cors = CORS()

app_settings_dict = {
    'default_webcam': '/dev/video0',
    'is_encoding': True,
    'frame_rate_no': 15,
    'is_auto_naming': True,
    'is_stream': False,
    'default_size_for_cam': '1280x720'
}


def create_app():
    app = Flask(__name__, static_url_path='/web/static')
    app.config.from_object(
        'pyWebCamWebServerMonitor.settings.DevelopmentConfig')
    app.config["SQLALCHEMY_DATABASE_URI"] = database_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        # socketio.init_app(app)
        cors.init_app(app)

        from . import models, routes, api, middleware

        models.init_app(app)
        if not dbExists:
            db.create_all()
            db.session.commit()
            create_admin_user()
            create_default_settings()
            print('DB Created & Seeded')
            print('DB at: ' + database_file)

        set_default_db_options()
        routes.init_app(app)
        middleware.init_app(app)
        serve_static_files(app)

    @app.teardown_appcontext
    def close_connection(exception):
        if db is not None:
            db.session.close()

    return app


def create_default_settings():
    from pyWebCamWebServerMonitor.models.setting import Setting

    for key in app_settings_dict:
        if Setting.query.filter_by(name=key).first() is not None:
            continue
        else:
            setting = Setting(name=key, value=str(app_settings_dict[key]))
            db.session.add(setting)
            db.session.commit()


def create_admin_user():
    from pyWebCamWebServerMonitor.models.user import User
    if User.query.filter_by(username="admin").first() is not None:
        return
    user = User(username="admin")
    user.hash_password("admin")
    db.session.add(user)
    db.session.commit()


def set_default_db_options():
    from pyWebCamWebServerMonitor.models.setting import Setting
    from pyWebCamWebServerMonitor.api.webcam import change_setting
    from distutils.util import strtobool

    ex_row_admin_missing = Exception(
        'The admin row is missing form db this should have not happen - recreate the admin User')

    try:
        from pyWebCamWebServerMonitor.models.user import User
        user = User.query.filter_by(username="admin").first()
        if user is None:
            raise ex_row_admin_missing
    except Exception as error:
        print(repr(error))
        create_admin_user()

    ex_row_setting_missing = Exception(
        'A setting row is missing this should have not happen - recreate settings')

    try:

        for key in app_settings_dict:
            setting = Setting.query.filter_by(name=key).first()
            if (setting) is not None:
                typeOfValue = type(app_settings_dict[key]).__name__
                if typeOfValue == 'bool':
                    value = bool(strtobool(setting.value))
                else:
                    value = getattr(builtins, typeOfValue)(setting.value)
                change_setting(key, value)
            else:
                raise ex_row_setting_missing

    except Exception as error:
        print(repr(error))
        create_default_settings()
        set_default_db_options()


def serve_static_files(app):
    @app.route('/')
    def static_index():
        return send_from_directory(static_path, 'index.html')

    @app.route('/<path:path>')
    def static_serve(path):
        return send_from_directory(static_path, path)
