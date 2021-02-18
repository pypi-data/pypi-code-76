from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from typing import Set

from ufo2ft.filters import BaseFilter
from ufoLib2.objects.font import Font
from ufoLib2.objects.glyph import Glyph
import math
import re
import datetime

logger = logging.getLogger(__name__)

import json
import os

class FixUnicode(BaseFilter):

    def set_context(self, font: Font, glyphSet: Set[Glyph]):

        # print("Base Dir:::::::::" + os.path.dirname(os.path.abspath(__file__)))
        # print(os.getcwd())
        unicode_dir = os.path.join((os.path.dirname(os.path.abspath(__file__))), "unicode.json")

        with open(unicode_dir) as f:
            self.standard_nam = json.load(f)

        return super().set_context(font, glyphSet)

    def filter(self, glyph: Glyph):

        if glyph.name in self.standard_nam:
            new_unicode = self.standard_nam[glyph.name]
            if glyph.unicode == self.standard_nam[glyph.name]:
                return False
            elif glyph.unicode:
                glyph.unicode = new_unicode
                del glyph.unicodes[1]
                print(f"Glyph: {glyph.name} assigned correct unicode {hex(glyph.unicode)}")
                return True
            else:
                glyph.unicode = new_unicode
                print(f"Glyph: {glyph.name} assigned new unicode {hex(glyph.unicode)}")
                return True

        return False
