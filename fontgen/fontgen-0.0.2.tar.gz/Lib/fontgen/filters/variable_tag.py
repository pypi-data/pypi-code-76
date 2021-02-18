from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from typing import Set

from ufo2ft.filters import BaseFilter
from ufoLib2.objects.font import Font
from ufoLib2.objects.glyph import Glyph
import math
import re
import datetime

from fontParts.world import CurrentFont

logger = logging.getLogger(__name__)

import json

class VariableTag(BaseFilter):

    def set_context(self, font: Font, glyphSet: Set[Glyph]):


        # For Variable fonts adding 'Variable' at the end of the font names

        tag = "Variable"
        family_name = font.info.familyName + " " + tag
        family_name_stripped = family_name.replace(" ", "")

        # Applying changes to family name

        font.info.familyName = family_name
        font.info.openTypeNamePreferredFamilyName = family_name

        font.info.postscriptFontName = family_name_stripped + "-" + font.info.styleName
        font.info.postscriptFullName = family_name + " " + font.info.styleName

        font.info.styleMapFamilyName = family_name

        print("Extended font family name with tag Variable")

        return super().set_context(font, glyphSet)

    def filter(self, glyph: Glyph):

        # if glyph.name in self.standard_nam:
        #     new_unicode = self.standard_nam[glyph.name]
        #     if glyph.unicode == self.standard_nam[glyph.name]:
        #         return False
        #     elif glyph.unicode:
        #         glyph.unicode = new_unicode
        #         del glyph.unicodes[1]
        #         print(f"Glyph: {glyph.name} assigned correct unicode {hex(glyph.unicode)}")
        #         return True
        #     else:
        #         glyph.unicode = new_unicode
        #         print(f"Glyph: {glyph.name} assigned new unicode {hex(glyph.unicode)}")
        #         return True

        return False
