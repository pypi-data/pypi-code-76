from fontTools import designspaceLib
# from ../extras import config
# # from extras import config
# # import config
import os
from ufoLib2.objects.font import Font
from ufoLib2.objects.glyph import Glyph
from typing import Set
from fontParts.world import *
from ufo2ft.util import _LazyFontName, _GlyphSet
import itertools
from collections import defaultdict
import re

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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DIR = os.path.join(os.path.join(BASE_DIR, "extras"), "temp")
SCRIPT_ABBR_CURRENT = "dv"
match_mI_variants = 1
masters = [("Light", 0), ("Bold", 100)]
position_marks_for_mI_variants = True
adjustment_for_matching_mI_variants_bold = 13
adjustment_for_matching_mI_variants_light = 20

# Important - example dvME
POTENTIAL_abvm_ANCHOR_NAMES = ["avbm" , "avbm.e", "abvm" , "abvm.e"]

TEST = False
INPUT_FILE_NAME = "Tihar Devanagari.designspace"
interpolationSteps = 40

# class Selfish:
#     def __init__(self, **kwargs):
#         for k in kwargs:
#             setattr(self, k, kwargs[k])

def main():
    # c = config.fontmake
    designspace_path = os.path.join(os.path.join(BASE_DIR, "masters") , INPUT_FILE_NAME)
    designspace = designspaceLib.DesignSpaceDocument.fromfile(designspace_path)

    paths = []
    for source in designspace.sources:
        paths.append(source.path)

    master1 = Font.open(paths[0])
    # master2 = Font.open(paths[1])
    print(SCRIPT_ABBR_CURRENT)

    if SCRIPT_ABBR_CURRENT + "mI_short" in master1:
        print("Found "+ SCRIPT_ABBR_CURRENT +"mI_short: Going ahead...")
    else:
        print("No "+ SCRIPT_ABBR_CURRENT +"mI_short found: Check the font file")

    bold = MatraIUtil()
    light = MatraIUtil()

    bold.interpolate_matrai(master1)
    bold.generate_matrai_match()

    # light.interpolate_matrai(master2)
    # light.generate_matrai_match()

    matches_bold = bold.matches
    # matches_light = light.matches
    bases = bold.bases

    generatedmi_1 = Font.open(bold.tempPath)
    # generatedmi_2 = Font.open(light.tempPath)

    match_dict = defaultdict(list)

    def find_match_matra(base, selected_matrai):
        for matra in selected_matrai:
            for matchbase in matra.bases:
                if matchbase.glyphs.name == base.glyphs.name:
                    return matra.name

    for base in bases:
        firstpair = find_match_matra(base, matches_bold)
        # secondpair = find_match_matra(base, matches_light)

        first_digit = re.findall("\d{2}", firstpair)
        # second_digit = re.findall("\d{2}", secondpair)
        new_name = SCRIPT_ABBR_CURRENT + "mI." + first_digit[0]

        # Check if new name already exists in match_dict.
        # If it exists, there is no need to create new glyph

        if not match_dict[new_name]:
            new_glyph_1 = generatedmi_1[firstpair].copy(new_name)
            generatedmi_1.addGlyph(new_glyph_1)

            # new_glyph_2 = generatedmi_2[secondpair].copy(new_name)
            # generatedmi_2.addGlyph(new_glyph_2)

        print("new glyph added {}".format(new_name))

        match_dict[new_name].append(base.glyphs.name)

        print("Found both pair")

    # p = os.path.split(font.path)
    # current_font_ufo_name = p[1]
    print("Hey")

    # if current_font_ufo_name == ufofiles[0]:

    for g1 in generatedmi_1:
        if not g1.name in master1:
            master1.addGlyph(g1)
            print("Added glyphs is: " + g1.name)
        else:
            del master1[g1.name]
            print("Deleted glyphs is: " + g1.name)

    # for g2 in generatedmi_2:
    #     if not g2.name in master2:
    #         master2.addGlyph(g2)
    #         print("Added glyphs is: " + g2.name)
    #     else:
    #         del master2[g2.name]
    #         print("Deleted glyphs is: " + g2.name)

    # Save to ufo files in masters directory (Originally designspace masters path)

    if TEST:
        master1.save(os.path.join(TEMP_DIR, "generated1.ufo"), overwrite=True)
        # master2.save(os.path.join(TEMP_DIR, "generated2.ufo"), overwrite=True)
    else:
        master1.save(master1.path, overwrite=True)
        # master2.save(master2.path, overwrite=True)



    print("Hello, I did some process")

    BASES_ALIVE_CLASS = []
    BASES_ALIVE = ""

    for b in bases:
        BASES_ALIVE_CLASS.append(b.glyphs.name)

    for g in BASES_ALIVE_CLASS:
        BASES_ALIVE = BASES_ALIVE + " " + g

    # SCRIPT_ABBR_CURRENT = "dv"
    substitute_rule_lines = []
    name_default = SCRIPT_ABBR_CURRENT + "mI"

    substitute_rule_lines.append("@BASES_ALIVE = [ " + BASES_ALIVE + " ];")

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

    with open(os.path.join(TEMP_DIR, "matrai.fea"), 'w') as the_file:
        for lines in substitute_rule_lines:
            the_file.write(lines + '\n')
    the_file.close()

    print("Hey")


