"""
    Expose the classes in the API
"""

import gettext
import locale
import os

LOC = locale.getdefaultlocale()[0]
LOC = 'en_GB'

locales_exe = os.getcwd()+os.sep+'locale'
locales_run = '../bfg_components/bfg_components/locale'
if os.path.isdir(locales_exe):
    LOCALES_DIRECTORY = locales_exe
else:
    LOCALES_DIRECTORY = locales_run

# print('cwd: {}'.format(os.getcwd()))
# print('locales_exe: {}'.format(locales_exe))
# print('Is locales_exe a directory: {}'.format(os.path.isdir(locales_exe)))
# print('locales_run: {}'.format(locales_run))
# print('Is locales_run a directory: {}'.format(os.path.isdir(locales_run)))
# print('LOCALES_DIRECTORY: {}'.format(LOCALES_DIRECTORY))
# print('Is LOCALES_DIRECTORY a directory: {}'.format(os.path.isdir(LOCALES_DIRECTORY)))
# print('LOC: {}'.format(LOC))

# As a last resort hard code the location of the locales directory
# (used in Sphinx when documenting other projects).
if not os.path.isdir(LOCALES_DIRECTORY):
    LOCALES_DIRECTORY = '/home/jeff/projects/bfg/bfg_components/bfg_components/locale'


translation = gettext.translation('bfg', localedir=LOCALES_DIRECTORY, languages=[LOC], fallback=False)
translation.install()
_ = translation.gettext

# from bfg_components.source.images import Images
from bfg_components.source.bidding_board import BiddingBoard
from bfg_components.source.file_objects import Files
from bfg_components.source.pbn import PBN
from bfg_components.source.comment_xref import CommentXref, convert_text_to_html
from bfg_components.source.strategy_xref import StrategyXref, strategy_descriptions
from bfg_components.source.bridge_tools import Bid, Pass, Double
from bfg_components.source.player import Player
# from bfg_components.source.bfg_wx_common import BidImage, HandDisplay, AuctionPanel, BidBox
# from bfg_components.source.deploy import Deploy
from bfg_components.source.dealer import Dealer
from bfg_components.source.dealer_engine import DealerEngine
from bfg_components.tests.board_xref import board_xref
import bfg_components.source.bfg_common as bfg_common
