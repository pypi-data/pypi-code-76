#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""setup.py"""

import os
import codecs
import setuptools
# from usb_imager import appinfo


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as filepath:
        return filepath.read()


def get_info(info: str):
    rel_path = "usb_imager/appinfo.py"
    for line in read(rel_path).splitlines():
        if line.startswith(info):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]

    raise RuntimeError("Unable to find info string.")


setuptools.setup(
    name=get_info("__appname__"),
    license=get_info("__license__"),

    description=get_info("__description__"),

    url=get_info("__url_source__"),
    project_urls={'Source': get_info("__url_source__")},

    author=get_info("__author__"),
    author_email=get_info("__author_email__"),
)

# =============================================================================
# setuptools.setup(
#     name=appinfo.__appname__,
#     license=appinfo.__license__,
#
#     description=appinfo.__description__,
#
#     url=appinfo.__url_source__,
#     project_urls={'Source': appinfo.__url_source__},
#
#     author=appinfo.__author__,
#     author_email=appinfo.__author_email__
# )
# =============================================================================
