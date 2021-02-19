# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Draft aware Record Resource Config override."""

from flask_resources.parsers import URLArgsParser
from invenio_records_resources.resources import \
    RecordResourceConfig as _RecordResourceConfig
from invenio_records_resources.resources.records.schemas_url_args import \
    SearchURLArgsSchema
from marshmallow import fields, validate

from ..drafts.schemas_links import DraftLinksSchema


class DraftSearchURLArgsSchema(SearchURLArgsSchema):
    """Validate status parameter in addition to normal search parameters."""

    status = fields.Str(
        validate=validate.OneOf(["published", "draft"]),
        missing="published",
    )


class RecordResourceConfig(_RecordResourceConfig):
    """Draft aware Record resource config."""

    request_url_args_parser = {
        "search": URLArgsParser(DraftSearchURLArgsSchema)
    }

    draft_links_config = {
        "record": DraftLinksSchema
    }