class MatraIUtil:

    def interpolate_matrai(self, font):

        glyphSet = _GlyphSet.from_layer(font)

        ufoPath = font.path

        p = os.path.split(ufoPath)
        q = TEMP_DIR
        self.tempPath = os.path.join(q, p[1])

        # settings

        extrapolateSteps = 0

        f = RFont(ufoPath, showInterface=False)
        g = RFont()

        source1 = f[SCRIPT_ABBR_CURRENT + "mI_short"]
        source2 = f[SCRIPT_ABBR_CURRENT + "mI_long"]

        # check if they are compatible
        if not source1.isCompatible(source2)[0]:
            # the glyphs are not compatible
            print("Incompatible masters: Glyph %s and %s are not compatible." % (source1.name, source2.name))

        else:
            # loop over the amount of required interpolations
            nameSteps = 0
            for i in range(-extrapolateSteps, interpolationSteps + extrapolateSteps + 1, 1):
                # create a new name
                name = SCRIPT_ABBR_CURRENT + "mI.alt%02i" % nameSteps
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
        # f.save(self.tempPath)
        g.save(self.tempPath)

        # Updating font and glyphSet object with new UFO or the existing UFO from 'temp' path
        abc = font.open(self.tempPath)

        for a in abc:
            font.addGlyph(a)

        # font = font.open(self.tempPath)
        oldset = glyphSet
        oldset = set(oldset)
        glyphSet.clear()
        glyphSet.update(font)
        newset = glyphSet
        newset = set(newset)
        diffset = newset.symmetric_difference(oldset)
        difflist = list(diffset)
        difflist.sort()

        # Start matching

        print("Now matching matrai for matrai_sub")

        self.fontobj = font
        self.glyphSet = glyphSet
        self.mi_class_name = difflist

        print("Hello")


    def get_path(self, temp=True):
        return (
            os.path.abspath("matrai.fea")
        )



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
            self.glyphs = feature.glyphSet[SCRIPT_ABBR_CURRENT + base_glyph_sequence[0]]
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



    @property
    def bases_alive(self):
        aliveBases = []
        alive = []
        res = []
        for glyph in self.glyphSet:
            name = glyph
            end = ""
            if name.startswith(SCRIPT_ABBR_CURRENT):
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
                    aliveBases.append(end)
                elif end.endswith("x"):
                    continue
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
            if name.startswith(SCRIPT_ABBR_CURRENT):
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
    def _get_adjustment(self):

        if "Bold" in self.tempPath:
            adjustment_for_matching_mI_variants = adjustment_for_matching_mI_variants_bold
        if "Light" in self.tempPath:
            adjustment_for_matching_mI_variants = adjustment_for_matching_mI_variants_light

        if adjustment_for_matching_mI_variants:
            return adjustment_for_matching_mI_variants
        else:
            return None

    def generate_matrai_match(self):

        path = self.fontobj.path

        self.font = self.glyphSet

        mI_variant_names = self.mi_class_name

        self.matches = [self.Match(self, i) for i in sorted(mI_variant_names)]

        ###########################
        # manually setting script abbreviation name. ex. Devanagari = dv
        # self.project.SCRIPT_ABBR_CURRENT = dv
        ###########################

        xfxfx = self.font["dvmE"]

        abvm_position_in_mE = self._get_abvm_position(
            self.font[SCRIPT_ABBR_CURRENT + "mE"],
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
        else:
            for i, base in enumerate(self.bases):
                self.bases[i].target += adjustment

        self.tolerance = self._get_stem_position(
            self.font[SCRIPT_ABBR_CURRENT + "VA"]
        ) * 0.5

        # print(self.tolerance)

        for base in self.bases:
            match = self.match_mI_variants(base)
            if match:
                match.bases.append(base)

        self.name_default = SCRIPT_ABBR_CURRENT + "mI"

        self.substitute_rule_lines = []
        for match in self.matches:
            self.output_mI_variant_matches(match)

if __name__ == '__main__':
    main()