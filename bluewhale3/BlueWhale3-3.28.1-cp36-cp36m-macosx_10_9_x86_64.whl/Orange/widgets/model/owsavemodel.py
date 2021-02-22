import pickle

from Orange.widgets.widget import Input
from Orange.base import Model
from Orange.widgets.utils.save.owsavebase import OWSaveBase
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.i18n_config import *


def __(key):
    return i18n.t("widget.model.model.owsavemodel." + key)

class OWSaveModel(OWSaveBase):
    name = __("name")
    description = __("desc")
    icon = "icons/SaveModel.svg"
    replaces = ["Orange.widgets.classify.owsaveclassifier.OWSaveClassifier"]
    priority = 3000
    keywords = []

    class Inputs:
        model = Input("Model", Model, label=i18n.t("common.general.model"))

    filters = ["Pickled model (*.pkcls)"]

    @Inputs.model
    def set_model(self, model):
        self.data = model
        self.on_new_input()

    def do_save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.data, f)


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWSaveModel).run()
