from ufo2ft.filters import loadFilters
from .filters import FixUnicode, FixFontinfo, VariableTag, MatraiSub, MatraiGen
# from extras import config
from os import path
import json, os

BASE_DIR = os.getcwd()
TEMP_DIR = os.path.join(BASE_DIR,"temp")

class setFilters:

    def loadFilters_patched(ufo):
        preFilters, postFilters = loadFilters(ufo=ufo)

        import sys
        sys.path.append(path.join(path.dirname(__file__), '..'))
        import fontgen

        # c = config.fontmake
        # d = build.setfilters

        with open(os.path.join(TEMP_DIR, "flags"), 'r') as f:
            variable_tag = json.load(f)

        if variable_tag:
            pre = [FixFontinfo, VariableTag] # FixUnicode
        else:
            pre = [FixFontinfo]

        # custom added filters
        post = [ ]

        for fClass in pre:
            filterObj = fClass()
            preFilters.append(filterObj)

        for postClass in post:
            postObj = postClass()
            postFilters.append(postObj)

        return preFilters, postFilters