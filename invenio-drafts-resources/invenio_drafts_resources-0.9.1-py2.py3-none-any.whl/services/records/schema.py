# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Record schema."""

from invenio_records_resources.services.records.schema import \
    RecordSchema as RecordSchemaBase
from marshmallow import fields, pre_load


class RecordSchema(RecordSchemaBase):
    """Schema for records in JSON."""

    conceptid = fields.Str(dump_only=True)
    expires_at = fields.Str(dump_only=True)

    @pre_load
    def clean(self, data, **kwargs):
        """Removes dump_only fields."""
        keys = [
            '$schema',
            'conceptid',
            'conceptpid',
            'created',
            'created',
            'expires_at',
            'fork_version_id',
            'pid',
            'updated',
            'uuid',
            'version_id',
        ]
        for k in keys:
            data.pop(k, None)
        return data
