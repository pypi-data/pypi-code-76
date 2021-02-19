# encoding: utf-8

import importlib.util
import os

for directory in os.listdir("features/tests/"):
    if os.path.isdir("features/tests/%s" % directory):
        # Let's import all "steps*" file from this folder
        for filename in os.listdir("features/tests/%s" % directory):
            if filename.startswith("steps"):
                path = "features/tests/%s/%s" % (directory, filename)
                spec = importlib.util.spec_from_file_location(filename, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
