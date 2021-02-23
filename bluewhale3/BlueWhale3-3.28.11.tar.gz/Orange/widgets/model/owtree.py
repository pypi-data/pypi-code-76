"""Tree learner widget"""

from collections import OrderedDict

from AnyQt.QtCore import Qt

from Orange.data import Table
from Orange.modelling.tree import TreeLearner
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.owlearnerwidget import OWBaseLearner
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.i18n_config import *



def __(key):
    return i18n.t("widget.model.model.owtree." + key)

class OWTreeLearner(OWBaseLearner):
    """Tree algorithm with forward pruning."""
    name = __("name")
    description = __("desc")
    icon = "icons/Tree.svg"
    replaces = [
        "Orange.widgets.classify.owclassificationtree.OWClassificationTree",
        "Orange.widgets.regression.owregressiontree.OWRegressionTree",
        "Orange.widgets.classify.owclassificationtree.OWTreeLearner",
        "Orange.widgets.regression.owregressiontree.OWTreeLearner",
    ]
    priority = 30
    keywords = ["Classification Tree"]

    LEARNER = TreeLearner

    binary_trees = Setting(True)
    limit_min_leaf = Setting(True)
    min_leaf = Setting(2)
    limit_min_internal = Setting(True)
    min_internal = Setting(5)
    limit_depth = Setting(True)
    max_depth = Setting(100)

    # Classification only settings
    limit_majority = Setting(True)
    sufficient_majority = Setting(95)

    spin_boxes = (
        (__("checkbox.leave_min_num"),
         "limit_min_leaf", "min_leaf", 1, 1000),
        (__("checkbox.not_split_smaller_subset"),
         "limit_min_internal", "min_internal", 1, 1000),
        (__("checkbox.limit_max_tree_depth"),
         "limit_depth", "max_depth", 1, 1000))

    classification_spin_boxes = (
        (__("checkbox.majority_reaches_stop"),
         "limit_majority", "sufficient_majority", 51, 100),)

    def add_main_layout(self):
        box = gui.widgetBox(self.controlArea, i18n.t("common.general.parameter"))
        # the checkbox is put into vBox for alignemnt with other checkboxes
        gui.checkBox(gui.vBox(box), self, "binary_trees", __("checkbox.induce_binary_tree"),
                     callback=self.settings_changed)
        for label, check, setting, fromv, tov in self.spin_boxes:
            gui.spin(box, self, setting, fromv, tov, label=label,
                     checked=check, alignment=Qt.AlignRight,
                     callback=self.settings_changed,
                     checkCallback=self.settings_changed, controlWidth=80)

    def add_classification_layout(self, box):
        for label, check, setting, minv, maxv in self.classification_spin_boxes:
            gui.spin(box, self, setting, minv, maxv,
                     label=label, checked=check, alignment=Qt.AlignRight,
                     callback=self.settings_changed, controlWidth=80,
                     checkCallback=self.settings_changed)

    def learner_kwargs(self):
        # Pylint doesn't get our Settings
        # pylint: disable=invalid-sequence-index
        return dict(
            max_depth=(None, self.max_depth)[self.limit_depth],
            min_samples_split=(2, self.min_internal)[self.limit_min_internal],
            min_samples_leaf=(1, self.min_leaf)[self.limit_min_leaf],
            binarize=self.binary_trees,
            preprocessors=self.preprocessors,
            sufficient_majority=(1, self.sufficient_majority / 100)[
                self.limit_majority])

    def create_learner(self):
        # pylint: disable=not-callable
        return self.LEARNER(**self.learner_kwargs())

    def get_learner_parameters(self):
        from Orange.widgets.report import plural_w
        items = OrderedDict()
        items[__("report.prune")] = ", ".join(s for s, c in (
            (plural_w(__("report.number_instance_leaves"),
                      self.min_leaf), self.limit_min_leaf),
            (plural_w(__("report.number_instance_internal_nodes"),
                      self.min_internal), self.limit_min_internal),
            (__("report.maximum_depth").format(self.max_depth), self.limit_depth)
        ) if c) or i18n.t("common.software.none")
        if self.limit_majority:
            items[__("report.split")] = __("report.classification_stop_split") %(self.sufficient_majority, "%")
        items[__("report.binary_trees")] = (__("report.cancel"), __("report.ok"))[self.binary_trees]
        return items


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWTreeLearner).run(Table("iris"))
