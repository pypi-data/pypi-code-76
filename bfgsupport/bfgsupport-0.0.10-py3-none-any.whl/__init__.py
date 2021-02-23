"""
    Expose the classes in the API
"""
##############################
VERSION = '0.10.99'
##############################

import gettext
import locale
import os
import re

LOC = locale.getdefaultlocale()[0]
LOC = 'en_GB'

locales_exe = os.path.join(os.getcwd(), 'locale')
locales_run = '../bfgsupport/bfgsupport/locale'
if os.path.isdir(locales_exe):
    LOCALES_DIRECTORY = locales_exe
else:
    LOCALES_DIRECTORY = locales_run

# As a last resort hard code the location of the locales directory
# (used in Sphinx when documenting other projects).
if not os.path.isdir(LOCALES_DIRECTORY):
    LOCALES_DIRECTORY = '/locale'


translation = gettext.translation('bfg', localedir=LOCALES_DIRECTORY, languages=[LOC], fallback=False)
translation.install()
_ = translation.gettext

VERSION_FILE="bfgsupport/_version.py"
with open(VERSION_FILE, 'r') as f_version:
    version_string = f_version.read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, version_string, re.M)
if mo:
    version_string = mo.group(1)
else:
    raise RuntimeError(f'Unable to find version string in {VERSION_FILE}.')
VERSION = version_string

# from bfgsupport.source.images import Images
from bfgsupport.source.bidding_board import BiddingBoard
from bfgsupport.source.file_objects import Files
from bfgsupport.source.pbn import PBN
from bfgsupport.source.comment_xref import CommentXref, convert_text_to_html
from bfgsupport.source.strategy_xref import StrategyXref, strategy_descriptions
from bfgsupport.source.bridge_tools import Bid, Pass, Double
from bfgsupport.source.player import Player
# from bfgsupport.source.bfg_wx_common import BidImage, HandDisplay, AuctionPanel, BidBox
# from bfgsupport.source.deploy import Deploy
from bfgsupport.source.dealer import Dealer
from bfgsupport.source.dealer_engine import DealerEngine
# from bfgsupport.tests.board_xref import board_xref
import bfgsupport.source.bfg_common as bfg_common
