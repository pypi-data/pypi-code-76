# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------
    File Name:              manage
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
from datetime import datetime

from flask_templates.common.logger import logger
from flask_templates import FlaskTemplate
from flask_templates.configs.template import WEB_CONFIG
from flask_templates.nacosinstance import NacosClient
from flask_templates.common.class_holder import class_register,class_getter,ClassHolder

app = FlaskTemplate().app
conf = WEB_CONFIG


@app.route('/')
def index():
    logger.error('error test')
    return 'hello,world!'

@class_register()
class Register:

    @class_register()
    class RegisterInner(NacosClient):
        pass

    @property
    @class_getter(NacosClient)
    def nacos_client(self):
        pass

    def __init__(self):
        self.nacos_client.start_heartbeat(app)

if __name__ == "__main__":
    start_t = time.time()
    logger.info('^v^ ^V^server start on {}'.format(conf['port']))
    app.run(host=conf['host'], port=conf['port'], debug=True, use_reloader=False)
    pass

    print("use time: %s" % (time.time() - start_t))
