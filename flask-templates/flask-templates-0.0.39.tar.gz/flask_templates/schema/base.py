#!/usr/bin/env python
# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, INCLUDE, EXCLUDE
from datetime import datetime
from flask_templates.views.base import ViewValidationError


class DateTimeEXT(fields.DateTime):
    """
    Class extends marshmallow standart DateTime with "timestamp" format.
    """

    SERIALIZATION_FUNCS = \
        fields.DateTime.SERIALIZATION_FUNCS.copy()
    DESERIALIZATION_FUNCS = \
        fields.DateTime.DESERIALIZATION_FUNCS.copy()

    SERIALIZATION_FUNCS['timestamp'] = lambda x: x.timestamp()
    DESERIALIZATION_FUNCS['timestamp'] = lambda x: datetime.fromtimestamp(float(x))


class ViewBaseSchema(Schema):
    def handle_error(self, exc, data, **kwargs):
        raise ViewValidationError(str(exc.messages), data)

    def validate_s(self,
                      data,
                      *,
                      many: bool = None,
                      partial):
        self._do_load(data, many=many, partial=partial, postprocess=False)


class ReqSchema(Schema):
    token = fields.Str(required=True)

    def handle_error(self, exc, data, **kwargs):
        raise ViewValidationError(str(exc.messages), data)



