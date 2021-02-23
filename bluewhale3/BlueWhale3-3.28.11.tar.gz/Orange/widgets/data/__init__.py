from Orange.i18n_config import *


def __(key):
    return i18n.t("widget.data.data." + key)


NAME = "Data"

ID = "orange.widgets.data"

LABEL = __("package_label")

DESCRIPTION = __("package_desc")

LONG_DESCRIPTION = __("package_long_desc")

ICON = "icons/Category-Data.svg"

BACKGROUND = "#FFD39F"

PRIORITY = 2
