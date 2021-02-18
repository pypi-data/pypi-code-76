from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from typing import Set

from ufo2ft.filters import BaseFilter
from ufoLib2.objects.font import Font
from ufoLib2.objects.glyph import Glyph

import pickle

import math
import re, os
import datetime, copy

from fontParts.world import *

from fontParts.fontshell import RFont

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMP_DIR = os.path.join(BASE_DIR, "temp")

from fontParts.world import CurrentFont

import itertools
import os.path

CONSONANT_STEMS = """
K KH G GH NG
C CH J JH NY
TT TTH DD DDH NN
T TH D DH N
P PH B BH M
Y R L V
SH SS S H
TTT NNN YY RR RRR LL LLL
TS DZ W ZH
""".split()

CONSONANTS_DEAD = CONSONANT_STEMS
script_abbr_current = "dv"
masters = [("Light", 0), ("Bold", 100)]
match_mI_variants = 1
position_marks_for_mI_variants = True
adjustment_for_matching_mI_variants = 0

# Important - example dvME
POTENTIAL_abvm_ANCHOR_NAMES = ["abvm.e", "abvm"]

class MatraiGen(BaseFilter):

    def get_path(self, temp=True):
        return (
            os.path.abspath("matrai.fea")
        )

    def _get_adjustment(self):
        if adjustment_for_matching_mI_variants:
            return adjustment_for_matching_mI_variants
        elif masters and adjustment_for_matching_mI_variants:
            (light_min, light_max), (bold_min, bold_max) = adjustment_for_matching_mI_variants
            axis_start = masters[0].location[0]
            axis_end = masters[-1].location[0]
            axis_range = axis_end - axis_start
            if axis_range == 0:
                ratio = 1
            else:
                ratio = (location[0] - axis_start) / axis_range
            return (
                light_min + (bold_min - light_min) * ratio,
                light_max + (bold_max - light_max) * ratio,
            )
        else:
            return None

    def _get_abvm_position(self, glyph, in_base=True):
        try:
            anchor_name_prefix = "" if in_base else "_"
            for potential_anchor_name in POTENTIAL_abvm_ANCHOR_NAMES:
                for anchor in glyph.anchors:
                    if anchor.name == anchor_name_prefix + potential_anchor_name:
                        return anchor.x
        except:
            return None

    def _get_stem_position(self, glyph):
        abvm_position = self._get_abvm_position(glyph)
        if abvm_position is None:
            return glyph.width - self.abvm_right_margin
        else:
            return abvm_position

    class Base(object):
        def __init__(self, feature, base_glyph_sequence):
            # self.glyphs = base_glyph_sequence
            # print(base_glyph_sequence)
            self.glyphs = feature.glyphSet[script_abbr_current + base_glyph_sequence[0]]
            #rahul
            # print("Yes, I am here!!!!")
            self.target = None
            # for g in reversed(self.glyphs):
            #     # TODO: Kerning.
            if self.target is None:
                self.target = feature._get_stem_position(self.glyphs)
                # print(self.target)
            else:
                self.target += self.glyphs.width

    class Match(object):
        def __init__(self, feature, mI_variant_name):
            self.name = mI_variant_name
            if self.name:
                # self.mI_variant = feature.font[self.name]
                self.mI_variant = feature.glyphSet[self.name]
                self.tag = self.mI_variant.name.partition(".")[2]
                # self.overhanging = abs(self.mI_variant.rightMargin)
                self.overhanging = abs(self.fontRightMargin(self.mI_variant))
            self.bases = []

        def fontRightMargin(self, glyphname):
            margin = 0
            for shape in glyphname.contours:
                for point in shape.points:
                    if point.x > margin:
                        margin = point.x
            margin = glyphname.width - margin
            return margin

    def mI_variants(family, glyph):
        match = re.match(
            family.project.script_abbr_current + kit.FeatureMatches.mI_VARIANT_NAME_PATTERN + r"$",
            glyph.name,
        )
        return bool(match)

    # def get_end(self):
    #     name = glyph.name
    #     end = ""
    #     if name.startswith(script_abbr_current):
    #         main, sep, suffix = name[2:].partition(".")
    #         end = main.split("_")[-1]
    #         if end.endswith("xA"):
    #             end = end[:-2] + "A"
    #         elif end.endswith("x"):
    #             end = end[:-1]
    #     return end

    @property
    def bases_alive(self):
        aliveBases = []
        alive = []
        res = []
        for glyph in self.glyphSet:
            name = glyph
            end = ""
            if name.startswith(script_abbr_current):
                # main, sep, suffix = name[2:].partition(".")
                # end = main.split("_")[-1]
                end = name[2:]
                if end.startswith('A') :
                    continue
                elif end.startswith('E') :
                    continue
                elif end.startswith('I'):
                    continue
                elif end.startswith('O'):
                    continue
                elif end.startswith('U'):
                    continue
                elif end.startswith('m'):
                    continue
                elif end.endswith("xA"):
                    end = end[:-2] + "A"
                elif end.endswith("x"):
                    end = end[:-1]
                elif not end.endswith('A'):
                    continue
                else:
                    aliveBases.append(end)
        for i in aliveBases:
            if i not in res:
                res.append(i)
        return res

    @property
    def bases_dead(self):
        deadBases = []
        dead = []
        res = []
        for glyph in self.glyphSet:
            name = glyph
            end = ""
            if name.startswith(script_abbr_current):
                main, sep, suffix = name[2:].partition(".")
                end = main.split("_")[-1]
                if end.endswith("xA"):
                    end = end[:-2] + "A"
                elif end.endswith("x"):
                    end = end[:-1]
                deadBases.append(end)
        for i in deadBases:
            for j in CONSONANTS_DEAD:
                if i == j:
                    dead.append(i)
        for i in dead:
            if i not in res:
                res.append(i)
        return res

    def _base_glyph_sequences(self):
        seeds = [self.bases_dead] * (match_mI_variants - 1) + [self.bases_alive]
        for sequence in itertools.product(*seeds):
            yield sequence

    def match_mI_variants(self, base):
        if base.target <= self.matches[0].overhanging:
            return self.matches[0]
        elif base.target < self.matches[-1].overhanging:
            i = 0
            while self.matches[i].overhanging < base.target:
                candidate_short = self.matches[i]
                i += 1
            candidate_enough = self.matches[i]
            if (
                    (candidate_enough.overhanging - base.target) <
                    (base.target - candidate_short.overhanging) / 3
            ):
                return candidate_enough
            else:
                return candidate_short
        elif base.target <= self.matches[-1].overhanging + self.tolerance:
            return self.matches[-1]
        else:
            # return self.not_matched
            self.matches[len(self.matches)-1].bases.append(base)
            # print(self.matches[len(self.matches)-1])
            # len(self.matches)
            print("this target is not matching")

    def output_mI_variant_matches(self, match):

        if not match.bases:
            print("\t\t`{}` is not used.".format(match.name))
            self.substitute_rule_lines.append(
                "# sub {}' _ by {};".format(self.name_default, match.name),
            )
            return

        single_glyph_bases = []
        multiple_glyph_bases = []
        for base in match.bases:
            if len(base.glyphs) == 1:
                single_glyph_bases.append(base)
            else:
                single_glyph_bases.append(base)
                # multiple_glyph_bases.append(base) # original one

        if single_glyph_bases:
            self.substitute_rule_lines.append(
                "sub {}' [{}] by {};".format(
                    self.name_default,
                    " ".join(i.glyphs.name for i in single_glyph_bases),
                    match.name,
                ),
            )

    def generate(self):

        path = self.fontobj.path

        self.font = self.glyphSet

        # for statment in self.context.feaFile.statements:
        #     if hasattr(statment, 'name'):
        #         if statment.name == 'mI_VARIANTS':
        #             print("Found mI_VARIANTS")
        #             mI_variant_names = statment.glyphs.glyphs

        mI_variant_names = self.mi_class_name

        # mI_variant_names = ['dvmI.alt00', 'dvmI.alt01', 'dvmI.alt02', 'dvmI.alt03', 'dvmI.alt04', 'dvmI.alt05', 'dvmI.alt06', 'dvmI.alt07', 'dvmI.alt08', 'dvmI.alt09', 'dvmI.alt10', 'dvmI.alt11', 'dvmI.alt12', 'dvmI.alt13', 'dvmI.alt14', 'dvmI.alt15', 'dvmI.alt16', 'dvmI.alt17', 'dvmI.alt18', 'dvmI.alt19', 'dvmI.alt20', 'dvmI.alt21', 'dvmI.alt22', 'dvmI.alt23', 'dvmI.alt24', 'dvmI.alt25', 'dvmI.alt26', 'dvmI.alt27', 'dvmI.alt28', 'dvmI.alt29', 'dvmI.alt30', 'dvmI.alt31', 'dvmI.alt32', 'dvmI.alt33', 'dvmI.alt34', 'dvmI.alt35', 'dvmI.alt36', 'dvmI.alt37', 'dvmI.alt38', 'dvmI.alt39', 'dvmI.alt40' ]

        self.matches = [self.Match(self, i) for i in sorted(mI_variant_names)]

        ###########################
        # manually setting script abbreviation name. ex. Devanagari = dv
        # self.project.script_abbr_current = dv
        ###########################

        abvm_position_in_mE = self._get_abvm_position(
            self.font[script_abbr_current + "mE"],
            in_base=False,
        )
        if abvm_position_in_mE is None:
            raise SystemExit("[WARNING] Can't find the abvm anchor in glyph `mE`!")
        else:
            self.abvm_right_margin = abs(abvm_position_in_mE)

        # Setting up right side margin of matrai variant

        self.bases = [self.Base(self, i) for i in self._base_glyph_sequences()]
        if not self.bases:
            raise ValueError("[WARNING] No bases.")

        # Adjustment in matraI fitting

        adjustment = self._get_adjustment()
        if adjustment is None:
            pass
        elif isinstance(adjustment, tuple):
            extremes = adjustment
            targets = [base.target for base in self.bases]
            TARGET_MIN = min(targets)
            TARGET_MAX = max(targets)
            for i, base in enumerate(self.bases):
                ratio = (base.target - TARGET_MIN) / (TARGET_MAX - TARGET_MIN)
                adjustment = extremes[0] + (extremes[1] - extremes[0]) * ratio
                self.bases[i].target += adjustment
        else:
            for i, base in enumerate(self.bases):
                self.bases[i].target += adjustment

        self.tolerance = self._get_stem_position(
            self.font[script_abbr_current + "VA"]
        ) * 0.5

        # print(self.tolerance)

        for base in self.bases:
            match = self.match_mI_variants(base)
            if match:
                match.bases.append(base)

        self.name_default = script_abbr_current + "mI"

        self.substitute_rule_lines = []
        for match in self.matches:
            self.output_mI_variant_matches(match)
        with open(self.get_path(), "w") as f:
            f.writelines([
                "lookup %s {\n" % self.name,
                # "  lookupflag IgnoreMarks;\n",
            ])
            f.writelines("  " + l + "\n" for l in self.substitute_rule_lines)
            f.writelines([
                # "  lookupflag 0;\n",
                "} %s;\n" % self.name,
            ])


    def set_context(self, font: Font, glyphSet: Set[Glyph]):

        # Checking if MatraI Variations are needed

        if 'dvmI_short' in glyphSet and 'dvmI_long' in glyphSet:
            print("Found dvmI_short and dvmI_long")

            ufoPath = font.path

            p = os.path.split(ufoPath)
            q = os.path.join(BASE_DIR, "temp")
            tempPath = os.path.join(q, p[1])

            if os.path.exists(tempPath):
                print("UFO with MatraI variation altedy exists: To generate again delete 'temp' directory")
            else:
                # settings
                interpolationSteps = 30
                extrapolateSteps = 0

                f = RFont(ufoPath, showInterface=False)
                g = RFont()

                source1 = f["dvmI_short"]
                source2 = f["dvmI_long"]

                classlist = []

                # check if they are compatible
                if not source1.isCompatible(source2)[0]:
                    # the glyphs are not compatible
                    print("Incompatible masters: Glyph %s and %s are not compatible." % (source1.name, source2.name))

                else:
                    # loop over the amount of required interpolations
                    nameSteps = 0
                    for i in range(-extrapolateSteps, interpolationSteps + extrapolateSteps + 1, 1):
                        # create a new name
                        name = "dvmI.alt%02i" % nameSteps
                        nameSteps += 1
                        # create the glyph if does not exist
                        src = f.newGlyph(name)
                        dup = g.newGlyph(name)
                        # get the interpolation factor (a value between 0.0 and 1.0)
                        factor = i / float(interpolationSteps)
                        # interpolate between the two masters with the factor
                        src.interpolate(factor, source1, source2)
                        dup.interpolate(factor, source1, source2)
                    f.changed()
                    g.changed()
                # f.save(tempPath)
                g.save(tempPath)

            # Updating font and glyphSet object with new UFO or the existing UFO from 'temp' path
            abc = font.open(tempPath)

            for a in abc:
                font.addGlyph(a)

            # font = font.open(tempPath)
            oldset = glyphSet
            oldset = set(oldset)
            glyphSet.clear()
            glyphSet.update(font)
            newset = glyphSet
            newset = set(newset)
            diffset = newset.symmetric_difference(oldset)
            difflist = list(diffset)
            difflist.sort()
            # classlist_string = ""
            # for ele in difflist:
            #     classlist_string = classlist_string + ele + " "
            # classlist_string = "@mI_VARIANTS = [ " + classlist_string + "];"
            # font.features.text = classlist_string + "\n" + font.features.text
        else:
            print("No need for MatraI Variation")

        # Start matching


        print("Now matching matrai for matrai_sub")

        self.fontobj = font
        self.glyphSet = glyphSet
        self.mi_class_name = difflist

        self.generate()

        def save_object(obj, filename):
            with open(filename, 'wb') as output:  # Overwrites any existing file.
                pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

        save_object(self.matches, tempPath + ".pkl")

        if os.path.exists(os.path.join(TEMP_DIR, "bases.pkl")):
            print("bases.pkl exists")
        else:
            save_object(self.bases, os.path.join(TEMP_DIR, "bases.pkl"))

        if os.path.exists(os.path.join(TEMP_DIR, "flag")):
            os.remove(os.path.join(TEMP_DIR, "flag"))

        return super().set_context(font, glyphSet)



    def filter(self, glyph: Glyph):
        return False
