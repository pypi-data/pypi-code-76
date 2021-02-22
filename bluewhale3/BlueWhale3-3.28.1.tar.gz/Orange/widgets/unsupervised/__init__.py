"""
============
Unsupervised
============

Unsupervised learning.

"""
from Orange.i18n_config import *


def __(key):
    return i18n.t("widget.unsupervised.unsupervised." + key)


# Category description for the widget registry

NAME = "Unsupervised"

LABEL = __("package_label")

DESCRIPTION = __("package_desc")

BACKGROUND = "#CAE1EF"

ICON = "icons/Category-Unsupervised.svg"

PRIORITY = 6
