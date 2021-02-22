from AnyQt.QtCore import Qt

from Orange.base import Learner
from Orange.data import Table
from Orange.i18n_config import *
from Orange.modelling import SklAdaBoostLearner, SklTreeLearner
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.owlearnerwidget import OWBaseLearner
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import Msg, Input


def __(key):
    return i18n.t("widget.model.model.owadaboost." + key)


class OWAdaBoost(OWBaseLearner):
    name = __("name")
    description = __("desc")
    icon = "icons/AdaBoost.svg"
    replaces = [
        "Orange.widgets.classify.owadaboost.OWAdaBoostClassification",
        "Orange.widgets.regression.owadaboostregression.OWAdaBoostRegression",
    ]
    priority = 80
    keywords = ["boost"]

    LEARNER = SklAdaBoostLearner

    class Inputs(OWBaseLearner.Inputs):
        learner = Input("Learner", Learner, label=i18n.t("common.general.learner"))

    #: Algorithms for classification problems
    algorithms = [__("gbox.samme"), __("gbox.samme_r")]
    #: Losses for regression problems
    losses = [i18n.t("common.general.linear"), __("gbox.square"), __("gbox.exponential")]

    n_estimators = Setting(50)
    learning_rate = Setting(1.)
    algorithm_index = Setting(1)
    loss_index = Setting(0)
    use_random_seed = Setting(False)
    random_seed = Setting(0)

    DEFAULT_BASE_ESTIMATOR = SklTreeLearner()

    class Error(OWBaseLearner.Error):
        no_weight_support = Msg(__("msg_base_learner_unsupported_weight"))

    def add_main_layout(self):
        # this is part of init, pylint: disable=attribute-defined-outside-init
        box = gui.widgetBox(self.controlArea, i18n.t("common.general.parameter"))
        self.base_estimator = self.DEFAULT_BASE_ESTIMATOR
        self.base_label = gui.label(
            box, self, __("row.base_estimator") + self.base_estimator.name.title())

        self.n_estimators_spin = gui.spin(
            box, self, "n_estimators", 1, 10000, label=__("row.num_estimator"),
            alignment=Qt.AlignRight, controlWidth=80,
            callback=self.settings_changed)
        self.learning_rate_spin = gui.doubleSpin(
            box, self, "learning_rate", 1e-5, 1.0, 1e-5,
            label=__("row.learn_rate"), decimals=5, alignment=Qt.AlignRight,
            controlWidth=80, callback=self.settings_changed)
        self.random_seed_spin = gui.spin(
            box, self, "random_seed", 0, 2 ** 31 - 1, controlWidth=80,
            label=__("checkbox_random_generator"), alignment=Qt.AlignRight,
            callback=self.settings_changed, checked="use_random_seed",
            checkCallback=self.settings_changed)

        # Algorithms
        box = gui.widgetBox(self.controlArea, __("box_boosting_method"))
        self.cls_algorithm_combo = gui.comboBox(
            box, self, "algorithm_index", label=__("row.class_algorithm"),
            items=self.algorithms,
            orientation=Qt.Horizontal, callback=self.settings_changed)
        self.reg_algorithm_combo = gui.comboBox(
            box, self, "loss_index", label=__("row.regress_loss_function"),
            items=self.losses,
            orientation=Qt.Horizontal, callback=self.settings_changed)

    def create_learner(self):
        if self.base_estimator is None:
            return None
        return self.LEARNER(
            base_estimator=self.base_estimator,
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate,
            random_state=self.random_seed,
            preprocessors=self.preprocessors,
            algorithm=self.algorithms[self.algorithm_index],
            loss=self.losses[self.loss_index].lower())

    @Inputs.learner
    def set_base_learner(self, learner):
        # base_estimator is defined in add_main_layout
        # pylint: disable=attribute-defined-outside-init
        self.Error.no_weight_support.clear()
        if learner and not learner.supports_weights:
            # Clear the error and reset to default base learner
            self.Error.no_weight_support()
            self.base_estimator = None
            self.base_label.setText(__("label.base_estimator_invalid"))
        else:
            self.base_estimator = learner or self.DEFAULT_BASE_ESTIMATOR
            self.base_label.setText(
                __("label.base_estimator") % self.base_estimator.name.title())
        if self.auto_apply:
            self.apply()

    def get_learner_parameters(self):
        return ((__("row.base_estimator"), self.base_estimator),
                (__("row.num_estimator"), self.n_estimators),
                (__("row.algorithm"), self.algorithms[self.algorithm_index].capitalize()),
                (__("row.loss"), self.losses[self.loss_index].capitalize()))


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWAdaBoost).run(Table("iris"))
