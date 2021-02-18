from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from typing import Set

from ufo2ft.filters import BaseFilter
from ufoLib2.objects.font import Font
from ufoLib2.objects.glyph import Glyph
import math
import re
import datetime

import pickle, fnmatch

from collections import defaultdict

from fontParts.world import CurrentFont

logger = logging.getLogger(__name__)

import json

import itertools
import os.path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMP_DIR = os.path.join(BASE_DIR, "temp")

class MatraiSub(BaseFilter):

    def set_context(self, font: Font, glyphSet: Set[Glyph]):

        # For Variable fonts adding 'Variable' at the end of the font names

        # if os.path.exists(os.path.join(TEMP_DIR, "flag")):
        #     print("Javado")
        #     return super().set_context(font, glyphSet)

        if 'dvmI_short' in glyphSet and 'dvmI_long' in glyphSet:
            print("In matrai_sub: Working on substitution algorithm")
            print("Here we will start writing MatraI matching script")

            # ufoPath = font.path

            # p = os.path.split(ufoPath)
            # q = os.path.join(BASE_DIR, "temp")
            # tempPath = os.path.join(q, p[1])

            listoffiles = os.listdir(TEMP_DIR)
            pattern = "*.pkl"
            pklfiles = []
            pattern_ufo = "*.ufo"
            ufofiles = []
            for entry in listoffiles:
                if entry == "bases.pkl":
                    continue
                else:
                    if fnmatch.fnmatch(entry, pattern):
                        pklfiles.append(entry)
            for ufoentry in listoffiles:
                if fnmatch.fnmatch(ufoentry, pattern_ufo):
                    ufofiles.append(ufoentry)

            generatedmi_1 = font.open(os.path.join(TEMP_DIR ,ufofiles[0]))
            generatedmi_2 = font.open(os.path.join(TEMP_DIR ,ufofiles[1]))

            with open(os.path.join(TEMP_DIR ,pklfiles[0]) ,  'rb' ) as a:
                matrai_1 = pickle.load(a)

            with open(os.path.join(TEMP_DIR ,pklfiles[1]) ,  'rb' ) as b:
                matrai_2 = pickle.load(b)

            with open(os.path.join(TEMP_DIR, "bases.pkl") , 'rb' ) as c:
                bases = pickle.load(c)

            print("Read all pkl files")

            match_dict = defaultdict(list)

            def find_match_matra(base, selected_matrai):
                for matra in selected_matrai:
                    for matchbase in matra.bases:
                        if matchbase.glyphs.name == base.glyphs.name:
                            return matra.name

            for base in bases:
                firstpair = find_match_matra(base, matrai_1)
                secondpair = find_match_matra(base, matrai_2)

                first_digit = re.findall("\d{2}", firstpair)
                second_digit = re.findall("\d{2}", secondpair)
                new_name = "dvmI." + first_digit[0] + second_digit[0]

                # Check if new name already exists in match_dict.
                # If it exists, there is no need to create new glyph

                if not match_dict[new_name]:
                    new_glyph_1 = generatedmi_1[firstpair].copy(new_name)
                    generatedmi_1.addGlyph(new_glyph_1)

                    new_glyph_2 = generatedmi_1[secondpair].copy(new_name)
                    generatedmi_2.addGlyph(new_glyph_2)

                print("new glyph added {}".format(new_name))

                match_dict[new_name].append(base.glyphs.name)

                print("Found both pair")

            p = os.path.split(font.path)
            current_font_ufo_name = p[1]

            if current_font_ufo_name == ufofiles[0]:
                for g1 in generatedmi_1:
                    if not g1.name in font:
                        font.addGlyph(g1)
                        print("Added glyphs is: " + g1.name)
                    else:
                        del font[g1.name]
                        print("Deleted glyphs is: " + g1.name)

            if current_font_ufo_name == ufofiles[1]:
                for g2 in generatedmi_2:
                    if not g2.name in font:
                        font.addGlyph(g2)
                        print("Added glyphs is: " + g2.name)
                    else:
                        del font[g2.name]
                        print("Deleted glyphs is: " + g2.name)

            glyphSet.clear()
            glyphSet.update(font)

            # Temporary saving fontufo
            font.save(os.path.join(BASE_DIR , "full_" + current_font_ufo_name ))
            print("Hello, I did some process")

            script_abbr_current = "dv"
            substitute_rule_lines = []
            name_default = script_abbr_current + "mI"

            for m in match_dict:
                n = match_dict[m]
                substitute_rule_lines.append(
                    "sub {}' [{}] by {};".format(
                        name_default,
                        " ".join(i for i in n),
                        m,
                    ),
                )

            print("Hey")

            def save_object(obj, filename):
                with open(filename, 'wb') as output:  # Overwrites any existing file.
                    pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

            if os.path.exists(os.path.join(TEMP_DIR, "substitute_rule_lines.pkl")):
                print("substitute_rule_lines exists")
            else:
                save_object(substitute_rule_lines, os.path.join(TEMP_DIR, "substitute_rule_lines.pkl"))

            with open( os.path.join(TEMP_DIR , "flag") , "w") as f:
                f.write("Hey")

        return super().set_context(font, glyphSet)

    def filter(self, glyph: Glyph):
        return False
