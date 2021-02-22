#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    flaskext.mongobit
    ~~~~~~~~~~~~~~~~~

    MongoBit support in Flask.

    :copyright: (c) 2012 by Lix Xu.
    :license: BSD, see LICENSE for more details.

"""

from mongobit.base import Model as BaseModel
from mongobit.fields import fields
from mongobit.mongobit import MongoBit as BaseBit

__version__ = "0.3.1"


class MongoBit(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config["alias"] = app.name
        self.app = app
        self.mongo = BaseBit(app.config)

        class Model(BaseModel):
            _db_alias = app.name

        self.model = Model

        self.str = fields.str
        self.string = fields.string
        self.unicode = fields.unicode
        self.text = fields.text
        self.list = fields.list
        self.dict = fields.dict
        self.tuple = fields.tuple
        self.int = fields.int
        self.float = fields.float
        self.date = fields.date
        self.datetime = fields.datetime
        self.objectid = fields.objectid
        self.bool = fields.bool
        self.any = fields.any

    @property
    def connection(self):
        return self.mongo.connection

    @property
    def database(self):
        return self.mongo.database

    def close(self):
        try:
            self.connection.close()
        except Exception:
            pass
