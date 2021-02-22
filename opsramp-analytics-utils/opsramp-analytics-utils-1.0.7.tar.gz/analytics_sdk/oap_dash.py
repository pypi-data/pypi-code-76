import os
import json

import dash
import flask
import plotly
import pkgutil
import requests
import mimetypes
import dash_renderer
import dash_core_components as dcc

from dash._utils import stringify_id

from .utilities import (
    BASE_API_URL,
    call_get_requests
)

class OAPDash(dash.Dash):
    static_files = {
        'css': [
            'bootstrap.min.css'
        ],
        'js': [ ]
    }

    def __init__(self, **kwargs):
        self.route = kwargs.pop('route')
        route_prefix = '/'+self.route if self.route else ''
        # assume this is not set by user
        kwargs['requests_pathname_prefix'] = route_prefix + '/'

        super(OAPDash, self).__init__(**kwargs)

    def init_app(self, app=None):
        """
        serve custom static files
        """
        super(OAPDash, self).init_app(app)

        # register manifest file
        self._add_url("opsramp-analytics-utils/<string:file_name>", self.serve_resource)
        self._add_url("asset-manifest.json", self.serve_manifest)

    def is_authenticated(self):
        url = f'{BASE_API_URL}/api/v2/alertTypes'
        res = call_get_requests(url)

        return res.status_code == 200

    def index(self, *args, **kwargs):  # pylint: disable=unused-argument
        index = super(OAPDash, self).index(args, kwargs)

        # check auth
        REQUIRE_AUTH_REDIRECT = os.getenv('REQUIRE_AUTH_REDIRECT') == 'true'
        if not REQUIRE_AUTH_REDIRECT or self.is_authenticated():
            return index
        else:
            PLATFORM_ROUTE = os.getenv("PLATFORM_ROUTE", '')
            redirect_url = f"https://localhost/tenancy/web/login?cb=/{PLATFORM_ROUTE}"

            return flask.redirect(redirect_url, code=302)

    def serve_manifest(self):
        return {
            "files": {
                "main.css": "/main.css",
                "main.js": "/main.js",
                "main.js.map": "/analytics-apps/static/js/main.b42d7633.js.map",
                "index.html": "/analytics-apps/index.html",
            },
            "entrypoints": [
                "main.css",
                "main.js"
            ]
        }

    def serve_resource(self, file_name):
        if file_name == 'main.css':
            return self._serve_main_css()
        elif file_name == 'main.js':
            return self._serve_main_js()
        elif file_name == 'dummy_dash_renderer.js':
            return ''
        else:
            extension = "." + file_name.split(".")[-1]
            mimetype = mimetypes.types_map.get(extension, "application/octet-stream")

            return flask.Response(
                pkgutil.get_data('dash_core_components', file_name), mimetype=mimetype
            )

    def _serve_main_css(self):
        body = ''

        # TODO: external css files using requests
        external_links = self.config.external_stylesheets

        # oap css files
        for file_path in self.static_files['css']:
            body += pkgutil.get_data('analytics_sdk', 'assets/'+file_path).decode("utf-8")

        # custom css files
        for resource in self.css.get_all_css():
            file_name = resource['asset_path']
            body += open(self.config.assets_folder+'/'+file_name).read()

        response = flask.Response(body, mimetype='text/css')

        return response

    def _serve_main_js(self):
        body = f"var oap_config = {json.dumps(self._config(), cls=plotly.utils.PlotlyJSONEncoder)};\n"

        # external js files
        external_links = self.config.external_scripts
        # urllib

        # inline scripts
        # self._inline_scripts

        # oap js files
        for file_path in self.static_files['js']:
            body += pkgutil.get_data('analytics_sdk', 'assets/'+file_path).decode("utf-8")

        # system js files
        mode = "dev" if self._dev_tools["props_check"] is True else "prod"

        deps = []
        for js_dist_dependency in dash_renderer._js_dist_dependencies:
            dep = {}
            for key, value in js_dist_dependency.items():
                dep[key] = value[mode] if isinstance(value, dict) else value

            deps.append(dep)

        dev = self._dev_tools.serve_dev_bundles

        resources = (
            self.scripts._resources._filter_resources(deps, dev_bundles=dev)
          + self.scripts.get_all_scripts(dev_bundles=dev)
          + self.scripts._resources._filter_resources(dash_renderer._js_dist, dev_bundles=dev)
        )

        srcs = []
        for resource in resources:
            is_dynamic_resource = resource.get("dynamic", False)

            if "relative_package_path" in resource:
                paths = resource["relative_package_path"]
                paths = [paths] if isinstance(paths, str) else paths

                for rel_path in paths:
                    self.registered_paths[resource["namespace"]].add(rel_path)

                    if not is_dynamic_resource:
                        _body = pkgutil.get_data(resource["namespace"], rel_path).decode("utf-8")
                        body += self.pre_process(_body, rel_path, dev)
            # elif "external_url" in resource:
            #     if not is_dynamic_resource:
            #         if isinstance(resource["external_url"], str):
            #             srcs.append(resource["external_url"])
            #         else:
            #             srcs += resource["external_url"]
            # elif "asset_path" in resource:
            #     static_url = self.get_asset_url(resource["asset_path"])
            #     # Add a cache-busting query param
            #     srcs.append(static_url)

        # from pprint import pprint
        # import pdb;pdb.set_trace()
        body += "var renderer = new DashRenderer();"
        response = flask.Response(body, mimetype='application/javascript')

        return response

    def pre_process(self, txt_body, file_name, dev):
        if file_name.startswith('dash_renderer.'):
            txt_body = txt_body.replace("JSON.parse(document.getElementById('_dash-config').textContent);", "oap_config;")
            txt_body = txt_body.replace('JSON.parse(document.getElementById("_dash-config").textContent);', 'oap_config;')

        return txt_body + "\n"

    def get_component_ids(self, layout):
        component_ids = []
        for component in layout._traverse():
            component_id = stringify_id(getattr(component, "id", None))
            component_ids.append(component_id)

        return component_ids

    def _layout_value(self):
        """
        add custom stores
        """
        _layout = self._layout() if self._layout_is_function else self._layout                        

        component_ids = self.get_component_ids(_layout)
        in_store_id = "_oap_data_in_" + self.route
        out_store_id = "_oap_data_out_" + self.route
        
        if in_store_id not in component_ids:
            _layout.children.append(dcc.Store(id="dummy-store"))
            _layout.children.append(dcc.Store(id=out_store_id, storage_type="local"))
            _layout.children.append(dcc.Store(id=in_store_id, storage_type="local"))

        return _layout

    def _generate_renderer(self):
        return f"""
            <script id="_dash-renderer" type="application/javascript"></script>
            <script src="{self.config.requests_pathname_prefix}opsramp-analytics-utils/dummy_dash_renderer.js"></script>
        """

    def _generate_config_html(self):
        return '<script id="_dash-config" type="application/json"></script>'

    def _generate_css_dist_html(self):
        return f'<link rel="stylesheet" href="{self.config.requests_pathname_prefix}opsramp-analytics-utils/main.css">'

    def _generate_scripts_html(self):
        return f'<script src="{self.config.requests_pathname_prefix}opsramp-analytics-utils/main.js"></script>'
