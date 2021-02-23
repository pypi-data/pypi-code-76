# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------
    File Name:              example
    Description:            
    Author:                 hzy
    date:                   2019/8/24
------------------------------------------------------------------
    Change Activity:
                            2019/8/24
------------------------------------------------------------------
"""
__author__ = 'hzy'

import time
from flask_templates.service.base import check_auth
from flask_templates.var import VISITOR_ID


# @check_auth()
def index(**kwargs):
    # da=WealthArticleDao()
    # res = da.insert(title='1233',title_image='12da',content='dasdad')
    # res2 = da.insert(title='12333', title_image='12da', content='dasdad')
    # res2 = WealthArticleDao().insert(title='1233',title_image='12da',content='dasdad')
    return f'example {kwargs[VISITOR_ID]}:hello,world!'


