"""This module defines the enum UIPreferenceName.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from enum import Enum


class UIPreferenceName(str, Enum):
    rubric_editor_v2 = "rubric_editor_v2"
    no_msg_for_mosaic_1 = "no_msg_for_mosaic_1"
    no_msg_for_mosaic_2 = "no_msg_for_mosaic_2"
    no_msg_for_mosaic_3 = "no_msg_for_mosaic_3"
    no_msg_for_nobel = "no_msg_for_nobel"
    no_msg_for_nobel_1 = "no_msg_for_nobel_1"
