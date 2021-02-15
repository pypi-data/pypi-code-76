#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, cl1
sys.path.insert(1, Formats.FilePath(__file__, back=4))
from syst3m.classes.cache import WebServer
webserver = WebServer(serialized=ast.literal_eval(cl1.get_argument("--serialized")))
webserver.start()