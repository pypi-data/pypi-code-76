"""
    Expose the classes in the API
"""
##############################
VERSION = '0.10.21'
##############################

import gettext
import locale
import os

LOC = locale.getdefaultlocale()[0]
LOC = 'en_GB'

locales_exe = os.path.join(os.getcwd(), 'locale')
locales_run = '../bfgsupport/bfgsupport/locale'
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
    LOCALES_DIRECTORY = '/locale'


translation = gettext.translation('bfg', localedir=LOCALES_DIRECTORY, languages=[LOC], fallback=False)
translation.install()
_ = translation.gettext

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
