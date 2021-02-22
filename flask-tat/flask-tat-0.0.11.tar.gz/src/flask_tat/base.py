#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
from flask.blueprints import Blueprint
from cdumay_rest_client.client import RESTClient


class BaseTATClient(object):
    def __init__(self, app=None):
        self.app = None
        self.blueprint = None
        self.blueprint_setup = None
        self._client = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if isinstance(app, Blueprint):
            app.record(self._deferred_blueprint_init)
        else:
            self._init_app(app)

    def _deferred_blueprint_init(self, setup_state):
        self._init_app(setup_state.app)

    def _init_app(self, app):
        """"""
        app.config.setdefault('TAT_URL', 'http://127.0.0.1')
        app.config.setdefault('TAT_USERNAME', 'test')
        app.config.setdefault('TAT_PASSWORD', 'test')
        app.config.setdefault("TAT_SSL_VERIFY", True)
        self.app = app

    @property
    def client(self):
        if self._client is None:
            self._client = RESTClient(
                server=self.app.config['TAT_URL'],
                headers={
                    "Tat_username": self.app.config["TAT_USERNAME"],
                    "Tat_password": self.app.config["TAT_PASSWORD"],
                    "Content-type": "application/json",
                },
                ssl_verify=self.app.config["TAT_SSL_VERIFY"],
            )

        return self._client
