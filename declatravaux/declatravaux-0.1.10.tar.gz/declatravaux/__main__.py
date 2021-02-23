#!/usr/bin/env python

import sys
import locale
import argparse
import logging
import pathlib

from PyQt5.QtWidgets import QApplication
from declatravaux.main_window import MainWindow
from declatravaux import configuration


def process_cl_args():
    """
    Parseur des options de ligne de commande
    :return: tuple
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fake_emailing", help="run DéclaTravaux without send emails",
                        action="store_true")
    p_args, unp_args = parser.parse_known_args()

    return p_args, unp_args


def set_logging_settings():
    """
    Set logging settings
    :return: None
    """

    path = pathlib.Path(configuration.Configuration.get_config_file_path().parent,
                        'declatravaux.log')

    logging.basicConfig(filename=path,
                        level=logging.DEBUG,
                        format='%(asctime)s | %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S')


if __name__ == '__main__':

    locale.setlocale(locale.LC_ALL, '')

    # Récupère les arguments traités et les arguments non identifiés
    parsed_args, unparsed_args = process_cl_args()
    # Le premier argument de QApplication doit être le nom du programme
    qt_args = sys.argv[:1] + unparsed_args

    set_logging_settings()

    app = QApplication(qt_args)
    main_window = MainWindow(fake_emailing=parsed_args.fake_emailing)
    main_window.show()

    rc = app.exec()
    sys.exit(rc)
