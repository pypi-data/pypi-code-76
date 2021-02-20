# -*- coding: utf-8 -*-

__doc__ = """This module implements some scrapers.
"""

from pathlib import Path

__version__ = "0.0.4"

# define the log dir which is created in the same folder this projcet is ran
LOG_DIR = Path("./log")
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
