import json
import os
import sys
from PySide6.QtWidgets import QApplication

from dotenv import load_dotenv

from repoly.app import App

basedir = "."  # os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

if __name__ == "__main__":
    app = QApplication([])

    App(
        n_entities=int(os.environ["N_ENTITIES"]),
        position=json.loads(os.environ["WIN_POS"]),
        dimensions=json.loads(os.environ["WIN_DIM"]),
        n_poly_sides=int(os.environ["N_POLY_SIDES"]),
        scale=int(os.environ["SCALE"]),
    ).show()

    sys.exit(app.exec_())
