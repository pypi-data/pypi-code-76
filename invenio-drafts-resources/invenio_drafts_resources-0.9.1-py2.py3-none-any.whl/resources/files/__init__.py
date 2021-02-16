# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Resources module to create REST APIs."""

from .config import DraftFileActionResourceConfig, DraftFileResourceConfig, \
    RecordFileActionResourceConfig, RecordFileResourceConfig
from .resource import DraftFileActionResource, DraftFileResource, \
    RecordFileActionResource, RecordFileResource

__all__ = (
    "DraftFileResourceConfig",
    "DraftFileResource",
    "DraftFileActionResourceConfig",
    "DraftFileActionResource",
    "RecordFileResourceConfig",
    "RecordFileActionResourceConfig",
    "RecordFileResource",
    "RecordFileActionResource",
)
