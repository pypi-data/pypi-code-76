from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from typing import Set

from ufo2ft.filters import BaseFilter
from ufoLib2.objects.font import Font
from ufoLib2.objects.glyph import Glyph
import math
import re, os
import datetime
from ..config import SetConfig

# from fontParts.world import *

# from fontParts.fontshell import RFont

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class FixFontinfo(BaseFilter):

    def set_context(self, font: Font, glyphSet: Set[Glyph]):

        highest_point = font.bounds.yMax
        lowest_point = font.bounds.yMin

        def round_up(n, decimals=-1):
            multiplier = 10 ** decimals
            return math.ceil(n * multiplier) / multiplier

        win_ascent = int(abs(round_up(abs(highest_point))))
        win_descent = int(abs(round_up(abs(lowest_point))))

        typo_ascender = win_ascent
        typo_descender = - win_descent

        hhea_ascender = typo_ascender
        hhea_descender = typo_descender

        typo_lineGap = int(round_up(0.12 * (typo_ascender + typo_descender)))
        hhea_lineGap = typo_lineGap

        if "Devanagari" in font.info.familyName:
            font.info.openTypeNameSampleText = "सभी मनुष्यों को गौरव और अधिकारों के मामले में जन्मजात स्वतन्त्रता और समानता प्राप्त है।"
        if "Gujarati" in font.info.familyName:
            font.info.openTypeNameSampleText = "પ્રતિષ્ઠા અને અધિકારોની દૃષ્ટિએ સર્વ માનવો જન્મથી સ્વતંત્ર અને સમાન હોય છે."
        if "Gurmukhi" in font.info.familyName:
            font.info.openTypeNameSampleText = "ਸਾਰਾ ਮਨੁੱਖੀ ਪਰਿਵਾਰ ਆਪਣੀ ਮਹਿਮਾ, ਸ਼ਾਨ ਅਤੇ ਹੱਕਾਂ ਦੇ ਪੱਖੋਂ ਜਨਮ ਤੋਂ ਹੀ ਆਜ਼ਾਦ ਹੈ ਅਤੇ ਸੁਤੇ ਸਿੱਧ ਸਾਰੇ ਲੋਕ ਬਰਾਬਰ ਹਨ।"
        if "Bangla" in font.info.familyName:
            font.info.openTypeNameSampleText = "সমস্ত মানুষ স্বাধীনভাবে সমান মর্যাদা এবং অধিকার নিয়ে জন্মগ্রহণ করে।"
        if "Bengali" in font.info.familyName:
            font.info.openTypeNameSampleText = "সমস্ত মানুষ স্বাধীনভাবে সমান মর্যাদা এবং অধিকার নিয়ে জন্মগ্রহণ করে।"
        if "Odia" in font.info.familyName:
            font.info.openTypeNameSampleText = "ସବୁ ମନୁଷ୍ଯ ଜନ୍ମକାଳରୁ ସ୍ବାଧୀନ. ସେମାନଙ୍କର ମର୍ଯ୍ଯାଦା ଓ ଅଧିକାର ସମାନ."
        if "Telugu" in font.info.familyName:
            font.info.openTypeNameSampleText = "ప్రతిపత్తిస్వత్వముల విషయమున మానవులెల్లరును జన్మతః స్వతంత్రులును సమానులును నగుదురు."
        if "Kannada" in font.info.familyName:
            font.info.openTypeNameSampleText = "ಎಲ್ಲಾ ಮಾನವರೂ ಸ್ವತಂತ್ರರಾಗಿಯೇ ಜನಿಸಿದ್ಧಾರೆ. ಹಾಗೂ ಘನತೆ ಮತ್ತು ಹಕ್ಕುಗಳಲ್ಲಿ ಸಮಾನರಾಗಿದ್ದಾರೆ."
        if "Malayalam" in font.info.familyName:
            font.info.openTypeNameSampleText = "മനുഷ്യരെല്ലാവരും തുല്യാവകാശങ്ങളോടും അന്തസ്സോടും സ്വാതന്ത്ര്യത്തോടുംകൂടി ജനിച്ചിട്ടുള്ളവരാണ്‌."
        if "Tamil" in font.info.familyName:
            font.info.openTypeNameSampleText = "மனிதப் பிறிவியினர் சகலரும் சுதந்திரமாகவே பிறக்கின்றனர்; அவர்கள் மதிப்பிலும், உரிமைகளிலும் சமமானவர்கள், அவர்கள் நியாயத்தையும் மனச்சாட்சியையும் இயற்பண்பாகப் பெற்றவர்கள்."
        if "Sinhala" in font.info.familyName:
            font.info.openTypeNameSampleText = "සියලු මනුෂ්‍යයෝ නිදහස්ව උපත ලබා ඇත. ගරුත්වයෙන් හා අයිතිවාසිකම්වලින් සමාන වෙති."
        if "Takri" in font.info.familyName:
            font.info.openTypeNameSampleText = "𑚞𑚥-𑚞𑚥 𑚖𑚤𑚮𑚣𑚳 𑚄𑚢𑚤 𑚠𑚙𑚭𑚝𑚯 𑚏𑚴𑚔 𑚝𑚢𑚯𑚫 𑚝𑚮𑚙 𑚊𑚭𑚥𑚑𑚳 𑚸𑚭𑚝𑚯 𑚨𑚭𑚩𑚲𑚫 𑚀𑚫𑚛𑚤 𑚨𑚱𑚫𑚊𑚭𑚫 𑚸𑚔𑚯 𑚒𑚱𑚕-𑚢𑚱𑚕 𑚑𑚯𑚝𑚭 𑚛𑚯 𑚞𑚔𑚯॥"
        if "Latin" in font.info.familyName:
            font.info.openTypeNameSampleText = "Quick Brown fox jumps over the lazy dog and steals the golden apple"

        # win_ascent = 1000
        # win_descent = 240
        # typo_ascender = 1050   # Indesign
        # typo_descender = -350   # Indesign
        # hhea_ascender = 1050
        # hhea_descender = -350
        # hhea_lineGap = 100
        # typo_lineGap = 100   # Indesign

        cf_weight = 0
        cf_win_a = 0
        cf_win_d = 0
        cf_typo_a = 0
        cf_typo_d = 0
        cf_hhea_a = 0
        cf_hhea_d = 0
        cf_hhea_l = 0
        cf_typo_l = 0
        font_name = ""

        verticalmatrixdir = os.path.join(os.path.join(os.getcwd(),"temp"), "verticalmatrix.txt")

        if not os.path.isfile(verticalmatrixdir):
            with open(verticalmatrixdir, "w") as f:
                f.close()

        with open(verticalmatrixdir) as f:
            vm = f.readlines()
            for l in vm:
                l = l.replace("\n","")
                k = l.split(":")
                if k[0] == "name":
                    font_name = k[1]
                if k[0] == "weight":
                    cf_weight = int(k[1])
                if k[0] == "win_a":
                    cf_win_a = int(k[1])
                if k[0] == "win_d":
                    cf_win_d = int(k[1])
                if k[0] == "typo_a":
                    cf_typo_a = int(k[1])
                if k[0] == "typo_d":
                    cf_typo_d = int(k[1])
                if k[0] == "hhea_a":
                    cf_hhea_a = int(k[1])
                if k[0] == "hhea_d":
                    cf_hhea_d = int(k[1])
                if k[0] == "hhea_l":
                    cf_hhea_l = int(k[1])
                if k[0] == "typo_l":
                    cf_typo_l = int(k[1])

        f.close()
        if font_name == font.info.familyName:

            if cf_win_a <= win_ascent:
                cf_win_a = win_ascent
            if cf_win_d <= win_descent:
                cf_win_d = win_descent
            if cf_typo_a <= typo_ascender:
                cf_typo_a = typo_ascender
            if cf_typo_d >= typo_descender:
                cf_typo_d = typo_descender
            if cf_hhea_a <= hhea_ascender:
                cf_hhea_a = hhea_ascender
            if cf_hhea_d >= hhea_descender:
                cf_hhea_d = hhea_descender
            if cf_hhea_l <= hhea_lineGap:
                cf_hhea_l = hhea_lineGap
            if cf_typo_l <= typo_lineGap:
                cf_typo_l = typo_lineGap

            with open(verticalmatrixdir, "w") as ff:
                ff.write("name:" + font_name + "\n")
                ff.write("weight:" + str(cf_weight) + "\n")
                ff.write("win_a:" + str(cf_win_a) + "\n")
                ff.write("win_d:" + str(cf_win_d) + "\n")
                ff.write("typo_a:" + str(cf_typo_a) + "\n")
                ff.write("typo_d:" + str(cf_typo_d) + "\n")
                ff.write("hhea_a:" + str(cf_hhea_a) + "\n")
                ff.write("hhea_d:" + str(cf_hhea_d) + "\n")
                ff.write("hhea_l:" + str(cf_hhea_l) + "\n")
                ff.write("typo_l:" + str(cf_typo_l) + "\n")
            ff.close()
        else:
            font_name = font.info.familyName
            cf_weight = font.info.openTypeOS2WeightClass
            cf_win_a = win_ascent
            cf_win_d = win_descent
            cf_typo_a = typo_ascender
            cf_typo_d = typo_descender
            cf_hhea_a = hhea_ascender
            cf_hhea_d = hhea_descender
            cf_hhea_l = hhea_lineGap
            cf_typo_l = typo_lineGap
            with open(verticalmatrixdir, "w") as ff:
                ff.write("name:" + font_name + "\n")
                ff.write("weight:" + str(cf_weight) + "\n")
                ff.write("win_a:" + str(cf_win_a) + "\n")
                ff.write("win_d:" + str(cf_win_d) + "\n")
                ff.write("typo_a:" + str(cf_typo_a) + "\n")
                ff.write("typo_d:" + str(cf_typo_d) + "\n")
                ff.write("hhea_a:" + str(cf_hhea_a) + "\n")
                ff.write("hhea_d:" + str(cf_hhea_d) + "\n")
                ff.write("hhea_l:" + str(cf_hhea_l) + "\n")
                ff.write("typo_l:" + str(cf_typo_l) + "\n")
            ff.close()



        print("===========")

        win_ascent = cf_win_a
        win_descent = cf_win_d
        typo_ascender = cf_typo_a
        typo_descender = cf_typo_d
        hhea_ascender = cf_hhea_a
        hhea_descender = cf_hhea_d
        hhea_lineGap = cf_hhea_l
        typo_lineGap = cf_typo_l

        print("win_ascent " + str(win_ascent))
        print("win_descent " + str(win_descent))
        print("typo_ascender " + str(typo_ascender))
        print("typo_descender " + str(typo_descender))
        print("hhea_ascender " + str(hhea_ascender))
        print("hhea_descender " + str(hhea_descender))
        print("hhea_lineGap " + str(hhea_lineGap))
        print("typo_lineGap " + str(typo_lineGap))


        font.info.openTypeOS2WinAscent = win_ascent
        font.info.openTypeOS2WinDescent = win_descent
        font.info.openTypeOS2TypoAscender = typo_ascender
        font.info.openTypeOS2TypoDescender = typo_descender
        font.info.openTypeHheaAscender = hhea_ascender
        font.info.openTypeHheaDescender = hhea_descender
        font.info.openTypeHheaLineGap = hhea_lineGap
        font.info.openTypeOS2TypoLineGap = typo_lineGap

        # Getting font info from configuration


        config = SetConfig()
        config.read()


        # Applying gathered font info

        cr = font.info.copyright

        if cr:
            years = re.findall("\d{4}", cr)
            if years:
                initial_release_year = min(years)
        else:
            initial_release_year = str(datetime.date.today().year)

        current_year = str(datetime.date.today().year)

        if initial_release_year == str(current_year):
            release_year_range = initial_release_year
        else:
            release_year_range = initial_release_year + "-{}".format(str(current_year))

        if config.copyright:
            font.info.copyright = config.copyright.format(release_year_range,config.manufacturer)
        if config.designer_url:
            if (not font.info.openTypeNameDesignerURL) or (font.info.openTypeNameDesignerURL == "~"):
                font.info.openTypeNameDesignerURL = config.designer_url
        if config.manufacturer:
            font.info.openTypeNameManufacturer = config.manufacturer
        if config.manufacturer_url:
            font.info.openTypeNameManufacturerURL = config.manufacturer_url
        if config.license:
            font.info.openTypeNameLicense = config.license
        if config.license_url:
            font.info.openTypeNameLicenseURL = config.license_url
        if config.vendor_id:
            font.info.openTypeOS2VendorID = config.vendor_id

        tm = font.info.familyName.split(" ")

        if config.trademark:
            font.info.trademark = config.trademark.format(tm[0],config.manufacturer)

        # fsType: Everything is allowed
        font.info.openTypeOS2Type = []

        # Only Preview and print
        #font.info.openTypeOS2Type.insert(0, 2)
        # font.info.openTypeOS2Type[0]=2


        delattr(font.info, 'openTypeHeadFlags')
        # If not removed this causes the problem when the generated font tile is converted to other formats.


        # Use Typo Matrix = True
        font.info.openTypeOS2Selection = [7]

        logger.info("Generated font info")

        return super().set_context(font, glyphSet)

    def filter(self, glyph: Glyph):
        return False
