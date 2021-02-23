from orangecontrib.blue_whale.i18n_config import *


def __(key):
    return i18n.t('bluewhale.' + key)


NAME = "Blue Whale"

LABEL = __("package_label")

DESCRIPTION = __("package_desc")


BACKGROUND = "#99CCFF"

PRIORITY = 1

ICON = "icons/bw.svg"