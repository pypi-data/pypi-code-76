from AnyQt.QtCore import Qt

from Orange.data import Table
from Orange.util import try_
from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Input, Output
from orangecontrib.timeseries import Timeseries
from orangecontrib.timeseries.i18n_config import *


def __(key):
    return i18n.t("timeseries.owinterpolate." + key)


class OWInterpolate(widget.OWWidget):
    name = __('name')
    description = __('desc')
    icon = 'icons/Interpolate.svg'
    priority = 15

    class Inputs:
        time_series = Input('Time Series', Table, label=i18n.t("timeseries.common.time_series"))

    class Outputs:
        interpolated = Output('Interpolated time series', Timeseries, default=True,
                              label=i18n.t("timeseries.common.interpolated_time_series"))
        timeseries = Output('Time Series', Timeseries, label=i18n.t("timeseries.common.time_series"))  # TODO
        # interpolator = Output("Interpolation model", Model)  # TODO

    want_main_area = False
    resizing_enabled = False

    interpolation = settings.Setting(__('gbox.linear'))
    multivariate = settings.Setting(False)
    autoapply = settings.Setting(True)

    UserAdviceMessages = [
        widget.Message(__('msg_interpolation_method'),
                       'discrete-interp',
                       widget.Message.Warning)
    ]

    def __init__(self):
        self.data = None
        box = gui.vBox(self.controlArea, __('box_interpolation_parameters'))
        gui.comboBox(box, self, 'interpolation',
                     callback=self.on_changed,
                     label=__('label.interpolation_missing_values'),
                     sendSelectedValue=True,
                     orientation=Qt.Horizontal,
                     items=('linear', 'cubic', 'nearest', 'mean'))
        gui.checkBox(box, self, 'multivariate',
                     label=__('label.multi-variate_interpolation'),
                     callback=self.on_changed)
        gui.auto_commit(box, self, 'autoapply', __('btn_apply'))

    @Inputs.time_series
    def set_data(self, data):
        self.data = None if data is None else \
                    Timeseries.from_data_table(data)
        self.on_changed()

    def on_changed(self):
        self.commit()

    def commit(self):
        data = self.data
        if data is not None:
            data = data.copy()
            data.set_interpolation(self.interpolation, self.multivariate)
        self.Outputs.timeseries.send(data)
        self.Outputs.interpolated.send(try_(lambda: data.interp()) or None)


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication

    a = QApplication([])
    ow = OWInterpolate()

    data = Timeseries.from_file('airpassengers')
    ow.set_data(data)

    ow.show()
    a.exec()
