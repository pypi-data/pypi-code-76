#!/usr/bin/env python
# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains tools to load and validate options dictionaryfiles.

# Copyright (C) 2018  Niklas Bohn (GFZ, <nbohn@gfz-potsdam.de>),
# German Research Centre for Geosciences (GFZ, <https://www.gfz-potsdam.de>)

# This software was developed within the context of the EnMAP project supported by the DLR Space Administration with
# funds of the German Federal Ministry of Economic Affairs and Energy (on the basis of a decision by the German
# Bundestag: 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.


from os.path import isfile
from jsmin import jsmin
from cerberus import Validator
from os import path
import json
import warnings
from .sicor_enmap_schema import sicor_enmap_schema


def _processing_dict():
    return {"Exception": None,
            "interface": {"args": (), "kwargs": {}},
            "Exception_type": "",
            "clear_fraction": None,
            "status": 1,
            "tIO": 0.0,
            "tRT": 0.0,
            "uncertainties": {}
            }


# noinspection PyClassHasNoInit
class SicorrValidator(Validator):
    def _validate_existing_path(self, existing_path, field, value):
        """ Test whether a given sting points an existing path

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        if existing_path is True and path.isdir(value) is False:
            warnings.warn("Path '%s' should exist." % value)


def json_to_python(dd):
    if type(dd) is dict:
        return {json_to_python(k): json_to_python(v) for k, v in dd.items()}
    elif type(dd) is list:
        return [json_to_python(v) for v in dd]
    else:
        if dd == "None":
            return None
        if dd == "slice(None, None, None)":
            return slice(None)
        if dd == "10.0":
            return 10.0
        if dd in ["10.0", "20.0", "60.0"]:
            return float(dd)
        if dd == "true":
            return True
        if dd == "false":
            return False
        else:
            return dd


def python_to_json(dd):
    if type(dd) is dict:
        return {python_to_json(k): python_to_json(v) for k, v in dd.items()}
    elif type(dd) is list:
        return [python_to_json(v) for v in dd]
    else:
        if dd is None:
            return "None"
        if dd == slice(None):
            return "slice(None, None, None)"

        if dd is True:
            return "true"
        if dd is False:
            return "false"
        else:
            return dd


def get_options(target, validation=True):
    """
    return dictionary will all options
    :param validation: True / False, whether to validate options read from files ot not
    :param target: if path to file, then json is used to load, otherwise the default template
    is used
    :return: dictionary with options
    """

    if isfile(target):
        with open(target, "r") as fl:
            options = json_to_python(json.loads(jsmin(fl.read())))
            options["processing"] = _processing_dict()

        if validation is True:
            vv = SicorrValidator(allow_unknown=True, schema=sicor_enmap_schema)
            if vv.validate(document=options) is False:
                raise ValueError("Options is malformed: %s" % str(vv.errors))

        return options
    else:
        raise FileNotFoundError("target:%s is not a valid file path" % target)
