from collections import OrderedDict

from Orange.widgets import widget, gui, settings
from orangecontrib.timeseries import Timeseries, VAR
from orangecontrib.timeseries.widgets._owmodel import OWBaseModel
from orangecontrib.timeseries.i18n_config import *


def __(key):
    return i18n.t("timeseries.owvarmodel." + key)


class OWVARModel(OWBaseModel):
    name = __('name')
    description = __('desc')
    icon = 'icons/VAR.svg'
    priority = 220

    maxlags = settings.Setting(1)
    ic = settings.Setting(0)
    trend = settings.Setting(0)

    UserAdviceMessages = [
        widget.Message(__('msg_series_stationary'),
                       'stationary',
                       widget.Message.Warning)
    ]

    IC_LABELS = OrderedDict(((__('btn.none'), None),
                             (__("btn.aic"), 'aic'),
                             (__('btn.bic'), 'bic'),
                             (__('btn.hannan–quinn'), 'hqic'),
                             (__("btn.fpe"), 'fpe'),
                             (__('btn.average_of_the_above'), 'magic')))
    TREND_LABELS = OrderedDict(((__('btn.none'), 'nc'),
                                (__('btn.constant'), 'c'),
                                (__('btn.constant_linear'), 'ct'),
                                (__('btn.constant_linear_quadratic'), 'ctt')))

    def add_main_layout(self):
        box = gui.vBox(self.controlArea, box=__('box.parameter'))
        gui.spin(box, self, 'maxlags', 1, 100, label=__('label.maxlags'),
                 callback=self.apply)
        gui.radioButtons(
            box, self, 'ic',
            btnLabels=tuple(self.IC_LABELS.keys()),
            box=__('box.information_criterion'), label=__('label.optimize_ar_order'),
            callback=self.apply)
        gui.radioButtons(
            box, self, 'trend',
            btnLabels=tuple(self.TREND_LABELS.keys()),
            box=__('box.trend'), label=__('label.add_trend_vector'),
            callback=self.apply)

    def create_learner(self):
        ic = self.IC_LABELS[tuple(self.IC_LABELS.keys())[self.ic]]
        trend = self.TREND_LABELS[tuple(self.TREND_LABELS.keys())[self.trend]]
        return VAR(self.maxlags, ic, trend)


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication

    a = QApplication([])
    ow = OWVARModel()

    data = Timeseries.from_file('airpassengers')
    ow.set_data(data)

    ow.show()
    a.exec()
