# Wrapper for Git and Git LFS
#
# Copyright (C) 2021 Collabora Ltd
# Andrej Shadura <andrew.shadura@collabora.co.uk>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import os
from pathlib import Path
from typing import Optional

import sh.contrib


def git(*args, index: Optional[Path] = None, **kwargs):
    """
    Wrapper for Git and Git LFS

    Differences from sh.contrib.git:
        * accepts index argument to set GIT_INDEX_FILE
    """
    e = os.environ.copy()
    if index:
        e["GIT_INDEX_FILE"] = str(index)
    return sh.contrib.git(*args, **kwargs, _env=e)


git.lfs = sh.contrib.git.lfs
