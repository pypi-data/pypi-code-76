# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Record File Resources."""

# from flask import abort, g
from flask_resources import CollectionResource
from invenio_records_resources.config import ConfigLoaderMixin
from invenio_records_resources.resources import FileActionResource, \
    FileResource
from invenio_records_resources.resources.actions import ActionResource

from .config import DraftFileActionResourceConfig, DraftFileResourceConfig, \
    RecordFileActionResourceConfig, RecordFileResourceConfig


class RecordFileResource(CollectionResource, ConfigLoaderMixin):
    """Record file resource.

    It does not inherit from Invenio-Records-Resources::FileResource to
    disable the queries to any other endpoint (e.g. create), which otherwise
    would need to be overwritten. Here they are merely not implemented.
    """

    default_config = RecordFileResourceConfig

    def __init__(self, config=None, service=None):
        """Constructor."""
        super(RecordFileResource, self).__init__(
            config=self.load_config(config))
        self.service = None  # Force user's set up

    # ListView GET
    def search(self, *args, **kwargs):
        """List files."""
        return None, 200

    # ItemView GET
    def read(self, *args, **kwargs):
        """Read a single file."""
        return None, 200


# ActionResource inherits ConfigLoaderMixin
class RecordFileActionResource(ActionResource):
    """Record file action resource."""

    default_config = RecordFileActionResourceConfig


class DraftFileResource(FileResource):
    """File resource."""

    default_config = DraftFileResourceConfig

    # TODO: No constructor for now.
    # Required when service level implementation.


# ActionResource inherits ConfigLoaderMixin
class DraftFileActionResource(FileActionResource):
    """File action resource.

    NOTE: `Commit` exists as an action to avoid having to split the
    `FileResource` into Collection + Singleton to have to POST operations.
    """

    default_config = DraftFileActionResourceConfig
