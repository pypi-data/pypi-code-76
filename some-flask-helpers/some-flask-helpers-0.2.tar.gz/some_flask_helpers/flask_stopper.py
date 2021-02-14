# -*- coding: utf-8 -*-

# Copyright (C) 2019  Marcus Rickert
#
# See https://github.com/marcus67/some_flask_helpers
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import logging
import urllib.parse
import uuid
from os.path import join

import flask
import requests

import some_flask_helpers
from some_flask_helpers import blueprint_adapter

SHUTDOWN_BLUEPRINT_NAME = "_shutdown"
SHUTDOWN_BLUEPRINT_ADAPTER = blueprint_adapter.BlueprintAdapter()


class FlaskStopper(object):

    def __init__(self, p_app, p_logger=None):

        self._app = p_app
        self._logger = p_logger

        if self._logger is None:
            self._logger = logging.getLogger('flaskstopper')

        # Install the shutdown handler
        self._blueprint = flask.Blueprint(SHUTDOWN_BLUEPRINT_NAME, some_flask_helpers.__name__)
        SHUTDOWN_BLUEPRINT_ADAPTER.assign_view_handler_instance(p_blueprint=self._blueprint, p_view_handler_instance=self)
        SHUTDOWN_BLUEPRINT_ADAPTER.check_view_methods()
        self._app.register_blueprint(self._blueprint)
        self._secret = "UNSET"

    def set_secret(self, p_secret):
        self._secret = p_secret

    @SHUTDOWN_BLUEPRINT_ADAPTER.route_method(p_rule="/shutdown/<p_secret>")
    def shutdown(self, p_secret=None):

        if self._secret is None or p_secret != self._secret:
            return flask.Response("Shutdown secret required!")

        shutdown_proc = flask.globals.request.environ.get('werkzeug.server.shutdown')

        if shutdown_proc is None:
            raise RuntimeError('Not running with the Werkzeug server')

        shutdown_proc()
        return flask.Response("Shutting down...")

    def stop(self, host=None, port=None):

        if host is None:
            host = '127.0.0.1'
        if port is None:
            server_name = self._app.config['SERVER_NAME']
            if server_name and ':' in server_name:
                port = int(server_name.rsplit(':', 1)[1])
            else:
                port = 5000

        try:

            # Siehe https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
            self.secret = uuid.uuid1().hex
            self.set_secret(p_secret=self.secret)

            url = urllib.parse.urlunsplit(
                (
                    'http',
                    "%s:%d" % (host, port),
                    join("/shutdown", self.secret),
                    None,
                    None
                ))

            msg = "Sending shutdown API request '{url}'"
            self._logger.info(msg.format(url=url))

            r = requests.get(url, stream=False)
            r.raise_for_status()
            r.close()


        except Exception as e:

            msg = "Exception '{exception}' while shutting down the web server"
            self._logger.error(msg.format(exception=str(e)))

    def destroy(self):
        SHUTDOWN_BLUEPRINT_ADAPTER.unassign_view_handler_instances()