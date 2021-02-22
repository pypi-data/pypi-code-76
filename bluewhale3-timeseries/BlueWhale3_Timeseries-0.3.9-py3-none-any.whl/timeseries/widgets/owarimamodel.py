from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Input

from orangecontrib.timeseries import Timeseries, ARIMA
from orangecontrib.timeseries.widgets._owmodel import OWBaseModel
from orangecontrib.timeseries.i18n_config import *


def __(key):
    return i18n.t("timeseries.owarimamodel." + key)


class OWARIMAModel(OWBaseModel):
    name = __('name')
    description = __('desc')
    icon = 'icons/ARIMA.svg'
    priority = 210

    p = settings.Setting(1)
    d = settings.Setting(0)
    q = settings.Setting(0)
    use_exog = settings.Setting(False)

    UserAdviceMessages = [
        widget.Message(__("warn.arima"),
                       'random-walk',
                       widget.Message.Warning)
    ]

    class Inputs(OWBaseModel.Inputs):
        exogenous_data = Input('Exogenous data', Timeseries, label=i18n.t("timeseries.common.exogenous_data"))

    def __init__(self):
        super().__init__()
        self.exog_data = None

    @Inputs.exogenous_data
    def set_exog_data(self, data):
        self.exog_data = data
        self.update_model()

    def add_main_layout(self):
        box = gui.vBox(self.controlArea, box=__('box_parameters'))
        gui.spin(box, self, 'p', 0, 100, label=__('label.auto-regression_order'),
                 callback=self.apply)
        gui.spin(box, self, 'd', 0, 2, label=__('label.difference_degree'),
                 callback=self.apply)
        gui.spin(box, self, 'q', 0, 100, label=__('label.move_average_order'),
                 callback=self.apply)
        gui.checkBox(box, self, 'use_exog',
                     __('checkbox_use_exogenous_var'),
                     callback=self.apply)

    def forecast(self, model):
        if self.use_exog and self.exog_data is None:
            return
        return model.predict(self.forecast_steps,
                             exog=self.exog_data,
                             alpha=1 - self.forecast_confint / 100,
                             as_table=True)

    def create_learner(self):
        return ARIMA((self.p, self.d, self.q), self.use_exog)


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication
    from Orange.data import Domain

    a = QApplication([])
    ow = OWARIMAModel()

    data = Timeseries.from_file('airpassengers')
    domain = Domain(data.domain.attributes[:-1], data.domain.attributes[-1])
    data = Timeseries.from_numpy(domain, data.X[:, :-1], data.X[:, -1])
    ow.set_data(data)

    ow.show()
    a.exec()
