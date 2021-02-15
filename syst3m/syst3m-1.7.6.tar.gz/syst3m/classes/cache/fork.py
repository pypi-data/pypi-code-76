#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from . import WebServer
import cl1, os
webserver = WebServer(serialized=ast.literal_eval(cl1.get_argument("--serialized")))
webserver.start()