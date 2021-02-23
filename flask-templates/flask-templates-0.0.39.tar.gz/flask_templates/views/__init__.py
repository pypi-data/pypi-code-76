# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------
    File Name:              __init__.py
    Description:            
    Author:                 hzy
    date:                   2019/8/23
------------------------------------------------------------------
    Change Activity:
                            2019/8/23
------------------------------------------------------------------
"""
__author__ = 'hzy'

import time
from flask import Blueprint

api = Blueprint('api', __name__)
point = api
# point = Blueprint('point', __name__)

from flask_templates.views import example

if __name__ == "__main__":
    start_t = time.time()

    pass

    print("use time: %s" % (time.time() - start_t))
