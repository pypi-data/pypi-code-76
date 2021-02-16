# -*- coding: utf-8 -*-
import os
DB_URL = {'sly': 'mysql+mysqlconnector://quant:quant@192.168.199.137/quant' if 'SYL_DB' not in os.environ else os.environ['SYL_DB']}

server = ('192.168.199.137', 50006, 'api.jdw.smartdata-x.top', 443)