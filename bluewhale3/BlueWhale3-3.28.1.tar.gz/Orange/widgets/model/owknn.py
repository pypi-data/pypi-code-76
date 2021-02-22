from AnyQt.QtCore import Qt

from Orange.data import Table
from Orange.i18n_config import *
from Orange.modelling import KNNLearner
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.owlearnerwidget import OWBaseLearner
from Orange.widgets.utils.widgetpreview import WidgetPreview


def __(key):
    return i18n.t("widget.model.model.owknn." + key)


class OWKNNLearner(OWBaseLearner):
    name = __("name")
    description = __("desc")
    icon = "icons/KNN.svg"
    replaces = [
        "Orange.widgets.classify.owknn.OWKNNLearner",
        "Orange.widgets.regression.owknnregression.OWKNNRegression",
    ]
    priority = 20
    keywords = ["k nearest", "knearest", "neighbor", "neighbour"]

    LEARNER = KNNLearner

    weights = ["uniform", "distance"]
    metrics = ["euclidean", "manhattan", "chebyshev", "mahalanobis"]

    learner_name = Setting(__("name"))
    n_neighbors = Setting(5)
    metric_index = Setting(0)
    weight_index = Setting(0)

    def add_main_layout(self):
        # this is part of init, pylint: disable=attribute-defined-outside-init
        box = gui.vBox(self.controlArea, i18n.t("common.general.neighbor"))
        self.n_neighbors_spin = gui.spin(
            box, self, "n_neighbors", 1, 100, label=__("row_num_of_neighbor"),
            alignment=Qt.AlignRight, callback=self.settings_changed,
            controlWidth=80)
        self.metrics_combo = gui.comboBox(
            box, self, "metric_index", orientation=Qt.Horizontal,
            label=__("row_metric"), items=[__("gbox.euclidean"), __("gbox.manhattan"), __("gbox.chebyshev"), __("gbox.mahalanobis")],
            callback=self.settings_changed)
        self.weights_combo = gui.comboBox(
            box, self, "weight_index", orientation=Qt.Horizontal,
            label=__("row_weight"), items=[__("gbox.uniform"), __("gbox.distance")],
            callback=self.settings_changed)

    def create_learner(self):
        return self.LEARNER(
            n_neighbors=self.n_neighbors,
            metric=self.metrics[self.metric_index],
            weights=self.weights[self.weight_index],
            preprocessors=self.preprocessors)

    def get_learner_parameters(self):
        return ((__("report.num_of_neighbor"), self.n_neighbors),
                (i18n.t("common.general.metric"), self.metrics[self.metric_index].capitalize()),
                (__("report.weight"), self.weights[self.weight_index].capitalize()))


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWKNNLearner).run(Table("iris"))
