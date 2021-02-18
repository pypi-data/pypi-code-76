#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import json


def read_json(file):
    """ Read json file.
    """

    with open(file) as f:
        return json.load(f)


def write_json(dic, file):
    """ Write a dictionary into json.
    """

    with open(file, 'w') as f:
        json.dump(dic, f)