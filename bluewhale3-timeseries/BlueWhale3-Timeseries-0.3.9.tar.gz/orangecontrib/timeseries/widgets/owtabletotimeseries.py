from itertools import chain

import numpy as np

from Orange.data import Table, ContinuousVariable, TimeVariable, Domain
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.itemmodels import VariableListModel
from Orange.widgets.widget import Input, Output

from orangecontrib.timeseries import Timeseries
from orangecontrib.timeseries.i18n_config import *


def __(key):
    return i18n.t("timeseries.owtabletotimeseries." + key)


class OWTableToTimeseries(widget.OWWidget):
    name = __('name')
    description = __('desc')
    icon = 'icons/TableToTimeseries.svg'
    priority = 10

    class Inputs:
        data = Input('Data', Table, label=i18n.t("timeseries.common.data"))

    class Outputs:
        time_series = Output('Time Series', Timeseries, label=i18n.t("timeseries.common.time_series"))

    want_main_area = False
    resizing_enabled = False

    radio_sequential = settings.Setting(0)
    selected_attr = settings.Setting('')
    autocommit = settings.Setting(True)

    class Information(widget.OWWidget.Information):
        nan_times = widget.Msg(__('msg_omit_null'))

    def __init__(self):
        self.data = None
        box = gui.vBox(self.controlArea, __('box_sequence'))
        group = gui.radioButtons(box, self, 'radio_sequential',
                                 callback=self.on_changed)
        hbox = gui.hBox(box)
        gui.appendRadioButton(group, __('btn.sequential_attribute'),
                              insertInto=hbox)

        attrs_model = self.attrs_model = VariableListModel()
        combo_attrs = self.combo_attrs = gui.comboBox(
            hbox, self, 'selected_attr',
            callback=self.on_changed,
            sendSelectedValue=True)
        combo_attrs.setModel(attrs_model)

        gui.appendRadioButton(group, __("btn.sequence_instance_order"),
                              insertInto=box)

        gui.auto_commit(self.controlArea, self, 'autocommit', __('btn.apply'))
        # gui.auto_commit(self.controlArea, self, 'autocommit', '&Apply')
        # TODO: seasonally adjust data (select attributes & season cycle length (e.g. 12 if you have monthly data))

    @Inputs.data
    def set_data(self, data):
        self.data = data
        self.attrs_model.clear()
        if self.data is None:
            self.commit()
            return

        if data.domain.has_continuous_attributes(include_metas=True):
            vars = [var for var in data.domain.variables if var.is_time] + \
                   [var for var in data.domain.metas if var.is_time] + \
                   [var for var in data.domain.variables
                    if var.is_continuous and not var.is_time] + \
                   [var for var in data.domain.metas if var.is_continuous and
                    not var.is_time]
            self.attrs_model[:] = vars
            self.selected_attr = data.time_variable.name if getattr(data, 'time_variable', False) else vars[0].name
        self.on_changed()

    def on_changed(self):
        self.commit()

    def commit(self):
        data = self.data
        self.Information.clear()
        if data is None or (self.selected_attr not in data.domain and not self.radio_sequential):
            self.Outputs.time_series.send(None)
            return

        if self.radio_sequential:
            ts = Timeseries.make_timeseries_from_sequence(data)
        else:
            ts = Timeseries.make_timeseries_from_continuous_var(data,
                                                                self.selected_attr)
            # Check if NaNs were present in data
            time_var = data.domain[self.selected_attr]
            values = Table.from_table(Domain([], [], [time_var]),
                                      source=data).metas.ravel()
            if np.isnan(values).any():
                self.Information.nan_times(time_var.name)

        self.Outputs.time_series.send(ts)


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication

    a = QApplication([])
    ow = OWTableToTimeseries()

    data = Timeseries.from_file('airpassengers')
    ow.set_data(data)

    ow.show()
    a.exec()
