#!/usr/bin/env python

import json
import os
import sys
from PySide6.QtWidgets import QApplication

from dotenv import load_dotenv

from repoly.app import App


def getorelse(key, default):
    return os.environ[key] if key in os.environ else default


def run():
    basedir = "."  # os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, ".env"))

    app = QApplication([])

    App(
        n_entities=int(getorelse("N_ENTITIES", 3)),
        position=json.loads(getorelse("WIN_POS", "[0, 0]")),
        dimensions=json.loads(getorelse("WIN_DIM", "[700, 700]")),
        n_poly_sides=int(getorelse("N_POLY_SIDES", 6)),
        scale=int(getorelse("SCALE", 14)),
    ).show()

    sys.exit(app.exec_())
