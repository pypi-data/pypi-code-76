"""
=========
Visualize
=========

Widgets for data visualization.

"""

# Category description for the widget registry
from Orange.i18n_config import *


def __(key):
    return i18n.t("widget.visualize.visualize." + key)


NAME = "Visualize"

ID = "orange.widgets.visualize"

LABEL = __("package_label")

DESCRIPTION = __("package_desc")


BACKGROUND = "#FFB7B1"

ICON = "icons/Category-Visualize.svg"

PRIORITY = 3
