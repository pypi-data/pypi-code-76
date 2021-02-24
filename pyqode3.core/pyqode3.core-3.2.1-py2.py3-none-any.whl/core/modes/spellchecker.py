# -*- coding: utf-8 -*-
"""
This module contains the pyFlakes checker mode
"""
from pyqode.core.modes import CheckerMode


def run_spellcheck(request_data):

    WARNING = 1
    messages = []
    messages.append((
        '[spellcheck] test',
        WARNING,
        0,
        (100, 115)
    ))

    messages.append((
        '[spellcheck] test2',
        WARNING,
        2)
    )
    return messages


class SpellCheckerMode(CheckerMode):

    def __init__(self):
        super(SpellCheckerMode, self).__init__(run_spellcheck, delay=1200)
