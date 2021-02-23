# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------
    File Name:              __init__.py
    Description:            
    Author:                 hzy
    date:                   2020/11/17
------------------------------------------------------------------
    Change Activity:
                            2020/11/17
------------------------------------------------------------------
"""
__author__ = 'hzy'

from flask import Flask
from flask_cors import CORS
from flask_templates.configs import config_update, BEFORE_CONFIG, BASE_CONFIG, template, nacos, before_config_filename, \
    config_replace
from flask_templates.var import API_PREFIX_PATH, POINT_PREFIX_PATH
from flask_templates.common.logger import logger
import time


class FlaskTemplate:

    def __init__(self, resource_path='project/resource', setting={}, *args, **kwargs):
        self.fresh_scope(resource_path=resource_path, setting=setting)
        self.app = self.create_app(*args, **kwargs)
        self.web_config = template.WEB_CONFIG

    @staticmethod
    def fresh_scope(resource_path='project/resource', setting={}):
        before_config = config_update(src_config=BEFORE_CONFIG, resource_path=resource_path,
                                      call_fix=[nacos.config_fix], src_config_filename=before_config_filename)
        config_replace(before_config)
        config_update(resource_path=resource_path, setting=before_config, final_setting=setting,
                      call_fix=[template.config_fix])

    @staticmethod
    def fresh_scope_final():
        config_replace(BASE_CONFIG)

    @staticmethod
    def create_app(*args, **kwargs):
        app = Flask(__name__)
        # init()
        from flask_templates.views import api as api_blueprint
        app.register_blueprint(api_blueprint, url_prefix=API_PREFIX_PATH)

        from flask_templates.views import point as point_blueprint
        app.register_blueprint(point_blueprint, url_prefix=POINT_PREFIX_PATH)

        CORS(app, supports_credentials=True)
        app.logger = logger
        return app

    def run(self, **kwargs):
        app_run_params = self.web_config.copy()
        app_run_params.update(kwargs)
        self.app.run(host=app_run_params.pop('host', None), port=app_run_params.pop('port', None),
                     debug=app_run_params.pop('debug', None),
                     load_dotenv=app_run_params.pop('load_dotenv', True))


if __name__ == "__main__":
    start_t = time.time()

    pass

    print("use time: %s" % (time.time() - start_t))
