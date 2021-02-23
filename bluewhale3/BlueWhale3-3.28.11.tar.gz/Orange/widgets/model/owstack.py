from collections import OrderedDict

from Orange.base import Learner
from Orange.data import Table
from Orange.ensembles.stack import StackedFitter
from Orange.widgets.settings import Setting
from Orange.widgets.utils.owlearnerwidget import OWBaseLearner
from Orange.widgets.widget import Input
from Orange.i18n_config import *



def __(key):
    return i18n.t("widget.model.model.owstack." + key)

class OWStackedLearner(OWBaseLearner):
    name = __("name")
    description = __("desc")
    icon = "icons/Stacking.svg"
    priority = 100

    LEARNER = StackedFitter

    learner_name = Setting(__("placeholder_name"))

    class Inputs(OWBaseLearner.Inputs):
        learners = Input("Learners", Learner, multiple=True, label=i18n.t("widget.model.model.common.learners"))
        aggregate = Input("Aggregate", Learner, label=i18n.t("widget.model.model.common.aggregate"))

    def __init__(self):
        self.learners = OrderedDict()
        self.aggregate = None
        super().__init__()

    def add_main_layout(self):
        pass

    @Inputs.learners
    def set_learners(self, learner, id):  # pylint: disable=redefined-builtin
        if id in self.learners and learner is None:
            del self.learners[id]
        elif learner is not None:
            self.learners[id] = learner
        self.apply()

    @Inputs.aggregate
    def set_aggregate(self, aggregate):
        self.aggregate = aggregate
        self.apply()

    def create_learner(self):
        if not self.learners:
            return None
        return self.LEARNER(
            tuple(self.learners.values()), aggregate=self.aggregate,
            preprocessors=self.preprocessors)

    def get_learner_parameters(self):
        return ((__("report.base_learners"), [l.name for l in self.learners.values()]),
                (__("report.aggregator"),
                 self.aggregate.name if self.aggregate else __('report.default')))


if __name__ == "__main__":
    import sys
    from AnyQt.QtWidgets import QApplication

    a = QApplication(sys.argv)
    ow = OWStackedLearner()
    d = Table(sys.argv[1] if len(sys.argv) > 1 else 'iris')
    ow.set_data(d)
    ow.show()
    a.exec_()
    ow.saveSettings()
