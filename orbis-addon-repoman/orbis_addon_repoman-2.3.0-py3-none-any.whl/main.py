# -*- coding: utf-8 -*-

import os
import logging

from orbis_addon_repoman.corpora import Main as MainCorpora
from orbis_eval.libs.decorators import clear_screen
from orbis_eval.core.base import AddonBaseClass

logger = logging.getLogger(__name__)


class Main(AddonBaseClass):
    """docstring for Repoman"""

    def __init__(self):
        super(AddonBaseClass, self).__init__()
        self.addon_path = os.path.realpath(__file__).replace("main.py", "")

    @clear_screen()
    def run(self):
        MainCorpora(self.addon_path).run()
