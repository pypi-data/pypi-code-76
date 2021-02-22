from Orange.data import Table
from Orange.i18n_config import *
from Orange.modelling.constant import ConstantLearner
from Orange.widgets.utils.owlearnerwidget import OWBaseLearner
from Orange.widgets.utils.widgetpreview import WidgetPreview


def __(key):
    return i18n.t("widget.model.model.owconstant." + key)


class OWConstant(OWBaseLearner):
    name = __("name")
    description = __("desc")
    icon = "icons/Constant.svg"
    replaces = [
        "Orange.widgets.classify.owmajority.OWMajority",
        "Orange.widgets.regression.owmean.OWMean",
    ]
    priority = 10
    keywords = ["majority", "mean"]

    LEARNER = ConstantLearner


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWConstant).run(Table("iris"))
