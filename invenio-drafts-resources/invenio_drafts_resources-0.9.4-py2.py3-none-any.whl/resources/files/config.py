# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""File resource configuration."""

from flask_resources.resources import ResourceConfig
from invenio_records_resources.resources import FileActionResourceConfig
from invenio_records_resources.resources import \
    FileResourceConfig as RecordFileResourceConfig
from invenio_records_resources.resources.actions import ActionResourceConfig


class RecordFileActionResourceConfig(FileActionResourceConfig):
    """Record resource config."""

    list_route = "/records/<pid_value>/files/<key>/<action>"
    action_commands = {
        'create': {},
        'read': {
            'content': 'download_file'
        },
        'update': {},
        'delete': {}
    }


class DraftFileResourceConfig(RecordFileResourceConfig):
    """Record resource config."""

    item_route = "/records/<pid_value>/draft/files/<key>"
    list_route = "/records/<pid_value>/draft/files"


class DraftFileActionResourceConfig(FileActionResourceConfig):
    """Record resource config."""

    list_route = "/records/<pid_value>/draft/files/<key>/<action>"
    action_commands = {
        'create': {
            'commit': 'commit_file'
        },
        'read': {
            'content': 'get_file_content'
        },
        'update': {
            'content': 'set_file_content'
        },
        'delete': {}
    }
